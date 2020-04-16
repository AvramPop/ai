# -*- coding: utf-8 -*-

import numpy as np

class Controller:
  def __init__(self, filename):
    data = self.__loadData(filename)
    normalisedData = self.__normaliseData(data)
    self.__X, self.__y, self.__theta = self.__splitData(normalisedData)

  def __loadData(self, filename):
    filedata = np.loadtxt(filename, dtype=np.float32)
    return filedata

  def __splitData(self, data):
    X = data[:, 0:-1]
    ones = np.ones([X.shape[0], 1])
    X = np.concatenate((ones, X), axis=1)
    y = data[:, [-1]]
    theta = np.zeros([1,len(data[0])])
    return X, y, theta

  def __normaliseData(self, data):
    return (data - data.mean()) / data.std()

  def __computeCost(self, X, y, theta):
    summand = np.power(((X @ theta.T) - y), 2)
    return np.sum(summand) / (2 * len(X))

  def __gradientDescent(self, X, y, theta, iters, alpha):
    cost = np.zeros(iters)
    for i in range(iters):
      theta = theta - (alpha/len(X)) * np.sum(X * (X @ theta.T - y), axis=0)
      cost[i] = self.__computeCost(X, y, theta)
    return theta, cost

  def results(self, alpha, iters):
    g, cost = self.__gradientDescent(self.__X, self.__y, self.__theta, iters, alpha)
    finalCost = self.__computeCost(self.__X, self.__y, g)
    return g, cost, finalCost
