from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

import glob

from pygadgetreader import *

#=============================
#Modelo pra fitar o perfil vertical do disco de gas
#=============================

def SigmaZ(z, z0, Mgas):
    sigma0 = Mgas / (4 * np.pi)
    return sigma0 / (np.cosh(z / z0)**2 * z0)

#=============================
#Listas onde serao armazenados os z0_gas das galaxias
#=============================

orb09_e10_fric = []
orb09_e10_pot = []
orb11_e09_fric = []
orb11_e09_pot = []
orb39_e09_fric = []
orb39_e09_pot = []


#Forma de armazenar os caminhos para todos os snapshots das simulacoes
v = glob.glob('/home/elismar/Documentos/Fisica/IC/queorbita/orbits_3rd_attempt/orb09_e1.0-fric/snapshot_*')
v.sort()

#=============================
#Jeito de separar as galaxias nos snapshots, a partir das posicoes delas no primeiro snapshot
#=============================

pos = readsnap(v[0], 'pos', 'gas')
x = pos[:, 0]
z = pos[:, 2]

mask_ngc2992 = x < 50
mask_ngc2993 = x > 50

id_gas = readsnap(v[0], 'pid', 'gas')

ids_ngc2992 = id_gas[mask_ngc2992]
ids_ngc2993 = id_gas[mask_ngc2993]

#=============================
#Loop que vai calcular os z0_gas em todos os snapshots das 6 simulacoes
#=============================

for snapshot, i in zip(v, range(0, len(v))):

    pos = readsnap(snapshot, 'pos', 'gas')
    z = pos[:, 2]

    mass = readsnap(snapshot, 'mass', 'gas')

    ids = readsnap(snapshot, 'pid', 'gas')

    #Aqui eh onde muda qual a galaxia eu quero selecionar (mudar para 2993 se necessario)
    ngc2992 = np.isin(ids, ids_ngc2992)
    z = z[ngc2992]
    mass = mass[ngc2992]

    sigma_z, z_edges = np.histogram(abs(z), bins=20, weights=mass)
    z_bin = (z_edges[1] - z_edges[0])
    z_edges += z_bin / 2

    #0.2 * 0.42 eh o chute inicial pro z0_gas, que eh 0.2 vezes o z0_disk que eu usei la no galstep pra NGC2992
    popt, popv = curve_fit(SigmaZ, z_edges[:-1], sigma_z / z_bin, p0=[0.2, 0.92])
    best_z0, best_Mgas = popt[0], popt[1]

    print('snapshot = ', snapshot[-30:])
    print('z0 = ', best_z0)
    print('Mgas = ', best_Mgas)

    if i in range(0, 23): orb09_e10_fric.append(best_z0)
    if i in range(23, 2*23): orb09_e10_pot.append(best_z0)
    if i in range(2*23, 3*23): orb11_e09_fric.append(best_z0)
    if i in range(3*23, 4*23): orb11_e09_pot.append(best_z0)
    if i in range(4*23, 5*23): orb39_e09_fric.append(best_z0)
    if i in range(5*23, 6*23): orb39_e09_pot.append(best_z0)

#=============================
#Plotando os resultados
#=============================

from matplotlib.pyplot import cm
color = cm.rainbow(np.linspace(0, 1, 5))

time = np.arange(0, 23, 1) * 50 #Myr
plt.plot(time, orb09_e10_fric, '--', color=color[0], label='orb09_1.0-fric')
# plt.plot(time, orb09_e10_pot, '--', color=cm[1], label='orb09_1.0-pot')
# plt.plot(time, orb11_e09_fric, '--', color=cm[2], label='orb11_0.9-fric')
# plt.plot(time, orb11_e09_pot, '--', color=cm[3], label='orb11_0.9-pot')
# plt.plot(time, orb39_e09_fric, '--', color=cm[4], label='orb39_0.9-fric')
# plt.plot(time, orb39_e09_pot, '--', color=cm[5], label='orb39_0.9-fric')
plt.xlabel(r'$time\ [Myr]$')
plt.ylabel(r'$z_{0_{gas}}\ [0.7\ kpc]$')
plt.legend()
plt.show()


#Essa tentativa aqui de estudar o z0_gas deu problema pq soh funciona se a galaxia tiver deitada no eixo z
#Ou seja, precisaria 'desgirar' ela, ou rodar ela em isolamento sem girar
#Nesse caso, resolvi confiar essa analise do z0_gas aos plots que eu fiz ano passado (2020)
