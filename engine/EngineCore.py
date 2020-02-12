import logging 
import random 
import heapq
import threading

class EngineCore(threading.Thread):
    ''' Engine thread executes in background''' 

    def __init__(self, engine):
        super().__init__()
        self._queue = engine.getQueue()
        self._lock = engine.getLock()
        # see if we can remove the dict
        self._dict = {}
        self.engine = engine  
        self.now = 0
        self.today = random.choice([0,1,2,3,4])
        logging.basicConfig(filename='sim.log', filemode='w')
        self.logger = logging.getLogger()

    def schedule(self, *events):
        with self._lock: 
            for event in events: 
                heapq.heappush(self._queue, (event.getExecutionPoint(), event))
        # If we can get remove working w/o this, we should
        self._dict[event.getId()] = event

    def getSimulationTime(self):
        return self.now

    def getDayOfTheWeek(self):
        return self.today

    def run(self):
        print("Engine Booting")
        while True: 
            # pop from heapq
            if (len(self._queue) > 0): 
                with self._lock: 
                    priority, event = heapq.heappop(self._queue)
            else: 
                continue 

            while not event.isValid():
                # TODO - some sort of logging
                self.logger.info("%s %s marked as invalid." % (event.__class__, event.getId()))
                # Here mark invalid event
                priority, event = heapq.heappop(self._queue)

            self.now = event.getExecutionPoint()
            events = event.execute()
            if events is not None: 
                for e in events: 
                    if not e.is_complicated(): 
                        self.schedule(e) 
                    else: 
                        self.engine.send(e)

            #TODO more logging
            self.logger.info("%s %s executed at %s" % (event.__class__, event.getId(), event.getExecutionPoint()))

    def remove(self, *events):
        ''' helper method, even though events can atomically
        invalidate themselves '''
        for event in events:
            event.invalidate()

    