import yt
import numpy as np
import yt.units as units
import pylab

#===============================
#Setting up the plot
#===============================

fname = '/home/elismar/Documentos/Fisica/IC/Gadget3/simulation_galmer-like_test2/snapshot_0035'

unit_base = {'UnitLength_in_cm'         : 3.08568e+21,
             'UnitMass_in_g'            :   1.989e+43,
             'UnitVelocity_in_cm_per_s' :      100000}

bbox_lim = 1e5 #kpc

bbox = [[-bbox_lim,bbox_lim],
        [-bbox_lim,bbox_lim],
        [-bbox_lim,bbox_lim]]

ds = yt.load(fname, unit_base=unit_base, bounding_box=bbox)
ds.index
ad = ds.all_data()

# total_mass returns a list, representing the total gas and dark matter + stellar mass, respectively
print ([tm.in_units('Msun') for tm in ad.quantities.total_mass()])

#================================
#Finding the peak of gas density
#================================
density = ad[("Gas","Density")]
wdens = np.where(density == np.max(density))
coordinates = ad[("Gas","Coordinates")]
center = coordinates[wdens][0]
print ('center = ',center)

#================================
#Creating a tight box to enclose the particles
#================================
new_box_size = ds.quan(20, 'code_length')
left_edge = center - new_box_size/2
right_edge = center + new_box_size/2
print (new_box_size.in_units('Mpc'))
print (left_edge.in_units('Mpc'))
print (right_edge.in_units('Mpc'))

#================================
#Zooming in
#================================
ad2 = ds.region(center=center, left_edge=left_edge, right_edge=right_edge)
print ([tm.in_units('Msun') for tm in ad2.quantities.total_mass()])

px = yt.ProjectionPlot(ds, 'z', ('gas', 'density'), center=center, width=new_box_size, max_level=1)
px.save('density.png')
