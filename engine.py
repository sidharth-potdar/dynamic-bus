import heapq
import random
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
        priority, event = heapq.heappop(self._queue)

        while not event.isValid():
            # TODO - some sort of logging
            self.logger.info("%s %s marked as invalid." % (event.__class__, event.getId()))
            # Here mark invalid event
            priority, event = heapq.heappop(self._queue)

        self.now = event.getExecutionPoint()
        event.execute()

        #TODO more logging
        self.logger.info("%s %s executed at %s" % (event.__class__, event.getId(), event.getExecutionPoint()))

    def remove(self, *events):
        ''' helper method, even though events can atomically
        invalidate themselves '''
        for event in events:
            event.invalidate()
