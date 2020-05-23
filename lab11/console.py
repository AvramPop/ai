# -*- coding: utf-8 -*-
from gpalgorithm import Controller

class Console:
    def __init__(self, controller):
        self.__controller = controller
        
    def run(self):
        while True:
            user = int(input("1. run\n0. exit\n>"))
            if user == 1:
                nrInd = int(input("number of individuals:")) 
                ITER = int(input("iterations per epoch:"))
                sizeofTrain = int(input("sizeof train(<4000):"))
                sizeofTest = int(input("sizeof train(<1457):"))
                mutationProbability = float(input("mutation probability:"))
                crossoverProbability = float(input("crossover probability:"))
                epsilon = float(input("epsilon"))
                self.__controller.run(nrInd, ITER, sizeofTrain, sizeofTest, mutationProbability, crossoverProbability, epsilon)
            elif user == 0:
                break
            else:
                print("wrong input")
