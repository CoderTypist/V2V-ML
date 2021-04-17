from tkinter import BooleanVar

# MODE
##########################################################
MODE_GATHER_DATA = 0
MODE_EXTRACT_FEATURES = 1
MODE_TEST_MODELS = 2
MODE_EXPORT_MODELS = 3
MODE_VISUALIZE = 4
MODE_PLOTS = 5
MODE = MODE_VISUALIZE

# MODE_GATHER_DATA
##########################################################
GATHER_DATA_NUM_EPOCHS = 1000

# MODE_TRAIN_MODELS
##########################################################
TRAIN_MODELS_NUM_TESTS = 100

# TKINTER
##########################################################

# screen size
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_DIM = '{}x{}'.format(SCREEN_WIDTH, SCREEN_HEIGHT)

# toolbar
TOOLBAR_NUM_LEVELS = 2
TOOLBAR_LEVEL_HEIGHT = 35

# canvas size
CANVAS_WIDTH = 1200
CANVAS_HEIGHT = SCREEN_HEIGHT - (TOOLBAR_NUM_LEVELS*TOOLBAR_LEVEL_HEIGHT)

# enable/disable features
SHOW_DEFAULT = True

# SIMULATION
##########################################################

# node allocation
NUM_INITIAL_NODES = 20

# simulation mode
SIM_AUTO = 0
SIM_MANUAL = 1
SIM_MODE = SIM_AUTO

# time to wait in SIM_AUTO
SIM_EPOCH_WAIT_TIME = 0.25

# NODE
##########################################################

# node distribution
PERCENT_GOOD = 60
PERCENT_FAULTY = 20
PERCENT_MALICIOUS = 20

MAX_COORD_HIST = 5
MAX_BSM_HIST = 6
