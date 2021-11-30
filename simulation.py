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
        self.roads.append(Road(212, (0, 0), (0, -100), self))
        self.roads.append(Road(3452, (0, -100), (-100, -100), self))
        self.roads.append(Road(34555, (-100, -100), (-100, 0), self))
        self.roads.append(Road(3453455, (-100, 0), (0, 0), self))
        
    # def generate_traffic_signals(self, num_traffic_lights):
    #     for i in range(num_traffic_lights):
    #         self.traffic_lights.append(TrafficSignal(i, 0, {}, self))

    def generate_vehicle(self, num_vehicles):
        for i in range(num_vehicles):
            self.roads[0].vehicles.append(Vehicle(i, self, {"path": [212, 3452, 34555, 3453455]}))
    
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
        "num_vehicles": 1
    }
)

sim.generate_model(
    num_roads=1,
    num_vehicles=1
)

for i in range(1500):
    sim.step()
    print(sim.vehicle_path())

#todo: calculate the optimal path of the vehicle
#todo: save position of the vehicle in the road