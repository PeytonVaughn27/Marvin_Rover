
from itertools import count
from math import erf
from scipy.interpolate import interp1d
from scipy.integrate import solve_ivp
import numpy as np

#from dictionary import rover, planet, end_event
#from define_experiment import experiment1

def is_scalar_or_1d(var):
    print(type(var))
    if (type(var) != float and type(var) != int) and var.ndim > 1:
        raise Exception("Input is not a 1D vector or scalar.")
    else:
        pass

def is_dict(var):
    if type(var) != dict:
        raise Exception("Input is not a dictionary")
    else:
        pass

def is_scalar(var):
    if (type(var) != float and type(var) != int) and type(var) != np.float64 and type(var) != np.int64:
        raise Exception("Input is not a scalar.")
    else:
        pass

def is_1d(var):
    if (type(var) != float and type(var) != int) and var.ndim != 1:
            raise Exception("Input is not a 1D vector.")
    else:
        pass
    
def is_eql_length(var1, var2):
    if len(var1) != len(var2):
        raise ValueError("Input arrays are not the same length.")


def get_mass(rover):
    if type(rover) != dict:
        raise TypeError("Input is not a dict.")
    else:
        m_wheels = (rover["wheel_assembly"]["wheel"]["mass"]*6)
        m_spd_rdcr = (rover["wheel_assembly"]["speed_reducer"]["mass"]*6)
        m_motor = (rover["wheel_assembly"]["motor"]["mass"]*6)
        m_chassis = (rover["chassis"]["mass"])
        m_payload = (rover["science_payload"]["mass"])
        m_pwr_systm = (rover["power_subsys"]["mass"])

        m_total = m_wheels + m_spd_rdcr + m_motor+ m_chassis + m_payload + m_pwr_systm
        return m_total

def get_gear_ratio(speed_reducer):
    if type(speed_reducer) != dict:
        raise TypeError("Input is not a dict.")
    
    if type(speed_reducer["type"]) != str:
        raise TypeError(f"Just.\n")

    if (speed_reducer["type"]).lower() != "reverted":
        raise TypeError("Type is not reverted.")
    
    ratio = (speed_reducer["diam_gear"]/speed_reducer["diam_pinion"])**2
    return ratio

def tau_dcmotor(omega, motor):
    if (type(omega) != float and type(omega) != int) and omega.ndim > 1:
        raise TypeError("Input is not a 1D vector or scalar.")

    if type(motor) != dict:
        raise TypeError("Input is not a dict.")

    if np.isscalar(omega):
        if (omega <= motor["speed_noload"]) and (omega >= 0):
            tau = motor["torque_stall"] - (((motor["torque_stall"]- motor["torque_noload"]) / motor['speed_noload']) * omega)
        elif (omega > motor["speed_noload"]):
            tau = 0
        elif (omega < 0):
            tau = motor["torque_stall"]
        else:
            raise Exception("Something went wrong")
    else:
        tau = np.array([])
        for i in range(len(omega)):
            if (omega[i] <= motor["speed_noload"]) and (omega[i] >= 0):
                tau = np.append(tau, motor["torque_stall"] - (((motor["torque_stall"]- motor["torque_noload"]) / motor['speed_noload']) * omega[i]))
            elif (omega[i] > motor["speed_noload"]):
                tau = np.append(tau, 0)
            elif (omega[i] < 0):
                tau = np.append(tau, motor["torque_stall"])
            else:
                raise Exception("Something went wrong")

    return tau

def F_drive(omega, rover):
    if type(rover) != dict:
        raise TypeError("Input is not a dict.")

    if type(omega) == list:
        raise TypeError("Input is not a 1D vector or scalar.")

    if (type(omega) != float and type(omega) != int) and omega.ndim > 1:
        raise TypeError("Input is not a 1D vector or scalar.")

    tau = tau_dcmotor(omega, rover["wheel_assembly"]["motor"])
    ng = get_gear_ratio(rover["wheel_assembly"]["speed_reducer"])
    Fd = np.array([])
    if not np.isscalar(omega):
        for i in tau:
            Fd = np.append(Fd,6*(i*ng) / rover["wheel_assembly"]["wheel"]["radius"])
    else:
        Fd = 6*(tau*ng) / rover["wheel_assembly"]["wheel"]["radius"]
        if not np.isscalar(Fd):
            Fd = Fd[0]

    return Fd

