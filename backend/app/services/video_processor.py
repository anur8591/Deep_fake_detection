import cv2


def extract_frames(video_path, frame_interval=5):

    video = cv2.VideoCapture(str(video_path))

    frame_count = 0

    while True:

        success, frame = video.read()

        if not success:
            break

        if frame_count % frame_interval == 0:
            yield frame

        frame_count += 1

    video.release()