from scipy.interpolate import interp1d
from define_experiment import experiment1
import numpy as np
import matplotlib.pyplot as plt


ex, end = experiment1()
alpha_dist = ex["alpha_dist"]
alpha_deg = ex["alpha_deg"]

alpha_fun = interp1d(alpha_dist, alpha_deg, kind = 'cubic', fill_value='extrapolate') 
#fit the cubic spline

x = np.linspace(start=0, stop = 1000, num= 100)


plt.plot(x, alpha_fun(x), marker="*",linestyle="")
plt.xlabel("Distance(m)")
plt.ylabel("Angle(Deg)")


plt.show()
