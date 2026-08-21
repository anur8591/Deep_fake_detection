from fastapi import APIRouter, UploadFile, File
from pathlib import Path
from app.services.video_processor import read_video_frames

router = APIRouter()

@router.post("/analyze")
async def analyze_video(
    video: UploadFile = File(...)
):
    upload_directory = Path("uploads")
    upload_directory.mkdir(exist_ok = True)

    video_path = upload_directory / video.filename

    with open(video_path, "wb") as file:
        file.write(await video.read())

    frame_count = 0

    for frame in read_video_frames(str(video_path)):
        frame_count += 1
    
    return {
        "message": "Video received successfully",
        "filename": video.filename,
        "frames_read": frame_count
    }

