# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from controller import *

class Console:
  def __init__(self, controller):
    self.__controller = controller

  def run(self):
    while True:
      userInput = int(input("1 - run\n0 - exit\n>"))
      if userInput == 1:
        alpha = float(input("alpha:"))
        iters = int(input("number of iterations:"))

        g, cost, finalCost = self.__controller.results(alpha, iters)
        print("the parameters are: ", g)
        print("the cost is: ", finalCost)

        fig, ax = plt.subplots()
        ax.plot(np.arange(iters), cost, 'r')
        ax.set_xlabel('Iterations')
        ax.set_ylabel('Cost')
        ax.set_title('Cost(iteration) plot')
        plt.show()
      else:
        print("bye")
        break
