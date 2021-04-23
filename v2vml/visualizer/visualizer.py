import math
import time
import tkinter as tk
from tkinter import messagebox
import v2vml.configuration as conf
import v2vml.globals as g
from v2vml.node import Node

# in order to make a new checkbutton:
# - __init__(): bool for feature
# - __init__(): add bool for feature to list
# - __init__(): create checkbutton for feature
# - init_buttons: create the checkbutton
# - init_buttons(): set variable for the button
# - init_buttons(): set function to call when clicking the buttons
# - init_buttons(): add checkbutton to list of checkbuttons


class Visualizer:

    COLOR_BACKGROUND = '#dedddc'

    # node colors
    COLOR_NODE_GOOD = '#00a32e'
    COLOR_NODE_FAULTY = '#c98104'
    COLOR_NODE_MALICIOUS = '#7400b3'

    # sensor radius colors
    COLOR_OUTER_RADIUS = '#bbbfbd'
    COLOR_INNER_RADIUS = '#8e9490'

    # BSM colors
    COLOR_BSM_GOOD = '#54de7d'
    COLOR_BSM_FAULTY = '#e6ac49'
    COLOR_BSM_MALICIOUS = '#c27aeb'

    # line colors
    COLOR_LINE_NORMAL = '#36c4cf'

    def __init__(self, root, canvas, sim):
        self.root = root
        self.canvas = canvas
        self.sim = sim
        self.init_display = True

        # enable/disable features
        self.features = []

        self.auto = tk.BooleanVar(value=True)
        self.on_off = tk.BooleanVar(value=conf.SHOW_DEFAULT)
        self.show_node_type = tk.BooleanVar(value=conf.SHOW_DEFAULT)
        self.show_node_hist = tk.BooleanVar(value=conf.SHOW_DEFAULT)
        self.show_outer_radius = tk.BooleanVar(value=conf.SHOW_DEFAULT)
        self.show_inner_radius = tk.BooleanVar(value=conf.SHOW_DEFAULT)
        self.show_inner_connections = tk.BooleanVar(value=conf.SHOW_DEFAULT)
        self.show_outer_connections = tk.BooleanVar(value=conf.SHOW_DEFAULT)
        self.show_bsm_hist = tk.BooleanVar(value=conf.SHOW_DEFAULT)

        self.features.append(self.auto)
        self.features.append(self.on_off)
        self.features.append(self.show_node_type)
        self.features.append(self.show_node_hist)
        self.features.append(self.show_outer_radius)
        self.features.append(self.show_inner_radius)
        self.features.append(self.show_inner_connections)
        self.features.append(self.show_outer_connections)
        self.features.append(self.show_bsm_hist)

        # check buttons
        self.cb = []
        self.cb_auto = None
        self.cb_on_off = None
        self.cb_show_node_type = None
        self.cb_show_node_hist = None
        self.cb_show_outer_radius = None
        self.cb_show_inner_radius = None
        self.cb_show_inner_connections = None
        self.cb_show_outer_connections = None
        self.cb_show_bsm_hist = None
        self.cb_show_node_hist = None
        self.init_buttons()

        self.bind_mouse()

        # show the initial screen
        self.draw()

    # puts the simulation in motion
    def start(self):

        while self.auto.get():
            time.sleep(conf.SIM_EPOCH_WAIT_TIME)
            self.draw()
            self.root.update()

        self.root.mainloop()

    def bind_mouse(self):

        # pressing the left mouse button will cause the screen to update
        self.canvas.bind("<Button-1>", self.mouse_click)

        # pressing the right mouse button on a node will print information about it
        self.canvas.bind("<Button-3>", self.mouse_click)

    # called by main when the simulation is in SIM_MANUAL
    def mouse_click(self, event):

        # only process mouse events if not in auto mode
        if self.auto.get():
            return

        # right mouse button
        if event.num == 1:

            # advance to next epoch
            if 0 < event.x < conf.CANVAS_WIDTH and 0 < event.y < conf.CANVAS_HEIGHT:
                self.draw()
            # button pressed
            else:
                pass

        # left mouse button
        else:
            for n in self.sim.nodes:
                if n.x-g.RADIUS_NODE < event.x < n.x+g.RADIUS_NODE and n.y-g.RADIUS_NODE < event.y < n.y+g.RADIUS_NODE:
                    print(n)
                    messagebox.showinfo('Node {} Details'.format(n.id), str(n))

    # called by main when the simulation is in SIM_AUTO
    def draw(self, advance_epoch=True):

        # clear the canvas
        self.canvas.delete("all")

        # make changes for the next epoch
        if self.init_display:
            self.init_display = False
        else:
            if advance_epoch:
                self.sim.next_epoch()

        # solid color background
        self.canvas.create_rectangle(0, 0, conf.CANVAS_WIDTH, conf.CANVAS_HEIGHT, fill=Visualizer.COLOR_BACKGROUND)

        # draw to the canvas
        self.draw_nodes()

        # throw the stuff we drew onto the canvas
        self.canvas.pack()

        self.root.title('v2vml: Attack Detection - Epoch ' + str(self.sim.epoch))

    def draw_nodes(self):

        # inner connections
        if self.show_inner_connections.get():
            self.draw_inner_connections()

        # outer connections
        if self.show_outer_connections.get():
            self.draw_outer_connections()

        # node history
        if self.show_node_hist.get():
            self.draw_node_history()

        # sensors outer radius
        if self.show_outer_radius.get():
            self.draw_sensor_outer_radius()

        # sensors inner radius
        if self.show_inner_radius.get():
            self.draw_sensor_inner_radius()

        # the nodes themselves
        self.draw_node_center()

        # coord reported by BSMs
        if self.show_bsm_hist.get():
            self.draw_bsm_history()

    def draw_inner_connections(self):

        for nt in self.sim.inner_neighbor_tuples:
            self.canvas.create_line(self.sim.hm_nodes[nt[0]].x, self.sim.hm_nodes[nt[0]].y,
                                    self.sim.hm_nodes[nt[1]].x, self.sim.hm_nodes[nt[1]].y,
                                    fill=Visualizer.COLOR_LINE_NORMAL, width=4)

    def draw_outer_connections(self):

        for nt in self.sim.outer_neighbor_tuples:
            self.canvas.create_line(self.sim.hm_nodes[nt[0]].x, self.sim.hm_nodes[nt[0]].y,
                                    self.sim.hm_nodes[nt[1]].x, self.sim.hm_nodes[nt[1]].y,
                                    fill=Visualizer.COLOR_LINE_NORMAL, width=1)

    def draw_node_history(self):

        for n in self.sim.nodes:

            color = ''
            if not self.show_node_type.get():
                color = 'black'
            elif Node.GOOD == n.type:
                color = Visualizer.COLOR_NODE_GOOD
            elif Node.FAULTY == n.type:
                color = Visualizer.COLOR_NODE_FAULTY
            else:
                color = Visualizer.COLOR_NODE_MALICIOUS

            for i in range(len(n.past_coord)):

                if 0 == i:
                    pass
                else:

                    # coord
                    self.canvas.create_oval(n.past_coord[i][0]-g.RADIUS_PAST_COORD, n.past_coord[i][1]-g.RADIUS_PAST_COORD,
                                            n.past_coord[i][0]+g.RADIUS_PAST_COORD, n.past_coord[i][1]+g.RADIUS_PAST_COORD,
                                            fill=color, outline='')

                    # line
                    self.canvas.create_line(n.past_coord[i][0], n.past_coord[i][1],
                                            n.past_coord[i-1][0], n.past_coord[i-1][1],
                                            fill=color, width=2)
            # line
            if len(n.past_coord) > 0:
                self.canvas.create_line(n.x, n.y,
                                        n.past_coord[len(n.past_coord)-1][0], n.past_coord[len(n.past_coord)-1][1],
                                        fill=color, width=2)

    def draw_bsm_history(self):

        for n in self.sim.nodes:

            color = ''
            if not self.show_node_type.get():
                color = 'black'
            elif Node.GOOD == n.type:
                color = Visualizer.COLOR_BSM_GOOD
            elif Node.FAULTY == n.type:
                color = Visualizer.COLOR_BSM_FAULTY
            else:
                color = Visualizer.COLOR_BSM_MALICIOUS

            for i in range(len(n.past_bsm_coord)):

                if 0 == i:
                    pass
                else:

                    # coord
                    self.canvas.create_oval(n.past_bsm_coord[i][0] - g.RADIUS_BSM_COORD,
                                            n.past_bsm_coord[i][1] - g.RADIUS_BSM_COORD,
                                            n.past_bsm_coord[i][0] + g.RADIUS_BSM_COORD,
                                            n.past_bsm_coord[i][1] + g.RADIUS_BSM_COORD,
                                            fill=color, outline='')

                    # line
                    self.canvas.create_line(n.past_bsm_coord[i][0], n.past_bsm_coord[i][1],
                                            n.past_bsm_coord[i - 1][0], n.past_bsm_coord[i - 1][1],
                                            fill=color)

    def draw_sensor_outer_radius(self):
        # draw the sensor radius
        for n in self.sim.nodes:
            self.canvas.create_oval(n.x - g.RADIUS_SENSOR, n.y - g.RADIUS_SENSOR,
                                    n.x + g.RADIUS_SENSOR, n.y + g.RADIUS_SENSOR,
                                    fill='', outline=Visualizer.COLOR_OUTER_RADIUS)

    def draw_sensor_inner_radius(self):
        # draw the sensor radius
        for n in self.sim.nodes:
            self.canvas.create_oval(n.x - g.RADIUS_SENSOR//2, n.y - g.RADIUS_SENSOR//2,
                                    n.x + g.RADIUS_SENSOR//2, n.y + g.RADIUS_SENSOR//2,
                                    fill='', outline=Visualizer.COLOR_INNER_RADIUS)

    def draw_node_center(self):

        for n in self.sim.nodes:
            color = ''
            if not self.show_node_type.get():
                color = 'black'
            elif Node.GOOD == n.type:
                color = Visualizer.COLOR_NODE_GOOD
            elif Node.FAULTY == n.type:
                color = Visualizer.COLOR_NODE_FAULTY
            else:
                color = Visualizer.COLOR_NODE_MALICIOUS

            self.canvas.create_oval(n.x-g.RADIUS_NODE, n.y-g.RADIUS_NODE,
                                    n.x+g.RADIUS_NODE, n.y+g.RADIUS_NODE,
                                    fill=color, outline='')

    ################################################

    # These functions are called when clicking on the checkbuttons

    def draw_no_epoch(self):
        self.draw(advance_epoch=False)

    def toggle_on_off(self):

        # the first check button is the auto button
        # the second button is the on/off check button

        val = self.on_off.get()

        for f in self.cb[2::]:

            if val:
                f.select()
            else:
                f.deselect()

        self.draw_no_epoch()

    ################################################

    def init_buttons(self):

        # create check buttons
        self.cb_auto = tk.Checkbutton(self.root, text="Auto", variable=self.auto,
                                      indicatoron=True, onvalue=True, offvalue=False,
                                      command=self.start, width=8)

        self.cb_on_off = tk.Checkbutton(self.root, text="On/Off", variable=self.on_off,
                                        indicatoron=True, onvalue=True, offvalue=False,
                                        command=self.toggle_on_off, width=8)

        self.cb_show_node_type = tk.Checkbutton(self.root, text="Node Type", variable=self.show_node_type,
                                                indicatoron=True, onvalue=True, offvalue=False,
                                                command=self.draw_no_epoch, width=8)

        self.cb_show_node_hist = tk.Checkbutton(self.root, text="Node History", variable=self.show_node_hist,
                                                indicatoron=True, onvalue=True, offvalue=False,
                                                command=self.draw_no_epoch, width=8)

        self.cb_show_outer_radius = tk.Checkbutton(self.root, text="Outer Radius", variable=self.show_outer_radius,
                                                   indicatoron=True, onvalue=True, offvalue=False,
                                                   command=self.draw_no_epoch, width=8)

        self.cb_show_inner_radius = tk.Checkbutton(self.root, text="Inner Radius", variable=self.show_inner_radius,
                                                   indicatoron=True, onvalue=True, offvalue=False,
                                                   command=self.draw_no_epoch, width=8)

        self.cb_show_outer_connections = tk.Checkbutton(self.root, text="Outer Connect",
                                                        variable=self.show_outer_connections, indicatoron=True,
                                                        onvalue=True, offvalue=False,
                                                        command=self.draw_no_epoch, width=8)

        self.cb_show_inner_connections = tk.Checkbutton(self.root, text="Inner Connect",
                                                        variable=self.show_inner_connections, indicatoron=True,
                                                        onvalue=True, offvalue=False,
                                                        command=self.draw_no_epoch, width=8)

        self.cb_show_bsm_hist = tk.Checkbutton(self.root, text="BSM History", variable=self.show_bsm_hist,
                                               indicatoron=True, onvalue=True, offvalue=False,
                                               command=self.draw_no_epoch, width=8)

        # add check buttons to list
        self.cb.append(self.cb_auto)
        self.cb.append(self.cb_on_off)
        self.cb.append(self.cb_show_node_type)
        self.cb.append(self.cb_show_node_hist)
        self.cb.append(self.cb_show_outer_radius)
        self.cb.append(self.cb_show_inner_radius)
        self.cb.append(self.cb_show_outer_connections)
        self.cb.append(self.cb_show_inner_connections)
        self.cb.append(self.cb_show_bsm_hist)

        # place check buttons on the screen
        side_pad = 0
        top_pad = 5

        columns_per_row = math.ceil(len(self.cb)/conf.TOOLBAR_NUM_LEVELS)
        fair_share = conf.CANVAS_WIDTH // columns_per_row

        level = 0
        for i in range(len(self.cb)):

            if i != 0 and i % columns_per_row == 0:
                print(i)
                level += 1

            self.cb[i].place(x=(fair_share * (i % columns_per_row)) + side_pad,
                             y=conf.CANVAS_HEIGHT + conf.TOOLBAR_LEVEL_HEIGHT * level + top_pad,
                             width=fair_share - side_pad)
