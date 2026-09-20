
import matplotlib.pyplot as plt
import numpy as np
import subfunctions as sf

stal_trq =170
nld_trq =  0
nld_spd = 3.8* sf.get_gear_ratio(speed_reducer)


max_w = nld_spd
w = np.linspace(0,max_w,1000)
t = stal_trq -w*(stal_trq-nld_trq)/nld_spd


pwr = -(nld_spd/stal_trq)*(t**2)+ nld_spd*t

fig, graphs = plt.subplots(nrows=3, ncols=1, figsize=(6, 8))

graphs[0].plot(t, w, color='red')
graphs[0].set_xlabel('Motor Shaft Torque (N/m)')
graphs[0].set_ylabel('Motor Shaft Speed (rad/s)')

graphs[1].plot(t,pwr, color='blue')
graphs[1].set_xlabel('Motor Shaft Torque (N/m)')
graphs[1].set_ylabel('Motor Power (W)')


graphs[2].plot(w,pwr, color='green')
graphs[2].set_xlabel('Motor Shaft Speed (rad/s)')
graphs[2].set_ylabel('Motor Power (W)')

# Clean up spacing so labels don't overlap
plt.tight_layout()

# Display the plots
plt.show()
