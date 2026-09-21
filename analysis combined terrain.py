from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import subfunctions as sf
from scipy.optimize import root_scalar # found online, might change if it doesnt work as well as the in class root fidinding methods


#create dict/ variables to test values with
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


#make meshgrid of Crr and slope values to test
Crr_array = np.linspace(0.01,0.5,25)

slope_array_deg = np.linspace(-15,35,25)

CRR, SLOPE = np.meshgrid(Crr_array, slope_array_deg)

VMAX = np.zeros(np.shape(CRR), dtype = float)

N = np.shape(CRR)[0]

for i in range(N):
    for j in range(N):

        Crr_sample = float(CRR[i,j])
        slope_sample = float(SLOPE[i,j])

#code to find the max speed at Crr_sample and slope_sample

        def net_force(omega):
            return sf.F_net(omega, slope_sample, rover, planet, Crr_sample)

        f_LOW= net_force(0)
        f_HIGH= net_force(3.8)
        
        # if the sign changes betweeen the two bounds then execute the following code
        if f_LOW * f_HIGH <= 0:
            
            result = root_scalar(net_force, bracket=[0, 3.8])

            if result.converged:
                omega_max = result.root

            #change the angular velocity to tangential V m/s
                gear_ratio = sf.get_gear_ratio(
                    rover["wheel_assembly"]["speed_reducer"]
                )
                wheel_radius = rover["wheel_assembly"]["wheel"]["radius"]

                VMAX[i,j] = (omega_max / gear_ratio) * wheel_radius
            else:
                VMAX[i,j] = np.nan    
        else:
            VMAX[i,j] = np.nan

figure = plt.figure()
ax = figure.add_subplot(111, projection='3d')


ax.plot_surface(CRR, SLOPE, VMAX)                
ax.set_xlabel('CRR')
ax.set_ylabel('Slope (degrees)')
ax.set_zlabel('Maximum Speed (m/s)')
ax.view_init(elev = 15, azim = 45)
plt.show()