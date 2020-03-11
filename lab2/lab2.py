#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 14:31:03 2020

@author: dani
"""

from copy import deepcopy

class Controller:
    def __init__(self, instance):
        self.__instance = instance
        
    def orderStates(self, states):
        states.sort(key=lambda b: self.__instance.heuristic(b))
    
    def dfs(self):
        visited = []
        stack = [self.__instance.getInitialState()]
        while len(stack) > 0:
            currentState = stack[-1]
            stack.pop()
            if currentState not in visited:
                visited.append(currentState)
            if self.__instance.isSolution(currentState):
                return currentState
            
            for state in self.__instance.expand(currentState):
                if state not in visited:
                    stack.append(state)
                    visited.append(state)
        return None 
        
    def gbfs(self):
        visited = []
        queue = [self.__instance.getInitialState()]
        while not len(queue) == 0:
            self.orderStates(queue)
            currentState = queue.pop(0)
            if self.__instance.isSolution(currentState):
                return currentState
            for state in self.__instance.expand(currentState):
                if state not in visited:
                    queue.append(state)
                    visited.append(state)
        return None
    

class State:
    def __init__(self, n):
        self.__n = n
        self.__matrix = [ [ 0 for i in range(n) ] for j in range(n) ]
                
    def getSize(self):
        return self.__n;
                
    def getMatrix(self):
        return self.__matrix
    
    def __str__(self):
        result = ''
        for i in range(self.__n):
            for j in range(self.__n):
                result += str(self.getMatrix()[i][j]) + ' '
            result += '\n'
        return result
    
    def __eq__(self, other):
        if not isinstance(other, State):
            # don't attempt to compare against unrelated types
            return NotImplemented

        if self.__n != other.getSize():
            return False
        for i in range(self.__n):
            for j in range(self.__n):
                if self.getMatrix()[i][j] != other.getMatrix()[i][j]:
                    return False
        return True
    
    def isValid(self):
        for i in range(self.__n): # never have 2 queens on same position
            for j in range(self.__n):
                if self.getMatrix()[i][j] > 1:
                    return False
       # print("passed double queen")
        for i in range(self.__n):
            for j in range(self.__n):
                if self.getMatrix()[i][j] == 1:
                    for k in range(self.__n): # never have 2 queens on same line or column
                        if (self.getMatrix()[i][k] == 1 and k != j) or (self.getMatrix()[k][j] == 1 and k != i):
                            return False
                  #  print("passed line/column")
                    # never have 2 queens on same diagonal
                    ii = i - 1
                    jj = j - 1
                    while ii >= 0 and jj >= 0:
                        if self.getMatrix()[ii][jj] == 1:
                            return False
                        ii = ii - 1
                        jj = jj - 1
                    ii = i - 1
                    jj = j + 1
                    while ii >= 0 and jj < self.__n:
                        if self.getMatrix()[ii][jj] == 1:
                            return False
                        ii = ii - 1
                        jj = jj + 1
                    ii = i + 1
                    jj = j - 1
                    while ii < self.__n and jj >= 0:
                        if self.getMatrix()[ii][jj] == 1:
                            return False
                        ii = ii + 1
                        jj = jj - 1                                
                    ii = i + 1
                    jj = j + 1
                    while ii < self.__n and jj < self.__n:
                        if self.getMatrix()[ii][jj] == 1:
                            return False
                        ii = ii + 1
                        jj = jj + 1

                 #   print("passed diagonal")
        return True

class Problem:
    def __init__(self, initialState):
        self.__initialState = initialState
        
    def getInitialState(self):
        return self.__initialState
    
    def expand(self, state):
        children = []
        for i in range(state.getSize()):
            for j in range(state.getSize()):
                temp = deepcopy(state)
                temp.getMatrix()[i][j] += 1
                if temp.isValid():
                    children.append(temp)
        return children
                
    
    def heuristic(self, state):
        queens = 0
        for i in range(state.getSize()):
            for j in range(state.getSize()):
                if state.getMatrix()[i][j] == 1:
                    queens += 1
        return queens
    
    def getComparator(self, a, b):
        if self.heuristic(a) > self.heuristic(b):
            return 1
        elif self.heuristic(a) == self.heuristic(b):
            return 0
        else:
            return -1
    
    def isSolution(self, state): # suffices to have n queens because we have generated only valid states
        queens = 0
        for i in range(state.getSize()):
            for j in range(state.getSize()):
                if state.getMatrix()[i][j] == 1:
                    queens += 1
        return queens == state.getSize()
    

class Console:
    def __init__(self, controller):
        self.__controller = controller
    
    def run(self):
        while True:
            print("- dfs")
            print("- gbfs")
            print("- exit")
            userInput = input(">")
            if userInput == "dfs":
                print(self.__controller.dfs())
            elif userInput == "gbfs":
                print(self.__controller.gbfs())
            elif userInput == "exit":
                print("bye")
                break
            else:
                print("wrong input!")

def main():
    n = (int(input("n = ")))
    initialState = State(n)
    problem = Problem(initialState)
    controller = Controller(problem)
    console = Console(controller)
    console.run()

main()