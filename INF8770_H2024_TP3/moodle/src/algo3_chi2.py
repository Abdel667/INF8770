# IMPORTS
import csv
from enum import Enum
import os
import time
import cv2
import numpy as np
from scipy.stats import chisquare

IMAGE_DIR = f"moodle/data/jpeg"
VIDEO_DIR = f"moodle/data/mp4"
TEST_CSV_PATH = f"moodle/results/test.csv"


#Définition de la classe générale et de ses paramètres (notament is_inside)
class FrameData:
    def __init__(self, video_name, timestamp):
        self.video:str = video_name
        self.time:str = timestamp

class Algo3Chi2:
    def __init__(self, hist_size:int=4):
        self.hist_size = hist_size
        self.image_dir = IMAGE_DIR
        self.histogram_matrix = []
        self.index_table = []
        self.indexation_time = 0
        self.minimum_treshold = 14000
        self.high_similarity_treshold = 1000
            
    def create_histogram(self, image):
        if image is None:
            print("Could not open or find the image")
            exit(0)
        if len(image.shape) == 2: # Grayscale image
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        channels = cv2.split(image)
        hist_r = []
        hist_g = []
        hist_b = []
        for channel in channels:
            hist = cv2.calcHist([channel], [0], None, [self.hist_size], [0, 256])
            if np.array_equal(channel, channels[0]): # Red channel
                hist_r = hist.flatten()
            elif np.array_equal(channel, channels[1]): # Green channel
                hist_g = hist.flatten()
            else: # Blue channel
                hist_b = hist.flatten()
        return np.concatenate((hist_r, hist_g, hist_b))
    
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
                        # Calculate histogram for the frame
                        histogram = self.create_histogram(frame)
                        
                        # Store the histogram in the matrix
                        self.histogram_matrix.append(histogram)
                        
                        # Store frame specifications in the index table
                        self.index_table.append(FrameData(file_text_name,cap.get(cv2.CAP_PROP_POS_MSEC) / 1000))
                    
                    frame_count += 1
                
                cap.release()

        # Convert the list of histograms into a NumPy array for easier manipulation
        # self.histogram_matrix = np.array(self.histogram_matrix)
        end_time = time.time()
        execution_time = end_time - start_time
        return execution_time
    
    def chi_squared_value(self, hist1, hist2):
    # Calculate the chi-squared statistic manually
        chi_squared = 0.5 * np.sum(((hist1 - hist2) ** 2) / (hist1 + hist2 + 1e-6))
        return chi_squared

    def get_closest_frame(self, image_path):
        image_hist = self.create_histogram(cv2.imread(image_path))
        closest_chi2 = self.minimum_treshold
        closest_frame = FrameData("", "") 

        for i in range(0, len(self.histogram_matrix)):
            frame_hist = self.histogram_matrix[i]
            if(len(frame_hist) != len(image_hist)): continue
            value = self.chi_squared_value(image_hist, frame_hist)
            if value < closest_chi2:
                closest_chi2 = value
                closest_frame.video = self.index_table[i].video
                closest_frame.time = self.index_table[i].time
                if(closest_chi2 < self.high_similarity_treshold):
                    return closest_frame, closest_chi2

        return closest_frame, closest_chi2
    
    

    def compare_images(self):
        self.indexation_time = self.indexation()
        for image_name in os.listdir(self.image_dir):
            start_time = time.time()
            image_path = os.path.join(self.image_dir, image_name)
            image_text_name,  _ = os.path.splitext(os.path.basename(image_path))
            closest_frame, closest_chi2 = self.get_closest_frame(image_path)
            print(f"Closest frame for {image_text_name} is {closest_frame.video}/{closest_frame.time} with a value of {closest_chi2}")
            with open(TEST_CSV_PATH, 'a', newline='') as file:
                writer = csv.writer(file)
                if closest_chi2 < self.minimum_treshold:
                    writer.writerow([image_text_name , closest_frame.video, closest_frame.time])
                else:
                    writer.writerow([image_text_name, 'out', ''])
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Execution time for image {image_name} is : {execution_time}")

    
def main():
    start_time = time.time()
    algo = Algo3Chi2()
    algo.compare_images()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time of indexation with histograms is : {algo.indexation_time}")
    print(f"Execution time of algo3 with Chi2 is : {execution_time}")


if __name__ == "__main__":
    main()