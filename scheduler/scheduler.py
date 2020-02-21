from uuid import uuid4
import random
import time
import sys

from scheduler.graph import Graph
from scheduler.graph import GraphUpdater
from events import PickupEvent, DropoffEvent, EndScheduleEvent, InvalidateEvent
from planners import GeneticAlgorithmPlanner
import threading
import multiprocessing as mp
from collections import deque


class Scheduler(mp.Process):
    def __init__(self, pipe_recv_from_engine = None, pipe_send_to_engine = None, graph=None, **kwargs):
        super().__init__()
        # Initiate Pipes
        self.to_engine = pipe_send_to_engine
        self.from_engine = pipe_recv_from_engine
        # Initialize Communication and Core
        self.comm = SchedulerComm(self, daemon=True)
        self.core = SchedulerCore(self)
        SchedulerCore.init(graph)

        # Setup Graph
        self.graph = graph
        ## Setup Graph Lock
        self._graph_lock = threading.Lock()
        self.graph.init_multicore(self._graph_lock)
        ## setup updater
        self._graph_updater = GraphUpdater(self.graph, self._graph_lock)

        # Start Threads

        self.execution_queue = deque()

    def send(self, msg):
        self.comm.send(msg)

    def execute(self, msg):
        self.core.execute(msg)

    def run(self):
        self.comm.start()
        self.core.start()
        self._graph_updater.start()
        self.core.join()

    def update(self, timestamp):
        self._graph_updater.request_update(timestamp)

    def getEngineRecvComm(self):
        return self.from_engine
    def getEngineSendComm(self):
        return self.to_engine

class SchedulerComm(threading.Thread):
    MAX_LOOP_SENDS = 10
    def __init__(self, scheduler, daemon=None):
        super().__init__(daemon=daemon, name="SchedulerComm")
        self.scheduler = scheduler
        self.engine_recv_comm = self.scheduler.getEngineRecvComm()
        self.engine_send_comm = self.scheduler.getEngineSendComm()
        self.send_buffer = deque()

    def format_msg(self, msg):
        return msg["function"] + "(" + ", ".join(map(str, msg['*args'])) + ")"

    def run(self):
        while True:
            if self.engine_recv_comm.poll():
                # add to execution queue
                msg = self.engine_recv_comm.recv();
                self.scheduler.execute(msg)
            if len(self.send_buffer) > 0:
                i = 0
                while len(self.send_buffer) > 0 and i < SchedulerComm.MAX_LOOP_SENDS:
                    self.engine_send_comm.send(self.send_buffer.popleft())
                    i += 1
    def send(self, msg):
        self.send_buffer.append(msg)

