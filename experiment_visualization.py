import scipy
import d



alpha_fun = interp1d(alpha_dist, alpha_deg, kind = 'cubic', fill_value='extrapolate') 
#fit the cubic spline