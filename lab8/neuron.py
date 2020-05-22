# -*- coding: utf-8 -*-
from random import random

class Neuron:
    def __init__(self, numberOfInputs, activationFunction):
        self.numberOfInputs = numberOfInputs
        self.activationFunction = activationFunction
        self.weights = [random() for i in range(self.numberOfInputs)]
        self.output = 0

    def setWeights(self, weights):
        self.weights = weights

    def fireNeuron(self, inputs):
        u = sum([x * y for x, y in zip(inputs, self.weights)])
        self.output = self.activationFunction(u)
        return self.output

    def __str__(self):
        return str(self.weights)