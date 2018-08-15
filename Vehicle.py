from Utils import get_distance, COMMUNICATION_RANGE, DOMAINS, DOMAIN_RANGE, MESSAGES_LIFETIME
from Message import Message


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
        self._extra_length_per_message  = {}  # id_domain/id_message: extra_length

    # *************
    # * GETS/SETS *
    # *************
    def get_messages(self):
        return self._messages

    def set_messages(self, _messages):
        self._messages = _messages

    def get_extra_length_per_message(self):
        return self._extra_length_per_message

    def set_extra_length_per_message(self, _extra_length_per_message):
        self._extra_length_per_message = _extra_length_per_message

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
                    new_message = Message(message_id=message.message_id,
                                          lifetime=message.lifetime,
                                          event_time_stamp=message.event_time_stamp,
                                          update_sequence=message.update_sequence.copy())

                    dest_vehicle.bufor[message.message_id] = new_message

                # at the end destinetion vehicle must collect the message
                dest_vehicle.collect_messages()

    def collect_messages(self):
        for id_message in self.bufor:
            if id_message not in self._messages:
                self._messages[id_message] = self.bufor[id_message]
                self._messages[id_message].update_sequence.append(self.id)

                vehicle_density = DOMAINS[id_message].vehicle_density
                self._extra_length_per_message[id_message] = DOMAIN_RANGE / vehicle_density
            else:
                pass

        self.bufor.clear()
        pass
