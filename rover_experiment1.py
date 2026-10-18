import subfunctions as sf
import matplotlib.pyplot as plt
from itertools import count
from math import erf
from scipy.interpolate import interp1d
from scipy.integrate import solve_ivp
import numpy as np

from define_experiment import experiment1
from dictionary import rover, planet

experiment, end_event = experiment1()
rover_output = sf.simulate_rover(rover, planet, experiment, end_event)

fig, axs = plt.subplots(3)
fig.subplots_adjust(hspace=0.5)
axs[0].set_title('Position of Marvin Rover')
axs[0].plot(rover_output['Time'], rover_output['position'])
axs[1].set_title('Velocity of Marvin Rover')
axs[1].plot(rover_output['Time'], rover_output['velocity'])
axs[2].set_title('Power of Marvin Rover')
axs[2].plot(rover_output['Time'], rover_output['power'])
plt.show()
