from math import *

COMMUNICATION_RANGE = 250  # range of communication [m]
DOMAIN_RANGE = 500  # range of domain [m]
DOMAIN_DURATION = 30  # duration of domain [s]
NUMBER_OF_EVENTS = 10
MESSAGES_LIFETIME = 10  # seconds

EVENTS = {}  # time: accidental_vehicle
DOMAINS = {}  # accidental_veh_id: Domain


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


def point_pos(x0, y0, d, theta):
    theta_rad = pi/2 - radians(theta)
    return x0 + d*cos(theta_rad), y0 + d*sin(theta_rad)
