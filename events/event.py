from uuid import uuid4
import time
# import itertools

class Event:
    # __counter = itertools.count()

    def __init__(self, ts=None, current_ts=None, *args, **kwargs):
        self._scheduled_ts = current_ts
        self._valid = True
        self._execute_at = ts
        # self._id = next(Event.__counter)
        self._id = uuid4()
        self.event = None

    def is_complicated(self): 
        ''' 
        Override this, and return whether or not it should go to the scheduler process
        ''' 
        return NotImplementedError

    def isValid(self):
        '''
        Instead of having to remove from the priority queue,
        mark entry as invalid so our engine ignores it
        '''
        return self._valid
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
        pass
    
    def __le__(self, other): 
        return self.__lt__(other) or self.__eq__(other) 
    
    def __ge__(self, other): 
        return self.__gt__(other) or self.__eq__(other) 
    
    def __lt__(self, other): 
        if self._execute_at < other._execute_at: 
            return True 
        elif self._execute_at == other._execute_at: 
            if self._scheduled_ts < other._scheduled_ts: 
                return True 
            else: 
                return False 
        else: 
            return False 

    def __gt__(self, other): 
        if self._execute_at > other._execute_at: 
            return True 
        elif self._execute_at == other._execute_at: 
            if self._scheduled_ts > other._scheduled_ts: 
                return True 
            else: 
                return False 
        else: 
            return False 

    def __eq__(self, other): 
        return self._execute_at == other._execute_at and self._scheduled_ts == other._scheduled_ts
