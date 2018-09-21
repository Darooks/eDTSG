from Utils import DOMAINS, in_domain, EVENTS_IS_ONLINE

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
                and vehicle.get_messages()[domain.id].lifetime == 0.0:
            total_aware_vehicles_in_domain += 1

    if total_active_vehicles_in_domain != 0:
        total_awareness = 100 * total_aware_vehicles_in_domain / total_active_vehicles_in_domain
        # print("[N] Total awared vehicles:", total_awareness, "%")
        # print("\n")
        string_to_write = str(actual_time_step - 35.0) + "\t" + str(total_awareness) + "%"
        output_file.write(string_to_write)
        print(string_to_write)
    else:
        print("There are no active vehicles")


def get_statistics(actual_time_step, vehicles, output_file):
    for domain in DOMAINS.values():
        if actual_time_step < domain.start_time:
            continue
        # print("\tDomain", domain.id, "\n\tStart time:", domain.start_time, "\n\tlane:", domain.lane, "\n\tcontains:")

        # get_awared_vehicles(vehicles, domain)
        if EVENTS_IS_ONLINE[domain.id] is False:
            get_awared_vehicles_non_active_domain(vehicles, domain, output_file, actual_time_step)
