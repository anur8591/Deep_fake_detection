from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import os

from app.services.video_processor import extract_frames
from app.services.frame_processor import preprocess_frame
from app.services.model_manager import ModelManager
from app.services.predictor import Predictor


router = APIRouter()


# Load all models only once
model_manager = ModelManager()
predictor = Predictor(model_manager)


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/analyze")
async def analyze_video(file: UploadFile = File(...)):

    # Check file type
    if not file.filename.endswith((".mp4", ".avi", ".mov", ".mkv")):
        raise HTTPException(
            status_code=400,
            detail="Unsupported video format"
        )

    # Temporary path
    video_path = UPLOAD_DIR / file.filename

    try:

        # Save uploaded video
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)


        # Create frame generator
        processed_frames = (
            preprocess_frame(frame)
            for frame in extract_frames(video_path)
        )


        # Predict complete video
        prediction_result = predictor.predict_video(processed_frames)

        # Final decision
        final_result = predictor.analyze_scores(
            prediction_result["model_scores"]
        )

        return {
            "result": final_result["result"],
            "technique": final_result["technique"],
            "confidence": round(
                final_result["confidence"] * 100,
                2
            ),
            "frames_analyzed": prediction_result["frame_count"],
            "model_scores": {
                name: round(score * 100, 2)
                for name, score in final_result["model_scores"].items()
            }
        }

    finally:

        # Delete temporary uploaded video
        if video_path.exists():
            os.remove(video_path)