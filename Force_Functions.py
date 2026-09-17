
import numpy as np
import math

def F_Drive (omega, rover):
    if type(omega) != np.ndarray:
        raise Exception("omega must be a numpy array")

    if type(rover) != dict:
        raise Exception("rover must be a dictionary")