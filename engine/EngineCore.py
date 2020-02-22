import logging
import random
import heapq
import threading
import time
from events import ScheduleEvent, EndScheduleEvent

class EngineCore(threading.Thread):
    ''' Engine thread executes in background'''

    def __init__(self, engine):
        super().__init__()
        self._queue = engine.getQueue()
        self._lock = engine.getLock()
        # see if we can remove the dict
        self._dict = {}
        self.engine = engine
        self.now = 6
        #self.today = random.choice([0,1,2,3,4])
        #logging.basicConfig(filename='sim.log', filemode='w')
        #self.logger = logging.getLogger()

    def schedule(self, *events):
        with self._lock:
            for event in events:
                heapq.heappush(self._queue, (event.getExecutionPoint(), event))
                self._dict[event.getId()] = event

        # If we can get remove working w/o this, we should

    def getSimulationTime(self):
        return self.now

    def run(self):
        print("Engine Booting")
        last_time = time.time()
        i = 0
        j = 0
        time.sleep(1)
        end = False 
        last_seen = time.time() 
        log_time = time.time() 
        lock_next = False 
        while not end:
            # pop from heapq
            if time.time() - log_time > 5: 
                print(f"Heap: {len(self._queue)}") 
                log_time = time.time() 
            if (len(self._queue) > 0):
                self.engine.send_heartbeat = True 
                last_seen = time.time() 
                with self._lock:
                    priority, event = heapq.heappop(self._queue)
            elif time.time() - last_seen > 5: 
                self.engine.send_heartbeat = False 
                if not self.engine.heartbeat: 
                    end = True
                continue 
            else:
                continue
            while not event.isValid() and len(self._queue) > 0:
                # TODO - some sort of logging
                # self.logger.info("%s %s marked as invalid." % (event.__class__, event.getId()))
                # Here mark invalid event
                priority, event = heapq.heappop(self._queue)
            self.now = event.getExecutionPoint()
            
            if type(event) == ScheduleEvent:
                now = time.time()
                if i % 100 == 0:
                    print(f"Executing {i} schedule events in", time.time() - last_time, ";", j, "other events executed")
                    i = 0
                    j = 0
                    last_time = time.time()
                if lock_next != False : 
                    self.engine.scheduleSemaphore.acquire()
                lock_next = event.getId() 
                i += 1
            else: 
                j += 1
            results = event.execute()

            if "events" in results:
                for e in results['events']:
                    self.schedule(e)
            if "scheduler_calls" in results:
                for call in results['scheduler_calls']:
                    self.engine.send(call)
            if "ids" in results:
                self.remove(*results['ids'])
                # print("Slept for", time.time() - now, "seconds")
                # floors speed to 60x real life
            #TODO more logging
            # self.logger.info("%s %s executed at %s" % (event.__class__, event.getId(), event.getExecutionPoint()))
        print("Engine Core Terminating")
    def remove(self, *uuids):
        ''' helper method, even though events can atomically
        invalidate themselves '''
        for eid in uuids:
            self._dict[eid].invalidate()
