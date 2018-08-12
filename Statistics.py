import Utils

# TIME_STEPS = sumo_upload('fcd_output.xml')
# EVENTS = {}  # time: id
# ACCIDENTAL_VEHICLES = []
# DOMAINS = {}  # accidental_veh_id: Domain
#
# COMMUNICATION_RANGE = eDTSGSimulation.COMMUNICATION_RANGE  # range of communication [m]
# DOMAIN_RANGE = eDTSGSimulation.DOMAIN_RANGE  # range of domain [m]
# NUMBER_OF_EVENTS = eDTSGSimulation.NUMBER_OF_EVENTS
# MESSAGES_LIFETIME = eDTSGSimulation.MESSAGES_LIFETIME  # seconds


def get_statistics(time_step, vehicles, domains):
    print("Time step: ", time_step)
    for domain in domains.values():
        print("\tDomain", domain.id, "\n\tStart time:", domain.start_time, "\n\tlane:", domain.lane, "\n\tcontains:")
        for vehicle in vehicles.values():
            if Utils.in_domain(vehicle, domain) is True:
                print("\t\t", vehicle.id, "angle:", vehicle.angle, "lane:", vehicle.lane)

        print("\n")
