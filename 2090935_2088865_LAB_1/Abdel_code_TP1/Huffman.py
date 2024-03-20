#inspiration : https://github.com/emersonmde/huffman , https://www.javatpoint.com/huffman-coding-using-python 
import os

import numpy as np

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



class MyHuffman:
    def __init__(self, path:str):
        self.huffmanDict = dict()

        self.path:str = path
        self.message:str = open(self.path, 'r').read()
        self.freqDict:dict = {}
        self.originalLength = 0
        self.finalLength = 0

    def frequencies(self):
        """Return a dict of frequencies for each letter found in text"""
        for c in self.message:
            self.freqDict.setdefault(c, 0)
            self.freqDict[c] += 1
        nbSymbols = len(self.freqDict)
        self.originalLength = np.ceil(np.log2(nbSymbols))*len(self.message)
        if(nbSymbols ==1):
            self.originalLength = len(self.message)
        return self.freqDict
    


    def assignCodes(self,node:Node = None, code=""):

        if not node:
            node = self.parentTreeNode

        if node.symbol:
            self.huffmanDict[str(node.symbol)] = code
        else:
            if node.left:
                self.assignCodes(node.left, code + "0")
            if node.right:
                self.assignCodes(node.right, code + "1")

        return self.huffmanDict
    
    def createTree(self):
        nodes = [Node(symbol=key, weight=value) for key, value in self.freqDict.items()]

        while len(nodes) > 1:
            nodes.sort(key=lambda x: x.weight)
            left_child = nodes.pop(0)
            right_child = nodes.pop(0)
            parent = Node(weight=left_child.weight + right_child.weight, left=left_child, right=right_child)
            nodes.append(parent)
        self.parentTreeNode:Node = nodes[0]

        return nodes[0].left.symbol, nodes[0].right.symbol
    
    def readHuffman(self, message:str):
        index:int = 0
        huffmanCode = []
        while(index < len(message)):
            currentSymbol: str = message[index]
            huffmanCode.append(self.huffmanDict[currentSymbol])
            self.finalLength += len(self.huffmanDict[currentSymbol])
            index += 1
        return huffmanCode
    

#Compression test    
compressor = MyHuffman(os.path.join("textes", "texte_1.txt"))
Message = compressor.message
print(compressor.frequencies())
print(compressor.createTree())
dictionnaire = compressor.assignCodes()
print(dictionnaire)
MessageCode = compressor.readHuffman(compressor.message)
print(MessageCode)



print(MessageCode)

print("Longueur = {0}".format(compressor.finalLength))
print("Longueur originale = {0}".format(compressor.originalLength))

