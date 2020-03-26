# -*- coding: utf-8 -*-
from Individual import *
import itertools


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
    
    def neighbourhood(self, neighbourhoodSize):
        if neighbourhoodSize > len(self.__population):
            neighbourhoodSize = len(self.__population)
        neighbours=[]
        for j in range(neighbourhoodSize):
            k = randint(0, len(self.__population) - 1)
            neighbours.append(copy.deepcopy(self.__population[k]))
        return neighbours