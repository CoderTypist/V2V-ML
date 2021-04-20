import v2vml.calculations as calc
import v2vml.configuration as conf
from v2vml.node import Node


class Simulation:

    def __init__(self, num_initial_nodes):

        # current iteration of the simulation
        self.epoch = 0

        # number of nodes to create at the start of the simulation
        self.num_initial_nodes = num_initial_nodes

        # nodes present in the simulation
        self.nodes = []

        # hashmap of nodes present in the simulation
        self.hm_nodes = {}

        # a set of all neighbors within the simulation
        self.inner_neighbor_tuples = []
        self.outer_neighbor_tuples = []

        # keeps track of total node type counts over the lifetime of the simulation
        self.lifetime_good_nodes = 0
        self.lifetime_faulty_nodes = 0
        self.lifetime_malicious_nodes = 0

        # create initial nodes
        for x in range(num_initial_nodes):
            self.create_node()

    # advance to the next epoch in our simulation
    def next_epoch(self):

        self.epoch += 1
        self.move_nodes()
        self.set_neighbors()

    # adds a node to the simulation
    def create_node(self, on_canvas=True):
        n = Node(on_canvas=on_canvas)
        self.nodes.append(n)
        self.hm_nodes[n.id] = n

        if n.type == Node.GOOD:
            self.lifetime_good_nodes += 1
        elif n.type == Node.FAULTY:
            self.lifetime_faulty_nodes += 1
        else:
            self.lifetime_malicious_nodes += 1

    # removes a node from the simulation
    def remove_node(self, n):

        # close the out file
        if conf.MODE == conf.MODE_GATHER_DATA:
            n.out_file.close()

        del self.hm_nodes[n.id]
        self.nodes.remove(n)

    # moves nodes and adds new ones if necessary
    def move_nodes(self):
        for n in self.nodes:
            n.update()

            if n.is_out():
                self.remove_node(n)
                self.create_node(on_canvas=False)

    # nodes detect their neighbors
    def set_neighbors(self):

        # let all nodes know who their neighbors are
        for i in range(len(self.nodes)):

            n1 = self.nodes[i]
            n1.inner_neighbors = []
            n1.outer_neighbors = []

            for j in range(len(self.nodes)):

                # don't compare a car to itself
                if i == j:
                    continue

                n2 = self.nodes[j]

                if calc.is_in_inner_radius(n1.x, n1.y, n2.x, n2.y):
                    n1.inner_neighbors.append(n2.id)

                if calc.is_in_outer_radius(n1.x, n1.y, n2.x, n2.y):
                    n1.outer_neighbors.append(n2.id)

        # create a set (not list) of all neighbors
        self.inner_neighbor_tuples = []
        self.outer_neighbor_tuples = []

        for n in self.nodes:
            self.inner_neighbor_tuples.extend(n.get_inner_neighbor_tuples())
            self.outer_neighbor_tuples.extend(n.get_outer_neighbor_tuples())

        self.inner_neighbor_tuples = list(set(self.inner_neighbor_tuples))
        self.outer_neighbor_tuples = list(set(self.outer_neighbor_tuples))
        # print(self.neighbor_tuples)

    def close_node_files(self):
        for n in self.nodes:
            n.out_file.close()
