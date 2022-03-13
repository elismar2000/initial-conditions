from astropy.table import Table
import matplotlib.pyplot as plt
import numpy as np

from sphviewer.tools import QuickView

fig, axs = plt.subplots(4, 3, figsize=(25, 25), sharey='row', sharex='col', dpi=60)

k = -1
for i in [1, 5, 9]:
    k += 1
    l = -1
    for j in [0.05, 1, 2, 3]:
        l += 1

        simulation = '/home/elismar/Documentos/Fisica/IC/GalMer/inflow/Tabelas_GalMer/tables_arp245_orbit' + str(i)
        snapshot = int((j/0.05) + 1)
        t = Table.read(simulation, snapshot)

        gas = t['P_TYPE'] == 0

        # box = [110, 110, 110, 110]
        # def pos(box):
        #     xmask = (t['X'][gas] < box) & (t['X'][gas] > -box)
        #     ymask = (t['Y'][gas][xmask] < box) & (t['Y'][gas][xmask] > -box)
        #
        #     x = t['X'][gas][xmask][ymask]
        #     y = t['Y'][gas][xmask][ymask]
        #
        #     return x, y
        #
        # x, y = pos(box[l])
        # axs[l, k].scatter(x, y, c='grey', s=0.05, marker='.')

        x = np.array(t['X'][gas])
        y = np.array(t['Y'][gas])
        z = np.array(t['Z'][gas])
        pos = np.column_stack((x, y, z))

        qv = QuickView(pos, r='infinity', plot=False, x=0,y=0,z=0, extent=[-110, 110, -110, 110])
        img = qv.get_image()
        extent = qv.get_extent()

        im = axs[l, k].imshow(img, extent=extent, cmap='twilight')
        #if (k == 2): fig.colorbar(im, ax=axs[l, k], pad=0.1)

        axs[l, k].tick_params(left=False, right=False, top=False, bottom=False,
             length=2, tickdir='in', labelsize=25)

        if (j == 3) and (i == 5): axs[l, k].set_xlabel('Kpc', fontsize=30)
        if (i == 1): axs[l, k].set_ylabel('Kpc', fontsize=30)

        if i == 9:
            axs[l, k].yaxis.set_label_position('right')
            if (j == 0.05): axs[l, k].set_ylabel('0.05 Gyr', fontsize=30)
            if (j == 1): axs[l, k].set_ylabel('1.0 Gyr', fontsize=30)
            if (j == 2): axs[l, k].set_ylabel('2.0 Gyr', fontsize=30)
            if (j == 3): axs[l, k].set_ylabel('3.0 Gyr', fontsize=30)

        if j == 0.05:
            axs[l, k].xaxis.set_label_position('top')
            if (i == 1): axs[l, k].set_xlabel('Orbit type 1', fontsize=30)
            if (i == 5): axs[l, k].set_xlabel('Orbit type 5', fontsize=30)
            if (i == 9): axs[l, k].set_xlabel('Orbit type 9', fontsize=30)

plt.subplots_adjust(wspace=-0.44, hspace=0)
# plt.savefig('simulation_plot.png')
plt.show()
