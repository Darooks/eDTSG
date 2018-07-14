from math import *
from eDTSGSimulation import DOMAIN_RANGE

ROAD_WIDTH = 1.6  # road width in sumo [m] - http://sumo.dlr.de/wiki/Simulation/SublaneModel

def get_distance(x1, y1, x2, y2):
    return sqrt(pow(x1 - x2, 2) +  pow(y1 - y2, 2))


def get_middle_if_domain(x, y, angle):
    x_ret = DOMAIN_RANGE/2 * cos(radians(angle)) + x
    y_ret = DOMAIN_RANGE/2 * sin(radians(angle)) + y
    return x_ret, y_ret

def get_point_by_angle_and_distance(x, y, angle, distance):
    x_ret = distance / 2 * cos(radians(angle)) + x
    y_ret = distance / 2 * sin(radians(angle)) + y
    return x_ret, y_ret
