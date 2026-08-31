import cv2
import numpy as np


IMG_SIZE = 224


def preprocess_frame(frame):

    # Resize frame
    frame = cv2.resize(
        frame,
        (IMG_SIZE, IMG_SIZE)
    )

    # OpenCV uses BGR
    # Convert BGR → RGB
    frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    # Convert to float
    frame = frame.astype(
        np.float32
    )

    # Normalize pixels from 0–255 to 0–1
    frame = frame / 255.0

    return frame