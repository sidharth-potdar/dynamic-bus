import threading
from collections import deque
from events import EndScheduleEvent
import time 
class EngineComm(threading.Thread):
    MAX_LOOP_SENDS = 10
    def __init__(self, engine, daemon=None, **kwargs): 
        super().__init__(daemon=daemon)
        self.engine = engine 
        self.schedule_recv_comm = self.engine.getScheduleRecvComm() 
        self.schedule_send_comm = self.engine.getScheduleSendComm() 
        self.eventgen_comm = self.engine.getEventgenComm() 
        self.send_buffer = deque()
        self.on = True 
    def run(self): 
        # Keep track of our heartbeat time
        last_heartbeat_time = time.time() 
        # keep track of last engine heartbeat signal
        last_schedule_heartbeat = time.time() 
        res_cache = None 
        while self.on: 
            if self.schedule_recv_comm.poll(): 
                res = self.schedule_recv_comm.recv() 
                if res == "heartbeat": 
                    self.engine.heartbeat = True 
                    last_schedule_heartbeat = time.time() 
                elif type(res) == EndScheduleEvent: 
                    self.engine.scheduleSemaphore.release() 
                else: 
                    self.engine.schedule(res) 
            
            if time.time() - last_heartbeat_time > 1 and self.engine.send_heartbeat: 
                self.schedule_send_comm.send("heartbeat")
                last_heartbeat_time = time.time() 

            if time.time() - last_schedule_heartbeat > 5: 
                self.engine.heartbeat = False 

            if self.eventgen_comm.poll(): 
                self.engine.schedule(self.eventgen_comm.recv())

            if len(self.send_buffer) > 0: 
                i = 0 # send 10 events a loop to avoid blocking communication 
                while len(self.send_buffer) > 0 and i < EngineComm.MAX_LOOP_SENDS: 
                    msg = self.send_buffer.popleft()
                    self.schedule_send_comm.send(msg)
                    i += 1
                    
    def send(self, msg, **kwargs): 
        self.send_buffer.append(msg) 

    