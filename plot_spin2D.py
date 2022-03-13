import numpy as np
from matplotlib import pyplot as plt

from pygadgetreader import *

import subprocess
import sys

snapshot = sys.argv[1]
theta    = np.deg2rad(float(sys.argv[2])) + np.pi/2 #input = position angle
phi      = np.deg2rad(float(sys.argv[3])) #inclinacao
inclination_axis = sys.argv[4]


# subprocess.Popen(["python", "rotate_galaxies.py", "../galstep/galstep/ngc2992.ic",
#     snapshot, sys.argv[2], sys.argv[3], inclination_axis])

#================================
#Reading particle's positions
#================================

pos_disk = readsnap(snapshot, 'pos', 'disk')
x_disk = pos_disk[:, 0]
y_disk = pos_disk[:, 1]
z_disk = pos_disk[:, 2]

#================================
#Defining components of spin vector
#================================

r = 10

v = [0, 0, -1]

Rz = np.array([[np.cos(theta), -np.sin(theta), 0], [np.sin(theta), np.cos(theta), 0], [0, 0, 1]])

if inclination_axis == 'x':
    Rx = np.array([[1, 0, 0], [0, np.cos(phi), -np.sin(phi)], [0, np.sin(phi), np.cos(phi)]])
    v = np.matmul(Rx, v)
    v = np.matmul(Rz, v)


if inclination_axis == 'y':
    Ry = np.array([[np.cos(phi), 0, np.sin(phi)], [0, 1, 0], [-np.sin(phi), 0, np.cos(phi)]])
    v = np.matmul(Ry, v)
    v = np.matmul(Rz, v)

x = v[0]
y = v[1]
z = v[2]

print('spin vector = ', [x, y, z])

#================================
#PLotting
#================================

fig = plt.figure()

ax1 = fig.add_subplot(131)
ax1.plot(x_disk, y_disk, ',', zorder=1)
ax1.arrow(0, 0, r*x, r*y, width = 0.05, head_width = 1.0, color='red', zorder=2)
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_aspect('equal')

ax2 = fig.add_subplot(132)
ax2.plot(z_disk, x_disk, ',', zorder=1)
ax2.arrow(0, 0, r*z, r*x, width = 0.05, head_width = 1.0, color='red', zorder=2)
ax2.set_xlabel('z')
ax2.set_ylabel('x')
ax2.set_aspect('equal')

ax3 = fig.add_subplot(133)
ax3.plot(z_disk, y_disk, ',', zorder=1)
ax3.arrow(0, 0, r*z, r*y, width = 0.05, head_width = 1.0, color='red', zorder=2)
ax3.set_xlabel('z')
ax3.set_ylabel('y')
ax3.set_aspect('equal')

plt.show()
