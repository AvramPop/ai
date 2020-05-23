from random import shuffle
from copy import deepcopy

from chromosome import Chromosome
from population import Population
from classifier import Classifier

HEADER = []


class Controller:
    def __init__(self, trainingFilename, inputFilename, outputFilename):
        self.n = 0
        self.input = []
        self.output = []
        self.inputTest = []
        self.outputTest = []
        self.inputTrain = []
        self.outputTrain = []
        self.trainingFilename = trainingFilename
        self.inputFilename = inputFilename
        self.outputFilename = outputFilename


    def run(self, nrInd, ITER, sizeofTrain, sizeofTest, mutationProbability, crossoverProbability, epsilon):
        self.nrInd = nrInd
        self.sizeofTrain = sizeofTrain
        self.sizeofTest = sizeofTest
        self.iterations = ITER
        self.population = Population(nrInd)
        self.probability_mutate = mutationProbability
        self.probability_crossover = crossoverProbability
        self.epsilon = epsilon
        self.loadData()

        accuracy = -1.0
        while accuracy < self.epsilon:
            self.population.evaluate(self.inputTrain, self.outputTrain)
    
            for i in range(self.iterations):
                print("Iteration: " + str(i))
                self.iteration(i)
                self.population.evaluate(self.inputTrain, self.outputTrain)
                self.population.selection(self.nrInd)
            best = self.population.best(1)[0]
            count = 0
            for i in range(len(self.inputTest)):
                if Classifier.classify(self.population.best(1)[0].predict(self.inputTest[i])) == Classifier.classify(self.outputTest[i]):
                    count += 1
            accuracy = float(count / len(self.inputTest) * 100)
            print("current accuracy: ", accuracy, "%")
            
        print("Best: " + str(best.root))
        print("correct guesses ", count)
        print("that is ", accuracy, "% accuracy")
        with open(self.outputFilename, "w") as f:
            f.write("correct guesses " + str(count))
            f.write("\nthat is " + str(accuracy) + "%")
            
            

    def loadData(self):
        global HEADER
        with open(self.trainingFilename, "r") as f:
            HEADER = f.readline().split(',')[:-1]
            inputLines = f.readlines()
            shuffle(inputLines)
            for line in inputLines[:self.sizeofTrain]:
                values = list(map(float, line.split(',')))
                self.inputTrain.append(values[:-1])
                self.outputTrain.append(values[-1])
                self.n += 1
                
        # c = list(zip(self.inputTrain, self.outputTrain))
        # shuffle(c)
        # self.inputTrain, self.outputTrain = zip(*c)
        
        with open(self.inputFilename, "r") as f:
            inputLines = f.readlines()
            shuffle(inputLines)
            for line in inputLines[:self.sizeofTest]:
                values = list(map(float, line.split(',')))
                self.inputTest.append(values[:-1])
                self.outputTest.append(values[-1])
                
        c = list(zip(self.inputTest, self.outputTest))
        shuffle(c)
        self.inputTest, self.outputTest = zip(*c)


    def iteration(self, i):
        parents = range(self.nrInd)
        nrChildren = len(parents) // 2
        offspring = Population(nrChildren)
        for i in range(nrChildren):
            offspring.individuals[i] = Chromosome.crossover(self.population.individuals[i << 1],
                                                            self.population.individuals[(i << 1) | 1],
                                                            self.probability_crossover)
            offspring.individuals[i].mutate(self.probability_mutate)
        offspring.evaluate(self.inputTrain, self.outputTrain)
        self.population.reunion(offspring)
        self.population.selection(self.nrInd)
