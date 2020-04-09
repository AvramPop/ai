# -*- coding: utf-8 -*-

from controller import Controller

class Console:
    def __init__(self, controller):
        self.__controller = controller
        
    def run(self):
        while True:
            print("Please choose the selection attribute algorithm:")
            userInput = int(input("1 - gini index\n2 - information gain\n0 - exit\n>"))
            if userInput == 1:
                self.__controller.run("gini")
            elif userInput == 2:
                self.__controller.run("gain")
            elif userInput == 0:
                break
            else:
                print("wrong input")
                