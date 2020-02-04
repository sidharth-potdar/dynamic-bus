from multiprocessing import Process
import time
import random

from events import RequestEvent

class EventProcess(Process):
    def __init__(self, queue, id, graph, distribution=None):
        super(EventProcess, self).__init__()
        self._queue = queue
        self._id = id
        self._graph = graph
        self._distribution = distribution

    def run(self):
        while True:
            origin_node = random.choice(self._graph.get_nodes())
            destination_node = random.choice(self._graph.get_nodes())
            event = RequestEvent(origin_node=origin_node, destination_node=destination_node)
            event.event = self._id
            self._queue.put(event)
            time.sleep(random.expovariate(0.3))
