# -*- coding: utf-8 -*-
from Population import *
from Problem import *
from qtpy.QtCore import QThread, Signal
from math import exp, inf, sqrt
import numpy as np
class ParticleSwarm:
    def __init__(self, problem, statsFilename):
        self.__problem = problem
        self.__statsFilename = statsFilename
    
    def readStatsData(self):
        file = open(self.__statsFilename, "r")
        data = (int(file.readline().strip()), float(file.readline().strip()), float(file.readline().strip()), float(file.readline().strip()), int(file.readline().strip()), int(file.readline().strip()), int(file.readline().strip()))
        file.close()
        return data    
    
    def setParams(self, populationSize, inertiaCoefficient, cognitiveLearningCoefficient, socialLearningCoefficient, numberOfIterations, neighbourhoodSize):       
        self.__populationSize = populationSize
        self.__inertiaCoefficient = inertiaCoefficient
        self.__cognitiveLearningCoefficient = cognitiveLearningCoefficient
        self.__socialLearningCoefficient = socialLearningCoefficient
        self.__numberOfIterations = numberOfIterations
        self.__neighbourhoodSize = neighbourhoodSize
        self.__population = Population(self.__populationSize, self.__problem.getSize())

    def setInertiaCoefficient(self, newCoefficient):
        self.__inertiaCoefficient = newCoefficient
        
    def getInertiaCoefficient(self):
        return self.__inertiaCoefficient

    def getNumberOfIterations(self):
        return self.__numberOfIterations

    def getPopulation(self):
        return self.__population

    def getProblem(self):
        return self.__problem
    
    def getStatsIterations(self):
        return self.__statsIterations
        
    def iteration(self):
        bestNeighbours=[]
        
        for i in range(len(self.__population.getPopulation())):
            neighbourhood = self.__population.neighbourhood(self.__neighbourhoodSize)
            bestNeighbours.append(copy.deepcopy(neighbourhood[0]))
            for j in range(1, len(neighbourhood)):
                if bestNeighbours[i].fitness() > neighbourhood[j].fitness():
                    bestNeighbours[i] = copy.deepcopy(neighbourhood[j])
                    
        for i in range(len(self.__population.getPopulation())):
            for j in range(len(self.__population.getPopulation()[0].getVelocity())):
                newVelocityS = self.__inertiaCoefficient * self.__population.getPopulation()[i].getVelocity()[j][0]
                newVelocityS = newVelocityS + self.__socialLearningCoefficient * random() * (self.__permutationsDistance(bestNeighbours[i].getRowS(j), self.__population.getPopulation()[i].getRowS(j)))    
                newVelocityS = newVelocityS + self.__cognitiveLearningCoefficient * random()* (self.__permutationsDistance(self.__population.getPopulation()[i].getBestPosition().getRowS(j), self.__population.getPopulation()[i].getRowS(j)))
                self.__population.getPopulation()[i].getVelocity()[j][0] = newVelocityS
                
                newVelocityT = self.__inertiaCoefficient * self.__population.getPopulation()[i].getVelocity()[j][1]
                newVelocityT = newVelocityT + self.__socialLearningCoefficient * random() * (self.__permutationsDistance(bestNeighbours[i].getRowT(j), self.__population.getPopulation()[i].getRowT(j)))    
                newVelocityT = newVelocityT + self.__cognitiveLearningCoefficient * random()* (self.__permutationsDistance(self.__population.getPopulation()[i].getBestPosition().getRowT(j), self.__population.getPopulation()[i].getRowT(j)))
                self.__population.getPopulation()[i].getVelocity()[j][1] = newVelocityT
        
        for i in range(len(self.__population.getPopulation())):
            for j in range(len(self.__population.getPopulation()[0].getVelocity())):
                if random() < self.__sigmoid(self.__population.getPopulation()[i].getVelocity()[j][0]):
                    self.__population.getPopulation()[i].setRowS(j, bestNeighbours[i].getRowS(j))
                if random() < self.__sigmoid(self.__population.getPopulation()[i].getVelocity()[j][1]):
                    self.__population.getPopulation()[i].setRowT(j, bestNeighbours[i].getRowT(j))
    
    def findBest(self):
        best = 0
        for i in range(1, len(self.__population.getPopulation())):
            if self.__population.getPopulation()[i].fitness() < self.__population.getPopulation()[best].fitness():
                best = i
        return best
    
    def __sigmoid(self, value):
        return exp(-np.logaddexp(0, -value)) # math trick to avoid overflow
    
    def __permutationsDistance(self, perm1, perm2):
        distance = 0
        for i in range(len(perm1)):
            distance += perm1[i] - perm2[i]
        return distance
    
    
class ParticleSwarmThread(QThread):
    findSignal = Signal('PyQt_PyObject')
    
    def __init__(self, particleSwarm):
        QThread.__init__(self)
        self.__particleSwarm = particleSwarm
    
    def run(self):
        self.running = True
        for i in range(self.__particleSwarm.getNumberOfIterations()):
            self.__particleSwarm.setInertiaCoefficient(self.__particleSwarm.getInertiaCoefficient() / (i + 1))
            if self.running == False:
                return
            self.__particleSwarm.iteration()
            best = self.__particleSwarm.findBest()
            self.findSignal.emit((self.__particleSwarm.getPopulation().getPopulation()[best], False))
        best = self.__particleSwarm.findBest()
        self.findSignal.emit((self.__particleSwarm.getPopulation().getPopulation()[best], True))
        return

class ParticleSwarmStatsThread(QThread):
    statsSignal = Signal('PyQt_PyObject')
    
    def __init__(self, particleSwarm):
        QThread.__init__(self)
        self.__particleSwarm = particleSwarm
    
    def findBest(self):
        for i in range(self.__particleSwarm.getNumberOfIterations()):
            print(i)
            self.__particleSwarm.setInertiaCoefficient(self.__particleSwarm.getInertiaCoefficient() / (i + 1))
            self.__particleSwarm.iteration()
        return self.__particleSwarm.getPopulation().getPopulation()[self.__particleSwarm.findBest()]
    
    def run(self):
        self.running = True
        statsData = self.__particleSwarm.readStatsData()
        fitnessSum = 0
        fitnesses = []
        best = None
        bestFitness = inf
        for i in range(statsData[6]):
            if self.running == False:
                return
            self.__particleSwarm.setParams(statsData[0], statsData[1], statsData[2], statsData[3], statsData[4], statsData[5])
            currentSolution = self.findBest()
            print(str(currentSolution))
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
        standardDeviation = sqrt(differencesSquaresSum / statsData[6])
        self.statsSignal.emit((best, True, average, standardDeviation, fitnesses))
        return 