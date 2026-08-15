import cv2
import os


class FrameExtractor:

    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder

    def extract_video_frames(self, video_path, video_output_folder):
        """
        Extract every frame from one video.
        """

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print(f"❌ Cannot open: {video_path}")
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
            f"✅ {os.path.basename(video_path)} "
            f"→ {frame_count} frames"
        )

    def extract_all_videos(self):
        """
        Extract frames from every video in the input folder.
        """

        os.makedirs(self.output_folder, exist_ok=True)

        for filename in os.listdir(self.input_folder):

            if filename.lower().endswith(".mp4"):

                video_path = os.path.join(
                    self.input_folder,
                    filename
                )

                video_name = os.path.splitext(filename)[0]

                video_output_folder = os.path.join(
                    self.output_folder,
                    video_name
                )

                self.extract_video_frames(
                    video_path,
                    video_output_folder
                )


if __name__ == "__main__":

    input_folder = "../FaceForensics++_C23/Deepfakes"

    output_folder = "../frames/Deepfakes"

    extractor = FrameExtractor(
        input_folder,
        output_folder
    )

    extractor.extract_all_videos()