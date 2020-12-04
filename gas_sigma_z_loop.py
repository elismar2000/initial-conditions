from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

from pygadgetreader import *

import sys

#=============================

def SigmaZ(z, z0, Mgas):
    sigma0 = Mgas / (4 * np.pi)
    return sigma0 / (np.cosh(z / z0)**2 * z0)

z_004 = []
z_010 = []
z_013 = []
z_018 = []
for z0_gas in [0.4, 1.0, 1.3, 1.8]:
    for snapshot in range(0, 12):
        s = '%04d' % (snapshot,)
        snapshot = '/home/elismar/Documentos/Fisica/IC/Gadget3/gas_disk_z0_tests/z_0' + str(z0_gas) + '/snapshot_' + str(s)

        pos = readsnap(snapshot, 'pos', 'gas')
        z = pos[:, 2]

        mass = readsnap(snapshot, 'mass', 'gas')

        sigma_z, z_edges = np.histogram(abs(z), bins=20, weights=mass)
        z_bin = (z_edges[1] - z_edges[0])
        z_edges += z_bin / 2

        popt, popv = curve_fit(SigmaZ, z_edges[:-1], sigma_z / z_bin, p0=[0.4 * 0.7, 0.92])
        best_z0, best_Mgas = popt[0], popt[1]

        print('simulation = ', z0_gas)
        print('snapshot = ', s)
        print('z0 = ', best_z0)
        print('Mgas = ', best_Mgas)

        if z0_gas == 0.4: z_004.append(best_z0)
        if z0_gas == 1.0: z_010.append(best_z0)
        if z0_gas == 1.3: z_013.append(best_z0)
        if z0_gas == 1.8: z_018.append(best_z0)

time = np.arange(0, 12, 1) * 5 #Myr
plt.plot(time, z_004, '--', color='darkorange', label='0.4')
plt.plot(time, z_010, '--', color='purple', label='1.0')
plt.plot(time, z_013, '--', color='lime', label='1.3')
plt.plot(time, z_018, '--', color='gold', label='1.8')
plt.xlabel(r'$time\ [Myr]$')
plt.ylabel(r'$z_{0_{gas}}\ [0.7\ kpc]$')
plt.legend()
plt.show()
