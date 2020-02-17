from uuid import uuid4
import random
import time
import sys

from graph import Graph
from planners import GeneticAlgorithmPlanner

class Scheduler:
    num_buses = 2
    bus_capacity = 5
    start_nodes = []
    buses = {}
    ride_statuses = {}
    queue = None
    graph = None

    @classmethod
    def init(cls, graph, comm, num_buses=2, bus_capacity=5):
        '''
        Initialize the scheduler with given constraints
        '''
        cls.num_buses = num_buses
        cls.bus_capacity = bus_capacity
        start_nodes = random.choices(graph.get_nodes(), k=num_buses)
        # bus_rides dict maps from ride_ids to (origin, destination) tuple pairs
        cls.buses = { i : { "rides": {}, "route": [], "location": start_nodes[i] } for i in range(num_buses)}
        cls.ride_statuses = {}
        cls.comm = comm
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

        return nearest_bus, time_to_pickup, time_to_dropoff

    @classmethod
    def pass_events(cls, *events):
        '''
        Passes given event objects back to multiprocessing queue for engine to execute
        '''
        for e in events:
            cls.comm.send(e)

if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.init()
