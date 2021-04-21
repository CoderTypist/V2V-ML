import v2vml.configuration as conf
import v2vml.globals as g
import math


# checks to see if a point is off the canvas
def is_point_out(x, y) -> bool:
    if x < 0 or x > conf.CANVAS_WIDTH:
        return True
    elif y < 0 or y > conf.CANVAS_HEIGHT:
        return True
    return False


def distance(x1, y1, x2, y2):

    # This is the distance formula
    return math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))


def is_in_inner_radius(x1, y1, x2, y2) -> bool:

    # This is the distance formula
    dis = distance(x1, y1, x2, y2)

    if dis <= g.RADIUS_SENSOR:
        return True

    return False


def is_in_outer_radius(x1, y1, x2, y2) -> bool:

    # This is the distance formula
    dis = distance(x1, y1, x2, y2)

    if dis <= 2*g.RADIUS_SENSOR:
        return True

    return False
