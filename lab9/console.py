# -*- coding: utf-8 -*-
from model import CNN
class Console:
    def run(self):
        while True:
            print("Hello to CNN!")
            userInput = int(input("please choose your option:\n1. CNN\n0. exit\n>"))
            if userInput == 1:
                print("configure CNN for MNIST")
                print("recommended configuration:")
                print("kernelXSize = 3")
                print("kernelYSize = 3")
                print("poolXSize = 2")
                print("poolYSize = 2")
                print("outputShape = 128")
                print("dropoutRate = 0.2")
                print("epochs = 10")
                kernelXSize = int(input("kernelXSize: "))
                kernelYSize = int(input("kernelXSize: "))
                poolXSize = int(input("poolXSize: "))
                poolYSize = int(input("poolYSize: "))
                outputShape = int(input("outputShape: "))
                dropoutRate = float(input("dropoutRate: "))
                epochs = int(input("epochs: "))
                cnn = CNN(kernelXSize, kernelYSize, poolXSize, poolYSize, outputShape, dropoutRate, epochs)
                cnn.evaluateModel()
            elif userInput == 0:
                break
            else:
                print("wrong input")

