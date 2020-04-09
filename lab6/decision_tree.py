from data import Entry
from copy import deepcopy
from math import log
from pprint import pprint
class DecisionTree:
    def __init__(self, trainData, strategy):
        self.__strategy = strategy
        self.__root = self.__buildTree(trainData, [i for i in range(len(trainData[0].getAttributes()))])
        
    def __buildTree(self, data, attributeList):
        if self.__wholeDataInSameClass(data):
            return Leaf(data[0].getClass())
        elif len(attributeList) == 0:
            return Leaf(self.__majorityClass(data))
        else:
            if self.__strategy == "gini":
                separationAttribute = self.__separationAttributeGiniIndex(data, attributeList)
            elif self.__strategy == "gain":
                separationAttribute = self.__separationAttributeInformationGain(data, attributeList)
            node = AttributeNode(separationAttribute)
            for category in data[0].getCategoriesForAttribute(separationAttribute):
                self.__setChildForCategory(category, data, separationAttribute, node, attributeList)
            return node
        
    def __setChildForCategory(self, category, data, separationAttribute, node, attributeList):
        entriesWithCategory = self.__entriesWithCategory(data, category, separationAttribute)
        if category == 0:
            if len(entriesWithCategory) == 0:
                node.setFalseChild(Leaf(self.__majorityClass(entriesWithCategory)))
            else:
                tempAttributeList = deepcopy(attributeList)
                tempAttributeList.remove(separationAttribute)
                node.setFalseChild(self.__buildTree(entriesWithCategory, tempAttributeList))
        else:
            if len(entriesWithCategory) == 0:
                node.setTrueChild(Leaf(self.__majorityClass(entriesWithCategory)))
            else:
                tempAttributeList = deepcopy(attributeList)
                tempAttributeList.remove(separationAttribute)
                node.setTrueChild(self.__buildTree(entriesWithCategory, tempAttributeList))
    
    def __entriesWithCategory(self, data, category, separationAttribute):
        result = []
        if category == 0:
            for entry in data:
                if entry.getAttributes()[separationAttribute] <= entry.getMedianValueForAttribute(separationAttribute):
                    result.append(entry)
        else:
            for entry in data:
                if entry.getAttributes()[separationAttribute] > entry.getMedianValueForAttribute(separationAttribute):
                    result.append(entry)
        return result
    
    def __wholeDataInSameClass(self, data):
        firstElementClass = data[0].getClass()
        for i in range(1, len(data)):
            if data[i].getClass() is not firstElementClass:
                return False
        return True
    
    def __majorityClass(self, data):
        occurences = {}
        for entry in data:
            if entry.getClass() not in occurences:
                occurences[entry.getClass()] = 0
            occurences[entry.getClass()] += 1
        return max(occurences, key=lambda k: occurences[k])
    
    def __computeSystemEntropy(self, data):
        entropies = {}
        for entry in data:
            if entry.getClass() not in entropies:
                entropies[entry.getClass()] = 0
            entropies[entry.getClass()] += 1
        entropy = 0
        for key, value in entropies.items():
            r = value / len(data)
            entropy += r * log(r, 3)
        return entropy * -1
    
    def __separationAttributeInformationGain(self, data, attributeList):
        gains = {}
        systemEntropy = self.__computeSystemEntropy(data)
        for attribute in attributeList:
            expectedInformation = 0
            for category in data[0].getCategoriesForAttribute(0):
                expectedInformation += self.__entropy(self.__entriesWithCategory(data, category, attribute))
            gains[attribute] = systemEntropy - expectedInformation
        return max(gains, key=lambda k: gains[k])
    
    def __entropy(self, entries):
        entropies = {}
        for entry in entries:
            if entry.getClass() not in entropies:
                entropies[entry.getClass()] = 0
            entropies[entry.getClass()] += 1
        entropy = 0
        for key, value in entropies.items():
            r = value / len(entries)
            entropy += r * log(r, 3)
        return entropy * -1
    
    def __separationAttributeGiniIndex(self, data, attributeList):
        indices = {}
        for attribute in attributeList:
            gini = 0
            for category in data[0].getCategoriesForAttribute(0):
                right = self.__entriesWithClass(self.__entriesWithCategory(data, category, attribute), "R") / len(self.__entriesWithCategory(data, category, attribute))
                left = self.__entriesWithClass(self.__entriesWithCategory(data, category, attribute), "L") / len(self.__entriesWithCategory(data, category, attribute))
                balanced = self.__entriesWithClass(self.__entriesWithCategory(data, category, attribute), "B") / len(self.__entriesWithCategory(data, category, attribute)) 
                giniForCategory = 1 - right ** 2 - left ** 2 - balanced ** 2
                gini += len(self.__entriesWithCategory(data, category, attribute)) / len(data) * giniForCategory
            indices[attribute] = gini
        return min(indices, key=lambda k: indices[k])
    
    def __entriesWithClass(self, data, entryClass):
        count = 0
        for entry in data:
            if entry.getClass() == entryClass:
                count += 1
        return count
                    
    def predict(self, entry):
       currentNode = self.__root
       while not isinstance(currentNode, Leaf):
           currentNode = currentNode.getChildrenFor(entry)
       return currentNode.getClass()
   
    def accuracy(self, testData):
        matches = 0
        for entry in testData:
            if entry.getClass() == self.predict(entry):
                matches = matches + 1
        return matches / len(testData)
    
    def printTree(self):
        self.__printUtil(self.__root)
        
    def __printUtil(self, current):
        print(str(current))
        if isinstance(current, AttributeNode):
            self.__printUtil(current.getFalseChild())
            self.__printUtil(current.getTrueChild())
        
    
class AttributeNode:
    def __init__(self, attributeNumber):
        self.__attributeNumber = attributeNumber 
        self.__trueChild = None
        self.__falseChild = None
    
    def setTrueChild(self, trueChild):
        self.__trueChild = trueChild
    
    def setFalseChild(self, falseChild):
        self.__falseChild = falseChild    
        
    def getTrueChild(self):
        return self.__trueChild
    
    def getFalseChild(self):
        return self.__falseChild
        
    def getChildrenFor(self, entry):
        if entry.getAttributes()[self.__attributeNumber] <= entry.getMedianValueForAttribute(self.__attributeNumber): 
            return self.__falseChild
        else:
            return self.__trueChild
        
    def __str__(self):
        return "Attribute node: " + str(self.__attributeNumber)
        
class Leaf:    
    def __init__(self, leafClass):
        self.__leafClass = leafClass
        
    def getClass(self):
        return self.__leafClass
    
    def __str__(self):
        return "Leaf node: " + self.__leafClass 
