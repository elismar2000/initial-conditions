from astropy.table import Table
import matplotlib.pyplot as plt

import numpy as np
from pygadgetreader import *

from snapwrite import process_input, write_snapshot
import sys

#================================
#U and rho vectors for SPH particles
#================================

snapshot = '/home/elismar/Documentos/Fisica/IC/simulations_ICs/ICs/galmer_galaxies/gal_col.ini'
u = readsnap(snapshot, 'u', 'gas')
rho = readsnap(snapshot, 'rho', 'gas')

t_path = '/home/elismar/Documentos/Fisica/IC/GalMer/inflow/Tabelas_GalMer/tables_arp245_orbit1'

for snapshot in range(1, 72):
    output = 'snapshot_' + '%03d' % (snapshot,)
    t = Table.read(t_path, snapshot)

    #===============================
    #Setting masks for galaxies and particle types
    #===============================

    gas = t['P_TYPE'] == 0
    star = t['P_TYPE'] == 1
    dm = t['P_TYPE'] == 2

    #==============================
    #Collecting positions of particles
    #==============================

    h = 0.75
    lf = h

    x_gas = t['X'][gas] * lf
    y_gas = t['Y'][gas] * lf
    z_gas = t['Z'][gas] * lf

    x_star = np.concatenate((t['X'][star][0:48000], t['X'][star][60000:108000])) * lf
    y_star = np.concatenate((t['Y'][star][0:48000], t['Y'][star][60000:108000])) * lf
    z_star = np.concatenate((t['Z'][star][0:48000], t['Z'][star][60000:108000])) * lf

    x_bulge = np.concatenate((t['X'][star][48000:60000], t['X'][star][108000:120000])) * lf
    y_bulge = np.concatenate((t['Y'][star][48000:60000], t['Y'][star][108000:120000])) * lf
    z_bulge = np.concatenate((t['Z'][star][48000:60000], t['Z'][star][108000:120000])) * lf

    x_dm = t['X'][dm] * lf
    y_dm = t['Y'][dm] * lf
    z_dm = t['Z'][dm] * lf

    #==================================
    #Collecting velocities of particles
    #==================================

    vx_gas = t['VX'][gas]
    vy_gas = t['VY'][gas]
    vz_gas = t['VZ'][gas]

    vx_star = np.concatenate((t['VX'][star][0:48000], t['VX'][star][60000:108000]))
    vy_star = np.concatenate((t['VY'][star][0:48000], t['VY'][star][60000:108000]))
    vz_star = np.concatenate((t['VZ'][star][0:48000], t['VZ'][star][60000:108000]))

    vx_bulge = np.concatenate((t['VX'][star][48000:60000], t['VX'][star][108000:120000]))
    vy_bulge = np.concatenate((t['VY'][star][48000:60000], t['VY'][star][108000:120000]))
    vz_bulge = np.concatenate((t['VZ'][star][48000:60000], t['VZ'][star][108000:120000]))

    vx_dm = t['VX'][dm]
    vy_dm = t['VY'][dm]
    vz_dm = t['VZ'][dm]

    #================================
    #Collecting masses of particles
    #================================

    mf = 2.25 * h / 10.0

    m_gas = t['MASS'][gas] * mf

    m_star = np.concatenate((t['MASS'][star][0:48000], t['MASS'][star][60000:108000])) * mf

    m_bulge = np.concatenate((t['MASS'][star][48000:60000], t['MASS'][star][108000:120000])) * mf

    print(m_star.shape)
    print(m_bulge.shape)

    m_dm = t['MASS'][dm] * mf

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

    Ngas = 40000
    Ndm = 80000
    Nstar = 96000
    Nbulge = 24000
    N = Ngas + Ndm + Nstar + Nbulge
    ids  = np.arange(0, N, 1)
    hsml = np.zeros(Ngas)

    #==================================
    #Writing snapshots in gadget format
    #==================================

    write_snapshot(n_part=[Ngas, Ndm, Nstar, Nbulge, 0, 0], from_text=False, outfile=output, data_list=[pos, vel, ids, m, u, rho, hsml])
