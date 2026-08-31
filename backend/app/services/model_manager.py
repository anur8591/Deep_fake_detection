from pathlib import Path
from tensorflow.keras.models import load_model


class ModelManager:
    def __init__(self):
        # Find backend folder
        backend_dir = Path(__file__).resolve().parents[2]
        # trained_models folder
        self.model_dir = backend_dir / "trained_models"
        # Load all models
        self.models = {
            "deepfakes": load_model(
                self.model_dir / "deepfakes.keras"
            ),
            "face2face": load_model(
                self.model_dir / "face2face.keras"
            ),
            "faceshifter": load_model(
                self.model_dir / "faceshifter.keras"
            ),
            "faceswap": load_model(
                self.model_dir / "faceswap.keras"
            ),
            "neuraltextures": load_model(
                self.model_dir / "neuraltextures.keras"
            ),
            "deepfake_detection": load_model(
                self.model_dir / "deepfake_detection.keras"
            )
        }

    def get_model(self, name):
        return self.models[name]