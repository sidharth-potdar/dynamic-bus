from multiprocessing import Process
import time
import random
from events import RequestEvent
from events import GraphUpdateEvent
from distributions import prob_dist

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
        update_event = GraphUpdateEvent(0, 7.5, 1)
        self._comm.send(update_event)
        for ride in self._rides:
            origin_node, destination_node, start_hr = ride
            event_ts = start_hr + random.random() # randomly pick a time within the hr to start
            event = RequestEvent(origin_node=origin_node, destination_node=destination_node, ts=event_ts, current_ts=6) # Current ts is 6 because everything is scheduled before starting
            event.event = self._id
            self._comm.send(event)
