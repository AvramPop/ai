# -*- coding: utf-8 -*-
from console import *

def main():
    controller = Controller("data.in")
    console = Console(controller)
    console.run()

main()