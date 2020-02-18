from multiprocessing import Process
import time
import random
from events import RequestEvent
from events import GraphUpdateEvent 
class EventProcess(Process):
    def __init__(self, queue, id, graph, engine, pickup_dist, dropoff_dist, timeLimit = 10800):
        super(EventProcess, self).__init__()
        # Time limit is 3 hr but make it a variable someplace
        # queue is a pipe now 
        self._comm = queue
        self._id = id
        self._graph = graph
        self._engine = engine
        self._pickup_dist = pickup_dist
        self._dropoff_dist = dropoff_dist
        self._timeLimit = timeLimit

    def run(self):
        day_of_the_week = self._engine.getDayOfTheWeek()
        update_event = GraphUpdateEvent(0, 7.5, 1) 
        self._comm.send(update_event)

        while self._engine.getSimulationTime() < self._timeLimit:
            found_ride = False
            while not found_ride:
                # TODO Replace 7 with variable from engine to indicate start of rush hr once code works
                current_hr = 7 + (self._engine.getSimulationTime() // 3600)
                origin_node = random.choices(population=self._graph.get_nodes(), k=1)
                destination_node = random.choices(population=self._graph.get_nodes(), k= 1)
                origin_node = origin_node[0]
                destination_node = destination_node[0]

                if origin_node != destination_node:
                    found_ride = True

            # 5 is a magic number for now. Once the code works, the timestep advancement will happen
            # based on scheduler logic and wait times and intra taz travel time.
            event = RequestEvent(origin_node=origin_node, destination_node=destination_node, ts=self._engine.getSimulationTime() + 5, current_ts=self._engine.getSimulationTime())
            event.event = self._id
            self._comm.send(event)
            time.sleep(0.1)
