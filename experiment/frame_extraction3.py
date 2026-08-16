import cv2


class FrameExtractor:

    def __init__(self, video_path):
        self.video_path = video_path

    def extract_frames(self):

        cap = cv2.VideoCapture(self.video_path)

        if not cap.isOpened():
            print(f"Cannot open: {self.video_path}")
            return

        frame_count = 0

        while True:

            success, frame = cap.read()

            if not success:
                break

            frame_count += 1

            yield frame

        cap.release()

        print(f"Total frames read: {frame_count}")

    def preprocess_frame(self, frame):

        frame = cv2.resize(frame, (128, 128))

        frame = frame.astype("float32") / 255.0

        return frame


if __name__ == "__main__":

    video_path = "FaceForensics++_C23/Deepfakes/000_003.mp4"

    extractor = FrameExtractor(video_path)

    for frame in extractor.extract_frames():

        frame = extractor.preprocess_frame(frame)

        print(frame.shape)