from pygadgetreader import *

import numpy as np

for j in [0.05, 1, 2, 3]:
    snapshot = int((j/0.05) + 1)
    s = '%04d' % (snapshot,)
    simulation = '/home/elismar/Documentos/Fisica/IC/Gadget3/simulation_galmer-like_test2/snapshot_' + str(s)
    pos = readsnap(simulation, 'pos', 'gas')

    file = 'simulation_' + str(s)
    np.save(file, pos)
