# IMPORTS
import csv
from enum import Enum
import os
import time
import cv2
import numpy as np
from frame_colector import sample_frames

IMAGE_DIR = f"moodle/data/jpeg"
VIDEO_DIR = f"moodle/data/mp4"
TEST_CSV_PATH = f"moodle/data/test.csv"
FRAME_DIR = f"moodle/video_frames"
TRESHOLD = 100000

#Définition de la classe générale et de ses paramètres (notament is_inside)
class FrameData:
    def __init__(self, video_name, frame_name, distance):
        self.video_name:str = video_name
        self.frame_index:str = frame_name
        self.distance:float = distance

class CompareMethod(Enum):
    EUCLIDEAN = "euclidean"
    CHI2 = "chi2"

class Algo3Euclide:
    def __init__(self, hist_size:int=4, frame_sampled:bool = True):
        self.frames_dir = FRAME_DIR
        self.hist_size = hist_size
        self.image_dir = IMAGE_DIR
        self.frame_histograms:dict = {}
        if not frame_sampled:
            sample_frames()
    
    # Fonction de Construction des histogrammes de couleurs 1D pour chaque trames (RGB ou YUV)
    #TODO sauvegarde des descripteurs des histogrammes de couleurs 1D afin de les réutiliser pour l'autre hypothèse
    def create_histogram(self, image_path):
        # Load the image
        image = cv2.imread(image_path)

        # Ensure the image is loaded correctly
        if image is None:
            print("Could not open or find the image")
            exit(0)

        if len(image.shape) == 2: # Grayscale image
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        # Split the image into its color channels
        channels = cv2.split(image)

        # Initialize lists to hold the histogram data
        hist_r = []
        hist_g = []
        hist_b = []

        # Calculate histograms for each channel with specified histSize
        for channel in channels:
            hist = cv2.calcHist([channel], [0], None, [self.hist_size], [0, 256])
            if np.array_equal(channel, channels[0]): # Red channel
                hist_r = hist.flatten()
            elif np.array_equal(channel, channels[1]): # Green channel
                hist_g = hist.flatten()
            else: # Blue channel
                hist_b = hist.flatten()

        # Print the histograms
        # print("Red Channel Histogram:", hist_r)
        # print("Green Channel Histogram:", hist_g)
        # print("Blue Channel Histogram:", hist_b)
        return np.concatenate((hist_r, hist_g, hist_b))
    
    # Fonction poour calculer la distance euclidienne entre deux histogrammes pour mesurer leur affinité
    def euclidean_distance(self,hist1, hist2):
        return np.linalg.norm(hist1 - hist2)
    
    #TODO ouvrir le dir des frames et déterminer la frame qui a la plus petite distance euclidienne par rapport à l'image
    def precompute_histograms(self):
        for video_dir in os.listdir(self.frames_dir):
            full_video_dir = os.path.join(self.frames_dir, video_dir)
            for frame in os.listdir(full_video_dir):
                frame_path = os.path.join(full_video_dir, frame)
                frame_hist = self.create_histogram(frame_path)
                # Store the histogram using the frame path as the key
                self.frame_histograms[frame_path] = frame_hist

    def get_closest_frame(self, image_path):
        isfound = False
        image_hist = self.create_histogram(image_path)
        closest_frame = FrameData("", "", TRESHOLD)
        for frame_path, frame_hist in self.frame_histograms.items():
            if(len(frame_hist) != len(image_hist)): continue
            distance = self.euclidean_distance(image_hist, frame_hist)
            if distance < closest_frame.distance:
                closest_frame.distance = distance
                closest_frame.video_name = os.path.dirname(frame_path)
                closest_frame.frame_index = os.path.basename(frame_path)
                isfound = True
            if(isfound):
                break
        return closest_frame
    
    def compare_images(self):
        self.precompute_histograms()  # Precompute the histograms before comparing images
        for image_name in os.listdir(self.image_dir):
            start_time = time.time()
            image_path = os.path.join(self.image_dir, image_name)
            closest_frame = self.get_closest_frame(image_path)
            print(f"Closest frame for {image_name} is {closest_frame.video_name}/{closest_frame.frame_index} with a distance of {closest_frame.distance}")
            with open(TEST_CSV_PATH, 'a', newline='') as file:
                writer = csv.writer(file)
                if closest_frame.distance < TRESHOLD:
                    writer.writerow([image_name, closest_frame.video_name, closest_frame.frame_index])
                else:
                    writer.writerow([image_name, 'out', ''])
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Execution time for image {image_name} is : {execution_time}")

    
def main():
    start_time = time.time()
    algo = Algo3Euclide()
    algo.compare_images()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time of algo3 with euclide is : {execution_time}")


if __name__ == "__main__":
    main()