from SumoUpload import *
from Vehicle import *
from Message import *
import random


TIME_STEPS = sumo_upload('fcd_output.xml')
EVENTS = {}  # time: id
ACCIDENTAL_VEHICLE = []
MAX_RANGE = 250  # range of communication
NUMBER_OF_EVENTS = 10


def draw_random_events():
    numEvents = NUMBER_OF_EVENTS
    while numEvents > 0:
        timeStep = random.choice(list(TIME_STEPS))

        if timeStep not in EVENTS.keys():
            vehicle = random.choice(list(TIME_STEPS[timeStep]))
            if vehicle in EVENTS.values():
                continue

            EVENTS[timeStep] = vehicle
            numEvents -= 1


def create_accidental_vehicle(vehicle):
    """ Creates new accidental car by parameters of vehicle that already exist. """
    new_accidental_vehicle = Vehicle(vehicle.id,
                                     vehicle.pos_x,
                                     vehicle.pos_y,
                                     speed=0,
                                     in_accident=True,
                                     angle=vehicle.angle)

    ACCIDENTAL_VEHICLE.append(new_accidental_vehicle)


def self_accident_dissemination(vehicles):
    """ Accidental nodes disseminate information about
    their accident to the vehicle that are in their domain and range"""
    pass


def simulate():
    for time_step in TIME_STEPS:
        vehicles = TIME_STEPS[time_step]

        if time_step in EVENTS.keys():
            create_accidental_vehicle(vehicles[EVENTS[time_step]])
        # TODO: 1) Accidental nodes disseminate information
        self_accident_dissemination(vehicles)

        for vehicle_id in vehicles:
            # TODO: 2) Send and collect the messages
            pass


def main():
    draw_random_events()
    simulate()


if __name__ == "__main__":
    main()
