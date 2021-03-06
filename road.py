from scipy.spatial import distance
from collections import deque
from mesa import Agent

class Road(Agent):
    """
    A road agent.
    """
    def __init__(self, unique_id, start, end, model):
        self.unique_id = unique_id
        self.start = start
        self.end = end
        self.model = model

        self.vehicles = deque()

        self.init_properties()

    def init_properties(self):
        self.length = distance.euclidean(self.start, self.end)
        self.angle_sin = (self.end[1] - self.start[1]) / self.length
        self.angle_cos = (self.end[0] - self.start[0]) / self.length
        self.has_traffic_signal = False

    def set_traffic_signal(self, signal, group):
        self.has_traffic_signal = True
        self.traffic_signal = signal
        self.traffic_signal_group = group

    @property
    def traffic_signal_state(self):
        if self.has_traffic_signal:
            i = self.traffic_signal_group
            return self.traffic_signal.current_cycle[i]
        return True

    def step(self, dt):
        n = len(self.vehicles)

        if n > 0:
            self.vehicles[0].step(dt)
            for i in range(1, n):
                self.vehicles[i].step(dt)
            
            if self.traffic_signal_state:
                self.vehicles[0].unstop()
                for vehicle in self.vehicles:
                    vehicle.unslow()
            else:
                if self.vehicles[0].x >= self.length - self.traffic_signal.slow_distance:
                    self.vehicles[0].slow(self.traffic_signal.slow_factor * self.vehicles[0]._v_max)
                if self.vehicles[0].x >= self.length - self.traffic_signal.stop_distance and self.vehicles[0].x <= self.length - self.traffic_signal.stop_distance / 2:
                    self.vehicles[0].stop()
