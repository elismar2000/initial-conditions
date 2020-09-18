from astropy.table import Table
import matplotlib.pyplot as plt
import numpy as np

from pygadgetreader import *

from snapwrite import process_input, write_snapshot

import sys

#================================
#U and rho vectors for SPH particles and reading GalMer snapshot
#================================

snapshot = '/home/elismar/Documentos/Fisica/IC/simulations_ICs/ICs/galmer_galaxies/gal_col.ini'
u = readsnap(snapshot, 'u', 'gas')
rho = readsnap(snapshot, 'rho', 'gas')

#taking only half of the vectors, once I'm constructing just one galaxy
u = u[0:20000]
rho = rho[0:20000]

t_path = sys.argv[1]
t_path = str(t_path)

snapshot = sys.argv[2]
snapshot = int(snapshot)

t = Table.read(t_path, snapshot)

#===============================
#Setting masks for galaxies and particle types
#===============================

gal1 = t['GAL'] == 1

gas = t['P_TYPE'][gal1] == 0
star = t['P_TYPE'][gal1] == 1
dm = t['P_TYPE'][gal1] == 2

#==============================
#Collecting positions of particles
#==============================

h = 1.0 #value of HubbleParam on param_file
lf = h

x_gas = t['X'][gal1][gas] * lf
y_gas = t['Y'][gal1][gas] * lf
z_gas = t['Z'][gal1][gas] * lf

x_star = t['X'][gal1][star][0:48000] * lf
y_star = t['Y'][gal1][star][0:48000] * lf
z_star = t['Z'][gal1][star][0:48000] * lf

x_bulge = t['X'][gal1][star][48000:60000] * lf
y_bulge = t['Y'][gal1][star][48000:60000] * lf
z_bulge = t['Z'][gal1][star][48000:60000] * lf

x_dm = t['X'][gal1][dm] * lf
y_dm = t['Y'][gal1][dm] * lf
z_dm = t['Z'][gal1][dm] * lf

#==================================
#Collecting velocities of particles
#==================================

vx_gas = t['VX'][gal1][gas]
vy_gas = t['VY'][gal1][gas]
vz_gas = t['VZ'][gal1][gas]

vx_star = t['VX'][gal1][star][0:48000]
vy_star = t['VY'][gal1][star][0:48000]
vz_star = t['VZ'][gal1][star][0:48000]

vx_bulge = t['VX'][gal1][star][48000:60000]
vy_bulge = t['VY'][gal1][star][48000:60000]
vz_bulge = t['VZ'][gal1][star][48000:60000]

vx_dm = t['VX'][gal1][dm]
vy_dm = t['VY'][gal1][dm]
vz_dm = t['VZ'][gal1][dm]

#================================
#Collecting masses of particles
#================================

mf = 2.25 * h / 10.0

m_gas = t['MASS'][gal1][gas] * mf

m_star = t['MASS'][gal1][star][0:48000] * mf

m_bulge = t['MASS'][gal1][star][48000:60000] * mf

print('star particles = ', m_star.shape)
print('bulge particles = ', m_bulge.shape)

m_dm = t['MASS'][gal1][dm] * mf

#================================
#Concatenating vectors for different galaxy components
#================================

m = np.concatenate((m_gas, m_dm, m_star, m_bulge))
x = np.concatenate((x_gas, x_dm, x_star, x_bulge))
y = np.concatenate((y_gas, y_dm, y_star, y_bulge))
z = np.concatenate((z_gas, z_dm, z_star, z_bulge))
vx = np.concatenate((vx_gas, vx_dm, vx_star, vx_bulge))
vy = np.concatenate((vy_gas, vy_dm, vy_star, vy_bulge))
vz = np.concatenate((vz_gas, vz_dm, vz_star, vz_bulge))

#=================================
#Stacking position and velocity vectors
#=================================

pos = np.column_stack((x, y, z))
pos.shape = (-1, 1)

vel = np.column_stack((vx, vy, vz))
vel.shape = (-1, 1)

#==================================
#number of particles, ids and hsml
#==================================

Ngas = 20000
Ndm = 40000
Nstar = 48000
Nbulge = 12000
N = Ngas + Ndm + Nstar + Nbulge
ids  = np.arange(0, N, 1)
hsml = np.zeros(Ngas)

#==================================
#Writing snapshots in gadget format
#==================================

output = sys.argv[3]
output = str(output)
write_snapshot(n_part=[Ngas, Ndm, Nstar, Nbulge, 0, 0], from_text=False, outfile=output, data_list=[pos, vel, ids, m, u, rho, hsml])
