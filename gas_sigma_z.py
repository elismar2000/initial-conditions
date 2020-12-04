from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

from pygadgetreader import *

import sys

#=========================
#Inputs
#=========================

snapshot = sys.argv[1]

#=========================
#gas sigma(z)
#=========================

pos = readsnap(snapshot, 'pos', 'gas')
z = pos[:, 2]

mass = readsnap(snapshot, 'mass', 'gas')

sigma_z, z_edges = np.histogram(abs(z), bins=20, weights=mass)
z_bin = (z_edges[1] - z_edges[0])
z_edges += z_bin / 2

#=========================
#Fitting model
#=========================

def SigmaZ(z, z0, Mgas):
    sigma0 = Mgas / (4 * np.pi)
    return sigma0 / (np.cosh(z / z0)**2 * z0)

popt, popv = curve_fit(SigmaZ, z_edges[:-1], sigma_z / z_bin, p0=[0.4 * 0.7, 0.92])
best_z0, best_Mgas = popt[0], popt[1]

print('z0 = ', best_z0)
print('Mgas = ', best_Mgas)
# best_z0 = 0.4 * 0.7

plt.plot(z_edges[:-1], sigma_z / z_bin, '--')
plt.plot(z_edges[:-1], SigmaZ(z_edges[:-1], best_z0, best_Mgas))
plt.show()
