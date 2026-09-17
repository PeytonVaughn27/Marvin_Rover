
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
    if type(speed_reducer["type"]) != str:
        raise TypeError(f"Just.\n fuck you")

    if (speed_reducer["type"]).lower() == "reverted":
        raise TypeError("Type is not reverted, fuck you")

    if type(speed_reducer) != dict:
        raise TypeError("Input is not a dict, fuck you")
    else:
        ratio = (speed_reducer["diam_gear"]/speed_reducer["diam_pinion"])**2
    return ratio

def tau_dcmotor(omega, motor):
    if type(omega) != np.ndarray or int or float:
        raise TypeError("Input is not a vector or scalar, fuck you")

    if type(motor) != dict:
        raise TypeError("Input is not a dict, fuck you")

    if omega < motor["speed_noload"]:
        tau = motor["torque_stall"] - (((motor["torque_stall"]- motor["torque_noload"]) / motor['speed_noload']) * omega)
    elif omega >= motor["speed_noload"]:
        tau = 0
    elif omega < 0:
        tau = motor["torque_stall"]
    else:
        raise Exception("Something went wrong")
    
    return tau

def F_Drive(omega, rover):
    if type(rover) != dict:
        raise TypeError("Input is not a dict, fuck you")

    if type(omega) != np.ndarray:
        raise TypeError("Input is not a np.ndarray, fuck you")

    
def F_gravity(terrain_angle, rover, planet):
    
    if type(terrain_angle) != np.ndarray:
        raise TypeError("Input is not a np.ndarray, fuck you")
    
    if type(rover) != dict:
        raise TypeError("Input is not a dict, fuck you")

    if type(planet) != dict:
        raise TypeError("Input is not a dict, fuck you")
    
    for i in terrain_angle:
        if i < -75 * np.pi/180 or i > 75 * np.pi/180:
            raise ValueError("Terrain angle is out of bounds, fuck you")
        
        angle = i
        mass = get_mass(rover)

        Force_g = mass * planet["gravity"] * np.sin(angle)  
    
    return Force_g                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
