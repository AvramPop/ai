# -*- coding: utf-8 -*-
from fuzzy_system import FuzzySystem
from function_factory import FunctionFactory
from fuzzy_rule import FuzzyRule
from fuzzy_description import FuzzyDescriptions
class Controller:
    def __init__(self, problemDataFilename, inputDataFilename, outputDataFilename):
        self.__out = outputDataFilename
        self.__loadData(problemDataFilename, inputDataFilename)

    def __loadData(self, problemDataFilename, inputDataFilename):
        rules = []
        temperature = FuzzyDescriptions()
        humidity = FuzzyDescriptions()
        time = FuzzyDescriptions()
        with open(problemDataFilename, 'r') as file:
            data = file.read()
        splitInput = data.splitlines()
        i = 0
        i = self.__addInputRegion(temperature, i, splitInput)
        i = self.__addInputRegion(humidity, i, splitInput)
        i = self.__addOutputRegion(time, i, splitInput);
        self.__addRules(rules, i, splitInput)
        self.__system = FuzzySystem(rules)
        self.__system.addDescription('temperature', temperature)
        self.__system.addDescription('humidity', humidity)
        self.__system.addDescription('time', time, out=True)
        self.__parseProblemInput(inputDataFilename)

    def __addInputRegion(self, buffer, i, splitInput):
        while splitInput[i] != "##":
            line = splitInput[i].split(",")
            if len(line) == 5:
                buffer.addRegion(line[0], FunctionFactory.trapezoidalRegion(int(line[1]), int(line[2]), int(line[3]), int(line[4])))
            else:
                buffer.addRegion(line[0], FunctionFactory.triangularRegion(int(line[1]), int(line[2]), int(line[3])))
            i = i + 1
        return i + 1

    def __addRules(self, buffer, i, splitInput):
        while splitInput[i] != "##":
            line = splitInput[i].split(",")
            buffer.append(FuzzyRule({"temperature": line[0], 'humidity': line[1]}, {'time': line[2]}))
            i = i + 1

    def __addOutputRegion(self, buffer, i, splitInput):
        while splitInput[i] != "##":
            firstLine = splitInput[i].split(",")
            i = i + 1
            secondLine = splitInput[i].split(",")
            if len(firstLine) == 5:
                if len(secondLine) == 2:
                    buffer.addRegion(firstLine[0], FunctionFactory.trapezoidalRegion(int(firstLine[1]), int(firstLine[2]), int(firstLine[3]), int(firstLine[4])), FunctionFactory.inverseLine(int(secondLine[0]), int(secondLine[1])))
                else:
                    buffer.addRegion(firstLine[0], FunctionFactory.trapezoidalRegion(int(firstLine[1]), int(firstLine[2]), int(firstLine[3]), int(firstLine[4])), FunctionFactory.inverseTriangular(int(secondLine[0]), int(secondLine[1]), int(secondLine[2])))
            else:
                if len(secondLine) == 2:
                    buffer.addRegion(firstLine[0], FunctionFactory.triangularRegion(int(firstLine[1]), int(firstLine[2]), int(firstLine[3])), FunctionFactory.inverseLine(int(secondLine[0]), int(secondLine[1])))
                else:
                    buffer.addRegion(firstLine[0], FunctionFactory.triangularRegion(int(firstLine[1]), int(firstLine[2]), int(firstLine[3])), FunctionFactory.inverseTriangular(int(secondLine[0]), int(secondLine[1]), int(secondLine[2])))
            i = i + 1
        return i + 1

    def __parseProblemInput(self, inputDataFilename):
        with open(inputDataFilename, 'r') as file:
            data = file.read()
            parsedData = data.splitlines();
        self.__inputs = {parsedData[0].split(",")[0]: int(parsedData[0].split(",")[1]), parsedData[1].split(",")[0]: int(parsedData[1].split(",")[1])}


    def getInputs(self):
        return self.__inputs

    def compute(self):
        result = str(self.__system.compute(self.__inputs))
        with open(self.__out, 'w') as file:
            file.write(result)
        return result


