from .event import Event

class ScheduleEvent(Event):
    def __init__(self, ts, ride_id, origin_node, destination_node):
        super(ScheduleEvent, self).__init__(ts)
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
                    "**kwargs" : {
                        "uuid": self._id,
                        "type": type(self),
                        "time": self.getExecutionPoint()
                    }

                }
            ]
        }
        return return_dict
