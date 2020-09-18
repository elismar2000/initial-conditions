from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
from pygadgetreader import *

import sys

#=========================
#inputs
#=========================

snapshot = sys.argv[1]
z0       = sys.argv[2]
z0_gas   = sys.argv[3]
Rd       = sys.argv[4]

z0     = float(z0)
z0_gas = float(z0_gas)
Rd     = float(Rd)

#=========================
#reading gas positions and masses
#=========================

pos_gas = readsnap(snapshot, 'pos', 'gas')
x_gas = pos_gas[:, 0]
z_gas = pos_gas[:, 2]

mass_gas = readsnap(snapshot, 'mass', 'gas')

#=========================
#how much gas between -z0_gas and z0_gas?
#=========================

z0_gas *= z0
mask = (z_gas < z0_gas) & (z_gas > -z0_gas)
mass_inside = mass_gas[mask]

print('z0_gas = ', z0_gas)
print('mass fraction inside = ', np.sum(mass_inside) / np.sum(mass_gas))

#==========================
#plotting
#==========================

plt.plot(x_gas, z_gas, ',')
plt.plot(x_gas[mask], z_gas[mask], ',', color='orange')
plt.plot(np.array([Rd, Rd]), np.array([0, z0_gas]), '-', color='red')
plt.plot(np.array([0, Rd]), np.array([0, 0]), '-', color='yellow')
plt.show()
