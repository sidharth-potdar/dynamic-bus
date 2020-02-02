from .event import Event
from scheduler import Scheduler

class RideRequestEvent(Event):
    def __init__(self):
        super(RideRequestEvent, self).__init__()

    def execute(self):
        '''
        Executes the ride request event by calling the scheduler
        '''
        pass
