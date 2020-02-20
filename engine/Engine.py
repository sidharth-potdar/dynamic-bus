import heapq
import logging
import random 
import multiprocessing as mp
import threading 
from engine.EngineCore import EngineCore
from engine.EngineComm import EngineComm

class Engine(mp.Process): 
    def __init__(self, pipe_recv_from_scheduler = None, pipe_recv_from_gen = None, pipe_send_to_scheduler = None, **kwargs): 
        super().__init__() 
        self.from_scheduler = pipe_recv_from_scheduler
        self.from_gen = pipe_recv_from_gen 
        self.to_scheduler = pipe_send_to_scheduler
        self.queue_lock = threading.Lock() 
        self.queue = [] 
        self.comm = EngineComm(self, daemon=True, **kwargs)
        self.core = EngineCore(self, **kwargs)
        self.time = 0 
        self.scheduleSemaphore = threading.Semaphore(0) 


    def getScheduleSendComm(self): 
        return self.to_scheduler
        
    def getScheduleRecvComm(self): 
        return self.from_scheduler

    def getEventgenComm(self): 
        return self.from_gen

    def getQueue(self): 
        return self.queue

    def getLock(self): 
        return self.queue_lock 
    
    def schedule(self, *args, **kwargs): 
        self.core.schedule(*args, **kwargs) 

    def send(self, *args, **kwargs): 
        self.comm.send(*args, **kwargs)

    def run(self): 
        self.comm.start() 
        self.core.start() 
        self.core.join() 
         
    def getDayOfTheWeek(self): 
        return 0 

    def getSimulationTime(self): 
        self.time += 1
        return self.time 

