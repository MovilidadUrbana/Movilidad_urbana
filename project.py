from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import math
import random


class Car(Agent):
    """A schedule that activates each agent once per step, in random order."""
    def __init__(self):
        self.agent_buffer = []

    def add(self, agent):
        """Add an agent to the schedule."""
        self.agent_buffer.append(agent)

    def remove(self, agent):
        """Remove all instances of a given agent from the schedule."""
        while agent in self.agent_buffer:
            self.agent_buffer.remove(agent)

    def get_num_agents(self):
        return len(self.agent_buffer)

    def get_num_agents_by_status(self, status):
        count = 0
        for agent in self.agent_buffer:
            if agent.status == status:
                count += 1
        return count

    def step(self):
        for agent in self.agent_buffer:
            agent.activate()
        self.agent_buffer = []

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.x = 0
        self.y = 0
        self.speed = 0
        self.direction = 0

    def move(self):
        self.x += self.speed * self.model.speed_multiplier * \
            self.model.cos_lookup_table[self.direction]
        self.y += self.speed * self.model.speed_multiplier * \
            self.model.sin_lookup_table[self.direction]

    def step(self):
        self.move()


class TrafficLight(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.x = 0
        self.y = 0
        self.direction = 0
        self.color = 0

    def step(self):
        pass

    def get_color(self):
        return self.color
    
    def set_color(self, color):
        self.color = color
    
    def get_direction(self):
        return self.direction

    def set_direction(self, direction):
        self.direction = direction
    
    def get_position(self):
        return (self.x, self.y)
    
    def set_position(self, x, y):
        self.x = x
        self.y = y
    

class TrafficModel(Model):
    def __init__(self, width, height, speed_multiplier):
        self.width = width
        self.height = height
        self.speed_multiplier = speed_multiplier
        self.cos_lookup_table = [0] * 360
        self.sin_lookup_table = [0] * 360
        self.schedule = None
        self.traffic_lights = []
        self.cars = []

    def generate_cos_sin_lookup_table(self):
        for i in range(360):
            self.cos_lookup_table[i] = math.cos(math.radians(i))
            self.sin_lookup_table[i] = math.sin(math.radians(i))

    def generate_traffic_lights(self, num_traffic_lights):
        for i in range(num_traffic_lights):
            self.traffic_lights.append(TrafficLight(i, self))

    def generate_cars(self, num_cars):
        for i in range(num_cars):
            self.cars.append(Car(i, self))

    def generate_schedule(self):
        self.schedule = RandomActivation(self)
        for agent in self.traffic_lights:
            self.schedule.add(agent)
        for agent in self.cars:
            self.schedule.add(agent)

    def generate_agents(self, num_traffic_lights, num_cars):
        self.generate_traffic_lights(num_traffic_lights)
        self.generate_cars(num_cars)

    def generate_model(self, width, height, speed_multiplier, num_traffic_lights, num_cars):
        self.generate_cos_sin_lookup_table()
        self.generate_agents(num_traffic_lights, num_cars)
        self.generate_schedule()

    def step(self):
        self.schedule.step()

class RandomActivation(Model):
    """A model that has some number of agents.
    Each agent has a single activation event that happens independently of
    any other agent's activation events.  The model ends when all agents have
    been activated.
    """
    def __init__(self, num_agents=100):
        self.num_agents = num_agents
        self.schedule = RandomActivationSchedule()
        self.running = True
        self.datacollector = DataCollector(
            {"Activated": lambda m: m.schedule.get_num_agents_by_status(True)})

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    def run_model(self, n):
        """
        Run the model for n steps.
        """
        for i in range(n):
            self.step()


class RandomActivationSchedule(object):
    """A schedule that activates each agent once per step, in random order."""
    def __init__(self):
        self.agent_buffer = []

    def add(self, agent):
        """Add an agent to the schedule."""
        self.agent_buffer.append(agent)

    def remove(self, agent):
        """Remove all instances of a given agent from the schedule."""
        while agent in self.agent_buffer:
            self.agent_buffer.remove(agent)

    def get_num_agents(self):
        return len(self.agent_buffer)

    def get_num_agents_by_status(self, status):
        count = 0
        for agent in self.agent_buffer:
            if agent.status == status:
                count += 1
        return count

    def step(self):
        for agent in self.agent_buffer:
            agent.activate()
        self.agent_buffer = []

def main():
    model = TrafficModel(100, 100, 1)
    model.generate_model(100, 100, 1, 1, 1)
    model.run_model(100)
    print(model.datacollector.get_model_vars_dataframe())
