import numpy as np
from pygadgetreader import *
import sys

#Code to translate a gadget snapshot to .npy file in order to use sphviewer.tools (only works in python3),
#avoiding conflicts with dependencies of pygadgetreader (only works in python2)

#This code must be run in python2, disabling anaconda environment

gadget_snapshot = sys.argv[1]
npy_file        = gadget_snapshot + '.npy'

pos = readsnap(gadget_snapshot, 'pos', 'gas')

np.save(npy_file, pos)
