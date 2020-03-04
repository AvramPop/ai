#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 14:00:43 2020

@author: dani
"""
import numpy as np
import copy as cpy
import random as ra
import string

def checkLines(game):
    for row in game:
        if len(row) > len(set(row)):
            return False
    return True

def checkColumns(game):
    temp = game.transpose()
    for row in temp:
        if len(row) > len(set(row)):
            return False
    return True

def checkSquares(game):
    for i in range(0, len(game[0]), int(np.sqrt(len(game[0])))):
        for j in range(0, len(game[0]), int(np.sqrt(len(game[0])))):
            xStart = i
            yStart = j
            temp = []
            for ii in range(xStart, xStart + int(np.sqrt(len(game[0])))):
                for jj in range(yStart, yStart + int(np.sqrt(len(game[0])))):
                    temp.append(game[ii][jj])
            if len(temp) > len(set(temp)):
                return False
    return True
            

def checkSudoku(game):
    return checkLines(game) and checkColumns(game) and checkSquares(game)

def readSudokuGrid():
    return np.loadtxt("sudoku.in", dtype = "i", delimiter = ",")
            
def seedSudoku(game):
    for row in game:
        for i in range(0, len(row)):
            if row[i] == 0:
                row[i] = ra.randint(1, len(row))
    return game


def solveSudoku(attempts):
    temp = readSudokuGrid()
    solved = False
    while attempts > 0:
        game = cpy.deepcopy(temp)
        game = seedSudoku(game)
        if checkSudoku(game):
            solved = game
            attempts = -1
        else:
            attempts = attempts - 1

    return solved

def seedCypher():
    alphabet = string.ascii_lowercase
    pool = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    cypher = {}
    for letter in alphabet:
        cypher.update({letter: pool[ra.randint(0, 15)]})
    return cypher

def readCryptarithmetic():
    file = open("crypt.in", "r")
    firstOperand = file.readline().strip()
    operator = file.readline().strip()
    secondOperand = file.readline().strip()
    result = file.readline().strip()
    file.close()
    return (firstOperand, operator, secondOperand, result)

def decimalValue(code, cypher):
    result = 0
    power = 1
    for letter in reversed(code):
        result = result + cypher[letter] * power
        power = power * 16  
    return result
        
def firstLetterZero(game, cypher):
    return cypher[game[0][0]] == 0 or cypher[game[2][0]] == 0 or cypher[game[3][0]] == 0 

def checkCryptarithmetic(game, cypher):
    if firstLetterZero(game, cypher):
        return False
    firstOperand = decimalValue(game[0], cypher)
    operator = game[1]
    secondOperand = decimalValue(game[2], cypher)
    result = decimalValue(game[3], cypher)
    if operator == "+":
        return firstOperand + secondOperand == result
    elif operator == "-":
        return firstOperand - secondOperand == result
    elif operator == "*":
        return firstOperand * secondOperand == result
    elif operator == "/":
        return firstOperand // secondOperand == result
    else:
        return False
        

def solveCryptarithmetic(attempts):
    temp = readCryptarithmetic()
    solved = False
    while attempts > 0:
        game = cpy.deepcopy(temp)
        cypher = seedCypher()
        if checkCryptarithmetic(game, cypher):
            solved = cypher
            attempts = -1
        else:
            attempts = attempts - 1

    return solved

def readGeometric():
    shapes = []
    shapes.append(np.matrix([1, 1, 1, 1]))
    shapes.append(np.matrix([[1, 0, 0], 
                             [1, 1, 1]]))
    shapes.append(np.matrix([[1, 0, 1],
                             [1, 1, 1]]))
    shapes.append(np.matrix([[1, 1, 1],
                             [0, 0, 1]]))
    shapes.append(np.matrix([[0, 1, 0],
                             [1, 1, 1]]))
    board = np.matrix([[0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0]])
    return (shapes, board)

def seedCorners(no):
    corners = []
    for i in range(0, no):
        xSeed = ra.randint(0, 4)
        ySeed = ra.randint(0, 5)
        corners.append((xSeed, ySeed))
    return corners

def checkGeometric(game, corners):
    shapes = game[0]
    board = game[1]
    for k in range(0, len(shapes)):
        if corners[k][0] + len(shapes[k]) - 1 >= 5 or corners[k][1] + shapes[k][0].size - 1 >= 6:  # out of borders
            return False
        else: # sum matrices
            shapeI = 0
            for i in range(corners[k][0], corners[k][0] + len(shapes[k])):
                shapeJ = 0
                for j in range(corners[k][1], corners[k][1] + shapes[k][0].size):
                    newData = board.item((i, j)) + shapes[k].item(shapeI, shapeJ)
                    board.itemset((i, j), newData)
                    shapeJ = shapeJ + 1
                shapeI = shapeI + 1
    for el in board.flatten().A[0]:
        if el > 1:
            return False
    return True

def solveGeometric(attempts):
    temp = readGeometric()
    solved = False
    while attempts > 0:
        game = cpy.deepcopy(temp)
        corners = seedCorners(len(game[0]))
        if checkGeometric(game, corners):
            solved = (corners, game[-1])
            attempts = -1
        else:
            attempts = attempts - 1

    return solved

def mainGames():
    while True:
        userInput = input(">")
        if userInput == "1":
            attempts = int(input("attempts: "))
            print(solveSudoku(attempts))
        elif userInput == "2":
            attempts = int(input("attempts: "))
            print(solveCryptarithmetic(attempts))
        elif userInput == "3":
            attempts = int(input("attempts: "))
            print(solveGeometric(attempts))
        elif userInput == "exit":
            break
        else:
            print("wrong input!")
            
mainGames()