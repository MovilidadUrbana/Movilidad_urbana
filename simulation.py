from road import Road
from vehicle import Vehicle
from traffic_signal import TrafficSignal
from copy import deepcopy
from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import math
import random
import networkx as nx

class Simulation(Model):
    """A model with some number of agents."""
    def __init__(self, config={}):
        self.set_default_config()

        for attr, value in config.items():
            setattr(self, attr, value)
        self.schedule = RandomActivation(self)

        self.datacollector = DataCollector(
            model_reporters={"data": lambda m: m.vehicle_path()}
        )

        self.G = nx.DiGraph()
        self.G_inverse = nx.DiGraph()
        

    def set_default_config(self):
        self.t = 0
        self.dt = 1/60
        self.speed_multiplier = 1
        self.roads = []
        self.traffic_lights = []

    def generate_roads(self):
        """
        Generate a road with a given number of lanes.
        """

        self.roads.append(Road(1, (-247.3,-78.7), (5.1,-78.7), self))
        self.roads.append(Road(2, (5.1,-78.7), (48.3,-98.7), self))
        self.roads.append(Road(3, (48.3,-98.7), (141.86,-98.7), self))
        self.roads.append(Road(4, (141.86,-98.7), (178.98,-134.7), self))
        self.roads.append(Road(5, (178.98,-134.7), (178.98,-241), self))
        self.roads.append(Road(6, (178.98,-241), (178.98,-342.6), self))
        self.roads.append(Road(7, (178.98,-342.6), (143.1,-378.6), self))
        self.roads.append(Road(8, (143.1,-378.6), (-256.5,-378.6), self))
        self.roads.append(Road(9, (-256.5,-378.6), (-283.8,-408.6), self))
        self.roads.append(Road(10, (-256.5,-378.6), (-283.8,-351.2), self))
        self.roads.append(Road(11, (-283.8,-351.2), (-283.8,-408.6), self))
        self.roads.append(Road(12, (-283.8,-408.6), (-319.5,-446.3), self))
        self.roads.append(Road(13, (-319.5,-446.3), (-356.4,-410.8), self))
        self.roads.append(Road(14, (-356.4,-410.8), (-356.4,-377.9), self))
        self.roads.append(Road(15, (-356.4,-377.9), (-319.7,-341.5), self))
        self.roads.append(Road(16, (-319.7,-341.5), (-246.4,-341.5), self))
        self.roads.append(Road(17, (-246.4,-341.5), (-190.5,-341.5), self))
        self.roads.append(Road(18, (-190.5,-341.5), (53.6,-341.5), self))
        self.roads.append(Road(19, (53.6,-341.5), (89.2,-303.4), self))
        self.roads.append(Road(20, (89.2,-303.4), (89.2,-241.1), self))
        self.roads.append(Road(21, (89.2,-241.1), (89.2,-176.8), self))
        self.roads.append(Road(22, (89.2,-176.8), (52.39,-141.2), self))
        self.roads.append(Road(23, (52.39,-141.2), (-283.8,-141.2), self))
        self.roads.append(Road(24, (-283.8,-351.2), (-283.8,-141.2), self))
        self.roads.append(Road(25, (-283.8,-141.2), (-283.8,-115), self))
        self.roads.append(Road(26, (-283.8,-115), (-247.3,-78.7), self))
        self.roads.append(Road(27, (178.98,-241), (89.2,-241), self))
        self.roads.append(Road(28, (89.2,-241), (-180.1,-241), self))
        self.roads.append(Road(29, (-180.1,-241), (-218.5,-277.7), self))
        self.roads.append(Road(30, (-218.5,-277.7), (-218.5,-312.5), self))
        self.roads.append(Road(31, (-190.5,-341.5), (-218.5,-312.5), self))
        self.roads.append(Road(32, (-246.4,-341.5), (-218.5,-312.5), self))

        # invert the direction of the roads
        self.roads.append(Road(101, (5.1,-78.7), (-247.3,-78.7), self))
        self.roads.append(Road(126,  (-247.3,-78.7),(-283.8,-115), self))
        self.roads.append(Road(125,  (-283.8,-115), (-283.8,-141.2), self))
        self.roads.append(Road(123,  (-283.8,-141.2),(52.39,-141.2), self))
        self.roads.append(Road(124,  (-283.8,-141.2),(-283.8,-351.2), self))
        self.roads.append(Road(102, (48.3,-98.7), (5.1,-78.7), self))
        self.roads.append(Road(103, (141.86,-98.7), (48.3,-98.7), self))
        self.roads.append(Road(104, (178.98,-134.7), (141.86,-98.7), self))
        self.roads.append(Road(105, (178.98,-241), (178.98,-134.7), self))
        self.roads.append(Road(106, (178.98,-342.6), (178.98,-241), self))
        self.roads.append(Road(107, (143.1,-378.6), (178.98,-342.6), self))
        self.roads.append(Road(108, (-256.5,-378.6), (143.1,-378.6), self))
        self.roads.append(Road(109,  (-283.8,-408.6), (-256.5,-378.6), self))
        self.roads.append(Road(110, (-283.8,-351.2), (-256.5,-378.6), self))
        self.roads.append(Road(111, (-283.8,-408.6), (-283.8,-351.2), self))
        self.roads.append(Road(112, (-319.5,-446.3), (-283.8,-408.6), self))
        self.roads.append(Road(113, (-319.5,-446.3), (-356.4,-410.8), self))
        self.roads.append(Road(114, (-356.4,-410.8), (-356.4,-377.9), self))
        self.roads.append(Road(115, (-356.4,-377.9), (-319.7,-341.5), self))
        self.roads.append(Road(116, (-319.7,-341.5), (-246.4,-341.5), self))
        self.roads.append(Road(117, (-190.5,-341.5),(-246.4,-341.5), self))
        self.roads.append(Road(118, (53.6,-341.5),(-190.5,-341.5), self))
        self.roads.append(Road(119,  (89.2,-303.4),(53.6,-341.5), self))
        self.roads.append(Road(120,  (89.2,-241.1), (89.2,-303.4),self))
        self.roads.append(Road(121,  (89.2,-176.8),(89.2,-241.1), self))
        self.roads.append(Road(122,  (52.39,-141.2),(89.2,-176.8), self))
        self.roads.append(Road(127,  (89.2,-241),(178.98,-241), self))
        self.roads.append(Road(128,  (-180.1,-241),(89.2,-241), self))
        self.roads.append(Road(129,  (-218.5,-277.7),(-180.1,-241), self))
        self.roads.append(Road(130,  (-218.5,-312.5),(-218.5,-277.7), self))
        self.roads.append(Road(131,  (-218.5,-312.5),(-190.5,-341.5), self))
        self.roads.append(Road(132,  (-218.5,-312.5),(-246.4,-341.5), self))
        
        self.G.add_edges_from([(1, 2, {'weight': 252.4}), (2, 3, {'weight': 47.6}), (3, 4, {'weight': 93.5}), (4, 5, {'weight': 51.7}), (5, 6, {'weight': 106.3}), (5, 27, {'weight': 0}), (6, 7, {'weight': 101.6}), (7, 8, {'weight': 50.8}), (8, 9, {'weight': 399.6}), (8, 10, {'weight': 399.6}), (9, 11, {'weight': 0}), (10, 11, {'weight': 0}), (11, 24, {'weight': 57.4}), (9, 12, {'weight': 40.5}), (12, 13, {'weight': 51.9}), (13, 14, {'weight': 51.2}), (14, 15, {'weight': 32.9}), (15, 16, {'weight': 50.9}), (16, 17, {'weight': 73.29}), (16, 32, {'weight': 0}), (17, 31, {'weight': 0}), (31, 30, {'weight': 40.3}), (17, 18, {'weight': 55.9}), (18, 19, {'weight': 244.1}), (19, 20, {'weight': 52.14}), (20, 27, {'weight': 62.29}), (21, 22, {'weight': 64.29}), (22, 23, {'weight': 51.2}), (23, 25, {'weight': 336.19}), (23, 24, {'weight': 0}), (10, 24, {'weight': 38.6}), (24, 25, {'weight': 210.0}), (25, 26, {'weight': 26.2}), (32, 30, {'weight': 40.24}), (30, 29, {'weight': 34.8}), (28, 27, {'weight': 269.3}), (26, 1, {'weight': 51.47}), (31, 18, {'weight': 0}), (27, 6, {'weight': 0}), (28, 21, {'weight': 0}), (20, 21, {'weight': 0})])

        # invert edges
        self.G_inverse.add_edges_from([(102, 101, {'weight': 252.4}), (103, 102, {'weight': 47.6}), (104, 103, {'weight': 93.5}), (105, 104, {'weight': 51.7}), (106, 105, {'weight': 106.3}), (127, 105, {'weight': 0}), (107, 106, {'weight': 101.6}), (108, 107, {'weight': 50.8}), (109, 108, {'weight': 399.6}), (110, 108, {'weight': 399.6}), (111, 109, {'weight': 0}), (111, 110, {'weight': 0}), (124, 111, {'weight': 57.4}), (112, 109, {'weight': 40.5}), (113, 112, {'weight': 51.9}), (114, 113, {'weight': 51.2}), (115, 114, {'weight': 32.9}), (116, 115, {'weight': 50.9}), (117, 116, {'weight': 73.29}), (132, 116, {'weight': 0}), (131, 117, {'weight': 0}), (130, 131, {'weight': 40.3}), (118, 117, {'weight': 55.9}), (119, 118, {'weight': 244.1}), (120, 119, {'weight': 52.14}), (127, 120, {'weight': 62.29}), (121, 127, {'weight': 0}), (122, 121, {'weight': 64.29}), (123, 122, {'weight': 51.2}), (125, 123, {'weight': 336.19}), (124, 123, {'weight': 0}), (124, 110, {'weight': 38.6}), (125, 124, {'weight': 210.0}), (126, 125, {'weight': 26.2}), (130, 132, {'weight': 40.24}), (129, 130, {'weight': 34.8}), (127, 128, {'weight': 269.3}), (101, 126, {'weight': 51.47}), (118, 131, {'weight': 0}), (106, 127, {'weight': 0}), (112, 111,  {'weight': 0}), (121, 128,  {'weight': 0})])
    # def generate_traffic_signals(self, num_traffic_lights):
    #     for i in range(num_traffic_lights):
    #         self.traffic_lights.append(TrafficSignal(i, 0, {}, self))

    def generate_vehicle(self, num_vehicles):
        for i in range(num_vehicles):
            path = []
            while len(path) == 0:
                start = random.randint(1, 32)
                end = random.randint(1, 32)
                print(start, end)
                try:
                    path1 = nx.shortest_path(self.G, start, end)
                except:
                    path1 = []
                try:
                    start = start + 100
                    end = end + 100
                    path2 = nx.shortest_path(self.G_inverse, start, end)
                except:
                    path2 = []
                if len(path1) > 0 and len(path2) > 0:
                    path = min(path1, path2, key=len)
                elif len(path1) == 0 and len(path2) == 0:
                    path = []
                elif len(path1) == 0 and len(path2) > 0:
                    path = path2
                else:
                    path = path1
                if len(path) > 0:
                    print(path)
                    for j in range(len(self.roads)):
                        if start == self.roads[j].unique_id:
                            start_road = j

                    self.roads[start_road].vehicles.append(Vehicle(i, self, {"path": path}))
    
    def generate_schedule(self):
        self.schedule = RandomActivation(self)
        # for agent in self.traffic_lights:
        #     self.schedule.add(agent)
        for road in self.roads:
            for agent in road.vehicles:
                self.schedule.add(agent)
    
    def generate_agents(self, num_vehicles):
        self.generate_roads()
        self.generate_vehicle(num_vehicles)
        self.generate_schedule()

    def generate_model(self, num_vehicles):
        self.generate_agents(num_vehicles)
        self.generate_schedule()

    def vehicle_path(self):
        vehicle_positions = []
        for road in self.roads:
            for car in road.vehicles:
                x = road.start[0] + road.angle_cos * car.x
                y = road.start[1] + road.angle_sin * car.x
                # current_road = road.unique_id
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

