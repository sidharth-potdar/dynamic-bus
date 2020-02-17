from .planner import Planner

from random import random, randint, sample
import time

class GeneticAlgorithmPlanner(Planner):

    def __init__(self, graph, origin_node, destination_nodes):
        super(GeneticAlgorithmPlanner, self).__init__(graph, origin_node, destination_nodes)
        self.population_size = 100
        self.tourn_size = int(self.population_size / 10)
        self.num_generations = 20
        self.mutation_rate = 0.02

    def find_optimal_route(self):
        # set up genes for each destination node, generate starting population
        print("Number of nodes: ", len(self.destination_nodes))
        start_time = time.time()

        origin = Gene(self.origin_node, self.graph)
        genes = [Gene(node_id, self.graph) for node_id in self.destination_nodes]
        population = Population.gen_individuals(self.population_size, genes, origin)
        counter, generations, min_cost = 0, 0, float("inf")

        while counter < self.num_generations:
            population = evolve(population, self.tourn_size, self.mutation_rate)
            cost = population.get_fittest().travel_cost

            if cost < min_cost:
                counter, min_cost = 0, cost
            else:
                counter += 1

            generations += 1

        fittest = population.get_fittest()
        best_route = [node.id for node in fittest.genes]
        print("Time for GA: ", time.time()-start_time)
        print("Best route: ", best_route)
        print("GA route time: ", fittest.travel_cost)
        return fittest.travel_cost, best_route



class Gene: # Node
    distances_table = {}

    def __init__(self, id, graph):
        self.id = id
        self.graph = graph

    def get_distance_to(self, dest):
        key = (self.id, dest.id)

        try:
            return Gene.distances_table[key]
        except KeyError as e:
            distance, _ = self.graph.find_shortest_path(self.id, dest.id)
            Gene.distances_table[key] = distance

            return distance


class Individual:  # Route: possible solution to TSP
    def __init__(self, genes, origin):
        self.genes = genes
        self.origin = origin
        self.__reset_params()

    def swap(self, gene_1, gene_2):
        self.genes[0]
        a, b = self.genes.index(gene_1), self.genes.index(gene_2)
        self.genes[b], self.genes[a] = self.genes[a], self.genes[b]
        self.__reset_params()

    def add(self, gene):
        self.genes.append(gene)
        self.__reset_params()

    @property
    def fitness(self):
        if self.__fitness == 0:
            self.__fitness = 1 / self.travel_cost  # Normalize travel cost
        return self.__fitness

    @property
    def travel_cost(self):  # Get total travelling cost
        if self.__travel_cost == 0:
            origin = self.origin
            for i in range(len(self.genes)):
                dest = self.genes[i]

                self.__travel_cost += origin.get_distance_to(dest)
                origin = self.genes[i]

        return self.__travel_cost

    def __reset_params(self):
        self.__travel_cost = 0
        self.__fitness = 0


class Population:
    def __init__(self, individuals, origin):
        self.individuals = individuals
        self.origin = origin

    @staticmethod
    def gen_individuals(sz, genes, origin):
        individuals = []
        for _ in range(sz):
            individuals.append(Individual(sample(genes, len(genes)), origin))
        return Population(individuals, origin)

    def add(self, route):
        self.individuals.append(route)

    def rmv(self, route):
        self.individuals.remove(route)

    def get_fittest(self):
        fittest = self.individuals[0]
        for route in self.individuals:
            if route.fitness > fittest.fitness:
                fittest = route

        return fittest


def evolve(pop, tourn_size, mut_rate):
    new_generation = Population([], pop.origin)
    pop_size = len(pop.individuals)
    elitism_num = pop_size // 2

    # elitism
    for _ in range(elitism_num):
        fittest = pop.get_fittest()
        new_generation.add(fittest)
        pop.rmv(fittest)

    # crossover
    for _ in range(elitism_num, pop_size):
        parent_1 = selection(new_generation, tourn_size)
        parent_2 = selection(new_generation, tourn_size)
        child = crossover(parent_1, parent_2)
        new_generation.add(child)

    # mutation
    for i in range(elitism_num, pop_size):
        mutate(new_generation.individuals[i], mut_rate)

    return new_generation


def crossover(parent_1, parent_2):
    def fill_with_parent1_genes(child, parent, genes_n):
        start_at = randint(0, len(parent.genes)-genes_n-1)
        finish_at = start_at + genes_n
        for i in range(start_at, finish_at):
            child.genes[i] = parent_1.genes[i]

    def fill_with_parent2_genes(child, parent):
        j = 0
        for i in range(0, len(parent.genes)):
            if child.genes[i] == None:
                while parent.genes[j] in child.genes:
                    j += 1
                child.genes[i] = parent.genes[j]
                j += 1

    genes_n = len(parent_1.genes)
    child = Individual([None for _ in range(genes_n)], parent_1.origin)
    fill_with_parent1_genes(child, parent_1, genes_n // 2)
    fill_with_parent2_genes(child, parent_2)

    return child


def mutate(individual, rate):
    for _ in range(len(individual.genes)):
        if random() < rate:
            sel_genes = sample(individual.genes, 2)
            individual.swap(sel_genes[0], sel_genes[1])


def selection(population, competitors_n):
    return Population(sample(population.individuals, competitors_n), population.origin).get_fittest()
