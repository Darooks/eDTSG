from SumoUpload import *
import random


TIME_STEPS = sumo_upload('output.xml')
EVENTS = {}
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


def simulate():
    for time_step in TIME_STEPS:
        print(time_step)
        vehicles = TIME_STEPS[time_step]

        for vehicleId in vehicles:
            print(vehicleId, vehicles[vehicleId].pos_x)


def main():
    draw_random_events()
    simulate()


if __name__ == "__main__":
    main()
