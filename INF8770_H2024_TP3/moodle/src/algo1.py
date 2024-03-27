import os

import numpy as np
import cv2
import csv

from PIL import Image
# Path to the directory containing JPEG images
image_dir = r'moodle\data\jpeg'

# Path to the directory containing MP4 videos
video_dir = r'moodle\data\mp4'

# Path to the CSV file
csv_file = r'moodle\data\test.csv'

def compare_images(frame, image):
    print('comparing images')
    # image = Image.open(bgr_image).convert('BGR')
    # frame_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    # A = np.array(image)
    # B = np.array(frame_image)
    mse = np.mean((image - frame) ** 2)
    return mse < 10


# Iterate through each JPEG image
for image_name in os.listdir(image_dir):
    print('iteration 1')
    image_path = os.path.join(image_dir, image_name)
    numpy_image = np.array(Image.open(image_path))
    bgr_image = cv2.cvtColor(numpy_image, cv2.COLOR_BGR2RGB)
    
    # Flag to check if a match is found
    match_found = False
    
    # Iterate through each MP4 video
    for video_name in os.listdir(video_dir):
        print('iteration 2')
        video_path = os.path.join(video_dir, video_name)

        # Open the video file
        cap = cv2.VideoCapture(video_path)

        # Iterate through each frame of the video
        frame_index = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Compare the current frame with the JPEG image
            # Replace this with your own image comparison logic
            if compare_images(frame, bgr_image):
                print('match found')
                # Match found, associate the image name with the video and frame index
                match_found = True
                match_video = video_name
                match_frame_index = frame_index
                break
            
            frame_index += 1
        
        cap.release()
        
        if match_found:
            break
    
    # Update the CSV file
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        if match_found:
            writer.writerow([image_name, match_video, match_frame_index])
        else:
            writer.writerow([image_name, 'out', ''])