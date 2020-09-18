import yt

#fname = '/home/elismar/Documentos/Fisica/IC/Gadget3/simulation_galmer-like_test2/snapshot_0010'
fname = '/home/elismar/Documentos/Fisica/IC/simulations_ICs/codes/snapshot10'

unit_base = {'UnitLength_in_cm'         : 3.08568e+21,
             'UnitMass_in_g'            :   1.989e+43,
             'UnitVelocity_in_cm_per_s' :      100000}

bbox_lim = 2000 #kpc

bbox = [[-bbox_lim,bbox_lim],
        [-bbox_lim,bbox_lim],
        [-bbox_lim,bbox_lim]]

ds = yt.load(fname, unit_base=unit_base, bounding_box=bbox)

p = yt.ParticlePlot(ds, 'particle_position_x', 'particle_position_y', 'particle_mass')

p.set_font({'family': 'sans-serif', 'style': 'italic',
            'size': 30})

p.annotate_title('0.5 Gyr')

p.set_unit('particle_mass', 'Msun')
p.zoom(20)
p.save('galmer_10.png')
