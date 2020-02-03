import random 
import math
import numpy.random as nrand
import heapq 
import itertools 

class Graph:
    _graph = None 
    @classmethod 
    def init_random(cls, N = 100, p = 0.02, max_weight = 100):
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

        # verify every node is reachable. 
        checked_set = set() 
        all_nodes = set(cls._graph.keys())
        for key, value in cls._graph.items(): 
            for edge in value[-1]: 
                checked_set.add(edge[0]) # add all visited nodes to the checked_set 
        difference_set = all_nodes.difference(checked_set)
        if len(difference_set) != 0: 
            for node in difference_set: 
                next_node = (node + 1) % N 
                entry = cls._graph[next_node]
                edge_list = list(entry[-1])
                edge_list.append((node, 1))
                new_entry = [entry[0], edge_list]
                cls._graph[next_node] = new_entry 
  
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
            if node is end: 
                found = True 
                break 
            # generate successors 
            edges = cls.get_neighbors(node) 
            # add to open set 
            for e in edges: 
                # don't go to nodes we hvae already visited
                if e[0] in closedset: 
                    continue 
                f_score = e[-1] + cls.dist(e[0], end) 
                heapq.heappush(openset, (f_score, e[0], node))
            closedset.add(node) 
        c = end 
        if found == False: 
            return (-1, None)
        while c is not None: 
            final_path.append(c) 
            c = path[c]
        final_path = final_path[::-1]
        # compute distance 
        total_distance = cls.compute_distance(final_path)
        return (total_distance, final_path)


if __name__ == "__main__": 
    import sys
    import pickle 
    g = Graph() 
    g.init_random()
    # verify good graph 
    nodes = g.get_nodes() 
    dumped = False 
    random_int = random.randint(0, 10000000)
    for i in range(len(nodes)): 
        for j in range(len(nodes)): 
            if i != j: 
                n1 = nodes[i]
                n2 = nodes[j]
                try: 
                    dist, path = g.find_shortest_path(n1, n2) 
                    print(n1, n2, dist, path) 
                except:
                    print(n1, n2, random_int, file=sys.stderr)
                    if not dumped: 
                        with open("graph_" + str(random_int) + ".pickle", 'wb') as f: 
                            pickle.dump(g._graph, f)
                        dumped = True 
                    raise 
