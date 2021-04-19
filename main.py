import os
import pandas as pd
import sys
import tkinter as tk
import v2vml.configuration as conf
import v2vml.ml as ml
from v2vml.node import Node
import v2vml.plots as plots
from v2vml.simulation import Simulation
from v2vml.visualizer import Visualizer


def main():

    pd.options.display.max_columns = None
    pd.options.display.expand_frame_repr = False

    if conf.MODE == conf.MODE_GATHER_DATA:
        start_mode_gather_data()

    elif conf.MODE == conf.MODE_EXTRACT_FEATURES:
        start_mode_extract_features()

    elif conf.MODE == conf.MODE_TEST_MODELS:
        start_mode_test_models()

    elif conf.MODE == conf.MODE_EXPORT_MODELS:
        start_mode_export_models()

    elif conf.MODE == conf.MODE_VISUALIZE:
        start_mode_visualize()

    elif conf.MODE == conf.MODE_PLOTS:
        start_mode_plots()

    else:
        print('main.py: main(): invalid mode:', conf.MODE)
        sys.exit(-1)


def start_mode_gather_data():

    # clear the old data

    for i in os.listdir('./data/raw_data/good'):
        os.remove('./data/raw_data/good/' + i)

    for i in os.listdir('./data/raw_data/faulty'):
        os.remove('./data/raw_data/faulty/' + i)

    for i in os.listdir('./data/raw_data/malicious'):
        os.remove('./data/raw_data/malicious/' + i)

    # run the simulation for n epochs

    sim = Simulation(conf.NUM_INITIAL_NODES)

    for i in range(conf.GATHER_DATA_NUM_EPOCHS):

        if sim.epoch % 100 == 0:
            print('epoch {}...'.format(sim.epoch))

        sim.next_epoch()

    print('epoch', sim.epoch)
    sim.close_node_files()

    # brief summary
    with open('./data/raw_data/summary.txt', 'w') as summary:
        summary.write('Num epochs:' + str(conf.GATHER_DATA_NUM_EPOCHS) + '\n')
        summary.write('Num good:' + str(sim.lifetime_good_nodes) + '\n')
        summary.write('Num faulty:' + str(sim.lifetime_faulty_nodes) + '\n')
        summary.write('Num malicious:' + str(sim.lifetime_malicious_nodes) + '\n')


def start_mode_extract_features():

    # clear the features

    for i in os.listdir('./data/processed_data'):
        os.remove('./data/processed_data/' + i)

    # extract features

    for i in os.listdir('./data/raw_data/good'):
        ml.features_from_file(i, './data/raw_data/good/' + i, Node.GOOD)

    for i in os.listdir('./data/raw_data/faulty'):
        ml.features_from_file(i, './data/raw_data/faulty/' + i, Node.FAULTY)

    for i in os.listdir('./data/raw_data/malicious'):
        ml.features_from_file(i, './data/raw_data/malicious/' + i, Node.MALICIOUS)


def start_mode_test_models():
    ml.test_models()


def start_mode_export_models():
    ml.export_models('./data/models')


def start_mode_visualize():

    # create the screen
    root = tk.Tk()
    root.title('v2vml: Attack Detection')
    root.geometry(conf.SCREEN_DIM)

    # place the canvas on the screen
    canvas = tk.Canvas(root, width=conf.CANVAS_WIDTH, height=conf.CANVAS_HEIGHT, bg=Visualizer.COLOR_BACKGROUND)

    # create our simulation data
    sim = Simulation(conf.NUM_INITIAL_NODES)

    # has functions for drawing our simulation onto the canvas
    viz = Visualizer(root, canvas, sim)
    viz.start()


def start_mode_plots():
    plots.plots()


if __name__ == '__main__':
    main()
