from gpalgorithm import GPAlgorithm

def main():
    algorithmGP = GPAlgorithm("training.in", "input.in", "output.out", 10, 5, 100, 25, 0.5, 0.5, 10)
    algorithmGP.run()

main()
