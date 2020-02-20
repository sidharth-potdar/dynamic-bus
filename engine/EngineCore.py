# import logging
import random
import heapq
import threading
import time
from db_logging import EventLogger
from events import EndEvent

class EngineCore(threading.Thread):
    ''' Engine thread executes in background'''

    def __init__(self, engine):
        super().__init__()
        self._queue = engine.getQueue()
        self._lock = engine.getLock()
        # see if we can remove the dict
        self._dict = {}
        self.engine = engine
        self.now = 6 # Beginning of rush_hr
        #self.today = random.choice([0,1,2,3,4])
        #logging.basicConfig(filename='sim.log', filemode='w')
        #self.logger = logging.getLogger()

        self.past_events = []

    def schedule(self, *events):
        with self._lock:
            for event in events:
                heapq.heappush(self._queue, (event.getExecutionPoint(), event))
        # If we can get remove working w/o this, we should
        self._dict[event.getId()] = event

    def getSimulationTime(self):
        return self.now

    def run(self):
        print("Engine Booting")
        last_time = time.time()
        i = 0
        while True:
            # pop from heapq
            if (len(self._queue) > 0):
                with self._lock:
                    priority, event = heapq.heappop(self._queue)
            else:
                continue
            i += 1
            if i % 100 == 0:
                i = 0
                print("Executing 100 events in", time.time() - last_time)
                last_time = time.time()
            while not event.isValid():
                # TODO - some sort of logging
                # self.logger.info("%s %s marked as invalid." % (event.__class__, event.getId()))
                # Here mark invalid event
                priority, event = heapq.heappop(self._queue)

            self.now = event.getExecutionPoint()
            self.past_events.append(event)
            results = event.execute()
            if "events" in results:
                for e in results['events']:
                    self.schedule(e)
            if "scheduler_calls" in results:
                for call in results['scheduler_calls']:
                    self.engine.send(call)
            #TODO more logging
            # self.logger.info("%s %s executed at %s" % (event.__class__, event.getId(), event.getExecutionPoint()))
            if isinstance(event, EndEvent):
            	el = EventLogger()
            	el.log_events(past_events)
            	break


    def remove(self, *events):
        ''' helper method, even though events can atomically
        invalidate themselves '''
        for event in events:
            event.invalidate()
