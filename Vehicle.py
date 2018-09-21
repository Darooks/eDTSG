from Utils import get_distance, COMMUNICATION_RANGE, DOMAINS, DOMAIN_RANGE, VehicleType, check_vehicle_type, \
    MAX_HELPING_VEHICLE_DESTINATION, MAX_INTEDED_VEHICLE_DESTINATION, in_domain, in_extra_region, Phase
from Message import Message

TO_DROP = "DROPPED"


class Vehicle:
    def __init__(self,
                 id,
                 pos_x,
                 pos_y,
                 speed,
                 lane=None,
                 in_accident=False,
                 angle=0):

        self.id                         = id
        self.pos_x                      = float(pos_x)
        self.pos_y                      = float(pos_y)
        self.speed                      = float(speed)
        self.lane                       = lane
        self.in_accident                = in_accident
        self.angle                      = float(angle)
        self.bufor                      = {}  # id_domain/id_message: message
        self._messages                  = {}  # id_domain/id_message: message
        self._extra_region_distance_per_message  = {}  # id_domain/id_message: extra_length

    # *************
    # * GETS/SETS *
    # *************
    def get_messages(self):
        return self._messages

    def get_messages_element(self, id_msg):
        return self._messages[id_msg]

    def set_messages(self, _messages):
        self._messages = _messages

    def set_messages_element(self, id_msg, message):
        self._messages[id_msg] = message

    def get_extra_length_per_message(self):
        return self._extra_region_distance_per_message

    def set_extra_length_per_message(self, _extra_length_per_message):
        self._extra_region_distance_per_message = _extra_length_per_message.copy()

    # *****************
    # * OTHER METHODS *
    # *****************
    def update_messages(self, _messages):
        self._messages.update(_messages)

    def check_if_message_is_in_bufor(self, message_id):
        if message_id in self.bufor.keys():
            return True
        else:
            return False

    def is_messages_dict_empty(self):
        if len(self._messages) > 0:
            return False
        else:
            return True

    @staticmethod
    def update_message_rebroadcast_state(message):
        """ Checking message counters. If Message should not be rebroadcasted then change sleeping state to true. """
        if message.vehicle_type is VehicleType.INTENDED and \
                message.get_helping_vehicle_counter() >= MAX_HELPING_VEHICLE_DESTINATION:
            message.is_sleeping = True
        elif message.vehicle_type is VehicleType.HELPING and \
                message.get_intended_vehicle_counter() >= MAX_INTEDED_VEHICLE_DESTINATION:
            message.is_sleeping = True

    def _pre_stable_message_process(self, message):
        vehicle_type = message.vehicle_type

        if message.is_sleeping is True:
            print("WEIRD SITUATION: message is asleep in pre-stable mode")
            message.is_sleeping = False

        if vehicle_type is VehicleType.HELPING:
            in_extra_region_flag = in_extra_region(self,
                                                   DOMAINS[message.message_id],
                                                   self._extra_region_distance_per_message[message.message_id])
            if in_extra_region_flag is True:
                DOMAINS[message.message_id].phase = Phase.STABLE
                # print("Domain gets STABLE state")

    def _drop_message(self, message):
        # print("I am vehicle nr", self.id, "[DROPPING THE MESSAGE]")
        del self._extra_region_distance_per_message[message.message_id]
        self._messages[message.message_id] = TO_DROP
        del message

    def _stable_message_process(self, message):
        vehicle_type = message.vehicle_type
        in_domain_flag = in_domain(self, DOMAINS[message.message_id])

        # Make message asleep or active depending on domain location
        if in_domain_flag is True and message.is_sleeping is False:
            message.is_sleeping = True
        elif in_domain_flag is False and message.is_sleeping is True:
            message.is_sleeping = False

        # Drop message if counters are full and domain location is satisfied
        if vehicle_type is VehicleType.HELPING:
            if message.get_intended_vehicle_counter() >= MAX_INTEDED_VEHICLE_DESTINATION and in_domain_flag is False:
                self._drop_message(message)

        elif vehicle_type is VehicleType.INTENDED:
            if message.get_helping_vehicle_counter() >= MAX_HELPING_VEHICLE_DESTINATION and in_domain_flag is False:
                self._drop_message(message)

    def update_messages_statuses(self):
        """ Decide to drop or keep the messages or to make them asleep. Decision should be made in every time step.

            For fast implementation of source vehicle decisions you can set:
            update_messages_statuses(self, vehicle_type=None) - because source vehicles don't have messages
            with proper vehicle_types.
        """
        for message in self._messages.values():
            domain_phase = DOMAINS[message.message_id].phase

            if domain_phase is Phase.PRE_STABLE:
                # print("I am vehicle nr", self.id, "[PRE-STABLE functionality]")
                self._pre_stable_message_process(message)
            else:
                # print("I am vehicle nr", self.id, "[STABLE functionality]")
                self._stable_message_process(message)

        # Update: delete dropped messages
        for message_id in list(self._messages):
            if self._messages[message_id] is TO_DROP:
                # print("Vehicle", self.id, "dropping message")
                del self._messages[message_id]

    def send_messages(self, dest_vehicles):
        for dest_vehicle in dest_vehicles:
            if dest_vehicle.id is self.id:
                continue

            distance = get_distance(self.pos_x,
                                    self.pos_y,
                                    dest_vehicle.pos_x,
                                    dest_vehicle.pos_y)
            if distance <= COMMUNICATION_RANGE:

                for message in self._messages.values():
                    if message.is_sleeping is True:
                        continue  # Vehicle should not broadcast the message

                    destination_vehicle_type = check_vehicle_type(self, dest_vehicle, message.vehicle_type)
                    if destination_vehicle_type is VehicleType.NONE:
                        continue  # if destination vehicle is not intended, helping or source vehicle go out

                    new_message = Message(message_id=message.message_id,
                                          lifetime=message.lifetime,
                                          event_time_stamp=message.event_time_stamp,
                                          update_sequence=message.update_sequence.copy(),
                                          vehicle_type=destination_vehicle_type,
                                          version_time_stamp=message.version_time_stamp)
                    dest_vehicle.bufor[message.message_id] = new_message

                    # Message is sent - update counters
                    if destination_vehicle_type is VehicleType.HELPING:
                        message.increment_helping_vehicle_counter()
                    elif destination_vehicle_type is VehicleType.INTENDED:
                        message.increment_intended_vehicle_counter()

                # at the end - destination vehicle must collect the message
                dest_vehicle.collect_messages()

    def collect_messages(self):
        for id_message in self.bufor:
            if id_message not in self._messages:
                self._messages[id_message] = self.bufor[id_message]
                self._messages[id_message].update_sequence.append(self.id)

                vehicle_density = DOMAINS[id_message].vehicle_density
                self._extra_region_distance_per_message[id_message] = DOMAIN_RANGE / vehicle_density
            elif id_message in self._messages \
                    and self._messages[id_message].version_time_stamp < self.bufor[id_message].version_time_stamp:
                """ Destination vehicle has the message but source vehicle's message is newer by version time stamp """
                self._messages[id_message] = self.bufor[id_message]
                self._messages[id_message].update_sequence.append(self.id)

                vehicle_density = DOMAINS[id_message].vehicle_density
                self._extra_region_distance_per_message[id_message] = DOMAIN_RANGE / vehicle_density

                # print("Vehicle:", self.id, "updates info")
                # TODO: Compute messages when they came to an end
            else:
                pass

        self.bufor.clear()
        pass
