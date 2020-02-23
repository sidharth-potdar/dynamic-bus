import multiprocessing as mp
import threading
import random
import time
from engine import Engine

from event_processes import EventProcess
from scheduler.scheduler import Scheduler
from scheduler.graph import Graph

import sys


def main(num_buses=100, bus_capacity=5):

    e_to_s_recv, e_to_s_send = mp.Pipe(False)
    s_to_e_recv, s_to_e_send = mp.Pipe(False)
    g_to_e_recv, g_to_e_send = mp.Pipe(False)


    graph = Graph()
    graph.init_file("./pickles/graph.pypkle")
    # pickup_dist, dropoff_dist = generateDistributions()

    # start the engine
    if num_buses == None: 
        num_buses = 100 
    if bus_capacity == None: 
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

    if len(sys.argv) > 1:
        nb = int(sys.argv[1])
        bc = int(sys.argv[2])
        main(nb,bc)
    else: 
        MAX_CONCURRENT_SIMS = 3
        RUNS_PER_PARAM = 15
        MIN_BUS_CAPACITY = 4
        MAX_BUS_CAPACITY = 7
        MIN_BUSSES = 100
        MAX_BUSSES = 100
        args = []
        for _ in range(RUNS_PER_PARAM): 
            for i in range(MIN_BUSSES, MAX_BUSSES + 1, 10): 
                for j in range(MIN_BUS_CAPACITY, MAX_BUS_CAPACITY): 
                    args.append({"num_buses":  i, "bus_capacity":  j})
        Ps = [None] * MAX_CONCURRENT_SIMS
        i = 0 
        while i < len(args): 
            for p_c, p in enumerate(Ps): 
                if p is None: 
                    Ps[p_c] = mp.Process(target=main, kwargs=args[i], name=str(args[i]), daemon=False) 
                    Ps[p_c].start() 
                    i += 1                
                    print(f"STARTING PROCESS {i} / {len(args)}")
                elif not p.is_alive(): 
                    # process ended. 
                    Ps[p_c] = mp.Process(target=main, kwargs=args[i], name=str(args[i]), daemon=False)
                    Ps[p_c].start() 
                    i += 1
                    print(f"STARTING PROCESS {i} / {len(args)}")

                else: 
                    time.sleep(1) # stability 
        for p in Ps:
            p.join() 
            