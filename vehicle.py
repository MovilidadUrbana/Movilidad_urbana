from mesa import Agent
import numpy as np

class Vehicle(Agent):
    """
    A vehicle agent.
    """
    def __init__(self, unique_id, model, config={}):
        self.unique_id = unique_id
        self.model = model
        self.set_default_config()

        for attr, value in config.items():
            setattr(self, attr, value)

        self.init_properties()

    def set_default_config(self):
        self.l = 4 #length?
        self.s0 = 4 #speed?
        self.T = 1 #time?
        self.v_max = 16.6 # max velocity?
        self.a_max = 1.44 # max acceleration?
        self.b_max = 4.61 # max deceleration?

        self.path = []
        self.current_road_index = 0

        self.x = 0
        self.v = self.v_max
        self.a = 0
        self.stopped = False

    def init_properties(self):
        self.sqrt_ab = 2 * np.sqrt(self.a_max * self.b_max)
        self._v_max = self.v_max

    def step(self, dt):
        if self.v + self.a*dt < 0:
            self.x -= 1/2*self.v*self.v/self.a
            self.v = 0
        else:
            self.v += self.a*dt
            self.x += self.v*dt + self.a*dt*dt/2
        # Update acceleration
        alpha = 0
        self.a = self.a_max * (1-(self.v/self.v_max)**4 - alpha**2)

        if self.stopped: 
            self.a = -self.b_max*self.v/self.v_max

    def stop(self):
        self.stopped = True
    
    def unstop(self):
        self.stopped = False
    
    def slow(self, v):
        self.v_max = v

    def unslow(self):
        self.v_max = self._v_max
