# libraries
import cv2

# Loading one video and inspecting it
video_path = "FaceForensics++_C23/original/000.mp4"

cap = cv2.VideoCapture(video_path)

# if not cap.isOpened():
#     print("❌ Could not open video")
# else:
#     frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#     print("✅ Video opened successfully")
#     print(f"Frames : {frame_count}")
#     print(f"FPS    : {fps}")
#     print(f"Width  : {width}")
#     print(f"Height : {height}")

# cap.release()

# read a single frame from the video and display it
if not cap.isOpened():
    print("❌ Could not open video")
    exit()

# Read first frame
success, frame = cap.read()

if success:
    print("✅ Frame extracted successfully")
    print("Frame shape:", frame.shape)

    cv2.imshow("First Frame", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("❌ Could not read frame")

cap.release()

