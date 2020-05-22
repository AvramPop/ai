# -*- coding: utf-8 -*-
from console import *

def main():
    ctrl = Controller("problem.in", "input.in", "output.out")
    console = Console(ctrl)
    console.run()

main()