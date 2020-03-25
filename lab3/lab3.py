#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 13:03:07 2020

@author: dani
"""
from mainUI import *
import sys
from qtpy.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())    
    
main()
