import eDTSGSimulation
import Utils
from math import *


def get_middle_if_domain(x, y, angle):
    x_ret = eDTSGSimulation.DOMAIN_RANGE * cos(radians(angle)) + x
    y_ret = eDTSGSimulation.DOMAIN_RANGE * sin(radians(angle)) + y
    return x_ret, y_ret


class Domain:
    def __init__(self,
                 id,
                 mid_x,
                 mid_y,
                 angle,
                 lane,
                 start_time,
                 end_time):
        self.id = id
        self.mid_x, self.mid_y = mid_x, mid_y
        self.angle = angle
        self.lane = lane
        self.range = eDTSGSimulation.DOMAIN_RANGE
        self.start_time = start_time
        self.end_time = end_time
