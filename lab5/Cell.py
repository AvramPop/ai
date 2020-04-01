# -*- coding: utf-8 -*-

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