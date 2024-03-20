import numpy as np
from Algo2 import Algo2
from PIL import Image

imagePaths = [
    "kodim01.png",
    "kodim02.png",
    "kodim05.png",
    "kodim13.png",
    "kodim23.png",
]

quantifications = [(8, 4, 4)]

algo2 = Algo2()

for i in range(len(imagePaths)):
    for j in range(len(imagePaths)):
        if i != j:
            imageToCompress = np.array(Image.open(imagePaths[i]))
            imageToKL = np.array(Image.open(imagePaths[j])) 
            toPrint = f"image To Compress is {imagePaths[i]} and image to KL is {imagePaths[j]}"
            # Call your function for each combination of images
            eigvec = algo2.calcKL(imageToKL)
            algo2.processImage(imageToCompress, eigvec, toPrint)
