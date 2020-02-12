import multiprocessing as mp
import random
import time
from graph import Graph
from event_processes import EventProcess
from scheduler import Scheduler
from volume_dist import generateDistributions

# Load configuration
# Graphs can be represented as an adjacency list
import heapq
import logging

class Engine:
    def __init__(self):
        self._queue = []
        # see if we can remove the dict
        self._dict = {}
        self.now = 0
        self.today = random.choice([0,1,2,3,4])

        logging.basicConfig(filename='sim.log', filemode='w')
        self.logger = logging.getLogger()

    def schedule(self, event):
        heapq.heappush(self._queue, (event.getExecutionPoint(), event))
        # If we can get remove working w/o this, we should
        self._dict[event.getId()] = event


    def getSimulationTime(self):
        return self.now

    def getDayOfTheWeek(self):
        return self.today

    def tick(self):
        # pop from heapq
        if (len(self._queue) > 0): 
            priority, event = heapq.heappop(self._queue)
        else: 
            return 

        while not event.isValid():
            # TODO - some sort of logging
            self.logger.info("%s %s marked as invalid." % (event.__class__, event.getId()))
            # Here mark invalid event
            priority, event = heapq.heappop(self._queue)

        self.now = event.getExecutionPoint()
        events = event.execute()
        if events is not None: 
            for e in events: 
                self.schedule(e) 

        #TODO more logging
        self.logger.info("%s %s executed at %s" % (event.__class__, event.getId(), event.getExecutionPoint()))

    def remove(self, *events):
        ''' helper method, even though events can atomically
        invalidate themselves '''
        for event in events:
            event.invalidate()


def main():
    scheduler_comm_e, scheduler_comm_s = mp.Pipe(True)
    eventgen_comm_e, eventgen_comm_g = mp.Pipe(True)
    graph = Graph()
    graph.init_file("./pickles/graph.pypkle")
    scheduler = Scheduler()
    scheduler.init(graph, scheduler_comm_s)
    engine = Engine()

    pickup_dist, dropoff_dist = generateDistributions()

    processes = [EventProcess(eventgen_comm_g, i, graph, engine, pickup_dist, dropoff_dist) for i in range(1)]

    for p in processes:
        p.start()

    while True:
        # check to see if any events are available 
        if scheduler_comm_e.poll(): 
            print("Found data on scheduler comm")
            engine.schedule(scheduler_comm_e.recv()) 
        if eventgen_comm_e.poll(): 
            print("Found data on Event Gen Comm. ")
            engine.schedule(eventgen_comm_e.recv())
        engine.tick()
if __name__=="__main__":
    main()
