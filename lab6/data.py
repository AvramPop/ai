from random import shuffle
from copy import deepcopy
class Data:
    def __init__(self, filename):
        self.__data = self.__loadData(filename)

    def __loadData(self, filename):
        file = open(filename, "r")
        lines = file.readlines()        
        data = []
        for line in lines:
            line = line.strip()
            line = line.split(',')
            data.append(Entry(line[0], [int(i) for i in line[1:]]))
        file.close()        
        return data
    
    def getData(self):
        temp = deepcopy(self.__data)
        shuffle(temp)
        return temp[:(int)(len(temp) * 0.8)], temp[(int)(len(temp) * 0.8):]

    def getTestData(self):
        return self.__data[(int)(len(self.__data) * 0.8):]

    def getTrainData(self):
        return self.__data[:(int)(len(self.__data) * 0.8)]

class Entry:
    def __init__(self, entryClass, attributes):
        self.__entryClass = entryClass
        self.__attributes = attributes

    def getClass(self):
        return self.__entryClass

    def getAttributes(self):
        return self.__attributes

    def getNumberOfAttributes(self):
        return len(self.__attributes)
    
    def getMedianValueForAttribute(self, attributeNumber):
        return 3    # 3 is the median value of 1 -> 5, the possible values
    
    def getCategoriesForAttribute(self, separationAttribute):
        return [0, 1]   # we work with binary distributions
    
    def __str__(self):
        attributes = ""
        for attr in self.getAttributes():
            attributes += str(attr) + " "
        return self.getClass() + " " + attributes
