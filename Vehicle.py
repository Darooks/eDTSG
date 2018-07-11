class Vehicle:
    def __init__(self,
                 id,
                 pos_x,
                 pos_y,
                 speed,
                 in_accident=False,
                 angle=0):

        self.id         = id
        self.pos_x      = pos_x
        self.pos_y      = pos_y
        self.speed      = speed
        self.in_accident= in_accident
        self.angle  = angle
        self.bufor      = []

    # TODO: Phase's - for every single message in bufor
    # TODO: Calculate domain for every message in bufor
