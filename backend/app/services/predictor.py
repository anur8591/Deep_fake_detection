import numpy as np


def predict_frame(frame, models):
    """
    Run one preprocessed frame through all available models.

    Parameters:
        frame  : preprocessed frame, shape (1, 224, 224, 3)
        models : dictionary of loaded models

    Returns:
        Dictionary containing each model's fake score.
    """

    predictions = {}

    for name, model in models.items():
        output = model.predict(frame, verbose=0)
        fake_score = float(output[0][0])
        predictions[name] = fake_score

    return predictions