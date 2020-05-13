import matplotlib.pyplot as plt
import numpy as np
from pygadgetreader import *

snapshot = '/home/elismar/Documentos/Fisica/IC/Gadget2/Gadget-2.0.7/galaxy_collision_galmer_test/snapshot_000'

pot_gas = readsnap(snapshot, 'pot', 'gas')
pot_halo = readsnap(snapshot, 'pot', 'dm')
pot_disk = readsnap(snapshot, 'pot', 'disk')
pot_bulge = readsnap(snapshot, 'pot', 'bulge')

import pdb; pdb.set_trace()
