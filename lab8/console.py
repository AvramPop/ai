# -*- coding: utf-8 -*-
from controller import Controller
import matplotlib as mpl

class Console:
    def __init__(self, controller):
        self.__controller = controller

    def run(self):
        while (True):
            userInput = int(input("1. Artificial Neural Network\n0. exit\n>"))
            if userInput == 1:
                iters = int(input("iterations: "))
                learningRate = float(input("rate: "))
                iterations, errors = self.__controller.fireANN(iters, learningRate)
                mpl.pyplot.plot(iterations, errors, label = 'loss value vs iteration')
                mpl.pyplot.xlabel('Iterations')
                mpl.pyplot.ylabel('loss function')
                mpl.pyplot.legend()
                mpl.pyplot.show()
            elif userInput == 0:
                break
            else:
                print("wrong input")
