from math import *
import eDTSGSimulation


def get_distance(x1, y1, x2, y2):
    return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))


def get_middle_if_domain(x, y, angle):
    x_ret = eDTSGSimulation.DOMAIN_RANGE/2 * cos(radians(angle)) + x
    y_ret = eDTSGSimulation.DOMAIN_RANGE/2 * sin(radians(angle)) + y
    return x_ret, y_ret


def in_domain(vehicle, domain):
    distance = get_distance(vehicle.pos_x,
                            vehicle.pos_y,
                            domain.mid_x,
                            domain.mid_y)

    if distance <= eDTSGSimulation.DOMAIN_RANGE and \
            vehicle.lane.replace('-', '') == domain.lane.replace('-', ''):  # delete '-' char from lane id
        return True
    else:
        return False


def point_pos(x0, y0, d, theta):
    theta_rad = pi/2 - radians(theta)
    return x0 + d*cos(theta_rad), y0 + d*sin(theta_rad)
