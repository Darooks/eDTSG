from SumoUpload import *
from Vehicle import *
from Message import *
from Domain import *
from Utils import *
from Statistics import *
import random


TIME_STEPS = sumo_upload('fcd_output.xml')


def update_vehicles_states(actual_vehicles, previous_step, actual_time_step):
    previous_vehicles = TIME_STEPS[previous_step]

    for vehicle_id in previous_vehicles:
        if vehicle_id in actual_vehicles.keys():
            actual_vehicles[vehicle_id].bufor.update(previous_vehicles[vehicle_id].bufor)
            actual_vehicles[vehicle_id].update_messages(previous_vehicles[vehicle_id].get_messages())

            actual_vehicles[vehicle_id].set_extra_length_per_message(
                previous_vehicles[vehicle_id].get_extra_length_per_message()
            )

            actual_vehicles[vehicle_id].update_messages_statuses(actual_time_step)

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
    EVENTS_IS_ONLINE[acc_id] = True

    message = Message(message_id=acc_id,
                      lifetime=MESSAGES_LIFETIME,
                      event_time_stamp=acc_time_step,
                      vehicle_type=VehicleType.SOURCE,
                      version_time_stamp=acc_time_step)

    acc_vehicle.set_messages_element(acc_id, message)

    print("Domain x:", new_acc_domain.mid_x, "y:", new_acc_domain.mid_y)
    print("Acc vehicle x:", acc_vehicle.pos_x, "y:", acc_vehicle.pos_y)


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


def send_message(destination_vehicle, message, actual_time_step):
    destination_vehicle.bufor[message.message_id] = message  # send message
    destination_vehicle.collect_messages(actual_time_step)                   # destination node get the message


def accident_node_dissemination(vehicles, actual_time_step):
    """ Accidental nodes disseminate information about
    their accident to the vehicle that are in their domain and range """

    for time_step in EVENTS:
        if float(time_step) > float(actual_time_step):
            continue

        accidental_vehicle = EVENTS[time_step]

        message_info = accidental_vehicle.get_messages_element(accidental_vehicle.id)

        #  Suddenly end the event
        if message_info.event_time_stamp + MESSAGES_LIFETIME_BREAK <= actual_time_step\
                and EVENTS_IS_ONLINE[accidental_vehicle.id] is True:
            # print("EVENT no longer exist")
            message_info.lifetime = 0.0
            message_info.version_time_stamp += actual_time_step
            EVENTS_IS_ONLINE[accidental_vehicle.id] = False

        for source_vehicle in vehicles.values():
            source_vehicle_type = check_vehicle_type(accidental_vehicle, source_vehicle, VehicleType.SOURCE)

            distance_between = get_distance(accidental_vehicle.pos_x, accidental_vehicle.pos_y,
                                            source_vehicle.pos_x, source_vehicle.pos_y)

            if distance_between < COMMUNICATION_RANGE and source_vehicle_type is not VehicleType.NONE:
                message = Message(message_id=message_info.message_id,
                                  lifetime=message_info.lifetime,
                                  event_time_stamp=message_info.event_time_stamp,
                                  vehicle_type=source_vehicle_type,
                                  version_time_stamp=message_info.version_time_stamp)

                send_message(source_vehicle, message, actual_time_step)
                # print("Sending message. \n\tSource id:", accidental_vehicle.id, "lane:", accidental_vehicle.lane,
                #       "\n\tDestination id:", source_vehicle.id, "lane:", source_vehicle.lane)


def simulate(output_file):
    previous_step = None
    for time_step in TIME_STEPS:
        # print("Time step:", time_step)
        # Update vehicles states- merging states between actual step with previous step
        vehicles = TIME_STEPS[time_step]  # get vehicles from current time step
        if previous_step is not None:
            vehicles = update_vehicles_states(vehicles, previous_step, time_step)  # merge states

        # Update domains
        for domain in DOMAINS.values():
            domain.update_domain(vehicles.values())

        # Accidental nodes disseminate information
        accident_node_dissemination(vehicles, time_step)

        for vehicle in vehicles.values():
            # TODO: 2) Send and collect the messages
            if vehicle.is_messages_dict_empty() is False:
                # vehicle.update_messages_statuses(time_step)
                vehicle.send_messages(vehicles.values(), time_step)
            pass

        if len(DOMAINS) != 0:
            get_statistics(time_step, vehicles, output_file)

        previous_step = time_step


def main():
    # draw_random_events()
    output_file = open("output_file.txt", "w")
    create_events()
    simulate(output_file)
    return STATISTIC_MEMORY_OBJECT.time_to_get_90_per, STATISTIC_MEMORY_OBJECT.time_to_get_100_per


if __name__ == "__main__":
    main()
