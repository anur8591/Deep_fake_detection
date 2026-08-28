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
from tensorflow.keras.callbacks import (
    EarlyStopping,
    ModelCheckpoint
)


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATASET_DIR = PROJECT_ROOT / "FaceForensics++_C23"

REAL_DIR = DATASET_DIR / "original"
FAKE_DIR = DATASET_DIR / "Deepfakes"

MODEL_DIR = PROJECT_ROOT / "backend" / "trained_models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "deepfakes.keras"


# ============================================================
# CONFIGURATION
# ============================================================

IMG_SIZE = 224
BATCH_SIZE = 16

# Maximum epochs
EPOCHS = 20

# Take every 5th frame
FRAME_INTERVAL = 5

VALIDATION_SPLIT = 0.20
RANDOM_SEED = 42


# ============================================================
# FIND VIDEOS
# ============================================================

def get_video_files(folder):

    extensions = {".mp4", ".avi", ".mov", ".mkv"}

    videos = []

    for file in folder.rglob("*"):

        if file.is_file() and file.suffix.lower() in extensions:
            videos.append(file)

    return videos


# ============================================================
# SPLIT VIDEOS
# ============================================================

def split_videos(videos):

    videos = videos.copy()

    random.shuffle(videos)

    validation_count = int(
        len(videos) * VALIDATION_SPLIT
    )

    validation_videos = videos[:validation_count]
    training_videos = videos[validation_count:]

    return training_videos, validation_videos


# ============================================================
# STREAM FRAMES
# ============================================================

def frame_generator(videos):
    """
    Opens each video once.
    Reads frames sequentially.
    Frames are never saved to disk.
    """

    for video_path, label in videos:

        capture = cv2.VideoCapture(str(video_path))

        if not capture.isOpened():

            print(f"Could not open: {video_path}")

            continue

        frame_number = 0

        while True:

            success, frame = capture.read()

            if not success:
                break

            frame_number += 1

            # Use every nth frame
            if frame_number % FRAME_INTERVAL != 0:
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

            yield frame, np.float32(label)

        capture.release()


# ============================================================
# CREATE TF.DATASET
# ============================================================

def create_dataset(videos, shuffle=True):

    output_signature = (
        tf.TensorSpec(
            shape=(IMG_SIZE, IMG_SIZE, 3),
            dtype=tf.float32
        ),

        tf.TensorSpec(
            shape=(),
            dtype=tf.float32
        )
    )

    dataset = tf.data.Dataset.from_generator(
        lambda: frame_generator(videos),
        output_signature=output_signature
    )

    if shuffle:

        dataset = dataset.shuffle(
            buffer_size=1000
        )

    dataset = dataset.batch(
        BATCH_SIZE
    )

    # Allows the dataset to be used again in the next epoch
    dataset = dataset.repeat()

    dataset = dataset.prefetch(
        tf.data.AUTOTUNE
    )

    return dataset


# ============================================================
# COUNT STEPS
# ============================================================

def count_frames(videos):

    total_frames = 0

    for video_path, label in videos:

        capture = cv2.VideoCapture(
            str(video_path)
        )

        if capture.isOpened():

            frame_count = int(
                capture.get(
                    cv2.CAP_PROP_FRAME_COUNT
                )
            )

            total_frames += (
                frame_count // FRAME_INTERVAL
            )

        capture.release()

    return total_frames


# ============================================================
# CREATE MODEL
# ============================================================

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

        MaxPooling2D((2, 2)),


        Conv2D(
            64,
            (3, 3),
            activation="relu"
        ),

        MaxPooling2D((2, 2)),


        Conv2D(
            128,
            (3, 3),
            activation="relu"
        ),

        MaxPooling2D((2, 2)),


        Flatten(),


        Dense(
            128,
            activation="relu"
        ),

        Dropout(0.5),


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


# ============================================================
# MAIN
# ============================================================

def main():

    # Reproducibility
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    tf.random.set_seed(RANDOM_SEED)


    # --------------------------------------------------------
    # Find videos
    # --------------------------------------------------------

    print("\nSearching dataset...\n")

    real_videos = get_video_files(REAL_DIR)
    fake_videos = get_video_files(FAKE_DIR)

    print(f"Original videos: {len(real_videos)}")
    print(f"Deepfake videos: {len(fake_videos)}")


    # --------------------------------------------------------
    # Split videos
    # --------------------------------------------------------

    real_train, real_validation = (
        split_videos(real_videos)
    )

    fake_train, fake_validation = (
        split_videos(fake_videos)
    )


    print("\nVideo split:")

    print(f"Original training: {len(real_train)}")
    print(f"Original validation: {len(real_validation)}")

    print(f"Deepfake training: {len(fake_train)}")
    print(f"Deepfake validation: {len(fake_validation)}")


    # --------------------------------------------------------
    # Add labels
    # --------------------------------------------------------

    training_videos = (
        [(video, 0) for video in real_train]
        +
        [(video, 1) for video in fake_train]
    )

    validation_videos = (
        [(video, 0) for video in real_validation]
        +
        [(video, 1) for video in fake_validation]
    )


    random.shuffle(training_videos)
    random.shuffle(validation_videos)


    # --------------------------------------------------------
    # Count frames for steps
    # --------------------------------------------------------

    print("\nCounting training frames...")

    training_frame_count = count_frames(
        training_videos
    )

    validation_frame_count = count_frames(
        validation_videos
    )


    steps_per_epoch = (
        training_frame_count // BATCH_SIZE
    )

    validation_steps = (
        validation_frame_count // BATCH_SIZE
    )


    print(
        f"Training frames: {training_frame_count}"
    )

    print(
        f"Validation frames: {validation_frame_count}"
    )

    print(
        f"Steps per epoch: {steps_per_epoch}"
    )

    print(
        f"Validation steps: {validation_steps}"
    )


    # --------------------------------------------------------
    # Create datasets
    # --------------------------------------------------------

    print("\nCreating streaming datasets...")

    training_data = create_dataset(
        training_videos,
        shuffle=True
    )

    validation_data = create_dataset(
        validation_videos,
        shuffle=False
    )


    # --------------------------------------------------------
    # Create model
    # --------------------------------------------------------

    model = create_model()

    model.summary()


    # --------------------------------------------------------
    # Callbacks
    # --------------------------------------------------------

    early_stopping = EarlyStopping(
        monitor="val_loss",
        patience=3,
        restore_best_weights=True,
        verbose=1
    )

    checkpoint = ModelCheckpoint(
        MODEL_PATH,
        monitor="val_loss",
        save_best_only=True,
        verbose=1
    )


    # --------------------------------------------------------
    # TRAIN
    # --------------------------------------------------------

    print("\nStarting training...\n")

    model.fit(
        training_data,

        steps_per_epoch=steps_per_epoch,

        validation_data=validation_data,

        validation_steps=validation_steps,

        epochs=EPOCHS,

        callbacks=[
            early_stopping,
            checkpoint
        ]
    )


    print("\n================================")
    print("Training completed!")
    print(f"Best model saved at:\n{MODEL_PATH}")
    print("================================")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()