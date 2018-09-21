from Utils import DOMAINS, in_domain, EVENTS_IS_ONLINE, STATISTIC_MEMORY_OBJECT

# TIME_STEPS = sumo_upload('fcd_output.xml')
# EVENTS = {}  # time: id
# ACCIDENTAL_VEHICLES = []
# DOMAINS = {}  # accidental_veh_id: Domain
#
# COMMUNICATION_RANGE = eDTSGSimulation.COMMUNICATION_RANGE  # range of communication [m]
# DOMAIN_RANGE = eDTSGSimulation.DOMAIN_RANGE  # range of domain [m]
# NUMBER_OF_EVENTS = eDTSGSimulation.NUMBER_OF_EVENTS
# MESSAGES_LIFETIME = eDTSGSimulation.MESSAGES_LIFETIME  # seconds


def get_awared_vehicles(vehicles, domain):
    total_active_vehicles_in_domain = 0
    total_aware_vehicles_in_domain = 0

    for vehicle in vehicles.values():
        if in_domain(vehicle, domain) is True:
            # print("\t\t", vehicle.id, "angle:", vehicle.angle, "lane:", vehicle.lane)
            total_active_vehicles_in_domain += 1

        if in_domain(vehicle, domain) is True and domain.id in vehicle.get_messages():
            total_aware_vehicles_in_domain += 1

    if total_active_vehicles_in_domain != 0:
        total_awareness = 100 * total_aware_vehicles_in_domain / total_active_vehicles_in_domain
        print("Total awared vehicles:", total_awareness, "%")
        print("\n")
    else:
        print("There are no active vehicles")


def get_awared_vehicles_non_active_domain(vehicles, domain, output_file, actual_time_step):
    total_active_vehicles_in_domain = 0
    total_aware_vehicles_in_domain = 0

    for vehicle in vehicles.values():
        if in_domain(vehicle, domain) is True:
            # print("\t\t", vehicle.id, "angle:", vehicle.angle, "lane:", vehicle.lane)
            total_active_vehicles_in_domain += 1

        if in_domain(vehicle, domain) is True \
                and domain.id in vehicle.get_messages() \
                and vehicle.get_messages()[domain.id].get_authentic_event() < vehicle.get_messages()[domain.id].get_non_authentic_event():
            total_aware_vehicles_in_domain += 1

    if total_active_vehicles_in_domain != 0:
        total_awareness = 100 * total_aware_vehicles_in_domain / total_active_vehicles_in_domain
        if total_awareness > 90.0 and STATISTIC_MEMORY_OBJECT.time_to_get_90_per == 0:
            STATISTIC_MEMORY_OBJECT.time_to_get_90_per = actual_time_step - 35

        if total_awareness == 100.0 and STATISTIC_MEMORY_OBJECT.time_to_get_100_per == 0:
            STATISTIC_MEMORY_OBJECT.time_to_get_100_per = actual_time_step - 35

        # print("[N] Total awared vehicles:", total_awareness, "%")
        # print("\n")
        string_to_write = str(actual_time_step - 35.0) + "\t" + str(total_awareness) + "%"
        output_file.write(string_to_write)
        print(string_to_write)
    else:
        print("There are no active vehicles")


def get_voting_registers(vehicles, domain, output_file, actual_time_step):
    highest_authentic_register_value = 0
    highest_non_authentic_register_value = 0

    for vehicle in vehicles.values():
        if domain.id not in vehicle.get_messages().keys():
            continue

        # if in_domain(vehicle, domain) is False:
        #     continue

        temp_value = 0
        temp_value = vehicle.get_messages()[domain.id].get_authentic_event()
        if temp_value > highest_authentic_register_value:
            highest_authentic_register_value = temp_value

        temp_value = 0
        temp_value = vehicle.get_messages()[domain.id].get_non_authentic_event()
        if temp_value > highest_non_authentic_register_value:
            highest_non_authentic_register_value = temp_value


    # string_to_write = str(actual_time_step) + "\t" + str(highest_authentic_register_value) + "\t" + str(highest_non_authentic_register_value) + "\n"
    string_to_write = str(STATISTIC_MEMORY_OBJECT.get_voted_yes()) + "\t" + str(STATISTIC_MEMORY_OBJECT.get_voted_no()) + "\n"
    output_file.write(string_to_write)

    pass


def get_statistics(actual_time_step, vehicles, output_file):
    for domain in DOMAINS.values():
        if actual_time_step < domain.start_time:
            continue
        # print("\tDomain", domain.id, "\n\tStart time:", domain.start_time, "\n\tlane:", domain.lane, "\n\tcontains:")

        # get_voting_registers(vehicles, domain, output_file, actual_time_step)

        # get_awared_vehicles(vehicles, domain)
        if EVENTS_IS_ONLINE[domain.id] is False:
            get_awared_vehicles_non_active_domain(vehicles, domain, output_file, actual_time_step)
            pass
