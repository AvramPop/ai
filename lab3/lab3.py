#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 13:03:07 2020

@author: dani
"""
import itertools
from random import randint, shuffle, random
import copy 
from numpy import sqrt
import matplotlib.pyplot as plt

class Cell:
    def __init__(self, x = -1, y = -1):
        self.__x = x
        self.__y = y
    
    def getValue(self):
        return (self.__x, self.__y)
    
    def setX(self, x):
        self.__x = x

    def setY(self, y):
        self.__y = y
    
    def __str__(self):
        return "(" + str(self.__x) + ", " + str(self.__y) + ")"
    
    def __eq__(self, other):
        if self.__x == -1 or self.__y == -1:
            return False
        return self.__x == other.__x and self.__y == other.__y
    
    def __hash__(self):
        return hash((self.__x, self.__y))

class Individual:
    def __init__(self, n):
        self.__n = n
        self.__matrix = [[Cell() for j in range(n)] for i in range(n)]
    
    def getSize(self):
        return self.__n
    
    def getCell(self, i, j):
        return self.__matrix[i][j]
     
    def setCell(self, i, j, value):
        self.__matrix[i][j] = value
        
    def setRow(self, i, row):
        self.__matrix[i] = row
        
    def getRow(self, i):
        return self.__matrix[i]
        
    def __str__(self):
        res = ""
        for i in range(self.__n):
            for j in range(self.__n):
                res += str(self.__matrix[i][j]) + " "
            res += "\n"
        return res
    
    def __duplicates(self):
#        count = 0
#        temp = copy.deepcopy(self.__matrix)
#        for i in range(self.__n):
#            for j in range(self.__n):
#                for ii in range(self.__n):
#                    for jj in range(self.__n):
#                        if temp[i][j] == temp[ii][jj] and (i != ii or j != jj):
#                            temp[ii][jj] = Cell()
#                            count += 1
#                temp[i][j] = Cell()
#        return count
        flattenedMatrix = []
        for i in range(self.getSize()):
            for j in range(self.getSize()):
                flattenedMatrix.append(self.__matrix[i][j])
        return pow(self.getSize(), 2) - len(set(flattenedMatrix))
    
    def __wrongColumns(self):
        count = 0
#        temp = copy.deepcopy(self.__matrix)
#        for j in range(self.__n):
#            for i in range(self.__n - 1):
#                foundX = False
#                foundY = False
#                for k in range(i + 1, self.__n): # TODO fix more than 3 aparitions issue
#                    if temp[i][j].getValue()[0] == temp[k][j].getValue()[0]:
#                        count += 1
#                        foundX = True
#                        temp[k][j].setX(-1)
#                    if temp[i][j].getValue()[1] == temp[k][j].getValue()[1]:
#                        count += 1
#                        foundY = True
#                        temp[k][j].setY(-1)
#                if foundX is True:
#                    temp[i][j].setX(-1)
#                if foundY is True:
#                    temp[i][j].setY(-1)
        for i in range(self.__n):
            columnS = self.__getColumnS(i)
            columnT = self.__getColumnT(i)
            count += (len(columnS) - len(set(columnS)))
            count += (len(columnT) - len(set(columnT)))
        return count
    
    def __getColumnS(self, columnNumber):
        column = []
        for row in self.__matrix:
            column.append(row[columnNumber].getValue()[0])
        return column

    def __getColumnT(self, columnNumber):
        column = []
        for row in self.__matrix:
            column.append(row[columnNumber].getValue()[1])
        return column
    
    def fitness(self):
        return self.__duplicates() + self.__wrongColumns()
    
    def swapS(self, row, firstColumn, secondColumn):
        temp = self.__matrix[row][firstColumn].getValue()[0]
        self.__matrix[row][firstColumn].setX(self.__matrix[row][secondColumn].getValue()[0])
        self.__matrix[row][secondColumn].setX(temp)
        
    def swapT(self, row, firstColumn, secondColumn):
        temp = self.__matrix[row][firstColumn].getValue()[1]
        self.__matrix[row][firstColumn].setY(self.__matrix[row][secondColumn].getValue()[1])
        self.__matrix[row][secondColumn].setY(temp)
        
    def mutate(self, mutationProbability):
        for i in range(self.getSize()):
            if mutationProbability > random():
                shuffle(self.getRow(i))
                
    def neighboursOf(self):
        neighbours = []
        for i in range(self.getSize()):
            nextNeighbour = copy.deepcopy(self)
            for j in range(self.getSize()):
                sFirstDraw = randint(0, self.getSize() - 1)
                sSecondDraw = randint(0, self.getSize() - 1)
                tFirstDraw = randint(0, self.getSize() - 1)
                tSecondDraw = randint(0, self.getSize() - 1)
                nextNeighbour.swapS(j, sFirstDraw, sSecondDraw)
                nextNeighbour.swapT(j, tFirstDraw, tSecondDraw)
            neighbours.append(nextNeighbour)
        return neighbours
    
    def crossover(self, parent2, crossoverProbability):
        n = self.getSize()
        child1 = Individual(n)
        child2 = Individual(n)
        for i in range(n): # uniform crossover
            if crossoverProbability > random():
                child1.setRow(i, copy.deepcopy(self.getRow(i)))
                child2.setRow(i, copy.deepcopy(parent2.getRow(i)))
            else:
                child1.setRow(i, copy.deepcopy(parent2.getRow(i)))
                child2.setRow(i, copy.deepcopy(self.getRow(i)))
    #    firstThird = n // 3  # n-cutting point crossover, n = 2
    #    secondThird = 2 * n // 3
    #    for i in range(firstThird):
    #        child1.setRow(i, copy.deepcopy(self.getRow(i)))
    #        child2.setRow(i, copy.deepcopy(parent2.getRow(i)))
    #    for i in range(firstThird, secondThird):
    #        child1.setRow(i, copy.deepcopy(parent2.getRow(i)))
    #        child2.setRow(i, copy.deepcopy(self.getRow(i)))  
    #    for i in range(secondThird, n):
    #        child1.setRow(i, copy.deepcopy(self.getRow(i)))
    #        child2.setRow(i, copy.deepcopy(parent2.getRow(i)))
        return (child1, child2)
    
class Population:
    def __init__(self, populationSize, individualSize):
        self.__population = self.__generatePopulation(populationSize, individualSize)
        
    def getPopulation(self):
        return self.__population
    
    def generateOneIndividual(self, n):
        allPermutations = self.__permutations(n)
        pool = []
        for j in range(2 * n):
            k = randint(0, len(allPermutations) - 1)
            pool.append(allPermutations.pop(k))
        newIndividual = Individual(n)
        for j in range(n):
            k = randint(0, len(pool) - 1)
            firstList = pool.pop(k)
            k = randint(0, len(pool) - 1)
            secondList = pool.pop(k)
            newRow = self.__mergeListsElementByElement(firstList, secondList)
            newIndividual.setRow(j, newRow)
        return newIndividual

    def __generatePopulation(self, populationSize, n):
        population = []
        for i in range(populationSize):
            population.append(self.generateOneIndividual(n))
        return population
    
    def __permutations(self, n):
        pool = [i + 1 for i in range(n)]
        return list(itertools.permutations(pool))

    def __mergeListsElementByElement(self, list1, list2):
        res = []    
        for i in range(len(list1)):
            res.append(Cell(list1[i], list2[i]))
        return res

class Problem:
    def __init__(self, filename):
        self.__n = self.__readIndividualSizeFromFile(filename)
        
    def __readIndividualSizeFromFile(self, filename):
        file = open(filename, "r")
        n = int(file.readline().strip())
        file.close()
        return n
    
    def getSize(self):
        return self.__n

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

    def __loadStatsData(self):
        file = open(self.__statsFilename, "r")
        data = (int(file.readline().strip()), float(file.readline().strip()), float(file.readline().strip()), int(file.readline().strip()), int(file.readline().strip()))
        file.close()
        return data
    
    def run(self):
        for i in range(self.__numberOfGenerations):
            self.__iteration(self.__population.getPopulation(), self.__mutationProbability, self.__crossoverProbability)
        return self.__population.getPopulation()[0]
    
    def __iteration(self, population, mutationProbability, crossoverProbability):
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
            
    def statistics(self):
        statsData = self.__loadStatsData()
        fitnessSum = 0
        fitnesses = []
        for i in range(statsData[4]):
            self.setParams(statsData[0], statsData[1], statsData[2], statsData[3])
            print("stats iteration #", i)
            currentSolution = self.run()
            currentFitness = currentSolution.fitness()
            print(currentFitness)
            fitnessSum += currentFitness
            fitnesses.append(currentFitness)
        average = fitnessSum / statsData[4]
        differencesSquaresSum = 0
        for i in range(statsData[4]):
            differencesSquaresSum += pow(fitnesses[i] - average, 2)
        standardDeviation = sqrt(differencesSquaresSum / statsData[4])
        return (average, standardDeviation, fitnesses)
        
    
class HillClimbAlgorithm:
    def __init__(self, problem, statsFilename):
        self.__problem = problem
        self.__statsIterations = self.__readStatsData(statsFilename)
    
    def __readStatsData(self, filename):
        file = open(filename, "r")
        n = int(file.readline().strip())
        file.close()
        return n
    
    def run(self):
        population = Population(1, self.__problem.getSize())
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

    def statistics(self):
        fitnessSum = 0
        fitnesses = []
        for i in range(self.__statsIterations):
            print("stats iteration #", i)
            currentSolution = self.run()
            currentFitness = currentSolution.fitness()
            print(currentFitness)
            fitnessSum += currentFitness
            fitnesses.append(currentFitness)
        average = fitnessSum / self.__statsIterations
        differencesSquaresSum = 0
        for i in range(self.__statsIterations):
            differencesSquaresSum += pow(fitnesses[i] - average, 2)
        standardDeviation = sqrt(differencesSquaresSum / self.__statsIterations)
        return (average, standardDeviation, fitnesses)
        
    
def main():
    problem = Problem("problemData.in")
    print("1 - EA")
    print("2 - Hill Climbing")
    option = int(input(">"))
    if option == 1:
        evolutionaryAlgorithm = EvolutionaryAlgorithm(problem, "ev.in") 
#        evolutionaryAlgorithm.setParams()
#        solution = evolutionaryAlgorithm.run()
#        print(str(solution))
#        print(str(solution.fitness()))
        stats = evolutionaryAlgorithm.statistics()
        print(stats[0])
        print(stats[1])
        plt.plot(stats[2])
        plt.show()
    elif option == 2:
        hillClimbAlgorithm = HillClimbAlgorithm(problem, "hill.in")
        hillClimbSolution = hillClimbAlgorithm.run()
        print(str(hillClimbSolution))
        print(hillClimbSolution.fitness())
        stats = hillClimbAlgorithm.statistics()
        print(stats[0])
        print(stats[1])
        plt.plot(stats[2])
        plt.show()
    
main()
