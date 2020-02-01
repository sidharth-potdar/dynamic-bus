from uuid import uuid4
import time
# import itertools

class Event:
    # __counter = itertools.count()

    def __init__(self, ts=None, *args, **kwargs):
        self._scheduled_ts = time.time()
        self._valid = True
        self._execute_at = time.time()
        # self._id = next(Event.__counter)
        self._id = uuid4()
        self.event = None

    def isValid(self):
        '''
        Instead of having to remove from the priority queue,
        mark entry as invalid so our engine ignores it
        '''
        return self._valid;
    def invalidate(self):
        self._valid = False

    def getExecutionPoint(self):
        return self._execute_at

    def getId(self):
        ''' Might not need this'''
        return self._id

    def execute(self):
        ''' enter code to do here upon execution
        - generate new events, etc
        '''
        print(self._id, self.event)
        pass
