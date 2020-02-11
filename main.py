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
    queue = mp.Queue()
    graph = Graph()
    graph.init_random()
    scheduler = Scheduler()
    scheduler.init(graph, queue)
    engine = Engine()

    pickup_dist, dropoff_dist = generateDistributions()

    processes = [EventProcess(queue, i, graph, engine, pickup_dist, dropoff_dist) for i in range(1)]

    for p in processes:
        p.start()

    while True:
        event = queue.get()
        engine.schedule(event)

        engine.tick()

if __name__=="__main__":
    main()
