import numpy as np
import matplotlib.pyplot as py
from PIL import Image
from numpy import linalg as LA
from skimage.metrics import structural_similarity, peak_signal_noise_ratio


class Algo2:

  def __init__(self):
    self.quant = (8, 4, 4)

  # TODO Changement de couleur RGB ou YUV if(type(color) == "rgb"))
  def processImage(self, imageLue, eigvec, toPrint):
    py.figure(figsize = (10,10))
    py.imshow(imageLue)
    py.show()
    image = imageLue.astype('double')


    # py.figure(figsize = (10,10))
    # py.imshow(image[:,:,0], cmap='gray')
    # py.show()
    # py.figure(figsize = (10,10))
    # py.imshow(image[:,:,1], cmap='gray')
    # py.show()
    # py.figure(figsize = (10,10))
    # py.imshow(image[:,:,2], cmap='gray')
    # py.show()

  #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\Moyenne////////////////////////////////////////
    sommeR = 0.0
    sommeG = 0.0
    sommeB = 0.0
    for i in range(len(image)):
        for j in range(len(image[0])):
            sommeR += image[i][j][0]
            sommeG += image[i][j][1]
            sommeB += image[i][j][2]
            
    nbPixels = len(image) * len(image[0])        
    moyR = sommeR / nbPixels
    moyG = sommeG / nbPixels
    moyB = sommeB / nbPixels

    print(moyR)
    print(moyG)
    print(moyB)

    #////////////////////////////////////////Application du changement de base////////////////////////////////////////
    imageKL = np.copy(image)
    vecMoy = [[moyR], [moyG], [moyB]]

    for i in range(len(imageKL)):
        for j in range(len(imageKL[0])):
            vecTemp = [[image[i][j][0]], [image[i][j][1]], [image[i][j][2]]]
            imageKL[i][j][:] = np.reshape(np.dot(eigvec, np.subtract(vecTemp, vecMoy)), (3))

#////////////////////////////////////////Quantification////////////////////////////////////////
    min0 = np.min(imageKL[:,:,0])
    min1 = np.min(imageKL[:,:,1])
    min2 = np.min(imageKL[:,:,2])

    range0 = np.max(imageKL[:,:,0]) - min0
    range1 = np.max(imageKL[:,:,1]) - min1
    range2 = np.max(imageKL[:,:,2]) - min2

    scaling0 = (range0 / (2**self.quant[0] - 1)) if self.quant[0] else 0
    scaling1 = (range1 / (2**self.quant[1] - 1)) if self.quant[1] else 0
    scaling2 = (range2 / (2**self.quant[2] - 1)) if self.quant[2] else 0

    for i in range(len(imageKL)):
        for j in range(len(imageKL[0])):
            imageKL[i][j][0] = (round((imageKL[i][j][0] - min0) / scaling0)) if self.quant[0] else 0
            imageKL[i][j][1] = (round((imageKL[i][j][1] - min1) / scaling1)) if self.quant[1] else 0
            imageKL[i][j][2] = (round((imageKL[i][j][2] - min2) / scaling2)) if self.quant[2] else 0
            
    print(imageKL)
            
    for i in range(len(imageKL)):
        for j in range(len(imageKL[0])):
            imageKL[i][j][0] = ((imageKL[i][j][0] * scaling0) + min0) if self.quant[0] else (min0 + (range0 / 2))
            imageKL[i][j][1] = ((imageKL[i][j][1] * scaling1) + min1) if self.quant[1] else (min1 + (range1 / 2))
            imageKL[i][j][2] = ((imageKL[i][j][2] * scaling2) + min2) if self.quant[2] else (min2 + (range2 / 2))

    #                          RECONSTRUCTION DE L'IMAGE ET EVALUATION
            
    invEigvec = LA.pinv(eigvec)
    vecMoy = [moyR, moyG, moyB] 
    imageInv = np.copy(image)

    for i in range(len(imageInv)):
        for j in range(len(imageInv[0])):
            vecTemp = [[imageKL[i][j][0]], [imageKL[i][j][1]], [imageKL[i][j][2]]]
            imageInv[i][j][:] = np.add(np.reshape(np.dot(invEigvec, vecTemp), (3)), vecMoy)



    imageInv = np.clip(imageInv, 0, 255)
    imageObtenue = imageInv.astype('uint8')

    compression = 1 - ((self.quant[0] + self.quant[1] + self.quant[2]) / 24)
    psnr = peak_signal_noise_ratio(imageLue, imageObtenue)
    ssim = structural_similarity(imageLue, imageObtenue, win_size=3, multichannel=True)
    print(toPrint)

    py.figure(figsize = (10,10))
    py.imshow(imageObtenue)
    title = f"{'RGB'}, self.Quantification: {self.quant[0]}/{self.quant[1]}/{self.quant[2]}, Compression: {compression:.2f}, PSNR: {psnr:.2f}, SSIM: {ssim:.2f}"
    py.title(title)
    py.axis('off')
    print(toPrint)
    py.show()

    py.figure(figsize = (10,10))
    py.imshow(imageLue)
    py.title('Image originale')
    py.axis('off')
    print(toPrint)
    py.show()

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\KL///////////////////////////////////////////////////////////////////////////////////

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\KL///////////////////////////////////////////////////////////////////////////////////
  def calcKL(self, imageLue):
    py.figure(figsize = (10,10))
    py.imshow(imageLue)
    py.show()
    image = imageLue.astype('double')


    # py.figure(figsize = (10,10))
    # py.imshow(image[:,:,0], cmap='gray')
    # py.show()
    # py.figure(figsize = (10,10))
    # py.imshow(image[:,:,1], cmap='gray')
    # py.show()
    # py.figure(figsize = (10,10))
    # py.imshow(image[:,:,2], cmap='gray')
    # py.show()

    sommeR = 0.0
    sommeG = 0.0
    sommeB = 0.0
    for i in range(len(image)):
        for j in range(len(image[0])):
            sommeR += image[i][j][0]
            sommeG += image[i][j][1]
            sommeB += image[i][j][2]
            
    nbPixels = len(image) * len(image[0])        
    moyR = sommeR / nbPixels
    moyG = sommeG / nbPixels
    moyB = sommeB / nbPixels

    print(moyR)
    print(moyG)
    print(moyB)
  
    covRGB = np.zeros((3,3), dtype = "double")
    for i in range(len(image)):
        for j in range(len(image[0])):
            vecTemp=[[image[i][j][0] - moyR], [image[i][j][1]] - moyG, [image[i][j][2] - moyB]]
            vecProdTemp = np.dot(vecTemp, np.transpose(vecTemp))
            covRGB = np.add(covRGB, vecProdTemp)

    covRGB /= nbPixels        
    print(covRGB)


    eigval, eigvec = LA.eig(covRGB)
    print(eigval)
    print()
    print(eigvec)
    eigvec = np.transpose(eigvec)
    return eigvec
