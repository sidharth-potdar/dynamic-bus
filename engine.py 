import time 
import heapq 
import itertools

class Event: 
    __counter = itertools.count() 

    def __init__(self, ts=None, *args, **kwargs): 
        self._scheduled_ts = time.time() 
        self._valid = True 
        self._execute_at = ts 
        self._id = next(Event.__counter)

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
        pass 

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
            
        
