# -*- coding: utf-8 -*-
from Controller import Controller
from Problem import Problem
import matplotlib.pyplot as plt

def main():
    problem = Problem("data.in")
    controller = Controller(problem)
    inp = int(input("1-one run\n2-stats\n0-exit\n>"))
    if inp == 1:
        solution = controller.runAlgorithm()
        print(str(solution) + "\nFitness:" + str(solution.evaluate()))
    elif inp == 2:
        sts = controller.stats(problem.getStatsIters())
        print("Average: " + str(sts[0]) + "\nStandard deviation:" + str(sts[1]))
        plt.plot(sts[2])
        plt.show()
    else:
        print("bye")
    
main()