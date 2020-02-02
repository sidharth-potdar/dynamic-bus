from uuid import uuid4
import random

class Scheduler:

    def __init__(self, graph, num_buses=5, bus_capacity=4):
        self.graph = graph
        self.bus_capacity = bus_capacity
        start_nodes = random.choices(graph.get_nodes(), num_buses)
        self.buses = { uuid4() : { "rides": [], "route": [], "location": start_nodes[i] } for i in range(num_buses)}
        self.ride_statuses = {}

    def register(self, *events):
        '''
        Given a variable number of ride request events, handle them according to current state
        '''
        for event in events:
            self.assign_ride((event.id, event.origin_node, event.destination_node, event.priority))

    def find_nearest_bus(self, request_node):
        '''
        Find nearest bus with capacity to request node id
        '''
        bus_locations = { bus_data["location"] : bus_id if len(bus_data["rides"]) < bus_capacity for bus_id, bus_data in buses.items()}

        # check if there's already a bus in the same area
        if request_node in bus_locations:
            return bus_locations[request_node]

        # otherwise, find the closest bus (greedy policy)
        min_distance = float("inf")
        min_bus = None
        for node_id, bus_id in bus_locations.items():
            distance, _ = graph.find_shortest_path(node_id, request_node)
            if distance < min_distance:
                min_distance = distance
                min_bus = bus_id

        return bus_id


    def assign_ride(self, ride_request):
        '''
        Given a ride request (ride_id, origin_node_id, destination_node_id, priority), assign it to a bus according to scheduler's policy
        '''
        ride_id, origin_node, destination_node, priority = ride_request
        nearest_bus = self.find_nearest_bus(request_node)

        # if there is an available bus, add new ride to bus route and load
        if nearest_bus is not None:
            new_ride = {
                "ride_id": ride_id,
                "origin_node": origin_node,
                "destination_node": destination_node,
                "priority": priority
            }
            self.buses[nearest_bus].rides.append(new_ride)
            # TODO: add logic to handle route changes
        else:
            pass
            # TODO: add logic to send ride request event back to engine

        return nearest_bus
