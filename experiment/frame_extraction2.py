import os 
import cv2
import pandas as pd

deepfakedetection = "../FaceForensics++_C23/DeepFakeDetection"
deepfake = "../FaceForensics++_C23/Deepfakes"
face2face = "../FaceForensics++_C23/Face2Face"
faceshifter = "../FaceForensics++_C23/FaceShifter"
faceswap = "../FaceForensics++_C23/FaceSwap"
neuraltextures = "../FaceForensics++_C23/NeuralTextures"
original = "../FaceForensics++_C23/Original"

input_folder = [
    deepfakedetection, 
    deepfake, 
    face2face, 
    faceshifter, 
    faceswap, 
    neuraltextures, 
    original
]

j = [
    "DeepFakeDetection", 
    "Deepfakes", 
    "Face2Face", 
    "FaceShifter", 
    "FaceSwap", 
    "NeuralTextures", 
    "Original"
]

data = {}

for i in range(len(input_folder)):
    data[j[i]] = os.listdir(input_folder[i])

data = pd.DataFrame(data)
print(data)

# class FrameExtractor:

#     def __init__(self, input_folder, output_folder):
#         self.input_folder = input_folder
#         self.output_folder = output_folder

#     def extract_video_frames(self, video_path, video_output_folder):
#         """"
#         Extract frames from a one video.
#         """

#         cap = cv2.VideoCapture(video_path)

#         if not cap.isOpened():
#             print(f"Cannot open: {video_path}")
#             return
        
#         os.makedirs(video_output_folder, exist_ok=True)

#         frame_count = 0

#         while True:


