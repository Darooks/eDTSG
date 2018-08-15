from SumoUpload import *
from Vehicle import *
from Message import *
from Domain import *
from Utils import *
from Statistics import *
import random


TIME_STEPS = sumo_upload('fcd_output.xml')


def update_vehicles_states(actual_vehicles, previous_step):
    previous_vehicles = TIME_STEPS[previous_step]

    for vehicle_id in previous_vehicles:
        if vehicle_id in actual_vehicles.keys():
            actual_vehicles[vehicle_id].bufor.update(previous_vehicles[vehicle_id].bufor)
            actual_vehicles[vehicle_id].update_messages(previous_vehicles[vehicle_id].get_messages())

            actual_vehicles[vehicle_id].set_extra_length_per_message(
                previous_vehicles[vehicle_id].get_extra_length_per_message()
            )

    return actual_vehicles


def create_events():
    """ Creates new accidental car by parameters of vehicle that already exist. """
    acc_time_step = 5.0
    acc_id = '0#acc'

    new_acc_domain = Domain(acc_id,
                            1037.67,
                            585.98,
                            252.64,
                            '10249819',
                            acc_time_step,
                            acc_time_step + DOMAIN_DURATION)

    DOMAINS[acc_id] = new_acc_domain

    acc_veh_x, acc_veh_y = point_pos(new_acc_domain.mid_x,
                                     new_acc_domain.mid_y,
                                     DOMAIN_RANGE / 2,
                                     new_acc_domain.angle)

    acc_vehicle = Vehicle(acc_id,
                          acc_veh_x,
                          acc_veh_y,
                          speed=0,
                          lane=new_acc_domain.lane,
                          in_accident=True,
                          angle=new_acc_domain.angle)

    EVENTS[acc_time_step] = acc_vehicle


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


def send_message(destination_vehicle, message):
    destination_vehicle.bufor[message.message_id] = message  # send message
    destination_vehicle.collect_messages()                   # destination node get the message


def accident_node_dissemination(vehicles, actual_time_step):
    """ Accidental nodes disseminate information about
    their accident to the vehicle that are in their domain and range"""

    for time_step in EVENTS:
        if float(time_step) > float(actual_time_step):
            continue

        accidental_vehicle = EVENTS[time_step]

        for source_vehicle in vehicles.values():
            distance_between = get_distance(accidental_vehicle.pos_x, accidental_vehicle.pos_y,
                                            source_vehicle.pos_x, source_vehicle.pos_y)

            if distance_between < COMMUNICATION_RANGE:
                message = Message(message_id=accidental_vehicle.id,
                                  lifetime=MESSAGES_LIFETIME,
                                  event_time_stamp=actual_time_step)

                send_message(source_vehicle, message)
                # print("Sending message. \n\tSource id:", accidental_vehicle.id,
                #       "\n\tDestination id:", source_vehicle.id)


def simulate():
    previous_step = None
    for time_step in TIME_STEPS:
        # Update vehicles states- merging states between actual step with previous step
        vehicles = TIME_STEPS[time_step]  # get vehicles from current time step
        if previous_step is not None:
            vehicles = update_vehicles_states(vehicles, previous_step)  # merge states

        # Update domains
        for domain in DOMAINS.values():
            domain.update_domain(vehicles.values())

        # 1) Accidental nodes disseminate information <done>
        accident_node_dissemination(vehicles, time_step)

        for vehicle in vehicles.values():
            # TODO: 2) Send and collect the messages
            if vehicle.is_messages_dict_empty() is False:
                vehicle.send_messages(vehicles.values())
            pass

        # if len(DOMAINS) != 0:
        #     get_statistics(time_step, vehicles)

        previous_step = time_step


def main():
    # draw_random_events()
    create_events()
    simulate()
    pass


if __name__ == "__main__":
    main()
