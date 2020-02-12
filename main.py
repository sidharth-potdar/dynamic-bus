import multiprocessing as mp
import threading 
import random
import time
from engine import Engine 

from event_processes import EventProcess
from scheduler.scheduler import Scheduler
from scheduler.graph import Graph
from volume_dist import generateDistributions


def main():
        
    e_to_s_recv, e_to_s_send = mp.Pipe(False)
    s_to_e_recv, s_to_e_send = mp.Pipe(False)
    g_to_e_recv, g_to_e_send = mp.Pipe(False) 


    graph = Graph()
    graph.init_file("./pickles/graph.pypkle")
    scheduler = Scheduler()
    scheduler.init(graph, s_to_e_send)
    pickup_dist, dropoff_dist = generateDistributions()

    # start the engine 
    engine = Engine(pipe_recv_from_scheduler = e_to_s_recv, pipe_recv_from_gen = g_to_e_recv, pipe_send_to_scheduler = e_to_s_send)
    engine.start() 


    processes = [EventProcess(g_to_e_send, i, graph, engine, pickup_dist, dropoff_dist) for i in range(1)]
    for p in processes:
        p.start()
    while True: 
        if s_to_e_recv.poll(): 
            s_to_e_recv.recv() 
        time.sleep(0.1)
    for p in processes: 
        p.join()

if __name__=="__main__":
    main()
