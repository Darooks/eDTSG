import eDTSGSimulation
from Utils import in_domain, DOMAIN_RANGE
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
        self.vehicle_density = 0

    def update_domain(self, vehicles):
        # Updating vehicle density
        vehicle_counter = 0
        for vehicle in vehicles:
            if in_domain(vehicle, self) is True:
                vehicle_counter += 1

        self.vehicle_density = vehicle_counter / (DOMAIN_RANGE / 1000)  # vehicle density per 1km
