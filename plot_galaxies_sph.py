import numpy as np
import matplotlib.pyplot as plt

from sphviewer.tools import QuickView

#1) Code to plot gas in snaspshots using sphviewer
#2) The way it is designed, it only works for particles' positions stored in .npy files
#4) This code only works with python3 environment (e.g. anaconda) enabled, and that's the reason why
#3) you need to use gadget_to_.npy to convert gadget snapshot to .npy files first


fig = plt.figure()
ax = fig.add_subplot(111)

attempt = '3rd'
simulation = 'orb09_e1.0-fric'
snapshot = 20

path = '/home/elismar/Documentos/Fisica/IC/queorbita/orbits_' + attempt + '_attempt/' + simulation + '/snapshot_00' + str(snapshot) + '.npy'
pos = np.load(path)

qv = QuickView(pos, r='infinity', plot=False, x=0,y=0,z=0, extent=[-40, 40, -40, 40])
img = qv.get_image()
extent = qv.get_extent()

image = ax.imshow(img, extent=extent, origin='lower', cmap='gnuplot')
ax.grid()
cbar = plt.colorbar(image)
cbar.set_label('Density of gas')

ax.set_title(attempt + ' - ' + simulation + '/' + str(snapshot))
ax.set_xlabel('x [Kpc]')
ax.set_ylabel('y [Kpc]')
plt.show()
