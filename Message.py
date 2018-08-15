class Message:
    def __init__(self,
                 message_id='0',
                 event_location=None,
                 lifetime=0,
                 event_time_stamp=0,
                 sender_location=None,
                 spread_and_assurance_lifetime=0,
                 update_sequence=None):
        self.message_id                      = message_id
        self.event_location                  = event_location
        self.lifetime                        = lifetime
        self.event_time_stamp                = event_time_stamp
        self.sender_location                 = sender_location
        self.spread_and_assurance_lifetime   = spread_and_assurance_lifetime
        self.update_sequence                 = [message_id] if update_sequence is None else update_sequence
        self._authentic_event                = None  # My modification
        self._non_authentic_event            = None  # My modification

    def set_authentic_event(self):
        pass

    def set_non_authentic_event(self):
        pass
