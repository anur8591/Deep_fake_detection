# backend/
# │
# ├── app/
# │   ├── __init__.py
# │   ├── main.py
# │   │
# │   ├── routes/
# │   │   ├── __init__.py
# │   │   └── analysis.py
# │   │
# │   ├── services/
# │   │   ├── __init__.py
# │   │   ├── video_processor.py
# │   │   ├── frame_processor.py
# │   │   ├── model_manager.py
# │   │   └── predictor.py
# │   │
# │   ├── models/
# │   │   └── model_config.py
# │   │
# │   └── utils/
# │       ├── __init__.py
# │       └── paths.py
# │
# ├── trained_models/
# │   ├── deepfake_detection.keras
# │   ├── deepfakes.keras
# │   ├── face2face.keras
# │   ├── faceshifter.keras
# │   ├── faceswap.keras
# │   └── neuraltextures.keras
# │
# ├── uploads/
# │
# ├── results/
# │
# └── requirements.txt


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="DeepGuard API",
    description="AI-powered Deepfake Detection System",
    version="1.0.0"
)


# Allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "DeepGuard API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }