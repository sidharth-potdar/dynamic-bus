from .event import Event
from .schedule_event import ScheduleEvent
from scheduler import Scheduler

import time

class RequestEvent(Event):
    def __init__(self, origin_node, destination_node, ts=None, current_ts=None,priority=1):
        super(RequestEvent, self).__init__(ts=ts, current_ts=current_ts)
        self.ts = ts
        self.current_ts = current_ts
        self.origin_node = origin_node
        self.destination_node = destination_node

    def execute(self):
        '''
        Executes the ride request event by calling the scheduler
        '''
        print(f"Executing ride request event {self._id} at {self.getExecutionPoint()} from {self.origin_node} to {self.destination_node}")
        Scheduler.request_ride(self._id)
        schedule_event = ScheduleEvent(ts=self.ts + 5, current_ts=self.ts, ride_id=self._id, origin_node=self.origin_node, destination_node=self.destination_node)
        
        return [schedule_event]
