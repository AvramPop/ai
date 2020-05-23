from console import *

def main():
    controller = Controller("training.in", "input.in", "output.out")
    console = Console(controller)
    console.run()

main()
