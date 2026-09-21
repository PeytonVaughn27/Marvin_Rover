import numpy as np
import matplotlib.pyplot as plt
import subfunctions as sf
from scipy.optimize import root_scalar

rover = {
    "wheel_assembly": {
         "wheel": { "radius": 0.3 , "mass": 1 },
         "speed_reducer": { "type": "reverted", "mass": 1.5, "diam_pinion": 0.04, "diam_gear": 0.07},
         "motor": { "torque_stall": 170, "torque_noload":0, "speed_noload": 3.8, "mass": 5 }},
    "chassis": { "mass": 659 },
    "science_payload": { "mass": 75 },
    "power_subsys": { "mass": 90 },}

planet = {"g": 3.72}

crr = 0.15
slope_array_deg = np.linspace(-15,35,25)
mass = sf.get_mass(rover)
slope_rad = np.radians([])
omega_max = np.array([])
v_max = np.array([])
Fd = 6*(170*sf.get_gear_ratio(rover["wheel_assembly"]["speed_reducer"])) / rover["wheel_assembly"]["wheel"]["radius"]

print(sf.get_gear_ratio(rover["wheel_assembly"]["speed_reducer"]))

for i in range(len(slope_array_deg)):
    slope_rad = np.append(slope_rad, np.radians(slope_array_deg[i]))
    terrain_angle = np.ndarray([])
    terrain_angle = np.append(terrain_angle, slope_rad[i])
    omega_max = np.append(omega_max, root_scalar(lambda x: sf.F_net(x, terrain_angle, rover, planet, crr), bracket=[0, rover["wheel_assembly"]["motor"]["speed_noload"]], method="bisect").root)
    v_max = np.append(v_max, (omega_max[i]/ sf.get_gear_ratio(rover["wheel_assembly"]["speed_reducer"])) * rover["wheel_assembly"]["wheel"]["radius"])

plt.plot(slope_array_deg, v_max)
plt.xlabel('Slope (degrees)')
plt.ylabel('Maximum Speed (m/s)')
plt.title('Terrain Angle vs Maximum Speed')
plt.grid(True)
plt.show()