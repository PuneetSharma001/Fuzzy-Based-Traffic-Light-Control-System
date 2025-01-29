# Import necessary libraries
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import random
import matplotlib

matplotlib.use('TkAgg')

traffic_density = ctrl.Antecedent(np.arange(0, 101, 1), 'traffic_density')
green_light_duration = ctrl.Consequent(np.arange(0, 150, 1), 'green_light_duration')

traffic_density['low'] = fuzz.trimf(traffic_density.universe, [0, 0, 50])
traffic_density['medium'] = fuzz.trimf(traffic_density.universe, [20, 50, 80])
traffic_density['high'] = fuzz.trimf(traffic_density.universe, [50, 100, 100])

green_light_duration['short'] = fuzz.trimf(green_light_duration.universe, [0, 0, 40])
green_light_duration['medium'] = fuzz.trimf(green_light_duration.universe, [20, 60, 100])
green_light_duration['long'] = fuzz.trimf(green_light_duration.universe, [80, 120, 120])

rule1 = ctrl.Rule(traffic_density['low'], green_light_duration['short'])
rule2 = ctrl.Rule(traffic_density['medium'], green_light_duration['medium'])
rule3 = ctrl.Rule(traffic_density['high'], green_light_duration['long'])

traffic_control_system = ctrl.ControlSystem([rule1, rule2, rule3])
traffic_simulation = ctrl.ControlSystemSimulation(traffic_control_system)

traffic_simulation.input['traffic_density'] = 70
traffic_simulation.compute()
print(f"Single Test -> Traffic Density: 70, Green Light Duration: {traffic_simulation.output['green_light_duration']:.2f} seconds")

print("\nSimulated Results for Various Traffic Densities:")
densities = range(0, 101, 10)
durations = []

for density in densities:
    traffic_simulation.input['traffic_density'] = density
    traffic_simulation.compute()
    duration = traffic_simulation.output['green_light_duration']
    durations.append(duration)
    print(f"Traffic Density: {density}, Green Light Duration: {duration:.2f} seconds")

try:
    plt.figure()
    plt.plot(densities, durations, marker='o', linestyle='-', color='b')
    plt.title("Traffic Density vs Green Light Duration")
    plt.xlabel("Traffic Density (vehicles)")
    plt.ylabel("Green Light Duration (seconds)")
    plt.grid()
    plt.show()
except Exception as e:
    print(f"Error displaying graph: {e}")
    plt.savefig("traffic_density_vs_duration.png")
    print("Graph saved as 'traffic_density_vs_duration.png'. Check the file in your directory.")

print("\nReal-Time Simulation with Random Traffic Densities:")
for _ in range(10):
    random_density = random.randint(0, 100)
    traffic_simulation.input['traffic_density'] = random_density
    traffic_simulation.compute()
    random_duration = traffic_simulation.output['green_light_duration']
    print(f"Random Traffic Density: {random_density}, Green Light Duration: {random_duration:.2f} seconds")
