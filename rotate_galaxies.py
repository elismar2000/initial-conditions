import numpy as np
import matplotlib.pyplot as plt

from numpy import *
from pygadgetreader import *
from snapwrite import process_input, write_snapshot

import sys

#-------------------------------------------------------
snapshot = sys.argv[1]
output = sys.argv[2]
theta = sys.argv[3]
phi = sys.argv[4]
#-------------------------------------------------------

header = readheader(snapshot, 'header')
Nhalo = header['ndm']
Ndisk = header['ndisk']

pos_halo = readsnap(snapshot, 'pos', 'dm')
x_halo = pos_halo[:, 0]
y_halo = pos_halo[:, 1]
z_halo = pos_halo[:, 2]

pos_disk = readsnap(snapshot, 'pos', 'disk')
x_disk = pos_disk[:, 0]
y_disk = pos_disk[:, 1]
z_disk = pos_disk[:, 2]

vel_halo = readsnap(snapshot, 'vel', 'dm')
vx_halo = vel_halo[:, 0]
vy_halo = vel_halo[:, 1]
vz_halo = vel_halo[:, 2]

vel_disk = readsnap(snapshot, 'vel', 'disk')
vx_disk = vel_disk[:, 0]
vy_disk = vel_disk[:, 1]
vz_disk = vel_disk[:, 2]

#--------------------------------------------------------
plot = False
if plot:
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')
    ax1.plot(x_disk, y_disk, z_disk, '.', zdir='z')
#--------------------------------------------------------

pos_halo = np.vstack((x_halo, y_halo, z_halo))
pos_disk = np.vstack((x_disk, y_disk, z_disk))
vel_halo = np.vstack((vx_halo, vy_halo, vz_halo))
vel_disk = np.vstack((vx_disk, vy_disk, vz_disk))

theta = float(theta)
phi = float(phi)
print('theta: ', theta)
print('phi: ', phi)

Rx = np.array([[1, 0, 0], [0, np.cos(theta), -np.sin(theta)], [0, np.sin(theta), np.cos(theta)]])
Rz = np.array([[np.cos(phi), -np.sin(phi), 0], [np.sin(phi), np.cos(phi), 0], [0, 0, 1]])

pos_disk = np.matmul(Rx, pos_disk)
pos_disk = np.matmul(Rz, pos_disk)

pos_halo = np.matmul(Rx, pos_halo)
pos_halo = np.matmul(Rz, pos_halo)

vel_halo = np.matmul(Rx, vel_halo)
vel_halo = np.matmul(Rz, vel_halo)

vel_disk = np.matmul(Rx, vel_disk)
vel_disk = np.matmul(Rz, vel_disk)

x_disk = pos_disk[0]
y_disk = pos_disk[1]
z_disk = pos_disk[2]

x_halo = pos_halo[0]
y_halo = pos_halo[1]
z_halo = pos_halo[2]

vx_disk = vel_disk[0]
vy_disk = vel_disk[1]
vz_disk = vel_disk[2]

vx_halo = vel_halo[0]
vy_halo = vel_halo[1]
vz_halo = vel_halo[2]

#---------------------------------------------------------
if plot:
    ax1.plot(x_disk, y_disk, z_disk, '.', zdir='z')
    plt.show()
#---------------------------------------------------------

m_halo = readsnap(snapshot, 'mass', 'dm')
m_disk = readsnap(snapshot, 'mass', 'disk')

x = concatenate((x_halo, x_disk))
y = concatenate((y_halo, y_disk))
z = concatenate((z_halo, z_disk))
vx = concatenate((vx_halo, vx_disk))
vy = concatenate((vy_halo, vy_disk))
vz = concatenate((vz_halo, vz_disk))

pos = np.column_stack((x, y, z))
pos.shape = (-1, 1)

vel = np.column_stack((vx, vy, vz))
vel.shape = (-1, 1)

m = concatenate((m_halo, m_disk))

N = Nhalo + Ndisk
ids = arange(0, N, 1)

write_snapshot(n_part=[0, Nhalo, Ndisk, 0, 0, 0], from_text=False, outfile=output, data_list=[pos, vel, ids, m])
