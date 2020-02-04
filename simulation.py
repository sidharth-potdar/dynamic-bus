from multiprocessing import Process

class Simulation(Process):
    def __init__(self):
        super(Simulation, self).__init__()

    def run(self):
        while True:
