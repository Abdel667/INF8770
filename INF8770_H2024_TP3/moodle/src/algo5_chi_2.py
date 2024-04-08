import csv
import time
import torch
from torchvision import models, transforms
import cv2
import os
import numpy as np
from PIL import Image

IMAGE_DIR = f"moodle/data/jpeg"
VIDEO_DIR = f"moodle/data/mp4"
TEST_CSV_PATH = f"moodle/results/test.csv"

# Check if GPU is available and set the device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the pre-trained model
model = models.resnet18(pretrained=True)
model.eval() # Set the model to evaluation mode

# Move the model to the device
model.to(device)

# Define the image transformation
transform = transforms.Compose([
    transforms.Resize(224),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
class FrameData:
    def __init__(self, video_name, timestamp):
        self.video = video_name
        self.time = timestamp

class Algo5Euclide:
    def __init__(self):
        self.descriptor_matrix = []
        self.index_table = []
        self.indexation_time = 0
        self.minimum_treshold = 14000
        self.high_similarity_treshold = 1000
        self.video_dir = VIDEO_DIR
        self.image_dir = IMAGE_DIR

    def get_frame_descriptor(self, frame):
        frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        frame_tensor = transform(frame_pil).unsqueeze(0)
        frame_tensor = frame_tensor.to(device)
    
        # Get descriptor
        with torch.no_grad():
            descriptor = model(frame_tensor)
            return descriptor.cpu().numpy()
    
    def indexation(self):
        start_time = time.time()
        for video_file in os.listdir(self.video_dir):
            if video_file.endswith('.mp4'): # Assuming MP4 videos
                video_path = os.path.join(self.video_dir, video_file)
                video_name,  _ = os.path.splitext(os.path.basename(video_file))
                cap = cv2.VideoCapture(video_path)
                
                frame_count = 0
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    # Extract every 15th frame
                    if frame_count % 15 == 1:
                        descriptor = self.get_frame_descriptor(frame)
                        self.descriptor_matrix.append(descriptor)
                        
                        # Store FrameData in index table
                        timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000 # Convert to seconds
                        frame_data = FrameData(video_name, timestamp)
                        self.index_table.append(frame_data)
                    
                    frame_count += 1
                
                cap.release()
                end_time = time.time()
        return end_time - start_time
    
    def chi_squared_value(self, hist1, hist2):
    # Calculate the chi-squared statistic manually
        chi_squared = 0.5 * np.sum(((hist1 - hist2) ** 2) / (hist1 + hist2 + 1e-6))
        return chi_squared
    
    def get_closest_frame(self, image_path):
        image_descriptor = self.get_frame_descriptor(cv2.imread(image_path))
        closest_distance = self.minimum_treshold
        closest_frame = FrameData("", "") 

        for i in range(0, len(self.descriptor_matrix)):
            frame_hist = self.descriptor_matrix[i]
            if(len(frame_hist) != len(image_descriptor)): continue
            distance = self.chi_squared_value(image_descriptor, frame_hist)
            if distance < closest_distance:
                closest_distance = distance
                closest_frame.video = self.index_table[i].video
                closest_frame.time = self.index_table[i].time
                if(closest_distance < self.high_similarity_treshold):
                    return closest_frame, closest_distance

        return closest_frame, closest_distance

    def compare_images(self):
        self.indexation_time = self.indexation()
        for image_name in os.listdir(self.image_dir):
            start_time = time.time()
            image_path = os.path.join(self.image_dir, image_name)
            image_text_name,  _ = os.path.splitext(os.path.basename(image_path))
            closest_frame, closest_distance = self.get_closest_frame(image_path)
            print(f"Closest frame for {image_text_name} is {closest_frame.video}/{closest_frame.time} with a distance of {closest_distance}")
            with open(TEST_CSV_PATH, 'a', newline='') as file:
                writer = csv.writer(file)
                if closest_distance < self.minimum_treshold:
                    writer.writerow([image_text_name , closest_frame.video, closest_frame.time])
                else:
                    writer.writerow([image_text_name, 'out', ''])
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Execution time for image {image_name} is : {execution_time}")

    
def main():
    start_time = time.time()
    algo = Algo5Euclide()
    algo.compare_images()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time of indexation with neural networks is : {algo.indexation_time}")
    print(f"Execution time of algo3 with euclide is : {execution_time}")

if __name__ == "__main__":
    main()