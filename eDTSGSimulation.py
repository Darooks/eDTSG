from SumoUpload import *
from Vehicle import *
from Message import *
from Domain import *
from Utils import *
from Statistics import *
import random


TIME_STEPS = sumo_upload('fcd_output.xml')
EVENTS = {}  # time: id
ACCIDENTAL_VEHICLES = []
DOMAINS = {}  # accidental_veh_id: Domain

COMMUNICATION_RANGE = 250  # range of communication [m]
DOMAIN_RANGE = 3000  # range of domain [m]
DOMAIN_DURATION = 30  # duration of domain [s]
NUMBER_OF_EVENTS = 10
MESSAGES_LIFETIME = 10  # seconds


def update_vehicles_states(actual_step, previous_step, actual_vehicles):
    previous_vehicles = TIME_STEPS[previous_step]

    for vehicle_id in previous_vehicles:
        if vehicle_id in actual_vehicles.keys():
            actual_vehicles[vehicle_id].bufor.update(previous_vehicles[vehicle_id].bufor)

    return actual_vehicles


def draw_random_events():
    num_events = NUMBER_OF_EVENTS
    while num_events > 0:
        time_step = random.choice(list(TIME_STEPS))

        if time_step not in EVENTS.keys():
            vehicle = random.choice(list(TIME_STEPS[time_step]))
            if vehicle in EVENTS.values():
                continue

            EVENTS[time_step] = vehicle
            num_events -= 1


def create_accidental_vehicle(vehicle, time_step):
    """ Creates new accidental car by parameters of vehicle that already exist. """
    new_accidental_vehicle = Vehicle(vehicle.id,
                                     vehicle.pos_x,
                                     vehicle.pos_y,
                                     speed=0,
                                     lane=vehicle.lane,
                                     in_accident=True,
                                     angle=vehicle.angle)

    ACCIDENTAL_VEHICLES.append(new_accidental_vehicle)

    DOMAINS[new_accidental_vehicle.id] = Domain(vehicle.id,
                                                vehicle.pos_x,
                                                vehicle.pos_y,
                                                vehicle.angle,
                                                vehicle.lane,
                                                float(time_step),
                                                float(time_step) + DOMAIN_DURATION)


def send_message(destination_vehicle, message):
    message.update_sequence.append(destination_vehicle.id)
    destination_vehicle.bufor[message.message_id] = message


def accident_node_dissemination(vehicles, actual_time_step):
    """ Accidental nodes disseminate information about
    their accident to the vehicle that are in their domain and range"""
    for accidental_vehicle in ACCIDENTAL_VEHICLES:
        message = Message(message_id=accidental_vehicle.id,
                          lifetime=MESSAGES_LIFETIME,
                          event_time_stamp=actual_time_step)

        for source_vehicle in vehicles.values():
            distance_between = get_distance(accidental_vehicle.pos_x, accidental_vehicle.pos_y,
                                            source_vehicle.pos_x, source_vehicle.pos_y)

            if distance_between < COMMUNICATION_RANGE and message not in source_vehicle.bufor:
                send_message(source_vehicle, message)
                # print("Sending message. \n\tSource id:", accidental_vehicle.id,
                #       "\n\tDestination id:", source_vehicle.id)


def simulate():
    previous_step = None
    for time_step in TIME_STEPS:
        # Update vehicles states- merging states between actual step with previous step
        vehicles = TIME_STEPS[time_step]  # get vehicles from current time step
        if previous_step is not None:
            vehicles = update_vehicles_states(time_step, previous_step, vehicles)  # merge states

        if time_step in EVENTS.keys():
            create_accidental_vehicle(vehicles[EVENTS[time_step]], time_step)
        # 1) Accidental nodes disseminate information <done>
        accident_node_dissemination(vehicles, time_step)

        for vehicle_id in vehicles:
            # TODO: 2) Send and collect the messages
            pass

        if len(DOMAINS) != 0:
            get_statistics(time_step, vehicles, ACCIDENTAL_VEHICLES, DOMAINS)

        previous_step = time_step


def main():
    draw_random_events()
    simulate()
    pass

if __name__ == "__main__":
    main()
