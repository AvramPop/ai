# -*- coding: utf-8 -*-
from ast import literal_eval

class FuzzySystem:
    def __init__(self, rules):
        self.inDescriptions = {}
        self.outDescriptions = None
        self.rules = rules

    def addDescription(self, name, outDescription, out=False):
        if out:
            if self.outDescriptions is None:
                self.outDescriptions = outDescription
        else:
            self.inDescriptions[name] = outDescription

    def compute(self, inputs):
        fuzzyInValues = self.__computeDescriptions(inputs)
        rules = self.__computeFuzzyRules(fuzzyInValues)

        fuzzyOutValues = [(list(description[0].values())[0], description[1]) for description in rules]
        weightedTotal = 0
        weightSum = 0
        for var in fuzzyOutValues:
            weightSum += var[1]
            print(var[1], " * ", self.outDescriptions.defuzzify(*var) * var[1], " + ")
            weightedTotal += self.outDescriptions.defuzzify(*var) * var[1]
        return weightedTotal / weightSum

    def __computeDescriptions(self, inputs):
        return {name: self.inDescriptions[name].fuzzify(inputs[name]) for name, value in inputs.items()}

    def __computeFuzzyRules(self, fuzzyInValues):
        return [rule.evaluateConjunction(fuzzyInValues) for rule in self.rules if rule.evaluateConjunction(fuzzyInValues)[1] != 0]
