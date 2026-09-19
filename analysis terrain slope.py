import numpy as np
import matplotlib.pyplot as plt
import subfunctions as sf

rover = {
    "wheel_assembly": {
         "wheel": { "radius": 0.3 , "mass": 1 },
         "speed_reducer": { "type": "reverted", "mass": 1.5, "diam_pinion": 0.04, "diam_gear": 0.07},
         "motor": { "torque_stall": 170, "torque_noload":0, "speed_noload": 3.8, "mass": 5 }},
    "chassis": { "mass": 659 },
    "science_payload": { "mass": 75 },
    "power_subsys": { "mass": 90 },}

planet = {"gravity": 3.72}

crr = 0.15
slope_array_deg = np.linspace(-15,35,25)
mass = sf.get_mass(rover)
omega = rover["wheel_assembly"]["motor"]["speed_noload"]
slope_rad = np.radians([])
F_net = np.array([])
v_max = np.array([])

for i in range(len(slope_array_deg)):
    slope_rad = np.append(slope_rad, np.radians(slope_array_deg[i]))
    F_net = np.append(F_net, sf.get_net_force(omega, slope_rad[i], rover, planet, crr))


plt.plot(slope_array_deg, v_max)
plt.xlabel('Slope (degrees)')
plt.ylabel('Maximum Speed (m/s)')
plt.title('Effect of Terrain Slope on Maximum Speed')
plt.grid(True)
plt.show()