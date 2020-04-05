from astropy.table import Table
import matplotlib.pyplot as plt

import numpy as np
from pygadgetreader import *

from snapwrite import process_input, write_snapshot
import sys

output1 = sys.argv[1]
output2 = sys.argv[2]

t_path = '/home/elismar/Documentos/Fisica/IC/GalMer/inflow/Tabelas_GalMer/tables_arp245_orbit1'
t = Table.read(t_path, 1)

#===============================
#Setting maks for galaxies and particles types
#===============================

gal1 = t['GAL'] == 1
gal2 = t['GAL'] == 2

gas1 = t['P_TYPE'][gal1] == 0
gas2 = t['P_TYPE'][gal2] == 0
star1 = t['P_TYPE'][gal1] == 1
star2 = t['P_TYPE'][gal2] == 1
dm1 = t['P_TYPE'][gal1] == 2
dm2 = t['P_TYPE'][gal2] == 2

#==============================
#Collecting positions of particles
#==============================

x_gas1 = t['X'][gal1][gas1]
y_gas1 = t['Y'][gal1][gas1]
z_gas1 = t['Z'][gal1][gas1]

x_gas2 = t['X'][gal2][gas2]
y_gas2 = t['Y'][gal2][gas2]
z_gas2 = t['Z'][gal2][gas2]

x_star1 = t['X'][gal1][star1][0:48000]
y_star1 = t['Y'][gal1][star1][0:48000]
z_star1 = t['Z'][gal1][star1][0:48000]

x_star2 = t['X'][gal2][star2][0:48000]
y_star2 = t['Y'][gal2][star2][0:48000]
z_star2 = t['Z'][gal2][star2][0:48000]

x_bulge1 = t['X'][gal1][star1][48000:60000]
y_bulge1 = t['Y'][gal1][star1][48000:60000]
z_bulge1 = t['Z'][gal1][star1][48000:60000]

x_bulge2 = t['X'][gal2][star2][48000:60000]
y_bulge2 = t['Y'][gal2][star2][48000:60000]
z_bulge2 = t['Z'][gal2][star2][48000:60000]

x_dm1 = t['X'][gal1][dm1]
y_dm1 = t['Y'][gal1][dm1]
z_dm1 = t['Z'][gal1][dm1]

x_dm2 = t['X'][gal2][dm2]
y_dm2 = t['Y'][gal2][dm2]
z_dm2 = t['Z'][gal2][dm2]

#==================================
#Collecting velocities of particles
#==================================

vx_gas1 = t['VX'][gal1][gas1]
vy_gas1 = t['VY'][gal1][gas1]
vz_gas1 = t['VZ'][gal1][gas1]

vx_gas2 = t['VX'][gal2][gas2]
vy_gas2 = t['VY'][gal2][gas2]
vz_gas2 = t['VZ'][gal2][gas2]

vx_star1 = t['VX'][gal1][star1][0:48000]
vy_star1 = t['VY'][gal1][star1][0:48000]
vz_star1 = t['VZ'][gal1][star1][0:48000]

vx_star2 = t['VX'][gal2][star2][0:48000]
vy_star2 = t['VY'][gal2][star2][0:48000]
vz_star2 = t['VZ'][gal2][star2][0:48000]

vx_bulge1 = t['VX'][gal1][star1][48000:60000]
vy_bulge1 = t['VY'][gal1][star1][48000:60000]
vz_bulge1 = t['VZ'][gal1][star1][48000:60000]

vx_bulge2 = t['VX'][gal2][star2][48000:60000]
vy_bulge2 = t['VY'][gal2][star2][48000:60000]
vz_bulge2 = t['VZ'][gal2][star2][48000:60000]

vx_dm1 = t['VX'][gal1][dm1]
vy_dm1 = t['VY'][gal1][dm1]
vz_dm1 = t['VZ'][gal1][dm1]

vx_dm2 = t['VX'][gal2][dm2]
vy_dm2 = t['VY'][gal2][dm2]
vz_dm2 = t['VZ'][gal2][dm2]

#================================
#Collecting masses of particles
#================================

m_gas1 = t['MASS'][gal1][gas1]

m_gas2 = t['MASS'][gal2][gas2]

m_star1 = t['MASS'][gal1][star1][0:48000]

m_star2 = t['MASS'][gal2][star2][0:48000]

m_bulge1 = t['MASS'][gal1][star1][48000:60000]

m_bulge2 = t['MASS'][gal2][star2][48000:60000]

m_dm1 = t['MASS'][gal1][dm1]

m_dm2 = t['MASS'][gal2][dm2]

#================================
#U and rho vectors for SPH particles
#================================

snapshot = '/home/elismar/Documentos/Fisica/IC/simulations_ICs/ICs/gSa_galaxies/snapshot0000'
u = readsnap(snapshot, 'u', 'gas')
rho = readsnap(snapshot, 'rho', 'gas')

#================================
#Concatenating vectors for different galaxy components
#================================

m1 = np.concatenate((m_gas1, m_dm1, m_star1, m_bulge1))
x1 = np.concatenate((x_gas1, x_dm1, x_star1, x_bulge1))
y1 = np.concatenate((y_gas1, y_dm1, y_star1, y_bulge1))
z1 = np.concatenate((z_gas1, z_dm1, z_star1, z_bulge1))
vx1 = np.concatenate((vx_gas1, vx_dm1, vx_star1, vx_bulge1))
vy1 = np.concatenate((vy_gas1, vy_dm1, vy_star1, vy_bulge1))
vz1 = np.concatenate((vz_gas1, vz_dm1, vz_star1, vz_bulge1))

m2 = np.concatenate((m_gas2, m_dm2, m_star2, m_bulge2))
x2 = np.concatenate((x_gas2, x_dm2, x_star2, x_bulge2))
y2 = np.concatenate((y_gas2, y_dm2, y_star2, y_bulge2))
z2 = np.concatenate((z_gas2, z_dm2, z_star2, z_bulge2))
vx2 = np.concatenate((vx_gas2, vx_dm2, vx_star2, vx_bulge2))
vy2 = np.concatenate((vy_gas2, vy_dm2, vy_star2, vy_bulge2))
vz2 = np.concatenate((vz_gas2, vz_dm2, vz_star2, vz_bulge2))

#=================================
#Stacking position and velocity vectors
#=================================

pos1 = np.column_stack((x1, y1, z1))
pos1.shape = (-1, 1)

pos2 = np.column_stack((x2, y2, z2))
pos2.shape = (-1, 1)

vel1 = np.column_stack((vx1, vy1, vz1))
vel1.shape = (-1, 1)

vel2 = np.column_stack((vx2, vy2, vz2))
vel2.shape = (-1, 1)

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
#import pdb; pdb.set_trace()
write_snapshot(n_part=[Ngas, Ndm, Nstar, Nbulge, 0, 0], from_text=False, outfile=output1, data_list=[pos1, vel1, ids, m1, u, rho, hsml])
write_snapshot(n_part=[Ngas, Ndm, Nstar, Nbulge, 0, 0], from_text=False, outfile=output2, data_list=[pos2, vel2, ids, m2, u, rho, hsml])
