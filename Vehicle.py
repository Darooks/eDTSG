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

    def check_if_message_is_in_bufor(self, message_id):
        if message_id in self.bufor.keys():
            return True
        else:
            return False

    # TODO: Phase's - for every single message in bufor
    # TODO: Calculate domain for every message in bufor
