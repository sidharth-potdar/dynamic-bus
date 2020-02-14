from .event import Event
from .pickup_event import PickupEvent
from .dropoff_event import DropoffEvent
from scheduler import Scheduler

class ScheduleEvent(Event):
    def __init__(self, ts, current_ts, ride_id, origin_node, destination_node, priority=1):
        super(ScheduleEvent, self).__init__(ts, current_ts)
        self.ride_id = ride_id
        self.origin_node = origin_node
        self.destination_node = destination_node

    def execute(self):
        '''
        Executes the pickup event
        '''
        print(f"Executing schedule event {self.ride_id} at {self.getExecutionPoint()} on bus {self.bus_id}")
        time_to_pickup, time_to_dropoff = Scheduler.assign_ride(self.ride_id, self.origin_node, self.destination_node)
        pickup_event = PickupEvent(ts=time_to_pickup, ride_id=self.ride_id, bus_id=self.bus_id, location=self.origin_node)
        dropoff_event = DropoffEvent(ts=time_to_dropoff, ride_id=self.ride_id, bus_id=self.bus_id, location=self.destination_node)

        # create new events for pickup and dropoff
        return pickup_event, dropoff_event
