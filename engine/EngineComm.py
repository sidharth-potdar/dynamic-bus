import threading
from collections import deque
from events import EndScheduleEvent

class EngineComm(threading.Thread):
    MAX_LOOP_SENDS = 10
    def __init__(self, engine, daemon=None): 
        super().__init__(daemon=daemon)
        self.engine = engine 
        self.schedule_recv_comm = self.engine.getScheduleRecvComm() 
        self.schedule_send_comm = self.engine.getScheduleSendComm() 
        self.eventgen_comm = self.engine.getEventgenComm() 
        self.send_buffer = deque()

    def run(self): 
        while True: 
            if self.schedule_recv_comm.poll(): 
                res = self.schedule_recv_comm.recv() 
                if type(res) == EndScheduleEvent: 
                    self.engine.scheduleSemaphore.release() 
                else: 
                    self.engine.schedule(res) 
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

    