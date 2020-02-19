from .planner import Planner

from random import random, randint, sample
import time

class GeneticAlgorithmPlanner(Planner):

    def __init__(self, graph, bus_node, node_pairs):
        super(GeneticAlgorithmPlanner, self).__init__(graph, bus_node, node_pairs)
        self.population_size = 100
        self.tourn_size = int(self.population_size / 10)
        self.num_generations = 20
        self.mutation_rate = 0.02

    def find_optimal_route(self):
        # set up genes for each destination node, generate starting population
        start_time = time.time()

        print("Bus node: ",self.bus_node)
        bus_gene = Gene(self.bus_node, self.graph)

        origin_genes = []
        dest_genes = []
        print("Pairs:")
        for pair in self.node_pairs:
            print(pair)

            # create a gene for each node in the (origin, destination) pair
            origin_gene = Gene(id=pair[0], graph=self.graph, origin=None, dest=None)
            dest_gene = Gene(id=pair[1], graph=self.graph, origin=None, dest=None)
            origin_gene.dest = dest_gene
            dest_gene.origin = origin_gene

            origin_genes.append(origin_gene)
            dest_genes.append(dest_gene)

        population = Population.gen_individuals(self.population_size, bus_gene, origin_genes, dest_genes)
        counter, generations, min_cost = 0, 0, float("inf")
        best_pop = None

        while counter < self.num_generations:
            population = evolve(population, self.tourn_size, self.mutation_rate)
            cost = population.get_fittest().travel_cost

            if cost < min_cost:
                counter, min_cost = 0, cost
                route = [node.id for node in population.get_fittest().genes]
                print("New best route: ", route, cost)
                best_fittest = Individual(population.get_fittest().genes, bus_gene)
            else:
                counter += 1

            print(cost, best_fittest.travel_cost)

            generations += 1

        print()
        print("FITTEST: ", best_fittest.travel_cost)
        best_route = [node.id for node in best_fittest.genes]
        print("Time for GA: ", time.time()-start_time)
        print("Best route: ", best_route)
        print("GA route time: ", best_fittest.travel_cost)

        total_distance = 0
        calc_distance = 0
        curr = self.bus_node
        for node in best_route:
            total_distance += self.graph.find_shortest_path(curr, node)[0]
            curr = node
        curr = bus_gene
        for g in best_fittest.genes:
            calc_distance += curr.get_distance_to(g)
            curr = g

        print("TOTAL DIST: ", total_distance, calc_distance)

        return best_fittest.travel_cost, best_route



class Gene: # Node
    distances_table = {}

    def __init__(self, id, graph, origin=None, dest=None):
        self.id = id
        self.graph = graph
        self.origin = origin
        self.dest = dest

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if other == None:
            return False
        return self.id == other.id

    def get_distance_to(self, dest):
        key = (self.id, dest.id)

        try:
            return Gene.distances_table[key]
        except KeyError as e:
            distance, _ = self.graph.find_shortest_path(self.id, dest.id)
            Gene.distances_table[key] = distance

        # distance, _ = self.graph.find_shortest_path(self.id, dest.id)
        return distance


class Individual:  # Route: possible solution to TSP
    def __init__(self, genes, origin):
        self.genes = genes
        self.origin = origin
        self.__reset_params()

    def swap(self, gene_1, gene_2):
        temp = [x for x in self.genes]
        a, b = temp.index(gene_1), temp.index(gene_2)
        temp[b], temp[a] = temp[a], temp[b]
        if validate(temp):
            self.genes = temp
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
            visited_origins = set()

            for i in range(len(self.genes)):
                dest = self.genes[i]

                if dest.origin != None and dest.origin not in visited_origins:
                    return float("inf")

                if dest.origin == None:
                    visited_origins.add(dest)

                self.__travel_cost += origin.get_distance_to(dest)
                origin = self.genes[i]

        return self.__travel_cost

    def __reset_params(self):
        self.__travel_cost = 0
        self.__fitness = 0


class Population:
    def __init__(self, bus_gene, individuals):
        self.bus_gene = bus_gene
        self.individuals = individuals

    @staticmethod
    def gen_individuals(sz, bus_gene, origin_genes, dest_genes):
        individuals = []
        for _ in range(sz-1):
            individuals.append(Individual(sample(origin_genes, len(origin_genes)) + sample(dest_genes, len(dest_genes)), bus_gene))
        individuals.append(Individual(origin_genes+dest_genes, bus_gene))
        return Population(bus_gene, individuals)

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

def validate(solution):
    visited_origins = set()

    for i in range(len(solution)):
        curr = solution[i]

        if curr.origin != None and curr.origin not in visited_origins:
            # print([g.id for g in solution.genes])
            # print("Illegal solution")
            return False

        visited_origins.add(curr)

    return  True

def evolve(pop, tourn_size, mut_rate):
    new_generation = Population(pop.bus_gene, [])
    pop_size = len(pop.individuals)
    elitism_num = pop_size // 2

    # elitism
    for _ in range(elitism_num):
        fittest = pop.get_fittest()
        new_generation.add(fittest)
        # pop.rmv(fittest)

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
                while j < len(parent.genes) and parent.genes[j] in child.genes:
                    j += 1
                child.genes[i] = parent.genes[j]
                j += 1

    # positions = random.sample(parent_1.genes)

    genes_n = len(parent_1.genes)
    child = Individual([None for _ in range(genes_n)], parent_1.origin)
    fill_with_parent1_genes(child, parent_1, genes_n // 2)
    fill_with_parent2_genes(child, parent_2)

    try:
        validate(child)
        return child
    except:
        # print("Illegal crossover")
        return parent_1


def mutate(individual, rate):
    for _ in range(len(individual.genes)):
        if random() < rate:
            gene1, gene2 = sample(individual.genes, 2)
            individual.swap(gene1, gene2)


def selection(population, competitors_n):
    return Population(population.bus_gene, sample(population.individuals, competitors_n)).get_fittest()
