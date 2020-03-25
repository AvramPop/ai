# -*- coding: utf-8 -*-
from qtpy.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QMainWindow, QApplication, QLineEdit, QLabel
import matplotlib.pyplot as plt
from EvolutionaryAlgorithm import *

class EvolutionaryAlgorithmWindow(QMainWindow):
    def __init__(self, parent=None):
        super(EvolutionaryAlgorithmWindow, self).__init__(parent)
        self.__setupUI()

    def setProblem(self, problem):
        self.problem = problem
        self.evolutionaryAlgorithm = EvolutionaryAlgorithm(self.problem, "ev.in") 
        self.evolutionaryAlgorithmThread = EvolutionaryAlgorithmThread(self.evolutionaryAlgorithm)
        self.evolutionaryAlgorithmThread.findSignal.connect(self.updateFindUI)
        self.evolutionaryAlgorithmStatsThread = EvolutionaryAlgorithmStatsThread(self.evolutionaryAlgorithm)
        self.evolutionaryAlgorithmStatsThread.statsSignal.connect(self.updateStatsUI)
        
        
    def __setupUI(self):
        self.stopFindButton = QPushButton('Stop find', self)
        self.stopFindButton.resize(self.stopFindButton.sizeHint())
        self.stopFindButton.move(50, 50)    
        self.stopFindButton.clicked.connect(self.__stopFindButtonClicked)
        
        self.findButton = QPushButton('Find', self)
        self.findButton.resize(self.findButton.sizeHint())
        self.findButton.move(50, 50)    
        self.findButton.clicked.connect(self.__findButtonClicked)
        
        self.stopStatsButton = QPushButton('Stop stats', self)
        self.stopStatsButton.resize(self.stopStatsButton.sizeHint())
        self.stopStatsButton.move(50, 50)    
        self.stopStatsButton.clicked.connect(self.__stopStatsButtonClicked)
        
        self.statsButton = QPushButton('Stats', self)
        self.statsButton.resize(self.statsButton.sizeHint())
        self.statsButton.move(50, 50)    
        self.statsButton.clicked.connect(self.__statsButtonClicked)
        
        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.findButton)
        self.hbox.addWidget(self.stopFindButton)
        self.hbox.addWidget(self.statsButton)
        self.hbox.addWidget(self.stopStatsButton)
        
        popSizeBox = QHBoxLayout()
        popSizeLabel = QLabel("Population size:")
        self.populationSizeInput = QLineEdit()
        popSizeBox.addWidget(popSizeLabel)
        popSizeBox.addWidget(self.populationSizeInput)
        
        mutationsBox = QHBoxLayout()
        mutationsLabel = QLabel("Mutations probability:")
        self.mutationProbabilityInput = QLineEdit()
        mutationsBox.addWidget(mutationsLabel)
        mutationsBox.addWidget(self.mutationProbabilityInput)
        
        crossoverBox = QHBoxLayout()
        crossoverLabel = QLabel("Crossover probability:")
        self.crossoverProbabilityInput = QLineEdit()
        crossoverBox.addWidget(crossoverLabel)
        crossoverBox.addWidget(self.crossoverProbabilityInput)
        
        gensBox = QHBoxLayout()
        gensLabel = QLabel("Number of generations:")
        self.numberOfGenerationsInput = QLineEdit()
        gensBox.addWidget(gensLabel)
        gensBox.addWidget(self.numberOfGenerationsInput)
        
        self.solutionLabel = QLabel()
        self.statsLabel = QLabel()
        self.vbox = QVBoxLayout()
        self.vbox.addStretch(1)
        self.vbox.addLayout(popSizeBox)
        self.vbox.addLayout(mutationsBox)
        self.vbox.addLayout(crossoverBox)
        self.vbox.addLayout(gensBox)
        self.vbox.addWidget(self.solutionLabel)
        self.vbox.addWidget(self.statsLabel)
        self.vbox.addLayout(self.hbox)
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(self.vbox)
        
    def updateFindUI(self, threadData):
        if threadData[1] == False:
            self.solutionLabel.setText("Looking for solutions\nBest solution until now:\n" + str(threadData[0]) + '\nFitness:' + str(threadData[0].fitness()) + '\n')
        else:
            self.solutionLabel.setText("Best solution found!\n" + str(threadData[0]) + '\nFitness:' + str(threadData[0].fitness()) + '\nDone!')

    def updateStatsUI(self, threadData):
        if threadData[1] == False:
            self.solutionLabel.setText("Generationg statistics\nBest solution until now:\n" + str(threadData[0]) + '\nFitness:' + str(threadData[0].fitness()) + '\n')
        else:
            self.solutionLabel.setText("Stats:\nBest solution found\n" + str(threadData[0]) + '\nFitness:' + str(threadData[0].fitness()) + "\nAverage: " + str(threadData[2]) + "\nStandard deviation:" + str(threadData[3]))
            plt.plot(threadData[4])
            plt.show()
            
    def __stopFindButtonClicked(self):
        self.evolutionaryAlgorithmThread.running = False

    def __stopStatsButtonClicked(self):
        self.evolutionaryAlgorithmStatsThread.running = False
        
    def __findButtonClicked(self):
        self.evolutionaryAlgorithm.setParams(int(self.populationSizeInput.text()), float(self.mutationProbabilityInput.text()), float(self.crossoverProbabilityInput.text()), int(self.numberOfGenerationsInput.text()))
        self.evolutionaryAlgorithmThread.start()         
        
    def __statsButtonClicked(self):
        self.evolutionaryAlgorithmStatsThread.start()  