# -*- coding: utf-8 -*-

from Cell import Cell
from random import random, randint
#import copy 

class Ant:
    def __init__(self, n):
        self.__n = n
        self.__solution = [[Cell() for j in range(n)] for i in range(n)]
        self.__graph = [i + 1 for i in range(n)]   
            
    def getSize(self):
        return self.__n
    
    def getCell(self, i, j):
        return self.__solution[i][j]
     
    def setCell(self, i, j, value):
        self.__solution[i][j] = value
        
    def __str__(self):
        res = ""
        for i in range(self.__n):
            for j in range(self.__n):
                res += str(self.__solution[i][j]) + " "
            res += "\n"
        return res
    
    def __getColumnS(self, columnNumber):
        column = []
        for row in self.__solution:
            column.append(row[columnNumber].getValue()[0])
        return column

    def __getColumnT(self, columnNumber):
        column = []
        for row in self.__solution:
            column.append(row[columnNumber].getValue()[1])
        return column
    
    def __duplicates(self):
        flattenedMatrix = []
        for i in range(self.getSize()):
            for j in range(self.getSize()):
                flattenedMatrix.append(self.__solution[i][j])
        return pow(self.getSize(), 2) - len(set(flattenedMatrix))
    
    def __wrongColumns(self):
        count = 0
        for i in range(self.__n):
            columnS = self.__getColumnS(i)
            columnT = self.__getColumnT(i)
            count += (len(columnS) - len(set(columnS)))
            count += (len(columnT) - len(set(columnT)))
        return count
    
    def getRow(self, i):
        return self.__solution[i]
    
    def evaluate(self):
        return self.__duplicates() + self.__wrongColumns()
        
    def update(self, q0, trace, alpha, beta, row, column, component):
        
        if column == 0:
            self.__graph = [i + 1 for i in range(self.__n)]
            pick = randint(0, len(self.__graph) - 1)
            self.__setValue(row, column, component, self.__graph[pick])
            self.__graph.pop(pick)
        else:    
            base = (0 if component == 0 else self.__n)
            coeffs = []
            for i in range(len(self.__graph)):
#                print()
#                print(len(trace), len(trace[0]), len(trace[0][0]))
#                print(self.getCell(row, column - 1).getValue()[component] - 1)
#                print(self.__graph[i] - 1)
#                print(base + row)
#                print(trace[self.getCell(row, column - 1).getValue()[component] - 1][self.__graph[i] - 1][base + row])
                coeffs.append((self.__graph[i] ** beta) * (trace[self.getCell(row, column - 1).getValue()[component] - 1][self.__graph[i] - 1][base + row] ** alpha))
            if random() < q0:
                bestCoeff = -1
                best = -1
                for i in range(len(coeffs)):
                    if coeffs[i] > bestCoeff:
                        bestCoeff = coeffs[i]
                        best = i
                self.__setValue(row, column, component, self.__graph[best])
                self.__graph.pop(best)
            else:
                s = sum(coeffs)
                if (s==0):
                    pick = randint(0, len(self.__graph) - 1)
                    self.__setValue(row, column, component, self.__graph[pick])
                    self.__graph.pop(pick)
                else:
                    coeffs = [ coeffs[i] / s for i in range(len(coeffs)) ]
                    coeffs = [ sum(coeffs[0:i+1]) for i in range(len(coeffs)) ]
                    r = random()
                    i = 0
                    while (r > coeffs[i]):
                        i = i + 1
                    self.__setValue(row, column, component, self.__graph[i])
                    self.__graph.pop(i)                   
        
    def __setValue(self, row, column, component, value):
        if component == 0:
            self.getCell(row, column).setX(value)
        else:
            self.getCell(row, column).setY(value)
