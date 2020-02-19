from graph import Graph
from planners import GeneticAlgorithmPlanner
from random import random, sample, choice

if __name__ == "__main__":

    g = Graph()
    g.init_file("pickles/graph.pypkle")

    nodes = g.get_nodes()
    bus_node = choice(nodes)
    o = [x[0] for x in g.get_neighbors(bus_node)[0:3]]
    d = [x[0] for x in g.get_neighbors(choice(nodes))[0:3]]
    # o = sample(nodes, 4)
    # d = sample(nodes, 4)
    pairs = [x for x in zip(o, d)]

    planner = GeneticAlgorithmPlanner(g, bus_node, pairs)
    ga_dist, ga_route = planner.find_optimal_route()

    print()

    nodes = o + d
    total_distance = 0
    curr = bus_node
    for n in nodes:
        total_distance += g.find_shortest_path(curr, n)[0]

    print("Unoptimized time: ", total_distance)
    print("Unoptimized route: ", nodes)
