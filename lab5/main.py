# -*- coding: utf-8 -*-
from Controller import Controller

def main():
    problem = Problem("data.in")
    controller = Controller(problem)
    solution = controller.runAlgorithm()
    print(str(solution) + "\nFitness:" + str(solution.evaluate()))
    
main()