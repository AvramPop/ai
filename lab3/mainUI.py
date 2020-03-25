# -*- coding: utf-8 -*-
from qtpy.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QMainWindow, QApplication, QLineEdit, QLabel
from eaUI import *
from hcUI import *

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.__setupUI()
        
    def __setupUI(self):
        self.evAlgorithmButton = QPushButton('Evolutionary Algorithm', self)
        self.evAlgorithmButton.resize(self.evAlgorithmButton.sizeHint())
        self.evAlgorithmButton.move(50, 50)    
        self.evAlgorithmButton.clicked.connect(self.__evAlgorithmButtonClicked)
        self.hillClimbButton = QPushButton('Hill Climbing Algorithm', self)
        self.hillClimbButton.resize(self.hillClimbButton.sizeHint())
        self.hillClimbButton.move(50, 50)    
        self.hillClimbButton.clicked.connect(self.__hillClimbButtonClicked)
        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.evAlgorithmButton)
        self.hbox.addWidget(self.hillClimbButton)
        secondBox = QHBoxLayout()
        label = QLabel("individual size:")
        self.problemSizeInput = QLineEdit()
        secondBox.addWidget(label)
        secondBox.addWidget(self.problemSizeInput)
        self.vbox = QVBoxLayout()
        self.vbox.addStretch(1)
        self.vbox.addLayout(secondBox)
        self.vbox.addLayout(self.hbox)
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(self.vbox)

        self.evAlgorithmButton.clicked.connect(self.__evAlgorithmButtonClicked)
        self.hillClimbButton.clicked.connect(self.__hillClimbButtonClicked)
        self.evolutionaryAlgorithmWindow = EvolutionaryAlgorithmWindow(self)
        self.hillClimbingAlgorithmWindow = HillClimbingAlgorithmWindow(self)
    
    def __evAlgorithmButtonClicked(self):
        self.evolutionaryAlgorithmWindow.setProblem(Problem(int(self.problemSizeInput.text())))
        self.evolutionaryAlgorithmWindow.show()
        
    def __hillClimbButtonClicked(self):
        self.hillClimbingAlgorithmWindow.setProblem(Problem(int(self.problemSizeInput.text())))
        self.hillClimbingAlgorithmWindow.show()

