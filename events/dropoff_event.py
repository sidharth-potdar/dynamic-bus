from .event import Event
from scheduler import Scheduler

class DropoffEvent(Event):
    def __init__(self, ts, ride_id, bus_id, location, priority=1):
        super(DropoffEvent, self).__init__(ts)
        self.ride_id = ride_id
        self.bus_id = bus_id
        self.location = location

    def execute(self):
        '''
        Executes the dropoff event
        '''
        print(f"Executing dropoff event {self.ride_id} at {self.getExecutionPoint()} on bus {self.bus_id}")
        Scheduler.ride_statuses[self.ride_id]["status"] = "completed"
        Scheduler.buses[self.bus_id] = {
            "rides": [],
            "route": [],
            "location": self.location
        }
