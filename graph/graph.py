import random 
import math
import numpy.random as nrand
import heapq 
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
        # generate random locations 
        locations = nrand.rand(N, 2) 
        # zip location, edges
        node_addr = list(zip(map(tuple, locations), edges))
        cls._graph = dict(zip(nodes, node_addr))
  
    @classmethod
    def get_nodes(cls): 
        return tuple(cls._graph.keys())
    
    @classmethod
    def get_neighbors(cls, node): 
        return cls._graph[node][-1]
    
    @classmethod 
    def dist(cls, N1,N2):
        x1, y1 = cls._graph[N1][0] 
        x2, y2 = cls._graph[N2][0]
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    @classmethod 
    def compute_distance(cls, path): 
        d = 0 
        for i, node in enumerate(path): 
            if i + 1 == len(path): 
                break 
            next_node = path[i+1]
            for e in cls.get_neighbors(node): 
                if e[0] == next_node: 
                    d += e[1] 
                    break 
        return d 
    @classmethod
    def find_shortest_path(cls, start, end): 
        # we're doing to do a* for now 
        openset = [] 
        # save node, origin pairs 
        path = dict() 
        closedset = set()  
        # openset contains f-score = weight + heuristic  
        # closed set only contains node 
        # we can just re-add to heap when node is encountered again 
        # because min-heap, we will only infrequently encounter 
        # the case when we reencounter a node 
        # but we can check against closed set for that. 
        heapq.heappush(openset, (0, start, None))
        final_path = [] 
        found = False 
        # while openset evaluates to T as long as openset is not empty
        while openset and not found: 
            f, node, origin = heapq.heappop(openset)
            if node in closedset: 
                continue # we already encountered it 
            path[node] = origin
            # generate successors 
            edges = cls.get_neighbors(node) 
            # add to open set 
            for e in edges: 
                # don't go to nodes we hvae already visited
                if e[0] is end: 
                    found = True 
                    path[end] = node
                    break 
                if e[0] in closedset: 
                    continue 
                f_score = e[-1] + cls.dist(e[0], end) 
                heapq.heappush(openset, (f_score, e[0], node))
            closedset.add(node) 
        c = end 
        while c is not None: 
            final_path.append(c) 
            c = path[c]
        final_path = final_path[::-1]
        # compute distance 
        total_distance = cls.compute_distance(final_path)
        return (total_distance, final_path)


if __name__ == "__main__": 
    g = Graph() 
    g.init_random()
    dist, path = g.find_shortest_path(1, 10) 
    print(dist, path) 