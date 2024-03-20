import numpy as np
from Algo1 import Algo1
from PIL import Image

imagePaths = [
    "kodim01.png",
    "kodim02.png",
    "kodim05.png",
    "kodim13.png",
    "kodim23.png",
]
# self.images = [Image.open(path) for path in self.paths]
# image = np.array(Image.open(imagePaths[4])) 

quantifications = [(8, 4, 4), (8, 8, 4), (8, 8, 8), (8, 4, 0)]
n = 3
base_couleur = "rgb"
if(base_couleur == "yuv"):
    algo1 = Algo1(quantifications[n],True)
else:
    algo1 = Algo1(quantifications[n],False)
for i in range(len(imagePaths)):
    image = np.array(Image.open(imagePaths[i])) 

    algo1.processImage(image)
