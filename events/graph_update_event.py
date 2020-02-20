from .event import Event 

class GraphUpdateEvent(Event):
    def __init__(self, ts, simulation_time, priority=1):
        super(GraphUpdateEvent, self).__init__(ts)
        self.simulation_time = simulation_time
    def execute(self):
        '''
        Executes the pickup event
        '''
        print(self.isValid())
        # print(f"Executing pickup event {self.ride_id} at {self.getExecutionPoint()} on bus {self.bus_id}")
        return_dict = {
            "scheduler_calls": [
                {
                    "function": "graph_update", 
                    "*args": (self.simulation_time,), 
                    "**kwargs" : {
                        "uuid": self._id, 
                        "type": type(self), 
                        "time": self.getExecutionPoint()
                    }

                }
            ]
        }
        return return_dict
