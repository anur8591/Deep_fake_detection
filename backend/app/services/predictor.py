import numpy as np


class Predictor:

    def __init__(self, model_manager):
        self.model_manager = model_manager

    def predict_frame(self, frame):

        input_frame = np.expand_dims(
            frame,
            axis=0
        )

        predictions = {}

        for name, model in self.model_manager.models.items():

            prediction = model.predict(
                input_frame,
                verbose=0
            )

            fake_probability = float(
                prediction[0][0]
            )

            predictions[name] = fake_probability

        return predictions


    def predict_video(self, frames):

        all_predictions = {}

        frame_count = 0

        for frame in frames:

            frame_predictions = self.predict_frame(
                frame
            )

            frame_count += 1

            for model_name, probability in frame_predictions.items():

                if model_name not in all_predictions:
                    all_predictions[model_name] = []

                all_predictions[model_name].append(
                    probability
                )


        # Average prediction of every model
        model_scores = {}

        for model_name, predictions in all_predictions.items():

            model_scores[model_name] = float(
                np.mean(predictions)
            )


        return {
            "frame_count": frame_count,
            "model_scores": model_scores
        }
    
    def analyze_scores(self, model_scores):

        # Find the model with the highest fake score
        best_model = max(
            model_scores,
            key=model_scores.get
        )

        best_score = model_scores[best_model]


        # 0.8 = decision threshold
        if best_score >= 0.8:

            result = "FAKE"

            technique = best_model

            confidence = best_score

        else:

            result = "REAL"

            technique = None

            confidence = 1 - best_score


        return {
            "result": result,
            "technique": technique,
            "confidence": confidence,
            "model_scores": model_scores
        }