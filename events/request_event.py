from .event import Event
from .schedule_event import ScheduleEvent
from scheduler import Scheduler

import time

class RequestEvent(Event):
    def __init__(self, origin_node, destination_node, priority=1):
        super(RequestEvent, self).__init__(time.time())
        self.origin_node = origin_node
        self.destination_node = destination_node

    def execute(self):
        '''
        Executes the ride request event by calling the scheduler
        '''
        print(f"Executing ride request event {self._id} at {self.getExecutionPoint()} from {self.origin_node} to {self.destination_node}")
        Scheduler.request_ride(self._id)
        nearest_bus = Scheduler.find_nearest_bus(self.origin_node)
        if nearest_bus is not None:
            schedule_event = ScheduleEvent(ts=time.time(), ride_id=self._id, bus_id=nearest_bus, origin_node=self.origin_node, destination_node=self.destination_node)
            Scheduler.pass_events(schedule_event)
        else:
            # TODO: logic for passing event back to engine
            pass
