import matplotlib.pyplot as plt
import numpy as np
from astropy.table import Table

from numpy import *
from pygadgetreader import *

import sys
from tables import *

snapshot   = sys.argv[1]
mode       = sys.argv[2]
projection = sys.argv[3]
snap       = sys.argv[4]

snapshot   = str(snapshot)
mode       = str(mode)
projection = str(projection)
snap       = int(snap)

cmap = plt.get_cmap('plasma')
colors = [cmap(i) for i in np.linspace(0, 1, 7)]

if mode == 'Galmer':
    if projection == '3D':
        t = Table.read(snapshot, 1)

        mask1 = t['GAL'] == 1
        mask2 = t['GAL'] == 2
        p_mask1 = t['P_TYPE'][mask1] != 2
        p_mask2 = t['P_TYPE'][mask2] != 2

        from mpl_toolkits.mplot3d import Axes3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(t['X'][mask1][p_mask1], t['Y'][mask1][p_mask1], t['Z'][mask1][p_mask1], 'r,')
        ax.plot(t['X'][mask2][p_mask2], t['Y'][mask2][p_mask2], t['Z'][mask2][p_mask2], 'b,')

    if projection == '2D':
        axis_cmap = plt.get_cmap('rainbow')
        axis_colors = [cmap(i) for i in np.linspace(0, 1, 7)]
        fig, axs = plt.subplots(3, 3, figsize=(40, 40))
        l = -1
        for i in [1, 17, 60]:
            l += 1
            k = -1
            for j in [1, 5, 9]:
                k += 1
                t = Table.read(snapshot, i)

                if projection == '2D':
                    axs[k, l].plot(t['X'], t['Y'], ',', color=colors[3])
                    axs[k, l].tick_params(axis='both', which='both', tickdir='in', labelsize=10,
                        top=True, right=True, width=1.5)
                    axs[k, 0].set_ylabel(r'$Y [kpc]$', fontsize=20)
                    axs[2, 1].set_xlabel(r'$X [kpc]$', fontsize=20)

        axs[0, 0].xaxis.set_label_position('top')
        axs[0, 0].xaxis.label.set_color(axis_colors[3])
        axs[0, 0].set_xlabel(r'$snapshot\ 1$', fontsize=30)

        axs[0, 1].xaxis.set_label_position('top')
        axs[0, 1].xaxis.label.set_color(axis_colors[1])
        axs[0, 1].set_xlabel(r'$snapshot\ 17$', fontsize=30)

        axs[0, 2].xaxis.set_label_position('top')
        axs[0, 2].xaxis.label.set_color(axis_colors[5])
        axs[0, 2].set_xlabel(r'$snapshot\ 60$', fontsize=30)

        axs[0, 2].yaxis.set_label_position('right')
        axs[0, 2].yaxis.label.set_color(axis_colors[0])
        axs[0, 2].set_ylabel(r'$orbit\ type\ 1$', fontsize=15)

        axs[1, 2].yaxis.set_label_position('right')
        axs[1, 2].yaxis.label.set_color(axis_colors[2])
        axs[1, 2].set_ylabel(r'$orbit\ type\ 5$', fontsize=15)

        axs[2, 2].yaxis.set_label_position('right')
        axs[2, 2].yaxis.label.set_color(axis_colors[4])
        axs[2, 2].set_ylabel(r'$orbit\ type\ 9$', fontsize=15)
        plt.subplots_adjust(wspace=0, hspace=0)


