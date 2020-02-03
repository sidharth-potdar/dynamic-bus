from event import Event
class ScheduleEvent(Event):

    def __init__(self, rider, bus, ts=None, *args, **kwargs):
        super().__init__()
        self.rider = rider
        self.bus = bus



    def execute(self):
        pass
