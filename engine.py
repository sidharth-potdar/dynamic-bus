import heapq

class Engine:
    def __init__(self):
        self._queue = []
        # see if we can remove the dict
        self._dict = {}

    def schedule(self, event):
        heapq.heappush(self._queue, (event.getExecutionPoint(), event))
        # If we can get remove working w/o this, we should
        self._dict[event.getId()] = event

    def tick(self):
        # pop from heapq
        priority, event = heapq.heappop(self._queue)

        while not event.isValid():
            # TODO - some sort of logging
            # Here mark invalid event
            priority, event = heapq.heappop(self._queue)
        event.execute()
        #TODO more logging

    def remove(self, *events):
        ''' helper method, even though events can atomically
        invalidate themselves '''
        for event in events:
            event.invalidate()
