from multiprocessing import Process
import time
import random

from events import Event

class EventFactory(Process):
    def __init__(self, queue, id, distribution=None):
        super(EventFactory, self).__init__()
        self._queue = queue
        self._id = id
        self._distribution = distribution

    def run(self):
        while True:
            event = Event()
            event.event = self._id
            self._queue.put(event)
            time.sleep(random.expovariate(1))
