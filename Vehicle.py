class Vehicle:
    def __init__(self,
                 id,
                 pos_x,
                 pos_y,
                 speed,
                 direction = 0,
                 inAccident = False):

        self.id         = id
        self.pos_x      = pos_x
        self.pos_y      = pos_y
        self.speed      = speed
        self.direction  = direction
        self.bufor      = []
        self.inAccident = inAccident

    # TODO: Phase's - for every single message in bufor
    # TODO: Calculate domain for every message in bufor
