# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
from qtpy.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QMainWindow, QApplication, QLineEdit, QLabel
import matplotlib.pyplot as plt
from ParticleSwarm import *

class ParticleSwarmWindow(QMainWindow):
    def __init__(self, parent=None):
        super(ParticleSwarmWindow, self).__init__(parent)
        self.__setupUI()

    def setProblem(self, problem):
        self.problem = problem
        self.particleSwarm = ParticleSwarm(self.problem, "ps.in") 
        self.particleSwarmThread = ParticleSwarmThread(self.particleSwarm)
        self.particleSwarmThread.findSignal.connect(self.updateFindUI)
        self.particleSwarmStatsThread = ParticleSwarmStatsThread(self.particleSwarm)
        self.particleSwarmStatsThread.statsSignal.connect(self.updateStatsUI)
        
        
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
        
        inertiaBox = QHBoxLayout()
        inertiaLabel = QLabel("Inertia coefficient:")
        self.inertiaInput = QLineEdit()
        inertiaBox.addWidget(inertiaLabel)
        inertiaBox.addWidget(self.inertiaInput)
        
        cognitiveBox = QHBoxLayout()
        cognitiveLabel = QLabel("Cognitive learning coefficient:")
        self.cognitiveInput = QLineEdit()
        cognitiveBox.addWidget(cognitiveLabel)
        cognitiveBox.addWidget(self.cognitiveInput)
        
        socialBox = QHBoxLayout()
        socialLabel = QLabel("Social learning coefficient:")
        self.socialInput = QLineEdit()
        socialBox.addWidget(socialLabel)
        socialBox.addWidget(self.socialInput)
        
        gensBox = QHBoxLayout()
        gensLabel = QLabel("Number of iterations:")
        self.numberOfGenerationsInput = QLineEdit()
        gensBox.addWidget(gensLabel)
        gensBox.addWidget(self.numberOfGenerationsInput)
        
        neighbourhoodSizeBox = QHBoxLayout()
        neighbourhoodSizeLabel = QLabel("Neighbourhood size:")
        self.neighbourhoodSizeInput = QLineEdit()
        neighbourhoodSizeBox.addWidget(neighbourhoodSizeLabel)
        neighbourhoodSizeBox.addWidget(self.neighbourhoodSizeInput)
        
        self.solutionLabel = QLabel()
        self.statsLabel = QLabel()
        self.vbox = QVBoxLayout()
        self.vbox.addStretch(1)
        self.vbox.addLayout(popSizeBox)
        self.vbox.addLayout(inertiaBox)
        self.vbox.addLayout(cognitiveBox)
        self.vbox.addLayout(socialBox)
        self.vbox.addLayout(gensBox)
        self.vbox.addLayout(neighbourhoodSizeBox)
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
        pass
        if threadData[1] == False:
            self.solutionLabel.setText("Generationg statistics\nBest solution until now:\n" + str(threadData[0]) + '\nFitness:' + str(threadData[0].fitness()) + '\n')
        else:
            self.solutionLabel.setText("Stats:\nBest solution found\n" + str(threadData[0]) + '\nFitness:' + str(threadData[0].fitness()) + "\nAverage: " + str(threadData[2]) + "\nStandard deviation:" + str(threadData[3]))
            plt.plot(threadData[4])
            plt.show()
            
    def __stopFindButtonClicked(self):
        self.particleSwarmThread.running = False

    def __stopStatsButtonClicked(self):
        self.particleSwarmStatsThread.running = False
        
    def __findButtonClicked(self):
        self.particleSwarm.setParams(int(self.populationSizeInput.text()), float(self.inertiaInput.text()), float(self.cognitiveInput.text()), float(self.socialInput.text()), int(self.numberOfGenerationsInput.text()), int(self.neighbourhoodSizeInput.text()))
        self.particleSwarmThread.start()         
        
    def __statsButtonClicked(self):
        self.particleSwarmStatsThread.start()  