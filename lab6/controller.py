from data import Data
from decision_tree import DecisionTree
from numpy import std, mean

class Controller:
    def __init__(self, data):
        self.__data = data
        
    def run(self, strategy):
        print("running 1000 tests")
        values = []
        for i in range(1000):
            trainData, testData = self.__data.getData()
            decisionTree = DecisionTree(trainData, strategy)
            accuracy = decisionTree.accuracy(testData)
            print("#", i, " run. Accuracy: ", accuracy)
            values.append(accuracy)
        valuesMean = mean(values)
        standardDeviation = std(values)
        print("Mean: ", valuesMean)
        print("Standard deviation: ", standardDeviation)