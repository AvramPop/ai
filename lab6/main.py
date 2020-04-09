from console import Console

def main():
    data = Data("balance-scale.data")
    controller = Controller(data)
    console = Console(controller)
    console.run()
    
main()