def F_gravity(terrain_angle, rover, planet):
    if (type(terrain_angle) != float and type(terrain_angle) != int) and terrain_angle.ndim > 1:
        raise TypeError("Input is not a np.ndarray.")

    if np.isscalar(terrain_angle):
        terrain_angle = np.array([terrain_angle])
    
    if type(rover) != dict:
        raise TypeError("Input is not a dict.")

    if type(planet) != dict:
        raise TypeError("Input is not a dict.")
    
    Force_g = np.array([])
    for angle in terrain_angle:
        if angle < -75  or angle > 75:
            raise ValueError(f"Terrain angle is outside of +75 or -75.")
            
        mass = get_mass(rover)
        Force_g = np.append(Force_g, -mass * planet["g"] * np.sin(np.radians(angle)))
        
    return Force_g                              

def F_rolling(omega, terrain_angle, rover, planet, crr):
    if (type(omega) != float and type(omega) != int) and omega.ndim > 1:
        raise TypeError("Input is not a 1D vector or scalar.")
    
    if (type(terrain_angle) != float and type(terrain_angle) != int) and terrain_angle.ndim > 1:
        raise TypeError("Input is not a 1D vector or scalar.")
    
    if not np.isscalar(omega):
        if len(terrain_angle) != len(omega):
            raise ValueError("Input arrays are not the same length.")
    
    if type(rover) != dict:
        raise TypeError("Input is not a dict.")

    if type(planet) != dict:
        raise TypeError("Input is not a dict.")
    
    if type(crr) != float and type(crr) != int:
        raise TypeError("Input is not a float or int.")

    if crr < 0:
        raise ValueError("Crr is negative.")

    if not np.isscalar(terrain_angle):
        for i in range(len(terrain_angle)):
            angle = terrain_angle[i]
            if angle < -75  or angle > 75:
                raise ValueError(f"Terrain angle {angle} out of array {terrain_angle} is out of bounds.")
        
    if type(omega) == float or type(omega) == int:
        v = (omega / get_gear_ratio(rover["wheel_assembly"]["speed_reducer"])) * rover["wheel_assembly"]["wheel"]["radius"]
        frr =-erf(40 * v) * crr * get_mass(rover) * planet["g"] * np.cos(np.radians(terrain_angle))
        if not np.isscalar(frr):
            frr = frr[0]
    else:
        frr = np.array([])
        for i in range(len(omega)):
            v = (omega[i] / get_gear_ratio(rover["wheel_assembly"]["speed_reducer"])) * rover["wheel_assembly"]["wheel"]["radius"]
            frr = np.append(frr, -erf(40 * v) * crr * get_mass(rover) * planet["g"] * np.cos(np.radians(terrain_angle[i])))
        
    return frr
    
def F_net(omega, terrain_angle, rover, planet, crr):

    if (type(omega) != float and type(omega) != int) and omega.ndim > 1:
        raise TypeError("Input is not a 1D vector or scalar.")

    if (type(terrain_angle) != float and type(terrain_angle) != int) and terrain_angle.ndim > 1:
        raise TypeError("Input is not a 1D vector or scalar.")

    if not np.isscalar(omega):
        if len(terrain_angle) != len(omega):
            raise ValueError("Input arrays are not the same length.")

    if type(rover) != dict:
        raise TypeError("Input is not a dict.")

    if type(planet) != dict:
        raise TypeError("Input is not a dict.")


    if type(crr) != float and type(crr) != int :
        raise Exception(f"Crr is not a scalar.")

    if crr < 0:
        raise ValueError("Crr is negative.")

    if not np.isscalar(omega):
        Fnet = np.array([])
        for i in range(len(omega)):
            Fnet = np.append(Fnet,F_rolling(omega, terrain_angle, rover, planet, crr)[i]+F_gravity(terrain_angle, rover, planet)[i]+F_drive(omega, rover)[i])
    else:
        Fnet = float(F_rolling(omega, terrain_angle, rover, planet, crr))+(F_gravity(terrain_angle, rover, planet)[0])+float(F_drive(omega, rover))

    return Fnet

