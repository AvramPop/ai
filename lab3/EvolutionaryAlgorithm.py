# -*- coding: utf-8 -*-
from Population import *
from Problem import *
from qtpy.QtCore import QThread, Signal
from math import inf, sqrt

class EvolutionaryAlgorithm:
    def __init__(self, problem, statsFilename):
        self.__problem = problem
        self.__statsFilename = statsFilename
        
    def setParams(self, populationSize, mutationProbability, crossoverProbability, numberOfGenerations):
        self.__populationSize = populationSize
        self.__mutationProbability = mutationProbability
        self.__crossoverProbability = crossoverProbability
        self.__numberOfGenerations = numberOfGenerations
        self.__population = Population(self.__populationSize, self.__problem.getSize())

    def loadStatsData(self):
        file = open(self.__statsFilename, "r")
        data = (int(file.readline().strip()), float(file.readline().strip()), float(file.readline().strip()), int(file.readline().strip()), int(file.readline().strip()))
        file.close()
        return data
    
    def getPopulationSize(self):
        return self.__populationSize
    
    def getNumberOfGenerations(self):
        return self.__numberOfGenerations
    
    def getMutationProbability(self):
        return self.__mutationProbability
    
    def getCrossoverProbability(self):
        return self.__crossoverProbability
    
    def getPopulation(self):
        return self.__population.getPopulation()
    
    def iteration(self, population, mutationProbability, crossoverProbability):
        i1 = randint(0, len(population) - 1)
        i2 = randint(0, len(population) - 1)
        if i1 != i2:
            children = population[i1].crossover(population[i2], crossoverProbability)
            child1 = children[0]
            child2 = children[1]
            child1.mutate(mutationProbability)
            child2.mutate(mutationProbability)
            population.append(child1)
            population.append(child2)
            population.sort(key=lambda b: b.fitness()) # remove most unfit 2 individuals
            population.pop()
            population.pop()

        
class EvolutionaryAlgorithmThread(QThread):
    findSignal = Signal('PyQt_PyObject')
    
    def __init__(self, evolutionaryAlgorithm):
        QThread.__init__(self)
        self.__evolutionaryAlgorithm = evolutionaryAlgorithm
    
    def run(self):
        self.running = True
        for i in range(self.__evolutionaryAlgorithm.getNumberOfGenerations()):
            if self.running == False:
                return
            self.__evolutionaryAlgorithm.iteration(self.__evolutionaryAlgorithm.getPopulation(), self.__evolutionaryAlgorithm.getMutationProbability(), self.__evolutionaryAlgorithm.getCrossoverProbability())
            self.findSignal.emit((self.__evolutionaryAlgorithm.getPopulation()[0], False))
        self.findSignal.emit((self.__evolutionaryAlgorithm.getPopulation()[0], True))
        return 

class EvolutionaryAlgorithmStatsThread(QThread):
    statsSignal = Signal('PyQt_PyObject')
    
    def __init__(self, evolutionaryAlgorithm):
        QThread.__init__(self)
        self.__evolutionaryAlgorithm = evolutionaryAlgorithm
        
    def findBest(self):
        for i in range(self.__evolutionaryAlgorithm.getNumberOfGenerations()):
            self.__evolutionaryAlgorithm.iteration(self.__evolutionaryAlgorithm.getPopulation(), self.__evolutionaryAlgorithm.getMutationProbability(), self.__evolutionaryAlgorithm.getCrossoverProbability())
        return self.__evolutionaryAlgorithm.getPopulation()[0]
            
    def run(self):
        self.running = True
        statsData = self.__evolutionaryAlgorithm.loadStatsData()
        fitnessSum = 0
        fitnesses = []
        best = None
        bestFitness = inf
        for i in range(statsData[4]):
            if self.running == False:
                return
            self.__evolutionaryAlgorithm.setParams(statsData[0], statsData[1], statsData[2], statsData[3])
            currentSolution = self.findBest()
            currentFitness = currentSolution.fitness()
            if currentFitness < bestFitness:
                best = currentSolution
                bestFitness = currentFitness
                self.statsSignal.emit((best, False)) 
            fitnessSum += currentFitness
            fitnesses.append(currentFitness)
        average = fitnessSum / statsData[4]
        differencesSquaresSum = 0
        for i in range(statsData[4]):
            differencesSquaresSum += pow(fitnesses[i] - average, 2)
        standardDeviation = sqrt(differencesSquaresSum / statsData[4])
        self.statsSignal.emit((best, True, average, standardDeviation, fitnesses))
        return 