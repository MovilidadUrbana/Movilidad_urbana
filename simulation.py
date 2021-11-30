from numpy.lib.function_base import select
from road import Road
from vehicle import Vehicle
from traffic_signal import TrafficSignal
from copy import deepcopy
from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import math
import random
import numpy as np
import matplotlib.pyplot as plt

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
        self.dt = 1/60
        self.speed_multiplier = 1
        self.cos_lookup_table = [math.cos(math.radians(i)) for i in range(360)]
        self.sin_lookup_table = [math.sin(math.radians(i)) for i in range(360)]
        self.schedule = None
        self.roads = []
        self.traffic_lights = []

    def generate_cos_sin_lookup_table(self):
        for i in range(360):
            self.cos_lookup_table[i] = math.cos(math.radians(i))
            self.sin_lookup_table[i] = math.sin(math.radians(i))
    
    def generate_roads(self, num_roads):
        # self.roads.append(Road(0, (0, 0), (100, 100), self))
        # self.roads.append(Road(1, (0, 0), (100, 0), self))
        # self.roads.append(Road(2, (0, 0), (0, 100), self))
        self.roads.append(Road(1, (-248.2, -79), (5.8, -79), self))
        self.roads.append(Road(2, (5.8, -79), (46.7, -98.8), self))
        self.roads.append(Road(3, (46.7, -98.8), (140,1. -98.8), self))
        self.roads.append(Road(4, (140, -98.8), (179.2, -132.8), self)) # curve
        self.roads.append(Road(5, (179.2, -132.8), (172.9, -343.2), self))
        self.roads.append(Road(6, (172.9, -343.2), (139.9, -378.6), self)) # curve
        self.roads.append(Road(7, (139.9, -378.6), (-259, -378.6), self))
        # fork
        self.roads.append(Road(8, (-259, -378.6), (-285.5, -411.5), self))
        self.roads.append(Road(9, (-259, -378.6), (-285.5, -341.5), self))
        
        self.roads.append(Road(10, (-285.5, -411.5), (-285.5, -341.5), self))
        self.roads.append(Road(11, (-285.5, -411.5), (-319.3, -447.1), self)) # curve
        self.roads.append(Road(12, (-355.9, -404.9), (-355.9, -377.7), self)) # curve
        self.roads.append(Road(13, (-355.9, -404.9), (-355.9, -377.7), self))

        
    # def generate_traffic_signals(self, num_traffic_lights):
    #     for i in range(num_traffic_lights):
    #         self.traffic_lights.append(TrafficSignal(i, 0, {}, self))

    def generate_vehicle(self, num_vehicles):
        for i in range(num_vehicles):
            self.roads[0].vehicles.append(Vehicle(i, self, {"path": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]}))
    
    def generate_schedule(self):
        self.schedule = RandomActivation(self)
        # for agent in self.traffic_lights:
        #     self.schedule.add(agent)
        for road in self.roads:
            for agent in road.vehicles:
                self.schedule.add(agent)
    
    def generate_agents(self, num_roads, num_vehicles):
        self.generate_roads(num_roads)
        self.generate_vehicle(num_vehicles)
        self.generate_schedule()

    def generate_model(self, num_roads, num_vehicles):
        self.generate_cos_sin_lookup_table()
        self.generate_agents(num_roads, num_vehicles)
        self.generate_schedule()

    def vehicle_path(self):
        vehicle_positions = []
        for road in self.roads:
            for car in road.vehicles:
                x = road.start[0] + road.angle_cos * car.x
                y = road.start[1] + road.angle_sin * car.x
                vehicle_positions.append((car.unique_id, x, y))
        return vehicle_positions

    def step(self):
        for road in self.roads:
            road.step(self.dt)

        for road in self.roads:
            if len(road.vehicles) == 0:
                continue

            vehicle = road.vehicles[0]

            if vehicle.x >= road.length:
                if vehicle.current_road_index + 1 < len(vehicle.path):
                    vehicle.current_road_index += 1
                    new_vehicle = deepcopy(vehicle)
                    new_vehicle.x = 0
                    # Add it to the next road
                    next_road_index = vehicle.path[vehicle.current_road_index]
                    for road_t in self.roads:
                        if road_t.unique_id == next_road_index:
                            road_t.vehicles.append(new_vehicle)
                            break

                # In all cases, remove it from its road
                road.vehicles.popleft() 
            
        self.t += self.dt
        self.datacollector.collect(self)


sim = Simulation(
    config={
        "width": 100,
        "height": 100,
        "speed_multiplier": 1,
        "num_roads": 1,
        # "num_traffic_lights": 1,
        "num_vehicles": 2
    }
)

sim.generate_model(
    num_roads=1,
    num_vehicles=2
)

for i in range(10000):
    sim.step()
    # print(sim.vehicle_path())

# plot route
sim.datacollector.collect(sim)
data = sim.datacollector.get_model_vars_dataframe()
data.to_json("data.json")
x = []
y = []
for i in range(len(data)):
    try:
        x.append(data.iloc[i]["Vehicle path"][0][1])
        y.append(data.iloc[i]["Vehicle path"][0][2])
    except:
        pass

plt.plot(x, y)
plt.show()

#todo: calculate the optimal path of the vehicle
#todo: save position of the vehicle in the road