# -*- coding: utf-8 -*-

class Problem:
    def __init__(self, n):
        self.__n = n
        
    def __readIndividualSizeFromFile(self, filename):
        file = open(filename, "r")
        n = int(file.readline().strip())
        file.close()
        return n
    
    def getSize(self):
        return self.__n