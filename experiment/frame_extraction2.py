import os
import cv2


deepfakedetection = "../FaceForensics++_C23/DeepFakeDetection"
deepfake = "../FaceForensics++_C23/Deepfakes"
face2face = "../FaceForensics++_C23/Face2Face"
faceshifter = "../FaceForensics++_C23/FaceShifter"
faceswap = "../FaceForensics++_C23/FaceSwap"
neuraltextures = "../FaceForensics++_C23/NeuralTextures"
original = "../FaceForensics++_C23/Original"


input_folders = [
    deepfakedetection,
    deepfake,
    face2face,
    faceshifter,
    faceswap,
    neuraltextures,
    original
]

folder_names = [
    "DeepFakeDetection",
    "Deepfakes",
    "Face2Face",
    "FaceShifter",
    "FaceSwap",
    "NeuralTextures",
    "Original"
]


class FrameExtractor:

    def __init__(self, input_folders, output_folder):
        self.input_folders = input_folders
        self.output_folder = output_folder

    def extract_video_frames(self, video_path, video_output_folder):

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print(f"Cannot open: {video_path}")
            return

        os.makedirs(video_output_folder, exist_ok=True)

        frame_count = 0

        while True:

            success, frame = cap.read()

            if not success:
                break

            frame_path = os.path.join(
                video_output_folder,
                f"frame_{frame_count:05d}.jpg"
            )

            cv2.imwrite(frame_path, frame)

            frame_count += 1

        cap.release()

        print(
            f"{os.path.basename(video_path)}"
            f" → {frame_count} frames"
        )

    def extract_all_videos(self, input_folder, folder_name):

        output_folder = os.path.join(
            self.output_folder,
            folder_name
        )

        os.makedirs(output_folder, exist_ok=True)

        for filename in os.listdir(input_folder):

            if filename.lower().endswith(".mp4"):

                video_path = os.path.join(
                    input_folder,
                    filename
                )

                video_name = os.path.splitext(filename)[0]

                video_output_folder = os.path.join(
                    output_folder,
                    video_name
                )

                self.extract_video_frames(
                    video_path,
                    video_output_folder
                )

    def extract_all_folders(self):

        for input_folder, folder_name in zip(
            self.input_folders,
            folder_names
        ):

            print(f"\nProcessing: {folder_name}")

            self.extract_all_videos(
                input_folder,
                folder_name
            )


if __name__ == "__main__":

    output_folder = "../frames"

    extractor = FrameExtractor(
        input_folders,
        output_folder
    )

    extractor.extract_all_folders()