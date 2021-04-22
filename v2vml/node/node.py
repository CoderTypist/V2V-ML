import numpy as np
import random
from typing import List
import v2vml.calculations as calc
import v2vml.configuration as conf
import v2vml.globals as g


class Node:

    num_nodes = 0

    # node types
    GOOD = 0
    FAULTY = 1
    MALICIOUS = 2

    # node errors
    ERROR_GOOD = 15
    ERROR_FAULTY = 40
    ERROR_MALICIOUS = 100

    # keep detected faulty or malicious nodes in memory for n epochs
    # 10 epochs is 1 second
    # 100 epochs is 10 seconds
    # 1000 epochs is 100 seconds
    EPOCHS_KEEP = 1000

    ####################################################################

    def __init__(self, on_canvas=True):

        # unique node id
        self.id = Node.num_nodes
        Node.num_nodes += 1

        random.seed()
        self.dir = random.randint(1, 4)
        self.type = Node.random_node_type()

        self.out_file = None
        if conf.MODE == conf.MODE_GATHER_DATA:
            str_out_file = './data/raw_data/{}/Node_{}.csv'.format(self.type_as_str(), self.id)
            self.out_file = open(str_out_file, 'w')
            self.out_file.write('x,y,bsm_x,bsm_y\n')

        # nodes that are off the canvas are removed
        # however, newly spawned nodes start off of the canvas
        # this prevents newly spawned nodes from being removed
        self.has_appeared = None

        # if the node is being placed on the canvas
        if on_canvas:
            self.has_appeared = True
            self.x = random.randint(0, conf.CANVAS_WIDTH)
            self.y = random.randint(0, conf.CANVAS_HEIGHT)

        # if the node is being placed off the canvas
        # a node is placed off the canvas when another node went off the canvas
        else:
            self.has_appeared = False

            if g.NORTH == self.dir:
                self.x = random.randint(0, conf.CANVAS_WIDTH)
                self.y = conf.CANVAS_HEIGHT + g.RADIUS_SENSOR

            elif g.SOUTH == self.dir:
                self.x = random.randint(0, conf.CANVAS_WIDTH)
                self.y = 0 - g.RADIUS_SENSOR

            elif g.EAST == self.dir:
                self.x = 0 - g.RADIUS_SENSOR
                self.y = random.randint(0, conf.CANVAS_HEIGHT)

            else:
                self.x = conf.CANVAS_WIDTH + g.RADIUS_SENSOR
                self.y = random.randint(0, conf.CANVAS_HEIGHT)

        self.speed = random.randint(20, 70)

        # keep track of the nodes previous positions
        # ex: [ (oldest_x, oldest_y), ... , (recent_x, recent_y) ]
        self.past_coord: List[tuple] = []

        # keep track of the nodes previous positions as reported by BSMs
        # ex: [ (oldest_bsm_x, oldest_bsm_y), ... , (recent_bsm_x, recent_bsm_y) ]
        self.past_bsm_coord: List[tuple] = []

        # current neighbors
        self.inner_neighbors: List[int] = []
        self.outer_neighbors: List[int] = []

        # current susses (potentially faulty and malicious nodes)
        self.susses: List[Sus] = []

        # the last BSM emitted by this node
        self.last_bsm = None

    @classmethod
    def random_node_type(cls) -> int:

        ran = random.random() * 100

        if ran <= conf.PERCENT_GOOD:
            return Node.GOOD
        elif conf.PERCENT_GOOD < ran <= conf.PERCENT_GOOD + conf.PERCENT_FAULTY:
            return Node.FAULTY
        else:
            return Node.MALICIOUS

    def type_as_str(self) -> str:

        if self.type == Node.GOOD:
            return 'good'
        elif self.type == Node.FAULTY:
            return 'faulty'
        else:
            return 'malicious'

    # handles all of the updates a node needs to make when going into a new epoch
    def update(self):

        # manages location history (for the visualizer)
        self.update_hist()

        # moves the node
        self.update_position()

        # creates a new bsm and updates the bsm list
        self.update_bsm_hist()

        # writes current location and bsm location to file
        if conf.MODE == conf.MODE_GATHER_DATA:
            self.output_to_file()

    # updates the list containing the nodes previous (x,y) coordinates
    def update_hist(self):

        if len(self.past_coord) == conf.MAX_COORD_HIST:

            # remove the oldest recorded position
            self.past_coord = self.past_coord[1:]

        # add the current position to the end of the list
        self.past_coord.append((self.x, self.y))

    def update_bsm_hist(self):

        if len(self.past_bsm_coord) == conf.MAX_BSM_HIST:

            # remove the oldest recorded position
            self.past_bsm_coord = self.past_bsm_coord[1:]

        # add the current position to the end of the list
        self.last_bsm = self.new_bsm_coord()
        self.past_bsm_coord.append(self.last_bsm)

    # writes current location and the location specified in the bsm to a file
    def output_to_file(self):
        out_str = '{},{},{},{}\n'.format(self.x, self.y, self.last_bsm[0], self.last_bsm[1])
        self.out_file.write(out_str)

    # generates the point to broadcast in the BSM
    def new_bsm_coord(self) -> tuple:

        # PERFECT node's BSMs will contain the x and y's that are VERY similar to the actual x and y
        # GOOD node's BSMs will contain x and y's that are a little bit off
        # FAULTY node's BSMs will contain x and y's that are noticeably off
        # MALICIOUS node's BSMs will arbitrary x and y's

        # point to include in broadcasted bsm
        bsm_x = None
        bsm_y = None

        error_radius = None
        angle = random.randint(0, 359)

        if Node.GOOD == self.type:
            error_radius = random.randint(0, Node.ERROR_GOOD-1)

        elif Node.FAULTY == self.type:
            error_radius = random.randint(0, Node.ERROR_FAULTY-1)

        else:
            error_radius = random.randint(0, Node.ERROR_MALICIOUS-1)

        bsm_x = self.x + (error_radius*np.cos(angle))
        bsm_y = self.y + (error_radius*np.sin(angle))

        return bsm_x, bsm_y

    # adjusts the nodes x and y
    def update_position(self):

        if g.NORTH == self.dir:
            self.y -= self.speed

        elif g.SOUTH == self.dir:
            self.y += self.speed

        elif g.EAST == self.dir:
            self.x += self.speed

        else:
            self.x -= self.speed

    # returns True if the node is completely off the canvas, including the node history
    def is_out(self) -> bool:

        # do not remove nodes that just spawned off of the canvas
        if not self.has_appeared:

            # if the node is now on the canvas
            if not calc.is_point_out(self.x, self.y):
                self.has_appeared = True

            return False

        # the node should not be on the canvas
        if not calc.is_point_out(self.x, self.y):
            return False

        # all points in the history should be off the canvas
        for pc in self.past_coord:
            if not calc.is_point_out(pc[0], pc[1]):
                return False

        # print('node.py: is_out(): NODE WENT OUT!!!!!!')
        return True

    # returns the list of neighbors as a list of tuples
    def get_inner_neighbor_tuples(self) -> List[tuple]:

        t = []
        for i in self.inner_neighbors:
            if i < self.id:
                t.append((i, self.id))
            else:
                t.append((self.id, i))

        return t

    # returns the list of neighbors as a list of tuples
    def get_outer_neighbor_tuples(self) -> List[tuple]:

        t = []
        for i in self.outer_neighbors:
            if i < self.id:
                t.append((i, self.id))
            else:
                t.append((self.id, i))

        return t

    def __str__(self):

        s = 'id: ' + str(self.id) + '\n'

        if Node.GOOD == self.type:
            s += 'type: good\n'
        elif Node.FAULTY == self.type:
            s += 'type: faulty\n'
        elif Node.MALICIOUS == self.type:
            s += 'type: malicious\n'

        if g.NORTH == self.dir:
            s += 'dir: north\n'
        elif g.SOUTH == self.dir:
            s += 'dir: south\n'
        elif g.EAST == self.dir:
            s += 'dir: east\n'
        else:
            s += 'dir: west\n'

        s += 'speed: ' + str(self.speed) + '\n'
        s += 'num_inner_neighbors: ' + str(len(self.inner_neighbors)) + '\n'
        s += 'inner_neighbors: ' + str(self.inner_neighbors) + '\n'
        s += 'num_outer_neighbors: ' + str(len(self.outer_neighbors)) + '\n'
        s += 'outer_neighbors: ' + str(self.outer_neighbors) + '\n'
        # s += 'neighbor_tuples:' + str(self.get_neighbor_tuples()) + '\n'
        s += 'cur_coord: ' + str((self.x, self.y)) + '\n'
        s += 'past_coord: ' + str(self.past_coord) + '\n'
        s += 'past_bsm_coord: ' + str(self.past_bsm_coord) + '\n'

        return s
