from PIL import Image
from Alice_LZW import AliceLZW
import os
import numpy as np


#inspiration https://github.com/ashmeet13/LZW-Image-Compression

class LZW:
    def __init__(self, path):
        self.path = path
        self.compressionDictionary, self.compressionIndex = self.createCompressionDict()
        self.freqDict = {}
        self.finalLength = 0

    
    ''''''
    ''' --------------------- Compression of the Image --------------------- '''
    ''''''

    def compress(self):
        self.initCompress()
        compressedcColors = []
        print("Compressing Image ...")
        compressedcColors.append(self.compressColor(self.red))
        print("Compressing Image ...")
        compressedcColors.append(self.compressColor(self.green))
        print("Compressing Image ...")
        compressedcColors.append(self.compressColor(self.blue))
        print("Image Compressed --------- Writing to File")
        filesplit = str(os.path.basename(self.path)).split('.')
        filename = filesplit[0] + 'Compressed1.lzw'
        savingDirectory = os.path.join(os.getcwd(),'CompressedFiles')
        if not os.path.isdir(savingDirectory):
            os.makedirs(savingDirectory)
        with open(os.path.join(savingDirectory,filename),'w') as file:
            for color in compressedcColors:
                for row in color:
                    file.write(row)
                    file.write("\n")
                
    def compressColor(self, colorList):
        compressedColor = []
        i = 0
        compressor = AliceLZW(dictionnary=self.compressionDictionary)

        for currentRow in colorList:
            # Split the input string using a comma as the separator
            values_list = currentRow.split(',')
            # Remove leading and trailing whitespaces from each element
            values_list = [value.strip() for value in values_list]

            compressor.readLZW(currentRow)
            compressedRow:str = ','.join(map(str, compressor.lzwCode))
            compressedColor.append(compressedRow)
        self.finalLength += compressor.finalLength
        return compressedColor

    

    ''''''
    ''' ---------------------- Class Helper Functions ---------------------- '''
    ''''''

    '''
    Used For: Compression of Image
    Function: This function breaks down the image into the three constituting
              image chanels - Red, Green and Blue.
    '''
    def initCompress(self):
        self.image = Image.open(self.path)
        self.height, self.width = self.image.size
        self.red, self.green, self.blue = self.processImage()

    '''
    Used For: Compression of Image
    Function: This function breaks down the image into the three constituting
              image chanels - Red, Green and Blue.
    '''
    def processImage(self):
        image = self.image.convert('RGB')
        red, green, blue = [], [], []
        pixel_values = list(image.getdata())
        iterator = 0
        for height_index in range(self.height):
            R, G, B = "","",""
            for width_index in range(self.width):
                RGB = pixel_values[iterator]
                R = R + str(RGB[0]) + ","
                G = G + str(RGB[1]) + ","
                B = B + str(RGB[2]) + ","
                self.freqDict.setdefault(RGB[0], 0)
                self.freqDict.setdefault(RGB[1], 0)
                self.freqDict.setdefault(RGB[2], 0)

                iterator+=1
            red.append(R[:-1])
            green.append(G[:-1])
            blue.append(B[:-1])
        return red,green,blue

    '''
    Used For: Compression of Image
    Function: This function will initialise the compression dictionary
    '''
    def createCompressionDict(self):
        dictionary = {}
        for i in range(10):
            dictionary[str(i)] = i
        dictionary[','] = 10
        return dictionary,11
    

#CompressionTest
compressor = LZW(os.path.join("Images", "image_4.png"))
compressor.compress()
nbSymbolsOriginal = len(compressor.freqDict)
nbSymbolsFinal = len(compressor.compressionDictionary)
if (nbSymbolsOriginal > 1):
    originalLength = np.ceil(np.log2(nbSymbolsOriginal))*(compressor.height * compressor.width * 3) 
else:
    originalLength = compressor.height * compressor.width * 3
print("Longueur = {0}".format(compressor.finalLength))
print("Longueur originale = {0}".format(originalLength))