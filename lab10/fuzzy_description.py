# -*- coding: utf-8 -*-
class FuzzyDescriptions:
    def __init__(self):
        self.regions = {}
        self.inverseMembershipFunction = {}

    def addRegion(self, region, membershipFunction, inverseMembershipFunction=None):
        self.regions[region] = membershipFunction
        self.inverseMembershipFunction[region] = inverseMembershipFunction

    def fuzzify(self, value):
        for name, membershipFunction in self.regions.items():
            print(name, "= ", membershipFunction(value))
        print()
        return {name: membershipFunction(value) for name, membershipFunction in self.regions.items()}

    def defuzzify(self, outputName, value):
        return self.inverseMembershipFunction[outputName](value)

