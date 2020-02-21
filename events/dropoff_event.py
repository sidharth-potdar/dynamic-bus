from .event import Event

class DropoffEvent(Event):
    def __init__(self, ts, ride_id, bus_id, location):
        super(DropoffEvent, self).__init__(ts)
        self.ride_id = ride_id
        self.bus_id = bus_id
        self.location = location

    def execute(self):
        '''
        Executes the dropoff event
        '''
        # print(f"Executing dropoff event {self.ride_id} at {self.getExecutionPoint()} on bus {self.bus_id}")
        print(f"Dropoff event {self.getExecutionPoint()}")
        return_dict = {
            "scheduler_calls" : [
                {
                    "function": "dropoff_event",
                    "*args" : (self.ride_id, self.bus_id, self.location),
                    "**kwargs" : {
                        "uuid": self._id,
                        "type": type(self),
                        "time": self.getExecutionPoint()
                    }
                }
            ]
        }
        return return_dict
