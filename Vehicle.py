from Utils import get_distance, COMMUNICATION_RANGE


class Vehicle:
    def __init__(self,
                 id,
                 pos_x,
                 pos_y,
                 speed,
                 lane=None,
                 in_accident=False,
                 angle=0):

        self.id         = id
        self.pos_x      = float(pos_x)
        self.pos_y      = float(pos_y)
        self.speed      = float(speed)
        self.lane       = lane
        self.in_accident= in_accident
        self.angle      = float(angle)
        self.bufor      = {}
        self._messages  = {}

    def check_if_message_is_in_bufor(self, message_id):
        if message_id in self.bufor.keys():
            return True
        else:
            return False

    def send_messages(self, vehicles):
        for vehicle in vehicles:
            if vehicle.id is self.id:
                continue

            distance = get_distance(self.pos_x,
                                    self.pos_y,
                                    vehicle.pos_x,
                                    vehicle.pos_y)

            if distance <= COMMUNICATION_RANGE:
                vehicle.bufor = self._messages.copy()

            # at the end destinetion vehicle must collect the message
            vehicle.collect_messages()

    def collect_messages(self):
        for id_message in self.bufor:
            if id_message not in self._messages:
                self._messages[id_message] = self.bufor[id_message]
                del self.bufor[id_message]
            else:
                pass
