from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATASET_DIR = PROJECT_ROOT / "FaceForensics++_C23"

REAL_DIR = DATASET_DIR / "original"
FAKE_DIR = DATASET_DIR / "Deepfakes"

def get_video_files(folder):

    extensions = {
        ".mp4",
        ".avi",
        ".mov",
        ".mkv"
    }

    return [
        file
        for file in folder.rglob("*")
        if file.is_file() and file.suffix.lower() in extensions
    ]


real_videos = get_video_files(REAL_DIR)
fake_videos = get_video_files(FAKE_DIR)


print("Dataset:")
print(DATASET_DIR)

print("\nOriginal:")
print(REAL_DIR)
print("Videos:", len(real_videos))

print("\nDeepfakes:")
print(FAKE_DIR)
print("Videos:", len(fake_videos))


print("\nSample Original videos:")

for video in real_videos[:3]:
    print(video)


print("\nSample Deepfake videos:")

for video in fake_videos[:3]:
    print(video)