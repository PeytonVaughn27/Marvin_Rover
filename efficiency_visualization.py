from scipy.interpolate import interp1d
from dictionary import rover
import matplotlib.pyplot as plt
import numpy as np

'''plot motor torque vs. efficiency'''

efficiency_tor = rover["wheel_assembly"]["motor"]["effcy_tau"] #vector
efficiency = rover["wheel_assembly"]["motor"]["effcy"] #vector

#make efficiency torque function
eta_fun = interp1d(efficiency_tor, efficiency, kind = 'cubic')

tau_eval = np.linspace(np.min(efficiency_tor), np.max(efficiency_tor), 100)
effcy_eval = eta_fun(tau_eval)

plt.plot(efficiency_tor, efficiency, '* ', label="Data")
plt.plot(tau_eval, effcy_eval, label="Cubic spline")
plt.xlabel("Torque(Nm)")
plt.ylabel("Efficiency")
plt.title('Motor Efficiency vs. Torque')
plt.legend()
plt.show()