class SchedulerCore(threading.Thread):
    num_buses = 2
    bus_capacity = 5
    start_nodes = []
    buses = {}
    ride_statuses = {}
    queue = None
    graph = None
    scheduler = None
    def __init__(self, scheduler):
        super().__init__(name="SchedulerCore")
        self.execution_queue = deque()
        self._scheduler = scheduler
        SchedulerCore.scheduler = self._scheduler

    def execute(self, msg):
        self.execution_queue.append(msg)

    def run(self):
        while True:
            if len(self.execution_queue) > 0:
                msg = self.execution_queue.popleft()
                getattr(SchedulerCore, msg['function'])(*msg['*args'], **msg['**kwargs'])

    @classmethod
    def init(cls, graph, num_buses=100, bus_capacity=4):
        '''
        Initialize the scheduler with given constraints
        '''
        cls.num_buses = num_buses
        cls.bus_capacity = bus_capacity
        start_nodes = random.choices(graph.get_nodes(), k=num_buses)
        # bus_rides dict maps from ride_ids to (origin, destination) tuple pairs
        cls.buses = { i : { "rides": {}, "route": [], "location": start_nodes[i] } for i in range(num_buses)}
        cls.ride_statuses = {}
        cls.graph = graph

    @classmethod
    def find_nearest_bus(cls, request_node):
        '''
        Find nearest bus with capacity to request node id
        '''
        bus_locations = { bus_data["location"] : bus_id for bus_id, bus_data in cls.buses.items() if len(bus_data["rides"]) < cls.bus_capacity}

        # check if there's already a bus in the same area
        if request_node in bus_locations:
            return bus_locations[request_node]

        # otherwise, find the closest bus (greedy policy)
        min_distance = float("inf")
        min_bus = None
        for node_id, bus_id in bus_locations.items():
            distance, _ = cls.graph.find_shortest_path(node_id, request_node)
            if distance < min_distance:
                min_distance = distance
                min_bus = bus_id

        return min_bus

    @classmethod
    def request_ride(cls, ride_id, **kwargs):
        '''
        Initializes ride status for requested ride
        '''
        cls.ride_statuses[ride_id] = {
            "status": "requested",
            "bus": None,
            "origin": None,
            "destination": None,
            "schedule_time": None,
            "schedule_event_id": None,
            "pickup_time": None,
            "pickup_event_id": None,
            "dropoff_time": None,
            "dropoff_event_id": None,
        }

    @classmethod
    def assign_ride(cls, ride_id, origin_node, destination_node, **kwargs):
        '''
        Given a ride request, assign it to a bus according to scheduler's policy
        Return execution times for pickup and dropoff events
        '''
        # find nearest eligible buses
        nearest_bus = cls.find_nearest_bus(origin_node)
        current_ts = kwargs["time"]

        if nearest_bus is None:
            # TODO: implement logic for no available bus
            print("Out of buses! Please implement solution")
            return

        bus_node = cls.buses[nearest_bus]["location"]

        if len(cls.buses[nearest_bus]["rides"]) == 0:
            # if no route planning needed
            pickup_time, pickup_route = cls.graph.find_shortest_path(bus_node, origin_node)
            dropoff_time, dropoff_route = cls.graph.find_shortest_path(origin_node, destination_node)
            pickup_time /= 3600
            dropoff_time /= 3600
            if dropoff_time < 0:
                print(f"Negative dropoff time in empty bus: {dropoff_time}")
            travel_times = { (origin_node, destination_node) : (pickup_time, dropoff_time) }
            route = pickup_route + dropoff_route
        else:
            # if more than one ride on bus -> plan route using chosen policy
            node_pairs = [(pair[0], pair[1]) for pair in cls.buses[nearest_bus]["rides"].values()]
            node_pairs.append((origin_node, destination_node))

            planner = GeneticAlgorithmPlanner(cls.graph, bus_node, node_pairs)
            total_time, route, travel_times = planner.find_optimal_route()

        # invalidate any yet to be executed events on the ride
        ride_ids = cls.buses[nearest_bus]["rides"].keys()
        for r_id in ride_ids:
            schedule_event_id = cls.ride_statuses[r_id]["schedule_event_id"]
            pickup_event_id = cls.ride_statuses[r_id]["pickup_event_id"]
            dropoff_event_id = cls.ride_statuses[r_id]["dropoff_event_id"]
            future_event_ids = [schedule_event_id, pickup_event_id, dropoff_event_id]
            invalidate_event = InvalidateEvent(*[fid for fid in future_event_ids if fid != None])
            cls.pass_events(invalidate_event)

        # update bus and ride status
        cls.buses[nearest_bus]["rides"][ride_id] = (origin_node, destination_node)
        cls.buses[nearest_bus]["route"] = route
        cls.ride_statuses[ride_id]["status"] = "scheduled"
        cls.ride_statuses[ride_id]["bus"] = nearest_bus
        cls.ride_statuses[ride_id]["schedule_time"] = current_ts
        cls.ride_statuses[ride_id]["origin"] = origin_node
        cls.ride_statuses[ride_id]["destination"] = destination_node

        # generate pickup and dropoff events
        events = []
        for (origin, dest), (pickup, dropoff) in travel_times.items():
            pickup_time = current_ts + pickup
            dropoff_time = current_ts + dropoff
            # print("Times: ", current_ts, pickup_time, dropoff_time)
            pickup_event = PickupEvent(ride_id=ride_id, bus_id=nearest_bus, location=origin, ts=pickup_time)
            dropoff_event = DropoffEvent(ride_id=ride_id, bus_id=nearest_bus, location=dest, ts=dropoff_time)
            # print(f"Pickup time: {pickup_event.getExecutionPoint()}, Dropoff time: {dropoff_event.getExecutionPoint()}")

            cls.pass_events(pickup_event, dropoff_event, EndScheduleEvent())

    @classmethod
    def pickup_event(cls, ride_id, bus_id, location, **kwargs):
        cls.ride_statuses[ride_id]["status"] = "picked up"
        cls.ride_statuses[ride_id]["pickup_time"] = kwargs["time"]
        cls.buses[bus_id]["location"] = location

        print(f"Bus {bus_id} picked up {ride_id} at {kwargs['time']}")

    @classmethod
    def dropoff_event(cls, ride_id, bus_id, location, **kwargs):
        cls.ride_statuses[ride_id]["status"] = "completed"
        cls.ride_statuses[ride_id]["dropoff_time"] = kwargs["time"]
        cls.buses[bus_id]["location"] = location
        try:
            del cls.buses[bus_id]["rides"][ride_id]
        except KeyError:
            print(f"Ride id {ride_id} not found on bus {bus_id}")
        pickup_time = cls.ride_statuses[ride_id]["schedule_time"]
        origin = cls.ride_statuses[ride_id]["origin"]
        dest = cls.ride_statuses[ride_id]["destination"]
        # print("Schedule: ", schedule_time)
        # print("Dropoff: ", kwargs["time"])
        # print(f"Real pickup time: {pickup_time}, Real dropoff time: {kwargs['time']}")
        # print(f"Total time for ride {ride_id}: {kwargs['time']-pickup_time}, with expected time: {cls.graph.find_shortest_path(origin, dest)[0]/3600}")
        print(f"Bus {bus_id} dropped off {ride_id} at {kwargs['time']}")

    @classmethod
    def pass_events(cls, *events):
        '''
        Passes given event objects back to multiprocessing queue for engine to execute
        '''
        for e in events:
            cls.scheduler.send(e)

    @classmethod
    def graph_update(cls, requested_timestamp, **kwargs):
        cls.scheduler.update(requested_timestamp)
if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.init()
