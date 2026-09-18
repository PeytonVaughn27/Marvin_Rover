
from math import erf

import numpy as np

def get_mass(rover):
    if type(rover) != dict:
        raise TypeError("Input is not a dict, fuck you")
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
        raise TypeError("Input is not a dict, fuck you")
    
    if type(speed_reducer["type"]) != str:
        raise TypeError(f"Just.\n fuck you")

    if (speed_reducer["type"]).lower() != "reverted":
        raise TypeError("Type is not reverted, fuck you")
    
    ratio = (speed_reducer["diam_gear"]/speed_reducer["diam_pinion"])**2
    return ratio

def tau_dcmotor(omega, motor):
    if (type(omega) != float and type(omega) != int) and omega.ndim > 1:
        raise TypeError("Input is not a 1D vector or scalar, fuck you")

    if type(motor) != dict:
        raise TypeError("Input is not a dict, fuck you")

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
        raise TypeError("Input is not a dict, fuck you")

    if type(omega) == list:
        raise TypeError("Input is not a 1D vector or scalar, fuck you")

    if (type(omega) != float and type(omega) != int) and omega.ndim > 1:
        raise TypeError("Input is not a 1D vector or scalar, fuck you")

    tau = tau_dcmotor(omega, rover["wheel_assembly"]["motor"])
    ng = get_gear_ratio(rover["wheel_assembly"]["speed_reducer"])
    Fd = np.array([])
    for i in tau:
        Fd = np.append(Fd,6*(i*ng) / rover["wheel_assembly"]["wheel"]["radius"])

    if type(Fd) != np.ndarray:
        raise TypeError("Output is not a np.ndarray, fuck you")
    
    return Fd

def F_gravity(terrain_angle, rover, planet):
    
    if type(terrain_angle) != np.ndarray:
        raise TypeError("Input is not a np.ndarray, fuck you")
    
    if type(rover) != dict:
        raise TypeError("Input is not a dict, fuck you")

    if type(planet) != dict:
        raise TypeError("Input is not a dict, fuck you")
    
    Force_g = np.array([])
    for angle in terrain_angle:
        if angle < -75  or angle > 75:
            raise ValueError(f"Terrain angle {angle} out of array {terrain_angle} is out of bounds, fuck you")
        
        mass = get_mass(rover)


        Force_g = np.append(Force_g, mass * planet["gravity"] * np.sin(np.radians(angle)))
    
    return Force_g                              

def F_rolling(omega, terrain_angle, rover, planet, crr):
    if (type(omega) != float and type(omega) != int) and omega.ndim > 1:
        raise TypeError("Input is not a 1D vector or scalar, fuck you")
    
    if type(terrain_angle) != np.ndarray:
        raise TypeError("Input is not a np.ndarray, fuck you")
    
    if type(rover) != dict:
        raise TypeError("Input is not a dict, fuck you")

    if type(planet) != dict:
        raise TypeError("Input is not a dict, fuck you")
    
    if type(crr) != float and type(crr) != int:
        raise TypeError("Input is not a float or int, fuck you")

    if crr < 0:
        raise ValueError("Crr is negative, fuck you")

    v = omega * rover["wheel_assembly"]["wheel"]["radius"]
    Frr = np.array([])
    for i in range(len(terrain_angle)):
        angle = terrain_angle[i]
        if angle < -75  or angle > 75:
            raise ValueError(f"Terrain angle {angle} out of array {terrain_angle} is out of bounds, fuck you")

        Frr = np.append(Frr, erf(40 * v.astype(float)) * crr * get_mass(rover) * planet["gravity"] * np.cos(np.radians(angle)) / 6)
    return Frr