
from math import erf
from scipy.interpolate import interp1d
from scipy.integrate import solve_ivp
import numpy as np

def is_scalar_or_1d(var):
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
    if (type(var) != float and type(var) != int):
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
    '''Here at mech power, we calculate the instantaneous power using the motor torque and shaft rotation speed.'''
    is_scalar_or_1d(v)
    is_dict(rover)

    
    motor = rover["wheel_assembly"]["motor"]
    mtr_w = motorW(v,rover)

    p = tau_dcmotor(mtr_w,motor) * mtr_w
    return p

def battenergy(t,v,rover):
    is_1d(t)
    is_1d(v)
    is_dict(rover)
    is_eql_length(t,v)

    p= mechpower(v,rover)
    w = motorW(v,rover)
    tau= tau_dcmotor(w,rover)

    E =1

    return E

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
    if rover is not dict or planet is not dict or experiment is not dict or end_event is not dict:
        raise TypeError("Input is not a dict")

    f = lambda t,y: rover_dynamics(t,y,rover,planet,experiment)

    t_0 = experiment['time_range'][0]
    t_end = experiment['time_range'][-1]

    sol = solve_ivp(f, (t_0,t_end), experiment['initial_conditions'], method = 'BDF')

    rover_output = rover
    rover_output['velocity'] = sol.y[0]
    rover_output['position'] = sol.y[1]

    return rover_output