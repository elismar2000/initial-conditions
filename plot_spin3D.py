import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

from pygadgetreader import *

import sys

snapshot = sys.argv[1]
theta = np.deg2rad(float(sys.argv[2])) + np.pi/2 #position angle, em torno de z
phi = np.deg2rad(float(sys.argv[3])) #inclinacao, em torno de x no sentido negativo
inclination_axis = sys.argv[4] #x or y
initial_spin = sys.argv[5] #1 or -1


#Para a NGC2992:
# P.A = 32
# phi = -70
# ao redor de x
#initial spin = -1

#================================
#Defining the Arrow3D artist
#================================

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

#================================
#Reading positions of disk particles of the galaxy
#================================

pos_disk = readsnap(snapshot, 'pos', 'disk')
x_disk = pos_disk[:, 0]
y_disk = pos_disk[:, 1]
z_disk = pos_disk[:, 2]

vel_disk = readsnap(snapshot, 'vel', 'disk')

#================================
#Plotting the galaxy
#================================

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x_disk, y_disk, z_disk, ',', color='blue', alpha=0.5, zorder=1)
ax.set_xlabel('x (kpc)')
ax.set_ylabel('y (kpc)')
ax.set_zlabel('z (kpc)')
ax.set_aspect('equal')

#================================
#Plotting spin vector
#================================

if initial_spin == '1': v_ini = [0, 0, 1]
elif initial_spin == '-1': v_ini = [0, 0, -1]
else: print('initial_spin must be either 1 or -1')
v = v_ini

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

r = 5
spin = Arrow3D([0, r*x], [0, r*y], [0, r*z],
    mutation_scale=20, lw=7, arrowstyle="-|>", color="yellow", zorder=3)
ax.add_artist(spin)

factor = 50
for i in range(0, 100):
    a = Arrow3D([pos_disk[i, 0], vel_disk[i, 0]/factor], [pos_disk[i, 1], vel_disk[i, 1]/factor],
        [pos_disk[i, 2], vel_disk[i, 2]/factor], mutation_scale=10, lw=1.0, arrowstyle="-|>", color="r", zorder=2)
    ax.add_artist(a)

fig.text(0.02, 0.5, "Rotation around "+inclination_axis, fontsize=10)
fig.text(0.02, 0.45, "i = "+str(sys.argv[3]), fontsize=10)
fig.text(0.02, 0.40, "P.A = "+str(sys.argv[2]), fontsize=10)
fig.text(0.02, 0.35, "initial spin = "+str(v_ini), fontsize=10)
fig.text(0.02, 0.30, "final spin = "+str(v), fontsize=10)

plt.show()
