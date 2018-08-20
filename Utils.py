from math import *
from enum import Enum

COMMUNICATION_RANGE = 250  # range of communication [m]
DOMAIN_RANGE = 500  # range of domain [m]
DOMAIN_DURATION = 30  # duration of domain [s]
NUMBER_OF_EVENTS = 10
MESSAGES_LIFETIME = 100  # seconds
MAX_INTEDED_VEHICLE_DESTINATION = 3  # how many intended vehicles should take the message
MAX_HELPING_VEHICLE_DESTINATION = 3  # how many helping vehicles should take the message

EVENTS = {}  # time: accidental_vehicle
DOMAINS = {}  # accidental_veh_id: Domain


class VehicleType(Enum):
    NONE = 0,
    SOURCE = 1,
    INTENDED = 2,
    HELPING = 3,


class Phase(Enum):
    PRE_STABLE = 0,
    STABLE = 1,


def check_vehicle_type(source_vehicle, destination_vehicle, source_vehicle_type):
    if source_vehicle_type is VehicleType.SOURCE:  # if source vehicle is disseminating
        if source_vehicle.lane == destination_vehicle.lane:
            return VehicleType.INTENDED
        elif source_vehicle.lane.strip('-') == destination_vehicle.lane.strip('-'):
            return VehicleType.HELPING
        else:
            return VehicleType.NONE
    else:  # if other vehicles are exchanging the messages
        if source_vehicle.lane == destination_vehicle.lane:
            return source_vehicle_type
        elif source_vehicle.lane.strip('-') == destination_vehicle.lane.strip('-'):
            if source_vehicle_type is VehicleType.INTENDED:
                return VehicleType.HELPING
            elif source_vehicle_type is VehicleType.HELPING:
                return VehicleType.INTENDED
            else:
                return VehicleType.NONE
        else:
            return VehicleType.NONE


def get_distance(x1, y1, x2, y2):
    return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))


def get_middle_if_domain(x, y, angle):
    x_ret = DOMAIN_RANGE/2 * cos(radians(angle)) + x
    y_ret = DOMAIN_RANGE/2 * sin(radians(angle)) + y
    return x_ret, y_ret


def in_domain(vehicle, domain):
    distance = get_distance(vehicle.pos_x,
                            vehicle.pos_y,
                            domain.mid_x,
                            domain.mid_y)

    if distance <= DOMAIN_RANGE and \
            vehicle.lane.replace('-', '') == domain.lane.replace('-', ''):  # delete '-' char from lane id
        return True
    else:
        return False


def in_extra_region(vehicle, domain, extra_region_distance):
    distance = get_distance(vehicle.pos_x,
                            vehicle.pos_y,
                            domain.mid_x,
                            domain.mid_y)

    if distance > DOMAIN_RANGE and \
            distance <= DOMAIN_RANGE + extra_region_distance and \
            vehicle.lane.replace('-', '') == domain.lane.replace('-', ''):
        return True
    else:
        return False



def point_pos(x0, y0, d, theta):
    theta_rad = pi/2 - radians(theta)
    return x0 + d*cos(theta_rad), y0 + d*sin(theta_rad)
