import matplotlib.pyplot as plt

from numpy import *
from pygadgetreader import *

from tables import *
import sys

#The goal of this code is to plot the same particles around galactic center
#in two different snapshots to see where do they go

snapshot1 = sys.argv[1]
snap = sys.argv[2]
snapshot2 = sys.argv[3]

snapshot1 = str(snapshot1)
snap = int(snap)
snapshot2 = str(snapshot2)

pos_disk = readsnap(snapshot1, 'pos', 'disk')
x_disk = pos_disk[:, 0]
y_disk = pos_disk[:, 1]
z_disk = pos_disk[:, 2]

pos_gas = readsnap(snapshot1, 'pos', 'gas')
x_gas = pos_gas[:, 0]
y_gas = pos_gas[:, 1]
z_gas = pos_gas[:, 2]

pos_bulge = readsnap(snapshot1, 'pos', 'bulge')
x_bulge = pos_bulge[:, 0]
y_bulge = pos_bulge[:, 1]
z_bulge = pos_bulge[:, 2]

x = concatenate((x_disk, x_gas, x_bulge))
y = concatenate((y_disk, y_gas, y_bulge))
z = concatenate((z_disk, z_gas, z_bulge))

pos = np.stack((x, y, z))

pid_disk = readsnap(snapshot1, 'pid', 'disk')
pid_gas = readsnap(snapshot1, 'pid', 'gas')
pid_bulge = readsnap(snapshot1, 'pid', 'bulge')
id = np.concatenate((pid_disk, pid_gas, pid_bulge))

mins = '/home/elismar/Documentos/Fisica/IC/GalMer/inflow/mins_Gadget/galmer-like_sim_test2_minima.h5'
h5file = open_file(mins, mode='r')
table = h5file.root.potential.readout

xmin1 = np.array([j['xmin1'] for j in table.iterrows()])
ymin1 = np.array([j['ymin1'] for j in table.iterrows()])
zmin1 = np.array([j['zmin1'] for j in table.iterrows()])
min1 = np.array([xmin1, ymin1, zmin1])

xmin2 = np.array([j['xmin2'] for j in table.iterrows()])
ymin2 = np.array([j['ymin2'] for j in table.iterrows()])
zmin2 = np.array([j['zmin2'] for j in table.iterrows()])
min2 = np.array([xmin2, ymin2, zmin2])

def dist(point1, point2):
    d = np.sqrt(np.sum(np.square(point1[i] - point2[i]) for i in range(3)))
    return d

dist1 = np.array([dist(pos[:, i], min1[:, snap]) for i in range(len(pos[0]))])
dist2 = np.array([dist(pos[:, i], min2[:, snap]) for i in range(len(pos[0]))])

mask1 = dist1 < 1.0
mask2 = dist2 < 1.0

id_mask1 = np.isin(id, id[mask1])
id_mask2 = np.isin(id, id[mask2])

pos_disk = readsnap(snapshot2, 'pos', 'disk')
x_disk = pos_disk[:, 0]
y_disk = pos_disk[:, 1]

pos_gas = readsnap(snapshot2, 'pos', 'gas')
x_gas = pos_gas[:, 0]
y_gas = pos_gas[:, 1]

pos_bulge = readsnap(snapshot2, 'pos', 'bulge')
x_bulge = pos_bulge[:, 0]
y_bulge = pos_bulge[:, 1]

x2 = concatenate((x_disk, x_gas, x_bulge))
y2 = concatenate((y_disk, y_gas, y_bulge))

pid_disk2 = readsnap(snapshot2, 'pid', 'disk')
pid_gas2 = readsnap(snapshot2, 'pid', 'gas')
pid_bulge2 = readsnap(snapshot2, 'pid', 'bulge')
id2 = np.concatenate((pid_disk2, pid_gas2, pid_bulge2))

id_mask1_2 = np.isin(id2, id[mask1])
id_mask2_2 = np.isin(id2, id[mask2])

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x[id_mask1], y[id_mask1], 'b,')
ax.plot(x[id_mask2], y[id_mask2], 'k,')
ax.plot(xmin1[snap], ymin1[snap], 'y*')
ax.plot(xmin2[snap], ymin2[snap], 'rX')

ax.plot(x2[id_mask1_2], y2[id_mask1_2], 'b,')
ax.plot(x2[id_mask2_2], y16[id_mask2_2], 'k,')
ax.plot(xmin1[snap + 1], ymin1[snap + 1], 'y*')
ax.plot(xmin2[snap + 1], ymin2[snap + 1], 'rX')
