from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.analysis import router as analysis_router


app = FastAPI(
    title="DeepGuard API",
    description="AI-powered Deepfake Detection System",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(analysis_router)


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