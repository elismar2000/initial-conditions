import numpy as np
import matplotlib.pyplot as plt

from pygadgetreader import *

snapshot = '/home/elismar/Documentos/Fisica/IC/simulations_ICs/ICs/gSa_galaxies/snapshot0000'

u = readsnap(snapshot, 'u', 'gas')
rho = readsnap(snapshot, 'rho', 'gas')
print(u)
print(rho.max())