def motorW(v, rover):
    '''This is motorW, this returns the angular velocity of the motor.'''
    if (type(v) != float and type(v) != int) and v.ndim > 1:
        raise Exception("Input is not a 1D vector or scalar.")
    if type(rover) != dict:
        raise Exception("Input is not a dict")
    w = get_gear_ratio(rover["wheel_assembly"]["speed_reducer"])*v/rover["wheel_assembly"]["wheel"]["radius"]
    return w

def rover_dynamics(t,y,rover,planet,experiment):
    '''This is rover dynamics, here we help you find the acceleration and velocity.'''
    is_scalar(t)
    is_1d(y)
    is_dict(rover)
    is_dict(planet)
    is_dict(experiment)

    alpha_dist = experiment["alpha_dist"]
    alpha_deg = experiment["alpha_deg"]
    alpha_fun = interp1d(alpha_dist, alpha_deg, kind = 'cubic', fill_value='extrapolate') 
    
    pos = y[1].item()
    vel = y[0].item()

    terrain_angle = np.array([alpha_fun(pos)])
    w = motorW(vel,rover)
    crr = experiment["Crr"]
    f = F_net(w,terrain_angle, rover,planet,crr)
    
    m = get_mass(rover)

    accel = f/m
    
    dydt = np.array([accel,vel])

    return dydt

def mechpower(v,rover):
    '''v is 1D array or scalar/float/int and rover is a dict. The output is a 1D array or scalar/float/int'''
    if (not isinstance(v, (int, float, np.ndarray))) or (not isinstance(rover, dict)):
        raise Exception("v must be a scalar or 1D array and rover must be a dictionary")

    #elif isinstance(v, (int, float)) and isinstance(rover, dict):
    P = tau_dcmotor(motorW(v, rover), rover["wheel_assembly"]["motor"]) * motorW(v, rover)

    #return power function should match the format of V inout (array,int, or float)
    #beware of units 
    return P  

def battenergy(t,v,rover):
    '''t is 1D array and v is 1D array or scalar/float/int and rover is a dict. 
    The output is a 1D array or scalar/float/int of the energy consumed by the battery over time.'''
    
    #check shit
    if not isinstance(v, (int, float, np.ndarray)):
        raise Exception("v must be a scalar or 1D array")
    
    if not isinstance(rover, dict):
        raise Exception("rover must be a dictionary")

    if not isinstance(t, (np.ndarray)):
        raise Exception("t must be a 1D array")

    if isinstance(v, (np.ndarray)) and (len(t) != len(v)):
        raise Exception("t and v must be the same length")

    p= mechpower(v,rover) #vector or scalar 
    w = motorW(v,rover) # same as v
    tau= tau_dcmotor(w,rover["wheel_assembly"]["motor"]) # vector
    
    # E_motor = []
    # for time in t:
    #     if time < 0:
    #         raise Exception("Time cannot be negative.")
    #     else:  
    #         E_motor += np.trapz(p, time) #vector or scalar
    
    # calculate efficiency of the motor based on torque and efficiency curve
    efficiency_tor = rover["wheel_assembly"]["motor"]["effcy_tau"] #vector
    efficiency = rover["wheel_assembly"]["motor"]["effcy"] #vector
    eta_fun = interp1d(efficiency_tor, efficiency, kind = 'cubic',fill_value='extrapolate')
    
    P_battery = p / (eta_fun(tau)) #vector or scalar
    
    # 3. Scalar input check
    if isinstance(v, (int, float)):
        return P_battery * t
    
    else:
        E_battery = np.trapezoid(P_battery,t)
        
    #vector input
    # E_battery = 0.0
    # for i in range(len(t)-1):
    #     E_battery += np.trapz(P_battery[i:i+2], t[i:i+2])
     
    # print(f"Energy consumed by the battery over time: {6* E_battery}")
    # print(f"Power consumed by the battery over time: {P_battery}")
    # print(f"Torque consumed by the motor over time: {tau}")
    # print(f"Efficiency of the motor over time: {eta}")
    # print(f"Mechanical power consumed by the motor over time: {p}")
    # print(f"Angular velocity of the motor over time: {w}")
    # print(f"Velocity of the rover over time: {v}")
    # print(f"Time array: {t}")
       
    return 6 *E_battery

