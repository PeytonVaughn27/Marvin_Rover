import numpy as np
import matplotlib.pyplot as plt
from define_edl_system import define_edl_system_1
from subfunctions_EDL import simulate_edl
from define_planet import define_planet
from define_mission_events import define_mission_events

def area (radius):
    '''Calculate the area of the parachute'''
    return np.pi * radius**2
    
def get_forces(mass, diameter, drag_coefficient, speed, g=3.72, air_density=0.015):
    '''Calculate the forces acting on the rover during descent'''
    radius = diameter / 2
    area = area(radius)
    drag_force = 0.5 * air_density * area * drag_coefficient * speed**2
    weight = mass * g
    buoyancy = air_density * g * area * 0.1  #picked .1 for small volume
    net_force = weight - drag_force - buoyancy
    return net_force, drag_force, weight

def return_time (t):
    '''Calculate the time it took for the simulation to run'''
    return t[-1]

def return_speed (Y):
    '''Calculate the terminal velocity'''
    vel_edl_term = Y[0, -1]
    vel_rov_rel_term = Y[5, -1]
    rover_touchdown_vel = vel_edl_term + vel_rov_rel_term
    return abs(rover_touchdown_vel)

def return_success (edl_system, alt_edl_term, rover_speed_term):
    '''Check if the simulation was successful'''
    if  (rover_speed_term <= 1) and (alt_edl_term >= 4.5):
        return 1
    else:
        return 0

time_sim = []
final_speed = []
success_list = []  

diameters = np.arange(14.0, 19.5, 0.5)
mars = define_planet()
mission_events = define_mission_events()
tmax = 4000  # picked random large number to set a cap for simultaion time

for d in diameters:
    #Initial values
    edl_system = define_edl_system_1()
    edl_system['altitude'] = 11000          
    edl_system['velocity'] = -590          
    edl_system['rocket']['on'] = False       
    edl_system['parachute']['deployed'] = True  
    edl_system['parachute']['ejected'] = False   
    edl_system['heat_shield']['ejected'] = False
    edl_system['sky_crane']['on'] = False        
    edl_system['speed_control']['on'] = False   
    edl_system['position_control']['on'] = False
    edl_system['rover']['on_ground'] = False    
    

    edl_system['parachute']['diameter'] = d
    
    t, Y, edl_system = simulate_edl(edl_system, mars, mission_events, tmax, False, use_Cd_mod=0)
    
    t_term = return_time(t)
    alt_edl_term = Y[1, -1]
    rover_speed_term = return_speed(Y)
    is_successful = return_success(edl_system, alt_edl_term, rover_speed_term)
    
    time_sim.append(t_term)
    final_speed.append(rover_speed_term)
    success_list.append(is_successful)

fig, axs = plt.subplots(3, 1, figsize=(8, 12), sharex=True)
 
    
axs[0].plot(diameters, time_sim, marker='o', linestyle='-', color='b')
axs[0].set_ylabel('Simulated Time (s)')
axs[0].set_title('Rover Descent simulation')
axs[0].grid(True)  

axs[1].plot(diameters, final_speed, marker='s', linestyle='-', color='r')
axs[1].set_ylabel('Terminal Speed (m/s)')
axs[1].grid(True)

axs[2].plot(diameters, success_list, marker='^', linestyle='--', color='g')
axs[2].set_ylabel('Landing Success\n(1 = Success, 0 = Failure)')
axs[2].set_xlabel('Parachute Diameter (m)')
axs[2].set_yticks([0, 1]) # Ensures y-axis only shows 0 and 1
axs[2].grid(True)

plt.tight_layout()
plt.show()