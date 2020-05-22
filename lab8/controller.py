# -*- coding: utf-8 -*-
from network import Network
from function_factory import FunctionFactory


class Controller:
    def __init__(self, filename):
        self.__inputData, self.__outputData = self.__readData(filename)

    def __readData(self, filename):
        inputDataFile = open(filename, 'r')
        lines = inputDataFile.readlines()
        inputValues = []
        outputValues = []
        for line in lines:
            line.strip()
            splitLine = line.split(" ")
            floatsInput = [float(value) for value in splitLine]
            outputValues.append([floatsInput[-1]])
            floatsInput.pop()
            inputValues.append(floatsInput)
        return inputValues, outputValues

    def fireANN(self, numberOfIterations, learnRate):
        neuralNetwork = Network([len(self.__inputData[0]), len(self.__inputData[0]), len(self.__outputData[0])], FunctionFactory.linearFunction, FunctionFactory.linearFunctionDifferentiated)

        errors = []
        iterations = []
        for i in range(numberOfIterations):
            iterations.append(i)
            e = []
            for j in range(len(self.__inputData)):
                e.append(neuralNetwork.computeLoss(self.__inputData[j], self.__outputData[j])[0])
                neuralNetwork.backPropagate(neuralNetwork.computeLoss(self.__inputData[j],self.__outputData[j]), learnRate)
            errors.append(sum([x**2 for x in e]))
        for j in range(len(self.__inputData)):
            print(self.__inputData[j], self.__outputData[j], neuralNetwork.feedForward(self.__inputData[j]))
        print(str(neuralNetwork))
        return iterations, errors