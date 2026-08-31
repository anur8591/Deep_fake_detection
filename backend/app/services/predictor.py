import numpy as np


class Predictor:
    def __init__(self, model_manager):
        self.model_manager = model_manager
    def predict_frame(self, frame):
        predictions = {}
        for name, model in self.model_manager.models.items():
            # Add batch dimension
            input_frame = np.expand_dims(frame, axis=0)
            # Get model prediction
            prediction = model.predict(
                input_frame,
                verbose=0
            )
            # Sigmoid output
            fake_probability = float(prediction[0][0])
            predictions[name] = fake_probability
        return predictions