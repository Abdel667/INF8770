# IMPORTS
from enum import Enum
import os
import cv2
import numpy as np
from scipy.stats import chisquare

#Définition de la classe générale et de ses paramètres (notament is_inside)
class FrameData:
    def __init__(self, video_name, frame_name, distance):
        self.video_name:str = video_name
        self.frame_name:str = frame_name
        self.distance:float = distance

class CompareMethod(Enum):
    EUCLIDEAN = "euclidean"
    CHI2 = "chi2"

class Algo3Euclide:
    def __init__(self, hist_size:int, frames_dir:str):
        self.frames_dir = frames_dir
        self.hist_size = hist_size

    # Fonction de Construction des histogrammes de couleurs 1D pour chaque trames (RGB ou YUV)
    #TODO sauvegarde des descripteurs des histogrammes de couleurs 1D afin de les réutiliser pour l'autre hypothèse
    def create_histogram(self, image_path, hist_size=4):
        # Load the image
        image = cv2.imread(image_path)

        # Ensure the image is loaded correctly
        if image is None:
            print("Could not open or find the image")
            exit(0)

        # Split the image into its color channels
        channels = cv2.split(image)

        # Initialize lists to hold the histogram data
        hist_r = []
        hist_g = []
        hist_b = []

        # Calculate histograms for each channel with specified histSize
        for channel in channels:
            hist = cv2.calcHist([channel], [0], None, [hist_size], [0, 256])
            if channel == channels[0]: # Red channel
                hist_r = hist.flatten()
            elif channel == channels[1]: # Green channel
                hist_g = hist.flatten()
            else: # Blue channel
                hist_b = hist.flatten()

        # Print the histograms
        print("Red Channel Histogram:", hist_r)
        print("Green Channel Histogram:", hist_g)
        print("Blue Channel Histogram:", hist_b)
        return np.concatenate((hist_r, hist_g, hist_b))
    
    # Fonction poour calculer la distance euclidienne entre deux histogrammes pour mesurer leur affinité
    def euclidean_distance(hist1, hist2):
        return np.linalg.norm(hist1 - hist2)
    
    #TODO ouvrir le dir des frames et conserver pour chaque dir le nom de la vidéo et le nom de la frame 
    #                 qui a la plus petite distance euclidienne par rapport à l'image
    def build_set(self, video_parent_dir,image_hist):# builds the set of euclidian distances
        closest_frame = FrameData("", "", float('inf'))
        for video_dir in os.listdir(video_parent_dir):
            for frame in os.listdir(video_dir):
                frame_path = os.path.join(video_dir, frame)
                frame_hist = self.create_histogram(frame_path)
                distance = self.euclidean_distance(image_hist, frame_hist)
                if distance < closest_frame['distance']:
                    closest_frame['distance'] = distance
                    closest_frame['video'] = video_dir
                    closest_frame['frame'] = frame
            
        
    #TODO déterminer la vidéo à laquelle apparrtient l'image et le temps le plus     
    # proche auquel elle a été prise
    def compare_histograms(self, hist1, hist2):
        return self.euclidean_distance(hist1, hist2)
    



# Fonction poour calculer le Chi 2 entre deux histogrammes pour mesurer leur affinité


#Fonction de comparaison des image  vidéo
    
