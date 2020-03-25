# -*- coding: utf-8 -*-

from Cell import *
from random import shuffle, random, randint
import copy 

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
        flattenedMatrix = []
        for i in range(self.getSize()):
            for j in range(self.getSize()):
                flattenedMatrix.append(self.__matrix[i][j])
        return pow(self.getSize(), 2) - len(set(flattenedMatrix))
    
    def __wrongColumns(self):
        count = 0
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
    