if mode == 'Gadget':
    if projection == '3D':
        pos_disk = readsnap(snapshot, 'pos', 'disk')
        x_disk = pos_disk[:, 0]
        y_disk = pos_disk[:, 1]
        z_disk = pos_disk[:, 2]

        pos_gas = readsnap(snapshot, 'pos', 'gas')
        x_gas = pos_gas[:, 0]
        y_gas = pos_gas[:, 1]
        z_gas = pos_gas[:, 2]

        pos_bulge = readsnap(snapshot, 'pos', 'bulge')
        x_bulge = pos_bulge[:, 0]
        y_bulge = pos_bulge[:, 1]
        z_bulge = pos_bulge[:, 2]

        x = concatenate((x_disk, x_gas, x_bulge))
        y = concatenate((y_disk, y_gas, y_bulge))
        z = concatenate((z_disk, z_gas, z_bulge))

        mask1 = x > 0
        mask2 = x < 0

        from mpl_toolkits.mplot3d import Axes3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(x[mask1], y[mask1], z[mask1], 'b,')
        ax.plot(x[mask2], y[mask2], z[mask2], 'r,')

    if projection == '2D':
        pos_disk = readsnap(snapshot, 'pos', 'disk')
        x_disk = pos_disk[:, 0]
        y_disk = pos_disk[:, 1]
        z_disk = pos_disk[:, 2]

        pos_gas = readsnap(snapshot, 'pos', 'gas')
        x_gas = pos_gas[:, 0]
        y_gas = pos_gas[:, 1]
        z_gas = pos_gas[:, 2]

        pos_bulge = readsnap(snapshot, 'pos', 'bulge')
        x_bulge = pos_bulge[:, 0]
        y_bulge = pos_bulge[:, 1]
        z_bulge = pos_bulge[:, 2]

        pos_star = readsnap(snapshot, 'pos', 'star')
        x_star = pos_star[:, 0]
        y_star = pos_star[:, 1]
        z_star = pos_star[:, 2]

        x = concatenate((x_disk, x_gas, x_bulge))
        y = concatenate((y_disk, y_gas, y_bulge))
        z = concatenate((z_disk, z_gas, z_bulge))

        pos_gas = stack((x_gas, y_gas, z_gas))
        pos_star = stack((x_star, y_star, z_star))

        mins = '/home/elismar/Documentos/Fisica/IC/GalMer/inflow/mins_Gadget/galmer-like_sim_test2_minima.h5'
        h5file = open_file(mins, mode='r')
        table = h5file.root.potential.readout

        def dist(point1, point2):
            d = np.sqrt(np.sum(np.square(point1[i] - point2[i]) for i in range(3)))
            return d

        if snap < 17:
            xmin1 = np.array([j['xmin1'] for j in table.where('snapshot == snap')])
            ymin1 = np.array([j['ymin1'] for j in table.where('snapshot == snap')])
            zmin1 = np.array([j['zmin1'] for j in table.where('snapshot == snap')])
            min1 = np.array([xmin1, ymin1, zmin1])

            xmin2 = np.array([j['xmin2'] for j in table.where('snapshot == snap')])
            ymin2 = np.array([j['ymin2'] for j in table.where('snapshot == snap')])
            zmin2 = np.array([j['zmin2'] for j in table.where('snapshot == snap')])
            min2 = np.array([xmin2, ymin2, zmin2])

            dist1_gas = np.array([dist(pos_gas[:, i], min1) for i in range(len(pos_gas[0]))])[:, 0]
            dist2_gas = np.array([dist(pos_gas[:, i], min2) for i in range(len(pos_gas[0]))])[:, 0]

            dist1_star = np.array([dist(pos_star[:, i], min1) for i in range(len(pos_star[0]))])[:, 0]
            dist2_star = np.array([dist(pos_star[:, i], min2) for i in range(len(pos_star[0]))])[:, 0]

            mask1_gas = dist1_gas < 0.01
            mask2_gas = dist2_gas < 0.01

            mask1_star = dist1_star < 0.01
            mask2_star = dist2_star < 0.01

            plt.plot(x, y, 'b,')
            plt.plot(x_gas[mask1_gas], y_gas[mask1_gas], '.', color='gold')
            plt.plot(x_gas[mask2_gas], y_gas[mask2_gas], '.', color='gold')

            plt.plot(x_star[mask1_star], y_star[mask1_star], '.', color='m')
            plt.plot(x_star[mask2_star], y_star[mask2_star], '.', color='m')

        if snap >= 17:
            xmin = np.array([j['xmin'] for j in table.where('snapshot == snap')])
            ymin = np.array([j['ymin'] for j in table.where('snapshot == snap')])
            zmin = np.array([j['zmin'] for j in table.where('snapshot == snap')])
            min = np.array([xmin, ymin, zmin])

            dist = np.array([dist(pos_gas[:, i], min) for i in range(len(pos_gas[0]))])[:, 0]

            mask = dist < 0.01

            plt.plot(x, y, 'b,')
            plt.plot(x_gas[mask], y_gas[mask], '.', color='red')


plt.show()
