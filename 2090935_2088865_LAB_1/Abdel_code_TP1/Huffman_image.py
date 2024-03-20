#inspiration : https://github.com/emersonmde/huffman , https://www.javatpoint.com/huffman-coding-using-python 
import os
import sys
from PIL import Image
import numpy as np

# print(sys.getrecursionlimit())
# sys.setrecursionlimit(300000)


class Node:  
    def __init__(self, weight, symbol=None, left = None, right = None):  
  
        # the symbol  
        self.symbol = symbol  
  
        # the left node  
        self.left = left  
  
        # the right node  
        self.right = right  

        self.weight = weight
  
        # the tree direction (0 or 1)  
        self.code = ''  



class MyHuffmanImage:
    def __init__(self, path:str):
        self.huffmanDict = dict()
        self.finalLength = 0
        
        self.path:str = path
        self.freqDict:dict = {}

    
    '''
    Used For: Compression of Image
    Function: This function breaks down the image into the three constituting
              image chanels - Red, Green and Blue.
    '''
    def initCompress(self):
        self.image = Image.open(self.path)
        self.height, self.width = self.image.size
        self.red, self.green, self.blue = self.processImage()
        self.parentTreeNode:Node = self.createTree()
        self.huffmanDict:dict  = self.assignCodes()


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
                self.freqDict[RGB[0]] += 1
                self.freqDict.setdefault(RGB[1], 0)
                self.freqDict[RGB[1]] += 1
                self.freqDict.setdefault(RGB[2], 0)
                self.freqDict[RGB[2]] += 1
                iterator+=1
            red.append(R[:-1])
            green.append(G[:-1])
            blue.append(B[:-1])
        return red,green,blue

    def assignCodes(self, node=None, code=""):
        if not node:
            node = self.parentTreeNode

        if node.symbol is not "":
            if(node.code == "0"):
                code = node.code
            self.huffmanDict[str(node.symbol)] = code
        else:
            if node.left:
                self.assignCodes(node.left, code + "0")
            if node.right:
                self.assignCodes(node.right, code + "1")

        return self.huffmanDict
    
    def createTree(self):
        nodes = [Node(symbol=key, weight=value) for key, value in self.freqDict.items()]
        if(len(nodes) == 1): 
            nodes[0].code = "0"

        while len(nodes) > 1:  
            nodes.sort(key=lambda x: x.weight)
            left_child = nodes.pop(0)
            right_child = nodes.pop(0)
            parent = Node(weight=left_child.weight + right_child.weight, left=left_child, right=right_child, symbol = '')
            nodes.append(parent)

        return nodes[0]
    

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
        filename = filesplit[0] + 'Compressed.huffman'
        savingDirectory = os.path.join(os.getcwd(),'CompressedFiles')
        if not os.path.isdir(savingDirectory):
            os.makedirs(savingDirectory)
        with open(os.path.join(savingDirectory,filename),'w') as file:
            for color in compressedcColors:
                for row in color:
                    file.write(row)
                    file.write("\n")


    def readHuffman(self, message:str):
        index:int = 0
        # Split the input string using a comma as the separator
        values_list = message.split(',')
        # Remove leading and trailing whitespaces from each element
        values_list = [value.strip() for value in values_list]
        
        huffmanCode = []
        while(index < len(values_list)):
            currentSymbol: str = values_list[index]
            huffmanCode.append(self.huffmanDict[currentSymbol])
            self.finalLength += len(self.huffmanDict[currentSymbol])
            index += 1
        compressedRow:str = ','.join(map(str, huffmanCode))
        return compressedRow
                
    def compressColor(self, colorList):
        compressedColor = []
        i = 0
        
        for currentRow in colorList:
            
            compressedRow:str = self.readHuffman(currentRow)

            compressedColor.append(compressedRow)
        return compressedColor


# Compression test
compressor = MyHuffmanImage(os.path.join("Images", "image_5.png"))
compressor.compress()

nbSymbolsOriginal = len(compressor.freqDict)
if (nbSymbolsOriginal > 1):
    originalLength = np.ceil(np.log2(nbSymbolsOriginal))*(compressor.height * compressor.width * 3) 
else:
    originalLength = compressor.height * compressor.width * 3
print("Longueur = {0}".format(compressor.finalLength))
print("Longueur originale = {0}".format(originalLength))
