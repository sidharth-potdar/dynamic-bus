from event import Event
from scheduler import Scheduler

class DropOffEvent(Event):

    def __init__(self, rider, bus, ts=None, *args, **kwargs):
        super().__init__(ts, *args, **kwargs)
        self.bus = bus


    def execute(self):
        Scheduler.getInstance().register(self)
        self.bus.deleteRider()
        print(self.rider)
