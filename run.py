from simulation import Simulation
import matplotlib.pyplot as plt

sim = Simulation()

sim.generate_model(
    num_vehicles=1
)

for i in range(5000):
    sim.step()
    # print(sim.vehicle_path())

# plot route
sim.datacollector.collect(sim)
data = sim.datacollector.get_model_vars_dataframe()
sorted(data, key=lambda x: x[2])
print(data)
data.to_json("data.json")
x = []
y = []

for j in range(2):
    x_i = []
    y_i = []
    for i in range(len(data)):
        try:
            x_i.append(data.iloc[i]["data"][j][1])
            y_i.append(data.iloc[i]["data"][j][2])
        except:
            pass
    x.append(x_i)
    y.append(y_i)

# print(x)

plt.scatter(x[0], y[0], s=0.5)
plt.show()
