import random 
import math
import numpy.random as nrand

import itertools 
def dist(N1,N2):
    x1, y1 = N1[0] 
    x2, y2 = N2[0]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


class Graph:
    _graph = None 
    @classmethod 
    def init_random(cls, N = 100, p = 0.1, max_weight = 100):
        ''' 
        Initialize a random graph with no planarity 
        ''' 
        nodes = tuple(range(100))
        weights = list((1 + i for i in range(max_weight)))
        edges = [] 
        ones = [1] * N 
        for i in range(N): 
            ones[i] = 0
            new_edges = tuple(random.choices(nodes, weights=ones, k=int(N*p)))
            ones[i] = 1 
            new_edge_weights = random.choices(weights, cum_weights= weights, k=int(N*p))
            new_dag_edges = tuple(zip(new_edges, new_edge_weights))
            edges.append(new_dag_edges)
        # generate random locations 
        locations = nrand.rand(N, 2) 
        # zip location, edges
        node_addr = list(zip(map(tuple, locations), edges))
        cls._graph = dict(zip(nodes, node_addr))

    def get_nodes(cls): 
        return tuple(cls._graph.keys())
    
    def get_neighbors(cls, node): 
        return cls._graph[node][-1]
    
    def fast_lookup(cls, start, end): 
        # we're doing to do a* for now 
        openset = set() 
        closedset = set() 
        current = start 
        openset.add(current) 
        # while openset evaluates to T as long as openset is not empty
        # while openset: 
            




