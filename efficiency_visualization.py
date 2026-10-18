from scipy.interpolate import interp1d
from dictionary import rover
import matplotlib.pyplot as plt
import numpy as np

'''plot motor torque vs. efficiency'''

efficiency_tor = rover["wheel_assembly"]["motor"]["effcy_tau"] #vector
efficiency = rover["wheel_assembly"]["motor"]["effcy"] #vector

#make efficiency torque function
eta_fun = interp1d(efficiency_tor, efficiency, kind = 'cubic')

x = np.linspace(0, 165, 200)

plt.plot(efficiency_tor, efficiency, marker="o", linestyle="", label="Data")
plt.plot(x, eta_fun(x), label="Cubic spline")
plt.xlabel("Torque(Nm)")
plt.ylabel("Efficiency")
plt.legend()
plt.show()
