# -*- coding: utf-8 -*-

from neuron import Neuron

class Layer:
    def __init__(self, numberOfInputs, activationFunction, numberOfNeurons):
        self.numberOfNeurons = numberOfNeurons
        self.neurons = [Neuron(numberOfInputs, activationFunction) for i in range(self.numberOfNeurons)]


    def forward(self, inputs):
        for neuron in self.neurons:
            neuron.fireNeuron(inputs)
        return([neuron.output for neuron in self.neurons])

    def __str__(self):
        s = ''
        for i in range(self.numberOfNeurons):
            s += ' n '+ str(i) + ' ' + str(self.neurons[i]) + '\n'
        return s

class FirstLayer(Layer):
    def __init__(self, numberOfNeurons, activationFunction, bias = False):
        if bias:
            numberOfNeurons = numberOfNeurons + 1
        Layer.__init__(self, 1, activationFunction, numberOfNeurons)
        for neuron in self.neurons:
            neuron.setWeights([1])

    def forward(self, inputs):
        for i in range(len(self.neurons)):
            self.neurons[i].fireNeuron([inputs[i]])
        return([x.output for x in self.neurons])
