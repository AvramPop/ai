# -*- coding: utf-8 -*-
from controller import Controller

class Console:
    def __init__(self, controller):
        self.__controller = controller

    def run(self):
        while True:
            userInput = int(input("1. run\n0. exit\n>"))
            if userInput == 1:
                print("INPUT")
                print(self.__controller.getInputs())
                print("OUTPUT")
                result = "{\'time\': " + self.__controller.compute() + "}"
                print(result)
            elif userInput == 0:
                break
            else:
                print("wrong input")
