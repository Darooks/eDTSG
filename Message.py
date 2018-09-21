from Utils import VehicleType, STATISTIC_MEMORY_OBJECT


class Message:
    def __init__(self,
                 message_id='0',
                 event_location=None,
                 lifetime=0,
                 event_time_stamp=0,
                 sender_location=None,
                 spread_and_assurance_lifetime=0,
                 update_sequence=None,
                 vehicle_type=None,
                 version_time_stamp=None,
                 authentic_event=None,
                 non_authentic_event=None):
        self.message_id                      = message_id
        self.event_location                  = event_location
        self.lifetime                        = lifetime
        self.event_time_stamp                = event_time_stamp
        self.sender_location                 = sender_location
        self.spread_and_assurance_lifetime   = spread_and_assurance_lifetime
        self.update_sequence                 = [message_id] if update_sequence is None else update_sequence
        self.vehicle_type                    = VehicleType.NONE if vehicle_type is None else vehicle_type
        self.is_sleeping = False
        self.version_time_stamp              = 0 if version_time_stamp is None else version_time_stamp

        self._intended_vehicle_counter       = 0
        self._helping_vehicle_counted        = 0
        self._authentic_event                = 0 if authentic_event is None else authentic_event
        self._non_authentic_event            = 0 if non_authentic_event is None else non_authentic_event

    def get_authentic_event(self):
        return self._authentic_event

    def set_authentic_event(self, time_stamp):
        self._authentic_event += time_stamp
        self.version_time_stamp += time_stamp
        STATISTIC_MEMORY_OBJECT.set_voted_yes()

    def get_non_authentic_event(self):
        return self._non_authentic_event

    def set_non_authentic_event(self, time_stamp):
        self._non_authentic_event += time_stamp
        self.version_time_stamp += time_stamp
        STATISTIC_MEMORY_OBJECT.set_voted_no()

    def get_intended_vehicle_counter(self):
        return self._intended_vehicle_counter

    def increment_intended_vehicle_counter(self):  # refactor the name please
        self._intended_vehicle_counter += 1

    def get_helping_vehicle_counter(self):
        return self._helping_vehicle_counted

    def increment_helping_vehicle_counter(self):  # refactor the name please
        self._helping_vehicle_counted += 1
