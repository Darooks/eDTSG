from Utils import VehicleType


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
                 version_time_stamp=None):
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
        self._authentic_event                = None  # My modification
        self._non_authentic_event            = None  # My modification

    def set_authentic_event(self):
        pass

    def set_non_authentic_event(self):
        pass

    def get_intended_vehicle_counter(self):
        return self._intended_vehicle_counter

    def increment_intended_vehicle_counter(self):  # refactor the name please
        self._intended_vehicle_counter += 1

    def get_helping_vehicle_counter(self):
        return self._helping_vehicle_counted

    def increment_helping_vehicle_counter(self):  # refactor the name please
        self._helping_vehicle_counted += 1
