import numpy as np
import matplotlib.pyplot as plt

from numpy import *
from pygadgetreader import *
from snapwrite import process_input, write_snapshot

import sys

#-------------------------------------------------------
snapshot = sys.argv[1] #o snashot contendo a galaxia que eh pra ser rodada
output = sys.argv[2] #o nome do output que a gente vai querer
theta = sys.argv[3] #o angulo theta, em radianos
sigma = sys.argv[4] #o angulo sigma, em radianos
phi = sys.argv[5] #o angulo phi, em radianos
#-------------------------------------------------------

header = readheader(snapshot, 'header')
Ngas = header['ngas']
Nhalo = header['ndm']
Ndisk = header['ndisk']
Nbulge = header['nbulge']

#positions:
pos_gas = readsnap(snapshot, 'pos', 'gas')
x_gas = pos_gas[:, 0]
y_gas = pos_gas[:, 1]
z_gas = pos_gas[:, 2]

pos_halo = readsnap(snapshot, 'pos', 'dm')
x_halo = pos_halo[:, 0]
y_halo = pos_halo[:, 1]
z_halo = pos_halo[:, 2]

pos_disk = readsnap(snapshot, 'pos', 'disk')
x_disk = pos_disk[:, 0]
y_disk = pos_disk[:, 1]
z_disk = pos_disk[:, 2]

pos_bulge = readsnap(snapshot, 'pos', 'bulge')
x_bulge = pos_bulge[:, 0]
y_bulge = pos_bulge[:, 1]
z_bulge = pos_bulge[:, 2]

pos_gas = np.vstack((x_gas, y_gas, z_gas))
pos_halo = np.vstack((x_halo, y_halo, z_halo))
pos_disk = np.vstack((x_disk, y_disk, z_disk))
pos_bulge = np.vstack((x_bulge, y_bulge, z_bulge))

#velocities:
vel_gas = readsnap(snapshot, 'vel', 'gas')
vx_gas = vel_gas[:, 0]
vy_gas = vel_gas[:, 1]
vz_gas = vel_gas[:, 2]

vel_halo = readsnap(snapshot, 'vel', 'dm')
vx_halo = vel_halo[:, 0]
vy_halo = vel_halo[:, 1]
vz_halo = vel_halo[:, 2]

vel_disk = readsnap(snapshot, 'vel', 'disk')
vx_disk = vel_disk[:, 0]
vy_disk = vel_disk[:, 1]
vz_disk = vel_disk[:, 2]

vel_bulge = readsnap(snapshot, 'vel', 'bulge')
vx_bulge = vel_bulge[:, 0]
vy_bulge = vel_bulge[:, 1]
vz_bulge = vel_bulge[:, 2]

vel_gas = np.vstack((vx_gas, vy_gas, vz_gas))
vel_halo = np.vstack((vx_halo, vy_halo, vz_halo))
vel_disk = np.vstack((vx_disk, vy_disk, vz_disk))
vel_bulge = np.vstack((vx_bulge, vy_bulge, vz_bulge))

#--------------------------------------------------------
plot = False
if plot:
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')
    ax1.plot(x_disk, y_disk, z_disk, '.', zdir='z')
#--------------------------------------------------------

#theta --> girar ao redor de x
#sigma --> girar ao redor de y
#phi --> girar ao redor de z

#o theta ou sigma sao equivalentes ao theta do sistema esferico. Uma vez que usa um, nao precisa do outro
#porque o que importa eh que estamos realizando uma rotacao a partir de z

theta = float(theta)
sigma = float(sigma)
phi = float(phi)
print('theta: ', theta)
print('sigma: ', sigma)
print('phi: ', phi)

if (theta != 0) and (sigma != 0):
    raise Exception('Either theta or sigma must be zero')

Rx = np.array([[1, 0, 0], [0, np.cos(theta), -np.sin(theta)], [0, np.sin(theta), np.cos(theta)]])
Ry = np.array([[np.cos(sigma), 0, np.sin(sigma)], [0, 1, 0], [-np.sin(sigma), 0, np.cos(sigma)]])
Rz = np.array([[np.cos(phi), -np.sin(phi), 0], [np.sin(phi), np.cos(phi), 0], [0, 0, 1]])

