import multiprocessing as mp
import random
import time
from graph import Graph  
from engine import Engine
<<<<<<< Updated upstream
from event_processes import EventProcess
=======
# from event_factory import EventFactory

# Load configuration 
# Graphs can be represented as an adjacency list 

>>>>>>> Stashed changes

def main():
    g = Graph() 
    g.init_random() 
    print(g._graph)
    engine = Engine()
    queue = mp.Queue()

    processes = [EventProcess(queue, i) for i in range(2)]

    for p in processes:
        p.start()

    while True:
        event = queue.get()
        engine.schedule(event)

        engine.tick()

if __name__=="__main__":
    main()
