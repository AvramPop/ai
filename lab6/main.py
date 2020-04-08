from data import Data
from decision_tree import DecisionTree

def main():
    data = Data("balance-scale.data")
    decisionTree = DecisionTree(data.getTrainData())
#    decisionTree.printTree()
    print(decisionTree.accuracy(data.getTestData()))
    
main()