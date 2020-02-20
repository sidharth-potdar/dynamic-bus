from .event import Event

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
        # print(f"Executing pickup event {self.ride_id} at {self.getExecutionPoint()} on bus {self.bus_id}")
        return_dict = {
            "scheduler_calls": [
                {
                    "function": "pickup_event", 
                    "*args": (self.ride_id, self.bus_id, self.location), 
                    "**kwargs" : {
                        "uuid": self._id, 
                        "type": type(self)
                    }

                }
            ]
        }
        return return_dict
