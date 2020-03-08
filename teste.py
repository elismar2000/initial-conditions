from numpy import *
from pygadgetreader import *

snapshot = '/home/elismar/Documentos/Fisica/IC/Workshop_UTFPr/galstep/galstep/ICs/ICs_wGas_noBulge/snapshot_0000'

posbulge = readsnap(snapshot, 'pos', 'bulge')

header = readheader(snapshot2,'header')
Nbulge = header['nbulge']

print(posbulge, Nbulge)
