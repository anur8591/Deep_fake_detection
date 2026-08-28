import cv2
import random
from pathlib import Path
import numpy as np
import tensorflow as tf

from tensorflow.keras import Sequential
from tensorflow.keras.layers import (
    Conv2D,
    MaxPooling2D,
    Flatten,
    Dense,
    Dropout
)
from tensorflow.keras.utils import Sequence
from tensorflow.keras.callbacks import EarlyStopping 

# PATHS

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_DIR = PROJECT_ROOT / "FaceForensics++_C23"
REAL_DIR = DATASET_DIR / "original"
FAKE_DIR = DATASET_DIR / "Deepfakes"
MODEL_DIR = PROJECT_ROOT / "backend" / "trained_models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODEL_DIR / "deepfakes.keras"

# CONFIGURATION

IMG_SIZE = 224
BATCH_SIZE = 16
EPOCHS = 20 
FRAME_INTERVAL = 5
VALIDATION_SPLIT = 0.20
RANDOM_SEED = 42

# FIND VIDEOS

def get_video_files(folder):
    extensions = {
        ".mp4",
        ".avi",
        ".mov",
        ".mkv"
    }

    videos = []
    for file in folder.rglob("*"):
        if file.is_file() and file.suffix.lower() in extensions:
            videos.append(file)
    return videos

# SPLIT VIDEOS

def split_videos(videos):
    videos = videos.copy()
    random.shuffle(videos)
    validation_count = int(
        len(videos) * VALIDATION_SPLIT
    )
    validation_videos = videos[:validation_count]
    training_videos = videos[validation_count:]
    return training_videos, validation_videos

# GET FRAME POSITIONS

def get_frame_positions(video_path):
    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        return []
    total_frames = int(
        capture.get(cv2.CAP_PROP_FRAME_COUNT)
    )
    capture.release()
    positions = list(
        range(
            0,
            total_frames,
            FRAME_INTERVAL
        )
    )
    return positions

# CREATE FRAME INDEX

def create_frame_index(videos):
    frame_index = []
    for video_path, label in videos:
        positions = get_frame_positions(video_path)
        for position in positions:
            frame_index.append(
                (
                    video_path,
                    position,
                    label
                )
            )
    return frame_index

# FRAME DATASET

class VideoFrameSequence(Sequence):
    def __init__(
        self,
        frame_index,
        batch_size,
        shuffle=True
    ):
        self.frame_index = frame_index
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.indexes = np.arange(
            len(self.frame_index)
        )
        self.on_epoch_end()

    def __len__(self):
        return int(
            np.ceil(
                len(self.frame_index)
                / self.batch_size
            )
        )

    def __getitem__(self, index):
        batch_indexes = self.indexes[
            index * self.batch_size:
            (index + 1) * self.batch_size
        ]
        batch_frames = []
        batch_labels = []

        for frame_index in batch_indexes:
            video_path, position, label = (
                self.frame_index[frame_index]
            )
            capture = cv2.VideoCapture(
                str(video_path)
            )
            capture.set(
                cv2.CAP_PROP_POS_FRAMES,
                position
            )
            success, frame = capture.read()
            capture.release()

            if not success:
                continue

            # Resize
            frame = cv2.resize(
                frame,
                (IMG_SIZE, IMG_SIZE)
            )

            # BGR → RGB
            frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            # Normalize
            frame = frame.astype(
                np.float32
            ) / 255.0
            batch_frames.append(frame)
            batch_labels.append(label)
        return (
            np.array(
                batch_frames,
                dtype=np.float32
            ),
            np.array(
                batch_labels,
                dtype=np.float32
            )
        )

    def on_epoch_end(self):
        if self.shuffle:
            np.random.shuffle(
                self.indexes
            )

# CNN MODEL

def create_model():
    model = Sequential([
        Conv2D(
            32,
            (3, 3),
            activation="relu",
            input_shape=(
                IMG_SIZE,
                IMG_SIZE,
                3
            )
        ),
        MaxPooling2D(
            (2, 2)
        ),
        Conv2D(
            64,
            (3, 3),
            activation="relu"
        ),
        MaxPooling2D(
            (2, 2)
        ),
        Conv2D(
            128,
            (3, 3),
            activation="relu"
        ),
        MaxPooling2D(
            (2, 2)
        ),
        Flatten(),
        Dense(
            128,
            activation="relu"
        ),
        Dropout(
            0.5
        ),
        Dense(
            1,
            activation="sigmoid"
        )
    ])

    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )
    return model

# MAIN

def main():
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    tf.random.set_seed(RANDOM_SEED)

    # Find videos

    print("\nSearching dataset...\n")
    real_videos = get_video_files(
        REAL_DIR
    )
    fake_videos = get_video_files(
        FAKE_DIR
    )
    print(
        f"Original videos : {len(real_videos)}"
    )
    print(
        f"Deepfake videos : {len(fake_videos)}"
    )
    if not real_videos:
        raise RuntimeError(
            f"No videos found in {REAL_DIR}"
        )
    if not fake_videos:
        raise RuntimeError(
            f"No videos found in {FAKE_DIR}"
        )

    # Video-level split

    real_train, real_validation = (
        split_videos(real_videos)
    )
    fake_train, fake_validation = (
        split_videos(fake_videos)
    )
    print("\nVideo-level split:")
    print(
        f"Original training   : {len(real_train)}"
    )
    print(
        f"Original validation : {len(real_validation)}"
    )
    print(
        f"Deepfake training   : {len(fake_train)}"
    )
    print(
        f"Deepfake validation : {len(fake_validation)}"
    )

    # Create labeled video lists

    training_videos = []
    validation_videos = []
    for video in real_train:
        training_videos.append(
            (video, 0)
        )
    for video in fake_train:
        training_videos.append(
            (video, 1)
        )
    for video in real_validation:
        validation_videos.append(
            (video, 0)
        )
    for video in fake_validation:
        validation_videos.append(
            (video, 1)
        )
    random.shuffle(training_videos)
    random.shuffle(validation_videos)

    # Build frame indexes

    print("\nBuilding frame indexes...")
    print(
        "This stores only video paths and frame numbers."
    )
    print(
        "Actual frames are NOT stored on disk."
    )
    training_index = create_frame_index(
        training_videos
    )
    validation_index = create_frame_index(
        validation_videos
    )
    print(
        f"\nTraining frames: "
        f"{len(training_index)}"
    )
    print(
        f"Validation frames: "
        f"{len(validation_index)}"
    )

    # Create generators

    training_data = VideoFrameSequence(
        training_index,
        BATCH_SIZE,
        shuffle=True
    )

    validation_data = VideoFrameSequence(
        validation_index,
        BATCH_SIZE,
        shuffle=False
    )

    # Create CNN

    model = create_model()
    model.summary()

    # Train

    print("\nStarting training...\n")

    model.fit(
        training_data,
        validation_data=validation_data,
        epochs=EPOCHS
    )

    # Save

    model.save(
        MODEL_PATH
    )

    print("\n===================================")
    print("Training completed!")
    print(
        f"Model saved to:\n{MODEL_PATH}"
    )
    print("===================================")

# ENTRY POINT

if __name__ == "__main__":
    main()