from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

from pygadgetreader import *
#=============================

def SigmaZ(z, z0, Mgas):
    sigma0 = Mgas / (4 * np.pi)
    return sigma0 / (np.cosh(z / z0)**2 * z0)

Rd_20 = []
Rd_30 = []
Rd_35 = []
Rd_40 = []
for Rd in [20, 30, 35, 40]:
    for snapshot in range(0, 12):
        s = '%04d' % (snapshot,)
        snapshot = '/home/elismar/Documentos/Fisica/IC/Gadget3/gas_Rd_z0_relation/Rd_' + str(Rd) + '/snapshot_' + str(s)

        pos = readsnap(snapshot, 'pos', 'gas')
        z = pos[:, 2]

        mass = readsnap(snapshot, 'mass', 'gas')

        sigma_z, z_edges = np.histogram(abs(z), bins=20, weights=mass)
        z_bin = (z_edges[1] - z_edges[0])
        z_edges += z_bin / 2

        popt, popv = curve_fit(SigmaZ, z_edges[:-1], sigma_z / z_bin, p0=[0.4 * 0.7, 0.92])
        best_z0, best_Mgas = popt[0], popt[1]

        print('simulation = ', Rd)
        print('snapshot = ', s)
        print('z0 = ', best_z0)
        print('Mgas = ', best_Mgas)

        if Rd == 20: Rd_20.append(best_z0)
        if Rd == 30: Rd_30.append(best_z0)
        if Rd == 35: Rd_35.append(best_z0)
        if Rd == 40: Rd_40.append(best_z0)

time = np.arange(0, 12, 1) * 5 #Myr
plt.plot(time, Rd_20, '--', color='darkorange', label='Rd_ini = 2.0 Kpc')
plt.plot(time, Rd_30, '--', color='purple', label='Rd_ini = 3.0 Kpc')
plt.plot(time, Rd_35, '--', color='lime', label='Rd_ini = 3.5 Kpc')
plt.plot(time, Rd_40, '--', color='gold', label='Rd_ini = 4.0 Kpc')
plt.xlabel(r'$time\ [Myr]$')
plt.ylabel(r'$z_{0_{gas}}\ [0.7\ kpc]$')
plt.legend()
plt.show()
