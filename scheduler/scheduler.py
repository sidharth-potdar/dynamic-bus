from uuid import uuid4
import random
import time
import sys

from scheduler.graph import Graph
from scheduler.graph import GraphUpdater
from events import PickupEvent, DropoffEvent 
from planners import GeneticAlgorithmPlanner
import threading 
import multiprocessing as mp 
from collections import deque 

from events import NumBusesEvent, BusCapacityEvent


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
    def init(cls, graph, num_buses=num_buses, bus_capacity=bus_capacity):
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
    def request_ride(cls, ride_id):
        '''
        Initializes ride status for requested ride
        '''
        cls.ride_statuses[ride_id] = {
            "status": "requested",
            "bus": None
        }

    @classmethod
    def assign_ride(cls, ride_id, origin_node, destination_node):
        '''
        Given a ride request, assign it to a bus according to scheduler's policy
        Return execution times for pickup and dropoff events
        '''
        # find nearest eligible buses
        nearest_bus = cls.find_nearest_bus(origin_node)

        #adhoc to stop crash, delete asap
        if nearest_bus is None:
            return

        if len(cls.buses[nearest_bus]["rides"]) == 0:
            # if no route planning needed
            total_time, route = cls.graph.find_shortest_path(origin_node, destination_node)
        else:
            # if more than one ride on bus -> plan route using chosen policy
            bus_origin_node = cls.buses[nearest_bus]["location"]
            ride_origin_nodes = [x[0] for ride_id, x in cls.buses[nearest_bus]["rides"].items()]
            ride_dest_nodes = [x[1] for ride_id, x in cls.buses[nearest_bus]["rides"].items()]

            planner = GeneticAlgorithmPlanner(cls.graph, bus_origin_node, ride_origin_nodes + ride_dest_nodes + [destination_node])
            total_time, route = planner.find_optimal_route()

        cls.buses[nearest_bus]["rides"][ride_id] = (origin_node, destination_node)
        cls.buses[nearest_bus]["route"] = route
        cls.ride_statuses[ride_id]["status"] = "scheduled"

        # random.shuffle(route)
        # planner = GeneticAlgorithmPlanner(cls.graph, origin_node, route[0:5])
        # t, r = planner.find_optimal_route()
        #
        # curr = origin_node
        # real_time = 0
        # for n in route[0:5]:
        #     real_time += cls.graph.find_shortest_path(curr, n)[0]
        #     curr = n
        # print("Route: ", route[0:5])
        # print("Randomized route time: ", real_time)
        # sys.exit()

        # calculate time and routes for bus to get to origin, and from origin to destination
        time_to_origin, start_route = cls.graph.find_shortest_path(cls.buses[nearest_bus]["location"], origin_node)
        time_to_destination, route = cls.graph.find_shortest_path(origin_node, destination_node)

        # update bus with new ride and route
        cls.buses[nearest_bus]["route"] = [x for x in start_route] + [y for y in route]

        cls.ride_statuses[ride_id]["status"] = "scheduled"

        time_to_pickup = time.time() + time_to_origin
        time_to_dropoff = time_to_pickup + time_to_destination

        pickup_event = PickupEvent(ts=time_to_pickup, ride_id=ride_id, bus_id=nearest_bus, location=origin_node)
        dropoff_event = DropoffEvent(ts=time_to_dropoff, ride_id=ride_id, bus_id=nearest_bus, location=destination_node)

        cls.pass_events(pickup_event, dropoff_event)

    @classmethod 
    def pickup_event(cls, ride_id, bus_id, location): 
        cls.ride_statuses[ride_id]["status"] = "picked up"
        cls.buses[bus_id]["location"] = location 

    @classmethod 
    def dropoff_event(cls, ride_id, bus_id, location): 
        cls.ride_statuses[ride_id]['status'] = 'completed'
        cls.buses[bus_id] = {
            "rides" : {}, 
            "route" : [],
            "location" : location
        }

    @classmethod
    def pass_events(cls, *events):
        '''
        Passes given event objects back to multiprocessing queue for engine to execute
        '''
        for e in events:
            cls.scheduler.send(e)

    @classmethod
    def graph_update(cls, requested_timestamp): 
        cls.scheduler.update(requested_timestamp)
if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.init()
    numbev = NumBusesEvent(0,scheduler.num_buses)
    capev = BusCapacityEvent(0, scheduler.bus_capacity)
    SchedulerCore.pass_events([numbev, capev])
