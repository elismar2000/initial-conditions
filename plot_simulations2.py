from astropy.table import Table
import matplotlib.pyplot as plt
import numpy as np

from sphviewer.tools import QuickView

fig, axs = plt.subplots(4, 2, figsize=(50, 50), sharey='row', sharex='col', dpi=60)

k = -1
for i in ['galmer', 'gadget']:
    k += 1
    l = -1
    for j in [0.05, 1, 2, 3]:
        l += 1

        snapshot = int((j/0.05) + 1)

        #============================
        #Gadget-3
        #============================
        if i == 'gadget':
            s = '%04d' % (snapshot,)
            file = 'simulation_' + str(s) + '.npy'
            pos = np.load(file)

        #=============================
        #GalMer
        #=============================
        if i == 'galmer':
            simulation = '/home/elismar/Documentos/Fisica/IC/GalMer/inflow/Tabelas_GalMer/tables_arp245_orbit1'
            t = Table.read(simulation, snapshot)
            gas = t['P_TYPE'] == 0

            x = np.array(t['X'][gas])
            y = np.array(t['Y'][gas])
            z = np.array(t['Z'][gas])
            pos = np.column_stack((x, y, z))

        #==============================

        qv = QuickView(pos, r='infinity', plot=False, x=0,y=0,z=0, extent=[-110, 110, -110, 110])
        img = qv.get_image()
        extent = qv.get_extent()

        im = axs[l, k].imshow(img, extent=extent, cmap='twilight')
        if (k == 1): fig.colorbar(im, ax=axs[l, k], pad=0.1)

        axs[l, k].tick_params(left=False, right=False, top=False, bottom=False,
             length=2, tickdir='in', labelsize=15)

        axs[l, k].set_xlabel('Kpc', fontsize=15)
        if (i == 'galmer'): axs[l, k].set_ylabel('Kpc', fontsize=15)

        if i == 'gadget':
            axs[l, k].yaxis.set_label_position('right')
            if (j == 0.05): axs[l, k].set_ylabel('0.05 Gyr', fontsize=15)
            if (j == 1): axs[l, k].set_ylabel('1.0 Gyr', fontsize=15)
            if (j == 2): axs[l, k].set_ylabel('2.0 Gyr', fontsize=15)
            if (j == 3): axs[l, k].set_ylabel('3.0 Gyr', fontsize=15)

        if j == 0.05:
            axs[l, k].xaxis.set_label_position('top')
            if (i == 'gadget'): axs[l, k].set_xlabel('GADGET-3', fontsize=20)
            if (i == 'galmer'): axs[l, k].set_xlabel('GalMer', fontsize=20)

plt.subplots_adjust(wspace=-0.83, hspace=0)

#import os
#os.chdir('/home/elismar/Documentos/Fisica/IC/figuras/RAS Poster')
#plt.savefig('simulation_plot.png')
# os.chdir('/home/elismar/Documentos/Fisica/IC/simulations_ICs/codes')

plt.show()
