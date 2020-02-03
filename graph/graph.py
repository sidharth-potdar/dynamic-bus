import random 
import itertools 
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
        cls._graph = dict(zip(nodes, edges))

    def get_nodes(cls): 
        return tuple(cls._graph.keys())
    



