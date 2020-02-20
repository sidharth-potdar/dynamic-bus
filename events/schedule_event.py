from .event import Event
from .pickup_event import PickupEvent
from .dropoff_event import DropoffEvent

class ScheduleEvent(Event):
    def __init__(self, ts, current_ts, ride_id, origin_node, destination_node, priority=1):
        super(ScheduleEvent, self).__init__(ts, current_ts)
        self.ride_id = ride_id
        self.origin_node = origin_node
        self.destination_node = destination_node
        self.bus_id = None

    def execute(self):
        '''
        Executes the pickup event
        '''
        # print(f"Executing schedule event {self.ride_id} at {self.getExecutionPoint()}")
        # bus_id, time_to_pickup, time_to_dropoff = Scheduler.assign_ride(self.ride_id, self.origin_node, self.destination_node)
        
        return_dict = {
            "scheduler_calls": [
                {
                    "function": "assign_ride", 
                    "*args": (self.ride_id, self.origin_node, self.destination_node), 
                    "**kwargs": {}
                }
            ]
        }        
        return return_dict

    def __repr__(self):
        return f"(0,{self.getId()},0,{self.ts},{self.current_ts},{self.origin_node},{self.destination_node},{self.priority},{self.bus_id})"


