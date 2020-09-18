from astropy.table import Table
import matplotlib.pyplot as plt
import numpy as np

from sphviewer.tools import QuickView

snapshot = '/home/elismar/Documentos/Fisica/IC/GalMer/inflow/Tabelas_GalMer/tables_arp245_orbit1'
t = Table.read(snapshot, 17)

x = np.array(t['X'])
y = np.array(t['Y'])
z = np.array(t['Z'])
pos = np.column_stack((x, y, z))

vx = np.array(t['VX'])
vy = np.array(t['VY'])
vz = np.array(t['VZ'])
vel = np.column_stack((vx, vy, vz))

#Calculate the density field
qv = QuickView(pos, r='infinity', x=0, y=0, z=0, plot=False, extent=[-100,100,-50,50], logscale=False)
density_field = qv.get_image()
extent = qv.get_extent()

vfield = []
for i in range(2):
     qv = QuickView(pos, vel[:,i], r='infinity', x=0, y=0, z=0, plot=False,
        extent=[-100,100,-50,50], logscale=False)
     vfield.append(qv.get_image()/density_field)

fig = plt.figure(1, figsize=(7,7))
ax = fig.add_subplot(111)
X = np.linspace(extent[0], extent[1], 500)
Y = np.linspace(extent[2], extent[3], 500)
ax.imshow(np.log10(density_field), origin='lower', extent=extent, cmap='bone')
v = np.log10(np.sqrt(vfield[0]**2+vfield[1]**2))
color = v/np.max(v)
lw = 2*color
streams = ax.streamplot(X,Y,vfield[0], vfield[1], color=color,
                        density=1.5, cmap='jet', linewidth=lw, arrowsize=1)
ax.set_xlim(extent[0],extent[1])
ax.set_ylim(extent[2],extent[3])
ax.minorticks_on()
ax.set_xlabel(r'$\rm X / \ Kpc \ h^{-1}$', size=25)
ax.set_ylabel(r'$\rm Y / \ Kpc \ h^{-1}$', size=25)
plt.show()
