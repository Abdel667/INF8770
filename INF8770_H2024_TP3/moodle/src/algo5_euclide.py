import time
import cv2
import numpy as np
import torch
import torchvision.transforms as transforms
import torchvision.models as models
import csv
import os

from PIL import Image
from einops import rearrange
from IPython.display import display
import matplotlib.pyplot as plt

IMAGE_DIR = f"moodle/data/jpeg"
VIDEO_DIR = f"moodle/data/mp4"
TEST_CSV_PATH = f"moodle/results/test.csv"

class FrameData:
    def __init__(self, video_name, timestamp):
        self.video:str = video_name
        self.time:str = timestamp

class ImageDescriptor:
    def __init__(self):
        self.model = models.resnet50(pretrained=True)
        self.model = torch.nn.Sequential(*(list(self.model.children())[:-1]))
        self.model.eval()

        self.preprocess = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def load_image(self, image:Image):
        input_tensor = self.preprocess(image)
        input_batch = input_tensor.unsqueeze(0)
        return input_batch

    def get_descriptor(self, input_batch):
        with torch.no_grad():
            output = self.model(input_batch)
            output = rearrange(output, 'b d h w -> (b d h w)')
            return output

    def visualize_descriptor(self, descriptor):
        plt.plot(descriptor)
        plt.title("Descripteur d'une image à l'aide de ResNet-18")
        plt.show()


descriptor = ImageDescriptor()
image_batch = descriptor.load_image("RGB.jpg")
output = descriptor.get_descriptor(image_batch)
descriptor.visualize_descriptor(output)

class Algo5Euclide:
    def __init__(self):
        self.image_dir = IMAGE_DIR
        self.descriptor_matrix = []
        self.index_table = []
        self.indexation_time = 0
        self.minimum_treshold = 100000
        self.high_similarity_treshold = 25000
        self.descriptor = ImageDescriptor()

    def indexation(self):
        start_time = time.time()
        for filename in os.listdir(VIDEO_DIR):
            if filename.endswith(".mp4") or filename.endswith(".avi"): # Add more video formats if needed
                file_text_name,  _ = os.path.splitext(os.path.basename(filename))
                video_path = os.path.join(VIDEO_DIR, filename)
                cap = cv2.VideoCapture(video_path)
                
                frame_count = 1
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    # Extract every 15th frame starting from frame 0
                    if frame_count % 10 == 1:
                        # Calculate descriptor_vector for the frame
                        image_batch = descriptor.load_image(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                        descriptor_vector = descriptor.get_descriptor(image_batch)
                        
                        # Store the descriptor_vector in the matrix
                        self.descriptor_matrix.append(descriptor_vector)
                        
                        # Store frame specifications in the index table
                        self.index_table.append(FrameData(file_text_name,cap.get(cv2.CAP_PROP_POS_MSEC) / 1000))
                    
                    frame_count += 1
                
                cap.release()

            # Convert the list of descriptor_vectors into a NumPy array for easier manipulation
            # self.descriptor_matrix = np.array(self.descriptor_matrix)
            end_time = time.time()
            execution_time = end_time - start_time
            return execution_time

    def euclidean_distance(self,hist1, hist2):
        return np.linalg.norm(hist1 - hist2)
    
    def get_closest_frame(self, image_path):
        image_descriptor = descriptor.get_descriptor(Image.open(image_path))
        closest_distance = self.minimum_treshold
        closest_frame = FrameData("", "") 

        for i in range(0, len(self.descriptor_matrix)):
            frame_hist = self.descriptor_matrix[i]
            if(len(frame_hist) != len(image_descriptor)): continue
            distance = self.euclidean_distance(image_descriptor, frame_hist)
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
