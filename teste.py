from pygadgetreader import *
import matplotlib.pyplot as plt
import numpy as np
import glob

v = glob.glob('/home/elismar/Documentos/Fisica/IC/queorbita/orbits_3rd_attempt/orb*/snapshot_*')
v.sort()

pos = readsnap(v[0], 'pos', 'gas')

x = pos[:, 0]
z = pos[:, 2]

mask_ngc2992 = x < 50
mask_ngc2993 = x > 50

id_gas = readsnap(v[0], 'pid', 'gas')

ngc2992 = np.isin(id_gas, id_gas[mask_ngc2992])
ngc2993 = np.isin(id_gas, id_gas[mask_ngc2993])

plt.scatter(x[ngc2992], z[ngc2992], color='purple', marker='.')
plt.scatter(x[ngc2993], z[ngc2993], color='khaki', marker='.')
plt.show()
