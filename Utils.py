from math import *
import eDTSGSimulation

def get_distance(x1, y1, x2, y2):
    return sqrt(pow(x1 - x2, 2) +  pow(y1 - y2, 2))


def get_middle_if_domain(x, y, angle):
    x_ret = eDTSGSimulation.DOMAIN_RANGE/2 * cos(radians(angle)) + x
    y_ret = eDTSGSimulation.DOMAIN_RANGE/2 * sin(radians(angle)) + y
    return x_ret, y_ret
