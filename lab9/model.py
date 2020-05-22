# -*- coding: utf-8 -*-
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D
from data import *

class CNN:
    def __init__(self, kernelXSize, kernelYSize, poolXSize, poolYSize, outputShape, dropoutRate, epochs):
        data = Data()
        self.__xTrain, self.__yTrain, self.__xTest, self.__yTest, self.__xSize, self.__ySize, self.__inputShape = data.getData()
        self.__model = Sequential()
        self.__setupLayers(kernelXSize, kernelYSize, poolXSize, poolYSize, outputShape, dropoutRate)
        self.__compileModel()
        self.__trainModel(epochs)

    def __setupLayers(self, kernelXSize, kernelYSize, poolXSize, poolYSize, outputShape, dropoutRate):
        self.__addConvolutionLayer(kernelXSize, kernelYSize)
        self.__addPoolingLayer(poolXSize, poolYSize)
        self.__flatten()
        self.__addDenseCustom(outputShape)
        self.__addDropout(dropoutRate)
        self.__addDenseFixed()

    def evaluateModel(self, ):
        self.__model.evaluate(self.__xTest, self.__yTest)

    def __addConvolutionLayer(self, kernelXSize, kernelYSize):
        self.__model.add(Conv2D(self.__xSize, kernel_size=(kernelXSize, kernelYSize), input_shape=self.__inputShape))

    def __addPoolingLayer(self, poolXSize, poolYSize):
        self.__model.add(MaxPooling2D(pool_size=(poolXSize, poolYSize)))

    def __flatten(self):
        self.__model.add(Flatten())

    def __addDenseCustom(self, outputShape):
        self.__model.add(Dense(outputShape, activation=tf.nn.relu))

    def __addDropout(self, dropoutRate):
        self.__model.add(Dropout(dropoutRate))

    def __addDenseFixed(self):
        self.__model.add(Dense(10, activation=tf.nn.softmax))

    def __compileModel(self):
        self.__model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

    def __trainModel(self, numberOfEpochs):
        self.__model.fit(x=self.__xTrain, y=self.__yTrain, epochs=numberOfEpochs)
