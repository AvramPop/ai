# -*- coding: utf-8 -*-

class FuzzyRule:
    def __init__(self, inputVariables, outputVariables):
        self.outputVariablesVariables = outputVariables
        self.inputVariables = inputVariables

    def evaluateConjunction(self, inputVariables):
        for description, outputName in self.inputVariables.items():
            print(description, " ", outputName, "= ", inputVariables[description][outputName])
        result = min([inputVariables[description][outputName] for description, outputName in self.inputVariables.items()])
        print("conjunction = ", result)
        return [self.outputVariablesVariables, result]
