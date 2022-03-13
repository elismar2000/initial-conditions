import numpy as np
import matplotlib.pyplot as plt

from sphviewer.tools import QuickView

#1) Code to plot a grid showing some snapshots of our attempts
#2) The way it is designed, it only works for particles' positions stored in .npy files
#4) This code only works with python3 environment (e.g. anaconda) enabled, and that's the reason why
#3) you need to use gadget_to_.npy to convert gadget snapshot to .npy files first


path_1st = '/home/elismar/Documentos/Fisica/IC/queorbita/snapshot_0040_1st_attempt.npy'
pos_1st = np.load(path_1st)

path_3rd = '/home/elismar/Documentos/Fisica/IC/queorbita/orbits_3rd_attempt/orb09_e1.0-pot/snapshot_0020.npy'
pos_3rd = np.load(path_3rd)

path_5th = '/home/elismar/Documentos/Fisica/IC/queorbita/orbits_5th_attempt/orb3-fric/snapshot_0040.npy'
pos_5th = np.load(path_5th)

path_7th = '/home/elismar/Documentos/Fisica/IC/queorbita/orbits_7th_attempt/orb3-fric/snapshot_0044.npy'
pos_7th = np.load(path_7th)

path_8th = '/home/elismar/Documentos/Fisica/IC/queorbita/orbits_8th_attempt/snapshot_200.npy'
pos_8th = np.load(path_8th)

path_9th = '/home/elismar/Documentos/Fisica/IC/queorbita/orbits_9th_attempt/ngc2993_rotated/snapshot_0040.npy'
pos_9th = np.load(path_9th)


positions = [pos_1st, pos_3rd, pos_5th, pos_7th, pos_8th, pos_9th]

titles = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)']


fig, axs = plt.subplots(3, 2, figsize=(40, 40), sharey=True, sharex=True)

for i in range(0, 6):

    pos = positions[i]

    qv = QuickView(pos, r='infinity', plot=False, x=0,y=0,z=0, extent=[-50, 50, -60, 40])

    # if i == 3: qv = QuickView(pos, r='infinity', plot=False, x=0,y=0,z=0, extent=[-50, 30, -60, 20])

    img = qv.get_image()
    extent = qv.get_extent()

    ax = axs[int(i/2), i%2]
    image = ax.imshow(img, extent=extent, origin='lower', cmap='nipy_spectral')

    if i%2 == 1:
        cbar = fig.colorbar(image, ax=ax, pad=0.02)
        cbar.set_label('Density of gas')

    if i%2 == 0: ax.set_ylabel('y [Kpc]')
    if int(i/2) == 2: ax.set_xlabel('x [Kpc]')

    ax.text(-2, 27, titles[i], color='white')


plt.subplots_adjust(wspace=-1.1, hspace=0.1)
plt.show()
