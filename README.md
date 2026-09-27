# DeepGuard — Deepfake Detection

DeepGuard is a web application for checking whether a video may contain manipulated faces. A user uploads a video in the React interface; the FastAPI backend samples its frames, preprocesses them, and runs the frames through saved TensorFlow/Keras CNN models. It averages model scores to return a `REAL` or `FAKE` result. The backend also asks local Ollama vision models for a second opinion on up to three frames.

> **Model files are required.** The backend loads six `.keras` files during startup. They are not included in this repository. See [Model files](#model-files) before starting the API.

## Tech stack

- **Frontend:** React 19, JavaScript, Vite, CSS, Lucide React icons
- **Backend/API:** Python, FastAPI, Uvicorn
- **Machine learning:** TensorFlow/Keras CNN models; NumPy
- **Video and image processing:** OpenCV
- **Optional second opinion:** Ollama with `llava:latest` and `gemma3:4b`
- **Dataset/training utilities:** FaceForensics++ C23 video dataset and a TensorFlow `tf.data` streaming training pipeline

## Project layout

```text
backend/
  app/                    FastAPI app, routes, video processing and prediction
  train_deepfakes.py      Train a CNN and save a model checkpoint
frontend/                 React/Vite user interface
experiment/               Earlier frame extraction scripts
FaceForensics++_C23/      Local training dataset (not tracked by Git)
requirement.txt           Python package pins
```

## Requirements

- Python 3.10 or 3.11 recommended for the pinned TensorFlow stack
- Node.js and npm
- The six trained model files listed below
- Ollama and its vision models for the second-opinion feature (optional; see [Ollama setup](#ollama-optional))

## Setup and run

Run each command from the repository root. Keep the backend and frontend terminals open while using the application.

### 1. Create and activate a Python virtual environment

**Windows PowerShell:**

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal, then activate again.

**macOS/Linux:**

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 2. Install the Python requirements

```bash
python -m pip install --upgrade pip
python -m pip install -r requirement.txt
```

Use `python -m pip` after activating the environment so packages install into the project environment. The file is named `requirement.txt` (singular).

### 3. Install frontend packages

Open a second terminal at the repository root, then run:

```bash
cd frontend
npm install
```

### 4. Add trained model files

Create `backend/trained_models/` and place the following files there. The filenames are case-sensitive on Linux and must match exactly:

```text
deepfakes.keras
face2face.keras
faceshifter.keras
faceswap.keras
neuraltextures.keras
deepfakedetection.keras
```

These files are loaded when the API starts. If a file is missing, backend startup fails. The training script in this repository produces `backend/trained_models/faceswap.keras`; it does not create the other five checkpoints. Obtain compatible checkpoints or train/provide them before launching the API.

### 5. Install the Ollama client and (optionally) set up Ollama

The backend imports the Ollama Python client when it starts, so install the client even if you do not plan to use the second-opinion feature. The local Ollama service and its vision models provide that feature. Install the Python client:

```bash
python -m pip install ollama
```

To enable the second opinion, install and start Ollama, then download the models:

```bash
ollama pull llava:latest
ollama pull gemma3:4b
```

Keep the Ollama service running while using the app. If Ollama or either model is unavailable, that frame's Ollama response reports an error; CNN analysis is performed separately. The Ollama package is not currently listed in `requirement.txt`, so install it separately as shown above.

### 6. Start the backend API

From the repository root, with the virtual environment active:

```bash
python -m uvicorn app.main:app --app-dir backend --reload --host 127.0.0.1 --port 8000
```

Check that `http://127.0.0.1:8000/health` returns `{"status":"healthy"}`. Interactive API documentation is at `http://127.0.0.1:8000/docs`.

### 7. Start the frontend

In the second terminal:

```bash
cd frontend
npm run dev
```

Open the local URL printed by Vite (normally `http://localhost:5173`), choose a video (`.mp4`, `.avi`, `.mov`, or `.mkv`) and submit it for analysis. The frontend sends uploads to `http://127.0.0.1:8000/analyze`.

## Train a model (optional)

The training script expects this dataset structure:

```text
FaceForensics++_C23/
  original/     Real videos
  FaceSwap/     FaceSwap videos
```

From the repository root, activate the virtual environment and run:

```bash
python backend/train_deepfakes.py
```

It streams sampled video frames into a CNN training pipeline, uses a video-level train/validation split, and saves the best checkpoint to `backend/trained_models/faceswap.keras`. The dataset is large and is not included; make sure you have the dataset and any required access/permissions before training.

## Python dependency file

`requirement.txt` contains pinned Python packages used by the project. To add or change dependencies, activate `.venv`, install the package, then update the file if you intend to capture the full environment:

```bash
python -m pip install package-name
python -m pip freeze > requirement.txt
```

`pip freeze` records every installed package in the environment, so run it in the project virtual environment rather than a global Python environment.

## API response

`POST /analyze` accepts a multipart upload under the field name `file`. Its JSON response includes the final `result`, predicted `technique` (when classified as fake), confidence percentage, number of frames analyzed, per-model scores, and Ollama second-opinion text.