def end_of_mission_event(end_event):
    """
    Defines an event that terminates the mission simulation. Mission is over
    when rover reaches a certain distance, has moved for a maximum simulation 
    time or has reached a minimum velocity.            
    """
    
    mission_distance = end_event['max_distance']
    mission_max_time = end_event['max_time']
    mission_min_velocity = end_event['min_velocity']
    
    # Assume that y[1] is the distance traveled
    distance_left = lambda t,y: mission_distance - y[1]
    distance_left.terminal = True
    
    time_left = lambda t,y: mission_max_time - t
    time_left.terminal = True
    
    velocity_threshold = lambda t,y: y[0] - mission_min_velocity;
    velocity_threshold.terminal = True
    velocity_threshold.direction = -1
    
    # terminal indicates whether any of the conditions can lead to the
    # termination of the ODE solver. In this case all conditions can terminate
    # the simulation independently.
    
    # direction indicates whether the direction along which the different
    # conditions is reached matters or does not matter. In this case, only
    # the direction in which the velocity treshold is arrived at matters
    # (negative)
    
    events = [distance_left, time_left, velocity_threshold]
    
    return events

def simulate_rover(rover, planet, experiment, end_event):
    '''Returns simulated rover telemetry data with input for rover, planet, experiment, and end_event dictionaries.'''
    is_dict(rover)
    is_dict(planet)
    is_dict(experiment)
    is_dict(end_event)

    f = lambda t,y: rover_dynamics(t,y,rover,planet,experiment)

    t_0 = experiment['time_range'][0]
    t_end = end_event['max_time']
    mission_events = end_of_mission_event(end_event)
    Dist_left = mission_events[0]
    Time_left = mission_events[1]
    Vel_thresh = mission_events[2]

    sol = solve_ivp(f, (t_0,t_end), experiment['initial_conditions'], method = 'RK45', events = [Dist_left, Time_left, Vel_thresh])
    rover_output = rover
    rover_output['Time'] = sol.t
    rover_output['completion_time']= sol.t_events
    rover_output['velocity'] = sol.y[0]
    rover_output['position'] = sol.y[1]
    rover_output['distance_traveled'] = sol.y[1][-1] - sol.y[1][0]
    rover_output['max_velocity'] = np.max(sol.y[0])
    rover_output['average_velocity'] = np.mean(sol.y[0])
    rover_output['power']= mechpower(sol.y[0],rover)*6
    rover_output['energy']= battenergy(sol.t,sol.y[0],rover)
    rover_output['energy_per_distance']= rover_output['energy']/rover_output['distance_traveled']
    
    return rover_output



# print(get_mass(rover))
# print(get_gear_ratio(rover["wheel_assembly"]["speed_reducer"]))
# print(tau_dcmotor(0, rover["wheel_assembly"]["motor"]))
# print(F_drive(0, rover))
# print(F_gravity(0, rover, planet))
# print(F_rolling(0, 0, rover, planet, 0.01))
# print(F_net(0, 0, rover, planet, 0.01))
# print(mechpower(0, rover))
# print(battenergy(np.array([0,1]), np.array([0,0]), rover))
# print(end_of_mission_event(end_event))
# print(rover_dynamics(0, np.array([0,0]), rover, planet, experiment1()[0]))
# print(motorW(0, rover))
# experiment, end_event = experiment1()
# rover_output = simulate_rover(rover, planet, experiment, end_event)
# print(rover_output)