import multiprocessing as mp
import random
import time
from graph import Graph
from engine import Engine
from event_processes import EventProcess
from scheduler import Scheduler
from volume_dist import generateDistributions

# Load configuration
# Graphs can be represented as an adjacency list


def main():
    scheduler_comm_e, scheduler_comm_s = mp.Pipe(True)
    eventgen_comm_e, eventgen_comm_g = mp.Pipe(True)
    graph = Graph()
    graph.init_file("./pickles/graph.pypkle")
    scheduler = Scheduler()
    scheduler.init(graph, scheduler_comm_s)
    engine = Engine()

    pickup_dist, dropoff_dist = generateDistributions()

    processes = [EventProcess(eventgen_comm_g, i, graph, engine, pickup_dist, dropoff_dist) for i in range(1)]

    for p in processes:
        p.start()

    while True:
        # check to see if any events are available 
        if scheduler_comm_e.poll(): 
            print("Found data on scheduler comm")
            engine.schedule(scheduler_comm_e.recv()) 
        if eventgen_comm_e.poll(): 
            print("Found data on Event Gen Comm. ")
            engine.schedule(eventgen_comm_e.recv())
        engine.tick()
if __name__=="__main__":
    main()
