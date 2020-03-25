# -*- coding: utf-8 -*-
from Population import *
from Problem import *
from qtpy.QtCore import QThread, Signal
from math import inf, sqrt

class HillClimbAlgorithm:
    def __init__(self, problem, statsFilename):
        self.__problem = problem
        self.__statsIterations = self.__readStatsData(statsFilename)
    
    def __readStatsData(self, filename):
        file = open(filename, "r")
        n = int(file.readline().strip())
        file.close()
        return n    

    def getProblem(self):
        return self.__problem
    
    def getStatsIterations(self):
        return self.__statsIterations
    
class HillClimbingAlgorithmThread(QThread):
    findSignal = Signal('PyQt_PyObject')
    
    def __init__(self, hillClimbingAlgorithm):
        QThread.__init__(self)
        self.__hillClimbingAlgorithm = hillClimbingAlgorithm
    
    def run(self):
        self.running = True
        population = Population(1, self.__hillClimbingAlgorithm.getProblem().getSize())
        currentNode = copy.deepcopy(population.getPopulation()[0])
        while currentNode.fitness() > 0:
            if self.running == False:
                return
            self.findSignal.emit((currentNode, False)) 
            self.sleep(1)
            neighbours = currentNode.neighboursOf()
            neighbours.sort(key=lambda b: b.fitness())
            bestNeighbour = neighbours[0]
            if bestNeighbour.fitness() < currentNode.fitness():
                currentNode = copy.deepcopy(bestNeighbour)
            else:
                self.findSignal.emit((currentNode, True)) 
                return 
        self.findSignal.emit((currentNode, True)) 
        return 
    
    
class HillClimbingStatsThread(QThread):
    statsSignal = Signal('PyQt_PyObject')
    
    def __init__(self, hillClimbingAlgorithm):
        QThread.__init__(self)
        self.__hillClimbingAlgorithm = hillClimbingAlgorithm
    
    def findBest(self):
        population = Population(1, self.__hillClimbingAlgorithm.getProblem().getSize())
        currentNode = copy.deepcopy(population.getPopulation()[0])
        while currentNode.fitness() > 0:
            neighbours = currentNode.neighboursOf()
            neighbours.sort(key=lambda b: b.fitness())
            bestNeighbour = neighbours[0]
            if bestNeighbour.fitness() < currentNode.fitness():
                currentNode = copy.deepcopy(bestNeighbour)
            else:
                return currentNode
        return currentNode
    
    def run(self):
        self.running = True
        fitnessSum = 0
        fitnesses = []
        best = None
        bestFitness = inf
        for i in range(self.__hillClimbingAlgorithm.getStatsIterations()):
            if self.running == False:
                return
            currentSolution = self.findBest()
            currentFitness = currentSolution.fitness()
            if currentFitness < bestFitness:
                best = currentSolution
                bestFitness = currentFitness
                self.statsSignal.emit((best, False)) 
            fitnessSum += currentFitness
            fitnesses.append(currentFitness)
        average = fitnessSum / self.__hillClimbingAlgorithm.getStatsIterations()
        differencesSquaresSum = 0
        for i in range(self.__hillClimbingAlgorithm.getStatsIterations()):
            differencesSquaresSum += pow(fitnesses[i] - average, 2)
        standardDeviation = sqrt(differencesSquaresSum / self.__hillClimbingAlgorithm.getStatsIterations())
        self.statsSignal.emit((best, True, average, standardDeviation, fitnesses))
        return 
      
        