from multiprocessing import Process
import time
import random
from events import RequestEvent
from events import GraphUpdateEvent
from events import InvalidateEvent
from distributions import prob_dist
from events import NumRidesEvent

class EventProcess(Process):
    def __init__(self, queue, id, graph):
        super(EventProcess, self).__init__()
        # queue is a pipe now
        self._comm = queue
        self._id = id
        self._graph = graph
        #self._engine = engine
        #self._pickup_dist = pickup_dist
        #self._dropoff_dist = dropoff_dist
        #self._timeLimit = timeLimit
        self._rides = prob_dist.generateRides()

    def run(self):
        min_hr = None
        max_hr = None
        for ride in self._rides[:len(self._rides) // 100 ]:
            origin_node, destination_node, start_hr = ride
            event_ts = start_hr + random.random() # randomly pick a time within the hr to start
            if min_hr is None: 
                min_hr = event_ts
                max_hr = event_ts
            else: 
                min_hr = min(min_hr, event_ts)
                max_hr = max(max_hr, event_ts)
            event = RequestEvent(origin_node=origin_node, destination_node=destination_node, ts=event_ts) # Current ts is 6 because everything is scheduled before starting
            event.event = self._id
            self._comm.send(event)
        print("Generated with", min_hr, max_hr)
        i = 6
        while i <= 10: 
            self._comm.send(GraphUpdateEvent(i, i))
            i += 0.5

        self._comm.send(NumRidesEvent(0,len(self._rides)))
