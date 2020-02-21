from .event import Event

class PickupEvent(Event):
    def __init__(self, ts, ride_id, bus_id, location, priority=1):
        super(PickupEvent, self).__init__(ts)
        self.ride_id = ride_id
        self.bus_id = bus_id
        self.location = location

        self.ts = ts
        self.priority = priority

    def execute(self):
        '''
        Executes the pickup event
        '''
        # print(f"Executing pickup event {self.ride_id} at {self.getExecutionPoint()} on bus {self.bus_id}")
        return_dict = {
            "scheduler_calls": [
                {
                    "function": "pickup_event", 
                    "*args": (self.ride_id, self.bus_id, self.location), 
                    "**kwargs": {}
                }
            ]
        }
        return return_dict

    def __repr__(self):
        return f"(0,{self.getId()},{self.ts},{self.location},{self.priority},{self.bus_id})"
