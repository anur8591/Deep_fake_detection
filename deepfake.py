# # libraries
# import cv2
# import os 

# ----------------------------------------------------------------------

# # Loading one video
# video_path = "FaceForensics++_C23/original/000.mp4"

# cap = cv2.VideoCapture(video_path)


# ------------------------#  inspecting it-----------------------------

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


# ---------------------------------------------------------------------------------------


# ----------------# read a single frame from the video and display it--------------------

# if not cap.isOpened():
#     print("❌ Could not open video")
#     exit()

# # Read first frame
# success, frame = cap.read()

# if success:
#     print("✅ Frame extracted successfully")
#     print("Frame shape:", frame.shape)

#     cv2.imshow("First Frame", frame)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
# else:
#     print("❌ Could not read frame")

# cap.release()


# ---------------------------------------------------------------------------------------



# if not cap.isOpened():
#     print("❌ Could not open video")
#     exit()

# total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# print("Total frames:", total_frames)

# # Extract 10 evenly spaced frames
# frame_numbers = [
#     int(i * (total_frames - 1) / 9)
#     for i in range(10)
# ]

# os.makedirs("frames", exist_ok=True)

# for i, frame_number in enumerate(frame_numbers):

#     cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

#     success, frame = cap.read()

#     if success:
#         filename = f"frames/frame_{i+1}.jpg"
#         cv2.imwrite(filename, frame)

#         print(f"✅ Saved {filename} | Original frame: {frame_number}")
#     else:
#         print(f"❌ Failed to read frame {frame_number}")

# cap.release()

# print("\nDone!")


