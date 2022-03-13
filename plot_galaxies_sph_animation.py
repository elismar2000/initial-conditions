import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from sphviewer.tools import QuickView


simulation = 'orb11_e0.9-fric'


#Criando o plot inicial da simulação (o primeiro snapshot aqui foi o 0039)
fig, axs = plt.subplots()

snapshot = '/home/elismar/Documentos/Fisica/IC/queorbita/orbits_4th_attempt/' + simulation + '/snapshot_0039.npy'
pos = np.load(snapshot)

qv = QuickView(pos, r='infinity', plot=False, x=0,y=0,z=0, extent=[-40, 40, -40, 40])
img = qv.get_image()
extent = qv.get_extent()
im = plt.imshow(img, extent=extent, origin='lower', cmap='gnuplot')

#Propriedades básicas dos plots
label = axs.text(0.5, 0.85, "", bbox={'facecolor':'w', 'alpha':0.8, 'pad':5},
                transform=axs.transAxes, ha="center")
label.set_text('Snapshot 39')

plt.grid()
cbar = plt.colorbar(im,)
cbar.set_label('Density of gas')

plt.title(simulation)
plt.xlabel('x [Kpc]')
plt.ylabel('y [Kpc]')


def init():
    im.set_data(img)
    return [im]


def animate(snapshot):
    snap_path = '/home/elismar/Documentos/Fisica/IC/queorbita/orbits_4th_attempt/' + simulation + '/snapshot_00' + str(snapshot) + '.npy'

    pos = np.load(snap_path)

    label.set_text(u"Snapshot {}".format(snapshot))

    qv = QuickView(pos, r='infinity', plot=False, x=0,y=0,z=0, extent=[-40, 40, -40, 40])
    img = qv.get_image()
    im.set_data(img)

    return [im], label


ani = FuncAnimation(fig, animate, frames=np.arange(39, 45, 1),
                    init_func=init, blit=False)
plt.show()
