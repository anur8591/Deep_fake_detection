from pathlib import Path
from tensorflow.keras.models import load_model
from app.models.model_config import MODEL_PATHS

class ModelManager:
    def __init__(self):
        self.models = {}

    def load_models(self):
        for name, path in MODEL_PATHS.item():
            if not path(path).exists():
                print(f"Model not found: {path}")
                continue
            self.models[name] = load_model(path)
            print(f"Loaded model: {name}")

    def get_model(self, name):
        return self.models.get(name)

    def get_all_models(self):
        return self.models