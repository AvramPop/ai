from layer import Layer, FirstLayer
from copy import deepcopy

class Network:
    def __init__(self, structure, activationFunction, derivate, bias = False):
        self.activationFunction = activationFunction
        self.derivate = derivate
        self.bias = bias
        self.structure = structure[:]
        self.numberOfLayers = len(self.structure)
        self.layers = [FirstLayer(self.structure[0], activationFunction, bias)]
        for i in range(1, len(self.structure)):
            self.layers = self.layers + [Layer(self.structure[i - 1],
                            activationFunction, self.structure[i])]

    def feedForward(self, inputs):
        self.signal = inputs[:]
        if self.bias:
            self.signal.append(1)
        for l in self.layers:
            self.signal = l.forward(self.signal)
        return self.signal

    def backPropagate(self, loss, learnRate):
        err = loss[:]
        delta = []
        currentLayer = self.numberOfLayers - 1
        newConfig = Network(self.structure, self.activationFunction, self.derivate, self.bias)
        # last layer
        for i in range(self.structure[-1]):
            delta.append(err[i] * self.derivate(self.layers[-1].neurons[i].output))
            for r in range(self.structure[currentLayer - 1]):
                newConfig.layers[-1].neurons[i].weights[r] = self.layers[-1].neurons[i].weights[r] + learnRate * delta[i] * self.layers[currentLayer-1].neurons[r].output

        for currentLayer in range(self.numberOfLayers-2, 0, -1):
            currentDelta = []
            for i in range(self.structure[currentLayer]):
                currentDelta.append(self.derivate(self.layers[currentLayer].neurons[i].output) * sum([self.layers[currentLayer + 1].neurons[j].weights[i] * delta[j] for j in range(self.structure[currentLayer + 1])]))

            delta = currentDelta[:]
            for i in range(self.structure[currentLayer]):
                for r in range(self.structure[currentLayer - 1]):
                    newConfig.layers[currentLayer].neurons[i].weights[r] = self.layers[currentLayer].neurons[i].weights[r] + learnRate * delta[i] * self.layers[currentLayer - 1].neurons[r].output
        self.layers=deepcopy(newConfig.layers)


    def computeLoss(self, inputData, outputData):
        loss = []
        out = self.feedForward(inputData)
        for i in range(len(outputData)):
            loss.append(outputData[i]-out[i])
        return loss[:]

    def __str__(self):
        s = ''
        for i in range(self.numberOfLayers):
            s += ' l '+ str(i) + ' :' + str(self.layers[i])
        return s