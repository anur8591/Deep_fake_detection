from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# cross origin resource sharing (cors) 

app = FastAPI(
    title = "DeepGuard API",
    description = "AI-powered Deepfake Detection System",
    version = "1.0.0"
)

# Allow react frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"]
    allow_headers=["*"]
)
