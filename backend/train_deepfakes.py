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
EPOCHS = 5
FRAME_INTERVAL = 5
VALIDATION_SPLIT = 0.2
RANDOM_SEED = 42

# GET VIDEO FILES

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
    random.seed(RANDOM_SEED)
    videos = videos.copy()
    random.shuffle(videos)
    validation_count = int(len(videos) * VALIDATION_SPLIT)
    validation_videos = videos[:validation_count]
    training_videos = videos[validation_count:]
    return training_videos, validation_videos

# READ FRAMES FROM VIDEOS

def frame_generator(videos, label):
    for video_path in videos:
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

            # Only use every FRAME_INTERVAL frame
            
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
            frame = frame.astype(np.float32) / 255.0
            yield frame, label

        capture.release()


# BATCH GENERATOR

def batch_generator(videos, label):
    frames = []
    labels = []
    for frame, frame_label in frame_generator(videos, label):
        frames.append(frame)
        labels.append(frame_label)
        if len(frames) == BATCH_SIZE:
            yield (
                np.array(frames, dtype=np.float32),
                np.array(labels, dtype=np.float32)
            )
            # IMPORTANT:
            # Clear the batch after sending it to the model.
            frames = []
            labels = []

    # Handle remaining frames
    if frames:
        yield (
            np.array(frames, dtype=np.float32),
            np.array(labels, dtype=np.float32)
        )

# CREATE CNN MODEL

def create_model():
    model = Sequential([
        Conv2D(
            32,
            (3, 3),
            activation="relu",
            input_shape=(IMG_SIZE, IMG_SIZE, 3)
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


# MAIN

def main():
    print("\nSearching for videos...\n")
    real_videos = get_video_files(REAL_DIR)
    fake_videos = get_video_files(FAKE_DIR)
    print(f"Real videos : {len(real_videos)}")
    print(f"Fake videos : {len(fake_videos)}")
    if not real_videos:
        raise RuntimeError(
            f"No videos found in: {REAL_DIR}"
        )
    if not fake_videos:
        raise RuntimeError(
            f"No videos found in: {FAKE_DIR}"
        )

    # Split at VIDEO level

    real_train, real_val = split_videos(real_videos)
    fake_train, fake_val = split_videos(fake_videos)
    print("\nDataset split:")
    print(f"Real training      : {len(real_train)}")
    print(f"Real validation    : {len(real_val)}")
    print(f"Deepfakes training : {len(fake_train)}")
    print(f"Deepfakes validation: {len(fake_val)}")

    # Create model

    model = create_model()
    model.summary()

    # Training

    print("\nStarting training...\n")
    for epoch in range(EPOCHS):
        print(
            f"\n========== Epoch "
            f"{epoch + 1}/{EPOCHS} ==========\n"
        )

        # Combine real + fake videos
        training_items = []

        for video in real_train:
            training_items.append((video, 0))

        for video in fake_train:
            training_items.append((video, 1))

        random.shuffle(training_items)

        total_loss = 0
        total_accuracy = 0
        batch_count = 0

        for video_path, label in training_items:
            for frames, labels in batch_generator(
                [video_path],
                label
            ):
                loss, accuracy = model.train_on_batch(
                    frames,
                    labels
                )
                total_loss += float(loss)
                total_accuracy += float(accuracy)
                batch_count += 1
                if batch_count % 10 == 0:
                    print(
                        f"Batches: {batch_count} | "
                        f"Loss: {loss:.4f} | "
                        f"Accuracy: {accuracy:.4f}"
                    )
        if batch_count > 0:
            print(
                f"\nEpoch result:"
                f"\nLoss: "
                f"{total_loss / batch_count:.4f}"
                f"\nAccuracy: "
                f"{total_accuracy / batch_count:.4f}"
            )

    # Save model

    model.save(MODEL_PATH)
    print("\n================================")
    print("Training completed!")
    print(f"Model saved at:")
    print(MODEL_PATH)
    print("================================")

if __name__ == "__main__":
    main()