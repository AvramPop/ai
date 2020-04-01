# -*- coding: utf-8 -*-

from Ant import Ant
from Problem import Problem
from copy import deepcopy
from math import inf, sqrt

class Controller:
    def __init__(self, problem):
        self.__problem = problem
        self.__population = []
        n = self.__problem.getSize()
        self.__trace = [[[1 for i in range(2 * n)] for j in range(n)] for k in range(n)]
        
    def __iteration(self):
        antSet = [Ant(self.__problem.getSize()) for i in range(self.__problem.getNumberOfAnts())]
        for component in range(2):
            for row in range(self.__problem.getSize()):
                for column in range(self.__problem.getSize()):
                    for ant in antSet:
                        ant.update(self.__problem.getQ0(), self.__trace, self.__problem.getAlpha(), self.__problem.getBeta(), row, column, component)

        deltaTrace = [ 1.0 / antSet[i].evaluate() for i in range(len(antSet))]
        for i in range(self.__problem.getSize()):
            for j in range(self.__problem.getSize()):
                for k in range(2 * self.__problem.getSize()):
                    self.__trace[i][j][k] = (1 - self.__problem.getRho()) * self.__trace[i][j][k]
                
        for i in range(len(antSet)):
            for row in range(self.__problem.getSize()):
                for column in range(self.__problem.getSize() - 1):
                    x = antSet[i].getRow(row)[column].getValue()[0] - 1
                    y = antSet[i].getRow(row)[column + 1].getValue()[0] - 1
                    self.__trace[x][y][row] = self.__trace[x][y][row] + deltaTrace[i]
                    x = antSet[i].getRow(row)[column].getValue()[1] - 1
                    y = antSet[i].getRow(row)[column + 1].getValue()[1] - 1
                    self.__trace[x][y][self.__problem.getSize() + row] = self.__trace[x][y][self.__problem.getSize() + row] + deltaTrace[i]
        
        bestFitness = inf
        best = -1
        for i in range(len(antSet)):
            if antSet[i].evaluate() < bestFitness:
                best = i
                bestFitness = antSet[i].evaluate()
        return antSet[best]
    
    def runAlgorithm(self):
        best = None
        bestFitness = inf
        for i in range(self.__problem.getNumberOfEpochs()):
            solution = deepcopy(self.__iteration())
            if solution.evaluate() < bestFitness:
                best = deepcopy(solution)
                bestFitness = solution.evaluate()
        return best

    def stats(self, iters):
        fitnessSum = 0
        fitnesses = []
        for i in range(iters):
            print("running stats")
            currentSolution = self.runAlgorithm()
            currentFitness = currentSolution.evaluate()
            fitnessSum += currentFitness
            fitnesses.append(currentFitness)
        average = fitnessSum / iters
        differencesSquaresSum = 0
        for i in range(iters):
            differencesSquaresSum += pow(fitnesses[i] - average, 2)
        standardDeviation = sqrt(differencesSquaresSum / iters)
        return (average, standardDeviation, fitnesses)
