import threading
from collections import deque

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
                self.engine.schedule(self.schedule_recv_comm.recv()) 
                print("EngineComm: Received Message on Schedule Comm")
            if self.eventgen_comm.poll(): 
                self.engine.schedule(self.eventgen_comm.recv())
                print("EngineComm: Received Message on Event Comm")

            if len(self.send_buffer) > 0: 
                i = 0 # send 10 events a loop to avoid blocking communication 
                print("EngineComm: Sending Message on Scheduler Comm")
                while len(self.send_buffer) > 0 and i < EngineComm.MAX_LOOP_SENDS: 
                    self.schedule_send_comm.send(self.send_buffer.popleft())
                    i += 1
                    
    def send(self, msg, **kwargs): 
        self.send_buffer.append(msg) 

    