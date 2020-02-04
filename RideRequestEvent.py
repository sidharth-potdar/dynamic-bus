from event import Event
from scheduler import Scheduler


class RideRequestEvent(Event):

    def __init__(self, rider, ts=None, *args, **kwargs):
        super().__init__()



    def execute(self):
        Scheduler.getInstance().register(self)
        print(self.rider)
