import threading 
import time 
from copy import deepcopy 
import math 
import numpy.random as random

class UpdateState: 
    init = False 
    def __init__(self): 
        if not UpdateState.init: 
            self.update_requested = False 
            self.time_requested = None 
            self.update_lock = threading.Lock()
            UpdateState.init = True  

    def request_update(self, time): 
        with self.update_lock: 
            self.update_requested = True 
            self.time_requested = time 
    def getRequestState(self): 
        return (self.update_requested, self.time_requested)
    def completeUpdate(self): 
        with self.getLock(): 
            self.update_requested = False 
            self.time_requested = None
    def getLock(self): 
        return self.update_lock
        
class GraphUpdater(threading.Thread): 
    def __init__(self, GraphObject, lock): 
        ''' params: 
            GraphObject: Object to update
            lock: Lock to grab before atomically updating.
        '''
        super().__init__(daemon=True)
        self.GraphObject = GraphObject
        self.update_state = UpdateState() 
        self.lock = lock 

    def request_update(self, time): 
        self.update_state.request_update(time) 

    def run(self): 
        while True: 
            if not self.update_state.getRequestState()[0]: 
                time.sleep(1) 
                continue 
            self.update_state.getLock().acquire() 
            _, time_req = self.update_state.getRequestState()
            local_copy = deepcopy(self.GraphObject._graph) 
            interpolate_req = False 
            interp_weight_1 = 1 
            interp_weight_2 = 0
            start = 0 
            end = 0
            requsted_time = time_req
            if requsted_time != int(requsted_time): 
                interpolate_req = True 
                start = math.floor(requsted_time)
                end = math.ceil(requsted_time)
                interp_weight_1 = requsted_time - start 
                interp_weight_2 = 1 - interp_weight_1
            for node in local_copy.keys(): 
                node_entry = local_copy[node] 
                edge_entry = node_entry[-1]
                new_edges = []
                edge_dist = None
                for neighbor, weight in edge_entry: 
                    # grab distribution 
                    if not interpolate_req: 
                        edge_dist = self.GraphObject._dist[(node, neighbor)][requsted_time]
                    else: 
                        edge_dist_1 = self.GraphObject._dist[(node, neighbor)][start]
                        edge_dist_2 = self.GraphObject._dist[(node, neighbor)][end] 
                        wa_mean = interp_weight_1 * edge_dist_1['mean'] + interp_weight_2 * edge_dist_2['mean']
                        wa_std  = math.sqrt((interp_weight_1 ** 2) * (edge_dist_1['stdev'] ** 2)  + (interp_weight_2**2)  * (edge_dist_2['stdev'] ** 2))
                        wa_gmean = interp_weight_1 * edge_dist_1['gmean'] + interp_weight_2 * edge_dist_2['gmean']
                        wa_gstdev = math.sqrt((interp_weight_1 ** 2) * (edge_dist_1['gstdev']**2) + (interp_weight_2 ** 2) * (edge_dist_2['gstdev'] ** 2))
                        edge_dist = {
                            "mean": wa_mean, 
                            "stdev": wa_std, 
                            "gmean": wa_gmean, 
                            "gstdev": wa_gstdev
                        }
                    # draw from distribution 
                    new_weight = random.normal(edge_dist['gmean'], edge_dist['gstdev']) 
                    new_edges.append((neighbor, new_weight))
                local_copy[node] = (node_entry[0], tuple(new_edges))
            with self.lock: 
                self.GraphObject._graph = local_copy
            self.update_state.getLock().release() 
            self.update_state.completeUpdate()
