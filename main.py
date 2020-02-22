import multiprocessing as mp
import threading
import random
import time
from engine import Engine

from event_processes import EventProcess
from scheduler.scheduler import Scheduler
from scheduler.graph import Graph


def main():

    e_to_s_recv, e_to_s_send = mp.Pipe(False)
    s_to_e_recv, s_to_e_send = mp.Pipe(False)
    g_to_e_recv, g_to_e_send = mp.Pipe(False)


    graph = Graph()
    graph.init_file("./pickles/graph.pypkle")
    # pickup_dist, dropoff_dist = generateDistributions()

    # start the engine
    num_buses = 100
    bus_capacity = 5
    engine = Engine(pipe_recv_from_scheduler = s_to_e_recv, pipe_recv_from_gen = g_to_e_recv, pipe_send_to_scheduler = e_to_s_send, num_buses = num_buses, bus_capacity=bus_capacity)
    engine.start()

    scheduler = Scheduler(pipe_send_to_engine=s_to_e_send, pipe_recv_from_engine=e_to_s_recv, graph=graph, num_buses = num_buses, bus_capacity = bus_capacity)

    scheduler.start()


    processes = [EventProcess(g_to_e_send, i, graph) for i in range(1)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    engine.join()
    scheduler.join()

if __name__=="__main__":
    main()
