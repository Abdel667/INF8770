import sys
from typing import List
import os

import numpy as np

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def starts_with_prefix(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
    
class AliceLZW:

    def __init__(self, path:str=None, dictionnary:dict=None):
        self.increment:int = 0
        self.lzwCode: List[str] = []
        self.index:int = 0
        self.originalLength:int = 0
        self.finalLength:int = 0
        self.dicKeysTrie:Trie = Trie()

        if(path != None):
            self.path:str = path
            self.message:str = open(self.path, 'r').read()
            self.myDict:dict = {}
            self.initDict(self.message)
        elif(dictionnary!= None):
            self.myDict:dict = dictionnary
        self.initDicTrie()
        
        
        

    def initDicTrie(self):
        for key in self.myDict.keys():
            self.dicKeysTrie.insert(key)

    def initDict(self,txt:str):
        nbSymbols = 1
        self.myDict[txt[0]] = 0
        for i in range(len(txt)):
            if txt[i] not in self.myDict:
                self.addToDict(txt[i])
                nbSymbols+=1
        self.originalLength = np.ceil(np.log2(nbSymbols))*len(self.message)  

    def resetDefault(self):
        self.initDicTrie = Trie()
        self.index = 0
        self.lzwCode = []


    def addToDict(self,symbol:str):
        # Initialiser une variable d'incrémentation si elle self.index'existe pas
        # Incrémenter la valeur pour la prochaine clé en binaire
        self.increment += 1

        # Convertir la valeur en binaire et l'associer à la clé
        binary_value = str(bin(self.increment)[2:])

        #Ajout de 1 bit si requis
        if len(binary_value) > len(str(list(self.myDict.values())[0])):
            for key, value in self.myDict.items():
                self.myDict[key] = '0' + str(value)

        self.myDict[symbol] = binary_value
        self.dicKeysTrie.insert(symbol)

    def processSymbol(self, currentSymbol: str, message):
        nextIndex = self.index + 1
        nextChar :str | None = message[nextIndex] if nextIndex < len(message) else None

        prefixExists = self.dicKeysTrie.starts_with_prefix(currentSymbol)

        if prefixExists:
            if nextChar is not None and self.dicKeysTrie.starts_with_prefix(currentSymbol + nextChar):
                currentSymbol += nextChar
                self.index += 1
                self.processSymbol(currentSymbol, message)
            else:
                self.lzwCode.append(self.myDict[currentSymbol])
                self.finalLength += len(str(self.myDict[currentSymbol])) 
                if nextChar is not None:
                    self.addToDict(currentSymbol + nextChar)
        else:
            self.addToDict(currentSymbol)
            self.lzwCode.append(self.myDict[currentSymbol])
            self.finalLength += len(self.myDict[currentSymbol]) 
            if nextChar is not None:
                self.addToDict(currentSymbol + nextChar)

            

    def readLZW(self,message): 
        self.resetDefault()
        while(self.index < len(message)):
            currentSymbol = message[self.index]
            self.processSymbol(str(currentSymbol), message)
            self.index += 1
        

    def compressTextFile(self):
        self.readLZW(self.message)
        print(self.lzwCode)
        print(self.myDict)
        print("Longueur = {0}".format(self.finalLength))
        print("Longueur originale = {0}".format(self.originalLength))
        # return self.lzwCode, self.myDict

# print(sys.getrecursionlimit())

#Compression test
# compressor = AliceLZW(os.path.join("textes", "texte_3.txt"))
# compressor.compressTextFile()