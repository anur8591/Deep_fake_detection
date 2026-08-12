# # libraries
# import cv2
# import os 

# ----------------------------------------------------------------------

# # Loading one video
# video_path = "FaceForensics++_C23/original/000.mp4"

# cap = cv2.VideoCapture(video_path)


# ------------------------#  inspecting it-----------------------------

# if not cap.isOpened():
#     print("❌ Could not open video")
# else:
#     frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#     print("✅ Video opened successfully")
#     print(f"Frames : {frame_count}")
#     print(f"FPS    : {fps}")
#     print(f"Width  : {width}")
#     print(f"Height : {height}")

# cap.release()


# ---------------------------------------------------------------------------------------


# ----------------# read a single frame from the video and display it--------------------

# if not cap.isOpened():
#     print("❌ Could not open video")
#     exit()

# # Read first frame
# success, frame = cap.read()

# if success:
#     print("✅ Frame extracted successfully")
#     print("Frame shape:", frame.shape)

#     cv2.imshow("First Frame", frame)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
# else:
#     print("❌ Could not read frame")

# cap.release()


# ---------------------------------------------------------------------------------------



# if not cap.isOpened():
#     print("❌ Could not open video")
#     exit()

# total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# print("Total frames:", total_frames)

# # Extract 10 evenly spaced frames
# frame_numbers = [
#     int(i * (total_frames - 1) / 9)
#     for i in range(10)
# ]

# os.makedirs("frames", exist_ok=True)

# for i, frame_number in enumerate(frame_numbers):

#     cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

#     success, frame = cap.read()

#     if success:
#         filename = f"frames/frame_{i+1}.jpg"
#         cv2.imwrite(filename, frame)

#         print(f"✅ Saved {filename} | Original frame: {frame_number}")
#     else:
#         print(f"❌ Failed to read frame {frame_number}")

# cap.release()

# print("\nDone!")


# # CNN empty structure for deepfake detection

# import tensorflow as tf
# from tensorflow.keras import Sequential
# from tensorflow.keras.layers import Conv2D, MaxPooling2D
# from tensorflow.keras.layers import Flatten, Dense, Dropout


# # CNN Model
# model = Sequential([

#     # Block 1
#     Conv2D(32, (3, 3), activation="relu", input_shape=(128, 128, 3)),
#     MaxPooling2D((2, 2)),

#     # Block 2
#     Conv2D(64, (3, 3), activation="relu"),
#     MaxPooling2D((2, 2)),

#     # Block 3
#     Conv2D(128, (3, 3), activation="relu"),
#     MaxPooling2D((2, 2)),

#     # Convert feature maps into a vector
#     Flatten(),

#     # Fully Connected Neural Network
#     Dense(128, activation="relu"),
#     Dropout(0.5),

#     # Binary classification
#     Dense(1, activation="sigmoid")
# ])


# # Compile the model
# model.compile(
#     optimizer="adam",
#     loss="binary_crossentropy",
#     metrics=["accuracy"]
# )


# # Display architecture
# model.summary()


import os
import cv2
import numpy as np
import tensorflow as tf

from tensorflow.keras import Model
from tensorflow.keras.layers import (
    Input,
    Conv2D,
    MaxPooling2D,
    Flatten,
    Dense,
    Dropout
)


# =========================================================
# 1. VIDEO → FRAMES
# =========================================================

def video_to_frames(video_path, max_frames=10):

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return []

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Select frames evenly from the video
    frame_numbers = np.linspace(
        0,
        total_frames - 1,
        max_frames,
        dtype=int
    )

    frames = []

    for frame_number in frame_numbers:

        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

        success, frame = cap.read()

        if success:

            # OpenCV BGR → RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # CNN input size
            frame = cv2.resize(frame, (128, 128))

            # Normalize
            frame = frame.astype(np.float32) / 255.0

            frames.append(frame)

    cap.release()

    return frames


# =========================================================
# 2. LOAD VIDEOS FROM A FOLDER
# =========================================================

def load_videos(folder_path, label, max_frames=10):

    data = []
    labels = []

    for filename in os.listdir(folder_path):

        if filename.endswith(".mp4"):

            video_path = os.path.join(folder_path, filename)

            frames = video_to_frames(
                video_path,
                max_frames
            )

            for frame in frames:

                data.append(frame)
                labels.append(label)

    return np.array(data), np.array(labels)


# =========================================================
# 3. CNN FEATURE EXTRACTION
# =========================================================

def create_cnn():

    inputs = Input(shape=(128, 128, 3))

    # Conv Block 1
    x = Conv2D(
        32,
        (3, 3),
        activation="relu"
    )(inputs)

    x = MaxPooling2D((2, 2))(x)

    # Conv Block 2
    x = Conv2D(
        64,
        (3, 3),
        activation="relu"
    )(x)

    x = MaxPooling2D((2, 2))(x)

    # Conv Block 3
    x = Conv2D(
        128,
        (3, 3),
        activation="relu"
    )(x)

    x = MaxPooling2D((2, 2))(x)

    # Flatten
    flattened = Flatten()(x)

    # Fully Connected Neural Network
    x = Dense(
        128,
        activation="relu"
    )(flattened)

    x = Dropout(0.5)(x)

    # REAL / FAKE
    output = Dense(
        1,
        activation="sigmoid"
    )(x)

    model = Model(
        inputs=inputs,
        outputs=output
    )

    return model


# =========================================================
# 4. LOAD DATA
# =========================================================

original_path = "FaceForensics++_C23/original"

fake_path = "FaceForensics++_C23/DeepFakeDetection"


print("Loading REAL videos...")

real_data, real_labels = load_videos(
    original_path,
    label=0,
    max_frames=10
)

print("REAL frames:", len(real_data))


print("Loading FAKE videos...")

fake_data, fake_labels = load_videos(
    fake_path,
    label=1,
    max_frames=10
)

print("FAKE frames:", len(fake_data))


# =========================================================
# 5. COMBINE DATA
# =========================================================

X = np.concatenate(
    (real_data, fake_data),
    axis=0
)

y = np.concatenate(
    (real_labels, fake_labels),
    axis=0
)


print("Total frames:", len(X))
print("X shape:", X.shape)
print("y shape:", y.shape)


# =========================================================
# 6. CREATE CNN
# =========================================================

model = create_cnn()


# =========================================================
# 7. COMPILE
# =========================================================

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)


model.summary()


# =========================================================
# 8. TRAIN
# =========================================================

model.fit(
    X,
    y,
    epochs=10,
    batch_size=32,
    validation_split=0.2,
    shuffle=True
)


# =========================================================
# 9. SAVE MODEL
# =========================================================

model.save("DeepFakeDetection_model.keras")

print("Model saved successfully!")