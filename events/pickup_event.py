from .event import Event
from scheduler.scheduler import Scheduler

class PickupEvent(Event):
    def __init__(self, ts, ride_id, bus_id, location, priority=1):
        super(PickupEvent, self).__init__(ts)
        self.ride_id = ride_id
        self.bus_id = bus_id
        self.location = location

    def execute(self):
        '''
        Executes the pickup event
        '''
        print(f"Executing pickup event {self.ride_id} at {self.getExecutionPoint()} on bus {self.bus_id}")
        Scheduler.ride_statuses[self.ride_id]["status"] = "picked up"
        Scheduler.buses[self.bus_id]["location"] = self.location