#Girando ao redor do eixo x
if theta != 0:
    pos_gas = np.matmul(Rx, pos_gas)
    pos_gas = np.matmul(Rz, pos_gas)

    pos_halo = np.matmul(Rx, pos_halo)
    pos_halo = np.matmul(Rz, pos_halo)

    pos_disk = np.matmul(Rx, pos_disk)
    pos_disk = np.matmul(Rz, pos_disk)

    pos_bulge = np.matmul(Rx, pos_bulge)
    pos_bulge = np.matmul(Rz, pos_bulge)


    vel_gas = np.matmul(Rx, vel_gas)
    vel_gas = np.matmul(Rz, vel_gas)

    vel_halo = np.matmul(Rx, vel_halo)
    vel_halo = np.matmul(Rz, vel_halo)

    vel_disk = np.matmul(Rx, vel_disk)
    vel_disk = np.matmul(Rz, vel_disk)

    vel_bulge = np.matmul(Rx, vel_bulge)
    vel_bulge = np.matmul(Rz, vel_bulge)

#Girando ao redor do eixo y
if sigma != 0:
    pos_gas = np.matmul(Ry, pos_gas)
    pos_gas = np.matmul(Rz, pos_gas)

    pos_halo = np.matmul(Ry, pos_halo)
    pos_halo = np.matmul(Rz, pos_halo)

    pos_disk = np.matmul(Ry, pos_disk)
    pos_disk = np.matmul(Rz, pos_disk)

    pos_bulge = np.matmul(Ry, pos_bulge)
    pos_bulge = np.matmul(Rz, pos_bulge)


    vel_gas = np.matmul(Ry, vel_gas)
    vel_gas = np.matmul(Rz, vel_gas)

    vel_halo = np.matmul(Ry, vel_halo)
    vel_halo = np.matmul(Rz, vel_halo)

    vel_disk = np.matmul(Ry, vel_disk)
    vel_disk = np.matmul(Rz, vel_disk)

    vel_bulge = np.matmul(Ry, vel_bulge)
    vel_bulge = np.matmul(Rz, vel_bulge)

#---------------------------------------------------------
if plot:
    ax1.plot(x_disk, y_disk, z_disk, '.', zdir='z')
    plt.show()
#---------------------------------------------------------

x_gas = pos_gas[0]
y_gas = pos_gas[1]
z_gas = pos_gas[2]

x_halo = pos_halo[0]
y_halo = pos_halo[1]
z_halo = pos_halo[2]

x_disk = pos_disk[0]
y_disk = pos_disk[1]
z_disk = pos_disk[2]

x_bulge = pos_bulge[0]
y_bulge = pos_bulge[1]
z_bulge = pos_bulge[2]


vx_gas = vel_gas[0]
vy_gas = vel_gas[1]
vz_gas = vel_gas[2]

vx_halo = vel_halo[0]
vy_halo = vel_halo[1]
vz_halo = vel_halo[2]

vx_disk = vel_disk[0]
vy_disk = vel_disk[1]
vz_disk = vel_disk[2]

vx_bulge = vel_bulge[0]
vy_bulge = vel_bulge[1]
vz_bulge = vel_bulge[2]

x = concatenate((x_gas, x_halo, x_disk, x_bulge))
y = concatenate((y_gas, y_halo, y_disk, y_bulge))
z = concatenate((z_gas, z_halo, z_disk, z_bulge))
vx = concatenate((vx_gas, vx_halo, vx_disk, vx_bulge))
vy = concatenate((vy_gas, vy_halo, vy_disk, vy_bulge))
vz = concatenate((vz_gas, vz_halo, vz_disk, vz_bulge))

pos = np.column_stack((x, y, z))
pos.shape = (-1, 1)

vel = np.column_stack((vx, vy, vz))
vel.shape = (-1, 1)

m_gas = readsnap(snapshot, 'mass', 'gas')
m_halo = readsnap(snapshot, 'mass', 'dm')
m_disk = readsnap(snapshot, 'mass', 'disk')
m_bulge = readsnap(snapshot, 'mass', 'bulge')
m = concatenate((m_gas, m_halo, m_disk, m_bulge))

u = readsnap(snapshot, 'u' ,'gas')
rho = readsnap(snapshot, 'rho', 'gas')
hsml = np.zeros(Ngas)

N = Ngas + Nhalo + Ndisk + Nbulge
ids = arange(0, N, 1)

write_snapshot(n_part=[Ngas, Nhalo, Ndisk, Nbulge, 0, 0], from_text=False, outfile=output, data_list=[pos, vel, ids, m, u, rho, hsml])
