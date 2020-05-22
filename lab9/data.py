# -*- coding: utf-8 -*-
import tensorflow as tf

class Data:
    def __init__(self):
        self.__xTrain, self.__yTrain, self.__xTest, self.__yTest, self.__xSize, self.__ySize = self.__loadData()
        self.__formatData()

    def getData(self):
        return self.__xTrain, self.__yTrain, self.__xTest, self.__yTest, self.__xSize, self.__ySize, (self.__xSize, self.__ySize, 1)

    def __loadData(self):
        (xTrain, yTrain), (xTest, yTest) = tf.keras.datasets.mnist.load_data()
        xSize, ySize = xTrain.shape[1], xTrain.shape[2]
        return xTrain, yTrain, xTest, yTest, xSize, ySize

    def __formatData(self):
        self.__reshapeData()
        self.__convertData()
        self.__normaliseData()

    def __reshapeData(self):
        self.__xTrain = self.__xTrain.reshape(self.__xTrain.shape[0], self.__xSize, self.__ySize, 1)
        self.__xTest = self.__xTest.reshape(self.__xTest.shape[0], self.__xSize, self.__ySize, 1)

    def __convertData(self):
        self.__xTrain = self.__xTrain.astype('float32')
        self.__xTest = self.__xTest.astype('float32')

    def __normaliseData(self):
        normalisationRGBValue = 255
        self.__xTrain /= normalisationRGBValue
        self.__xTest /= normalisationRGBValue
