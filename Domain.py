import eDTSGSimulation
import Utils
from math import *

def get_middle_if_domain(x, y, angle):
    x_ret = eDTSGSimulation.DOMAIN_RANGE * cos(radians(angle)) + x
    y_ret = eDTSGSimulation.DOMAIN_RANGE * sin(radians(angle)) + y
    return x_ret, y_ret

class Domain:
    def __init__(self,
                 vehicle_x,
                 vehicle_y,
                 angle,
                 lane):
        self.mid_x, self.mid_y = get_middle_if_domain(vehicle_x, vehicle_y, angle)
        self.angle = angle
        self.lane = lane
        self.range = eDTSGSimulation.DOMAIN_RANGE
