#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 13:58:38 2020

@author: dani
"""

import matplotlib.pyplot as plt
import numpy as np

def normal(loc, scale, size):
    return np.random.normal(loc, scale, size)

def poisson(lam, size):
    return np.random.poisson(lam, size)

def student(df, size):
    return np.random.standard_t(df, size)

def binomial(n, p, size):
    return np.random.binomial(n, p, size)

def main():
    while True:
        userInput = input(">")
        if userInput == "normal":
            plt.plot(normal(float(input("loc: ")), float(input("scale: ")), int(input("size: "))), "ro")
            plt.ylabel("numbers")
            plt.xticks([])
            plt.show()
        elif userInput == "binomial":
            plt.plot(binomial(int(input("n: ")), float(input("p: ")), int(input("size: "))), "ro")
            plt.ylabel("numbers")
            plt.xticks([])
            plt.show()
        elif userInput == "poisson":
            plt.plot(poisson(float(input("lam: ")), int(input("size: "))), "ro")
            plt.ylabel("numbers")
            plt.xticks([])
            plt.show()
        elif userInput == "student":
            plt.plot(student(float(input("df: ")), int(input("size: "))), "ro")
            plt.ylabel("numbers")
            plt.xticks([])
            plt.show()
        elif userInput == "exit":
            break
        else:
            print("wrong input!")
    
main()

