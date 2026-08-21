from pathlib import Path

#backend
BASE_DIR = Path(__file__).resolve().parents[2]

#backend/trained_models/
MODEL_DIR = BASE_DIR / "trained_models"

MODEL_PATHS = {
    "deepfake_detection": MODEL_DIR / "deepfake_detection.keras",
    "deepfakes": MODEL_DIR / "deepfakes.keras",
    "face2face": MODEL_DIR / "face2face.keras",
    "faceshifter": MODEL_DIR / "faceshifter.keras",
    "neuraltextures": MODEL_DIR / "neuraltextures.keras"
}