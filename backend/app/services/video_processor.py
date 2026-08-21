import cv2
def read_video_frames(video_path):
    """
        Read a video frame by frame.
        frame are kept temporarily in memory
    """
    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        raise ValueError("Could not open video")
    frame_count = 0

    while True:
        success, frame = video.read()

        if not success:
            break

        frame_count += 1

        yield frame

    video.release()