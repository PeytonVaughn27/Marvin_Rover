import numpy as np

rover = {
    "wheel_assembly": {
        "wheel": {
            "radius": 0.30,        # m
            "mass": 1.0,           # kg (one wheel)
        },
        "speed_reducer": {
            "type": "reverted",
            "diam_pinion": 0.04,   # m
            "diam_gear": 0.07,     # m
            "mass": 1.5,           # kg
        },
        "motor": {
            "torque_stall": 170,   # N-m
            "torque_noload": 0,    # N-m
            "speed_noload": 3.80,  # rad/s
            "mass": 5.0,           # kg (one motor)
            "effcy_tau": np.array([0, 10, 20, 40, 70, 165]),           # N-m
            "effcy": np.array([0, 0.55, 0.75, 0.71, 0.50, 0.05]),      # unitless
        },
    },
    "chassis": {"mass": 659},         # kg
    "science_payload": {"mass": 75},  # kg
    "power_subsys": {"mass": 90},     # kg
}

planet = {"g": 3.72}  # m/s^2 (Mars)

end_event = {
    "max_distance": 50,    # m
    "max_time": 5000,      # s
    "min_velocity": 0.01,  # m/s
}