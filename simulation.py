from road import Road
from vehicle import Vehicle
from traffic_signal import TrafficSignal
from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import math
import random

class Simulation(Model):
    """A model with some number of agents."""
    def __init__(self, config={}):
        self.set_default_config()

        for attr, value in config.items():
            setattr(self, attr, value)

        self.grid = MultiGrid(self.width, self.height, True)
        self.schedule = RandomActivation(self)

        self.datacollector = DataCollector(
            model_reporters={"Vehicle path": lambda m: m.vehicle_path()}
        )


    def set_default_config(self):
        self.t = 0
        self.speed_multiplier = 1
        self.cos_lookup_table = [math.cos(math.radians(i)) for i in range(360)]
        self.sin_lookup_table = [math.sin(math.radians(i)) for i in range(360)]
        self.schedule = None
        self.roads = []
        self.traffic_lights = []
        self.cars = []

    def generate_cos_sin_lookup_table(self):
        for i in range(360):
            self.cos_lookup_table[i] = math.cos(math.radians(i))
            self.sin_lookup_table[i] = math.sin(math.radians(i))
    
    def generate_roads(self, num_roads):
        for i in range(num_roads):
            x_0 = random.randint(0, self.width)
            y_0 = random.randint(0, self.height)
            x_1 = random.randint(0, self.width)
            y_1 = random.randint(0, self.height)
            self.roads.append(Road(i, (x_0, y_0), (x_1, y_1), self))
        
    # def generate_traffic_signals(self, num_traffic_lights):
    #     for i in range(num_traffic_lights):
    #         self.traffic_lights.append(TrafficSignal(i, 0, {}, self))

    def generate_vehicle(self, num_cars):
        for i in range(num_cars):
            self.cars.append(Vehicle(i, self))
    
    def generate_schedule(self):
        self.schedule = RandomActivation(self)
        # for agent in self.traffic_lights:
        #     self.schedule.add(agent)
        for agent in self.cars:
            self.schedule.add(agent)
    
    def generate_agents(self, num_roads, num_cars):
        self.generate_roads(num_roads)
        self.generate_vehicle(num_cars)
        self.generate_schedule()

    def generate_model(self, width, height, speed_multiplier, num_roads, num_cars):
        self.generate_cos_sin_lookup_table()
        self.generate_agents(num_roads, num_cars)
        self.generate_schedule()

    # def generate_agents(self, num_roads, num_traffic_lights, num_cars):
    #     self.generate_roads(num_roads)
    #     self.generate_traffic_signals(num_traffic_lights)
    #     self.generate_vehicle(num_cars)
    
    # def generate_model(self, width, height, speed_multiplier, num_roads, num_traffic_lights, num_cars):
    #     self.generate_cos_sin_lookup_table()
    #     self.generate_agents(num_roads, num_traffic_lights, num_cars)
    #     self.generate_schedule()

    def vehicle_path(self):
        return [car.path for car in self.cars]

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        self.t += 1


sim = Simulation(
    config={
        "width": 100,
        "height": 100,
        "speed_multiplier": 1,
        "num_roads": 1,
        # "num_traffic_lights": 1,
        "num_cars": 1
    }
)

sim.generate_model(
    width=100,
    height=100,
    speed_multiplier=1,
    num_roads=1,
    num_cars=1
)

for i in range(10):
    sim.step()
    print(sim.vehicle_path())
