from .event import Event
from .schedule_event import ScheduleEvent

import time

class RequestEvent(Event):
    def __init__(self, origin_node, destination_node, ts=None):
        super(RequestEvent, self).__init__(ts=ts)
        self.origin_node = origin_node
        self.destination_node = destination_node

    def execute(self):
        '''
        Executes the ride request event by calling the scheduler
        '''
        # print(f"Executing ride request event {self._id} at {self.getExecutionPoint()} from {self.origin_node} to {self.destination_node}")
        schedule_event = ScheduleEvent(ts=self.getExecutionPoint(), ride_id=self._id, origin_node=self.origin_node, destination_node=self.destination_node)

        return_dict = {
            "events": [schedule_event],
            "scheduler_calls": [
                {
                    "function": "request_ride",
                    "*args": (self._id,),
                    "**kwargs" : {
                        "uuid": self._id,
                        "type": type(self),
                        "time": self.getExecutionPoint()
                    }
                }
            ]
        }

        return return_dict
