# -*- coding: utf-8 -*-

class Problem:
    def __init__(self, filename):
        self.__filename = filename
        self.__loadProblem()
        
    def __loadProblem(self):
        file = open(self.__filename, "r")
        self.__n = int(file.readline().strip())
        self.__numberOfEpochs = int(file.readline().strip())
        self.__numberOfAnts = int(file.readline().strip())
        self.__alpha = float(file.readline().strip())
        self.__beta = float(file.readline().strip())
        self.__rho = float(file.readline().strip())
        self.__q0 = float(file.readline().strip())
        file.close()

    def getSize(self):
        return self.__n
    
    def getNumberOfEpochs(self):
        return self.__numberOfEpochs
    
    def getNumberOfAnts(self):
        return self.__numberOfAnts
    
    def getAlpha(self):
        return self.__alpha
    
    def getBeta(self):
        return self.__beta
    
    def getRho(self):
        return self.__rho
    
    def getQ0(self):
        return self.__q0