import sys

# directions
NORTH = 1
SOUTH = 2
EAST = 3
WEST = 4

# drawing constants
RADIUS_NODE = 10
RADIUS_SENSOR = 210
RADIUS_PAST_COORD = 4
RADIUS_BSM_COORD = 2

SAMPLE_SIZE = 3

if SAMPLE_SIZE < 3:
    print('globals.py: SAMPLE_SIZE must be greater than 2')
    sys.exit(-1)
