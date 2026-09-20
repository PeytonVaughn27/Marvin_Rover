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

Crr_array = np.linspace(0.01,0.5,25)

slope_array_deg = np.linspace(-15,35,25)

CRR, SLOPE = np.meshgrid(Crr_array, slope_array_deg)

VMAX = np.zeros(np.shape(CRR), dtype = float)

N = np.shape(CRR)[0]
for i in range(N):
    #for j in range(N):
        #Crr_sample = float(CRR[i,j])
        #slope_sample = float(SLOPE[i,j])
        #VMAX[i,j] = ... # here you put code to find the max speed at Crr_sample and slope_sample
    for j in range(N):

        Crr_sample = float(CRR[i,j])
        slope_sample = float(SLOPE[i,j])

        def net_force(omega):
            return sf.F_net(omega, slope_sample, rover, planet, Crr_sample)

        result = root_scalar(net_force, bracket=[0, 3.8])

        if result.converged:
            omega_max = result.root

            gear_ratio = sf.get_gear_ratio(
                rover["wheel_assembly"]["speed_reducer"]
            )
            wheel_radius = rover["wheel_assembly"]["wheel"]["radius"]

            VMAX[i,j] = (omega_max / gear_ratio) * wheel_radius
        else:
            VMAX[i,j] = np.nan    