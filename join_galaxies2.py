from os import path
from argparse import ArgumentParser as parser

import numpy as np

from snapwrite import process_input, write_snapshot

from numpy import *
from pygadgetreader import *
import sys

#python join.py haloA haloB haloAB  0 0 0  0 0 0

#input and output files from command line
snapshot1 = sys.argv[1]
snapshot2 = sys.argv[2]
output    = sys.argv[3]
Dx        = sys.argv[4]
Dy        = sys.argv[5]
Dz        = sys.argv[6]
Dvx       = sys.argv[7]
Dvy       = sys.argv[8]
Dvz       = sys.argv[9]

#-------------------------------------------------
#read input file 1
header  = readheader(snapshot1,'header')
Nhalo1 = header['ndm']
Ngas1  = header['ngas']
Ndisk1 = header['ndisk']
Nbulge1 = header['nbulge']

#dark matter halo:

poshalo1 = readsnap(snapshot1,'pos','dm')
velhalo1 = readsnap(snapshot1,'vel','dm')
mhalo1   = readsnap(snapshot1,'mass','dm')

xhalo1 = poshalo1[:, 0]
yhalo1 = poshalo1[:, 1]
zhalo1 = poshalo1[:, 2]

vxhalo1 = velhalo1[:, 0]
vyhalo1 = velhalo1[:, 1]
vzhalo1 = velhalo1[:, 2]

#disk:

posdisk1 = readsnap(snapshot1,'pos','disk')
veldisk1 = readsnap(snapshot1,'vel','disk')
mdisk1   = readsnap(snapshot1,'mass','disk')

xdisk1 = posdisk1[:, 0]
ydisk1 = posdisk1[:, 1]
zdisk1 = posdisk1[:, 2]

vxdisk1 = veldisk1[:, 0]
vydisk1 = veldisk1[:, 1]
vzdisk1 = veldisk1[:, 2]

#gas:

gas1 = False
if Ngas1 > 0:
    gas1 = True

if gas1:
    posgas1 = readsnap(snapshot1,'pos','gas')
    velgas1 = readsnap(snapshot1,'vel','gas')
    mgas1   = readsnap(snapshot1,'mass','gas')
    u1      = readsnap(snapshot1,'u'  ,'gas')
    rho1    = readsnap(snapshot1,'rho','gas')

    xgas1   = posgas1[:, 0]
    ygas1   = posgas1[:, 1]
    zgas1   = posgas1[:, 2]

    vxgas1  = velgas1[:, 0]
    vygas1  = velgas1[:, 1]
    vzgas1  = velgas1[:, 2]

#bulge:

bulge1 = False
if Nbulge1 > 0:
    bulge1 = True

if bulge1:
    posbulge1 = readsnap(snapshot1, 'pos', 'bulge')
    velbulge1 = readsnap(snapshot1, 'vel', 'bulge')
    mbulge1 = readsnap(snapshot1, 'mass', 'bulge')

    xbulge1 = posbulge1[:, 0]
    ybulge1 = posbulge1[:, 1]
    zbulge1 = posbulge1[:, 2]

    vxbulge1 = velbulge1[:, 0]
    vybulge1 = velbulge1[:, 1]
    vzbulge1 = velbulge1[:, 2]

#-------------------------------------------------
#read input file 2
header = readheader(snapshot2,'header')
Nhalo2 = header['ndm']
Ngas2  = header['ngas']
Ndisk2 = header['ndisk']
Nbulge2 = header['nbulge']

#dark matter halo:

poshalo2 = readsnap(snapshot2,'pos','dm')
velhalo2 = readsnap(snapshot2,'vel','dm')
mhalo2   = readsnap(snapshot2,'mass','dm')

xhalo2 = poshalo2[:, 0]
yhalo2 = poshalo2[:, 1]
zhalo2 = poshalo2[:, 2]
vxhalo2 = velhalo2[:, 0]
vyhalo2 = velhalo2[:, 1]
vzhalo2 = velhalo2[:, 2]

#disk:

posdisk2 = readsnap(snapshot2,'pos','disk')
veldisk2 = readsnap(snapshot2,'vel','disk')
mdisk2   = readsnap(snapshot2,'mass','disk')

xdisk2 = posdisk2[:, 0]
ydisk2 = posdisk2[:, 1]
zdisk2 = posdisk2[:, 2]
vxdisk2 = veldisk2[:, 0]
vydisk2 = veldisk2[:, 1]
vzdisk2 = veldisk2[:, 2]

#gas:

gas2 = False
if Ngas2 > 0:
    gas2 = True

if gas2:
    posgas2 = readsnap(snapshot2,'pos','gas')
    velgas2 = readsnap(snapshot2,'vel','gas')
    mgas2   = readsnap(snapshot2,'mass','gas')
    u2      = readsnap(snapshot2,'u'  ,'gas')
    rho2    = readsnap(snapshot2,'rho','gas')

    xgas2   = posgas2[:, 0]
    ygas2   = posgas2[:, 1]
    zgas2   = posgas2[:, 2]
    vxgas2  = velgas2[:, 0]
    vygas2  = velgas2[:, 1]
    vzgas2  = velgas2[:, 2]

#bulge:

bulge2 = False
if Nbulge2 > 0:
    bulge2 = True

if bulge2:
    posbulge2 = readsnap(snapshot2, 'pos', 'bulge')
    velbulge2 = readsnap(snapshot2, 'vel', 'bulge')
    mbulge2 = readsnap(snapshot2, 'mass', 'bulge')

    xbulge2 = posbulge2[:, 0]
    ybulge2 = posbulge2[:, 1]
    zbulge2 = posbulge2[:, 2]

    vxbulge2 = velbulge2[:, 0]
    vybulge2 = velbulge2[:, 1]
    vzbulge2 = velbulge2[:, 2]

#-------------------------------------------------

gas = False
if gas1 & gas2:
    gas = True

else:
    print("At least one of the galaxies has no gas")

bulge = False
if bulge1 & bulge2:
    bulge = True

else:
    print("At least one of the galaxies has no bulge")

#-------------------------------------------------
#shift positions and velocities:

#dark matter halo:

xhalo2  = xhalo2  + float(Dx)
yhalo2  = yhalo2  + float(Dy)
zhalo2  = zhalo2  + float(Dz)
vxhalo2 = vxhalo2 + float(Dvx)
vyhalo2 = vyhalo2 + float(Dvy)
vzhalo2 = vzhalo2 + float(Dvz)

#disk:

xdisk2  = xdisk2  + float(Dx)
ydisk2  = ydisk2  + float(Dy)
zdisk2  = zdisk2  + float(Dz)
vxdisk2 = vxdisk2 + float(Dvx)
vydisk2 = vydisk2 + float(Dvy)
vzdisk2 = vzdisk2 + float(Dvz)

#gas:

if gas2:
    xgas2  = xgas2  + float(Dx)
    ygas2  = ygas2  + float(Dy)
    zgas2  = zgas2  + float(Dz)
    vxgas2 = vxgas2 + float(Dvx)
    vygas2 = vygas2 + float(Dvy)
    vzgas2 = vzgas2 + float(Dvz)

#bulge:

if bulge2:
    xbulge2  = xbulge2  + float(Dx)
    ybulge2  = ybulge2  + float(Dy)
    zbulge2  = zbulge2  + float(Dz)
    vxbulge2 = vxbulge2 + float(Dvx)
    vybulge2 = vybulge2 + float(Dvy)
    vzbulge2 = vzbulge2 + float(Dvz)

#-------------------------------------------------
#join

#dark matter halo:

Nhalo   = Nhalo1 + Nhalo2
mhalo = concatenate([mhalo1, mhalo2])
xhalo = concatenate([xhalo1, xhalo2])
yhalo = concatenate([yhalo1, yhalo2])
zhalo = concatenate([zhalo1, zhalo2])
vxhalo = concatenate([vxhalo1, vxhalo2])
vyhalo = concatenate([vyhalo1, vyhalo2])
vzhalo = concatenate([vzhalo1, vzhalo2])

#disk:

Ndisk   = Ndisk1 + Ndisk2
mdisk = concatenate([mdisk1, mdisk2])
xdisk = concatenate([xdisk1, xdisk2])
ydisk = concatenate([ydisk1, ydisk2])
zdisk = concatenate([zdisk1, zdisk2])
vxdisk = concatenate([vxdisk1, vxdisk2])
vydisk = concatenate([vydisk1, vydisk2])
vzdisk = concatenate([vzdisk1, vzdisk2])

#gas:

if (gas == True) & (bulge == True):
    Ngas   = Ngas1 + Ngas2
    mgas = concatenate([mgas1, mgas2])
    xgas = concatenate([xgas1, xgas2])
    ygas = concatenate([ygas1, ygas2])
    zgas = concatenate([zgas1, zgas2])
    vxgas = concatenate([vxgas1, vxgas2])
    vygas = concatenate([vygas1, vygas2])
    vzgas = concatenate([vzgas1, vzgas2])
    u     = concatenate([u1, u2])
    rho   = concatenate([rho1, rho2])

    Nbulge   = Nbulge1 + Nbulge2
    mbulge = concatenate([mbulge1, mbulge2])
    xbulge = concatenate([xbulge1, xbulge2])
    ybulge = concatenate([ybulge1, ybulge2])
    zbulge = concatenate([zbulge1, zbulge2])
    vxbulge = concatenate([vxbulge1, vxbulge2])
    vybulge = concatenate([vybulge1, vybulge2])
    vzbulge = concatenate([vzbulge1, vzbulge2])

    m  = concatenate([mgas, mhalo, mdisk, mbulge])
    x  = concatenate([xgas, xhalo, xdisk, xbulge])
    y  = concatenate([ygas, yhalo, ydisk, ybulge])
    z  = concatenate([zgas, zhalo, zdisk, zbulge])
    vx = concatenate([vxgas, vxhalo, vxdisk, vxbulge])
    vy = concatenate([vygas, vyhalo, vydisk, vybulge])
    vz = concatenate([vzgas, vzhalo, vzdisk, vzbulge])

#bulge:

if (bulge == True) & (gas == False):
    Nbulge   = Nbulge1 + Nbulge2
    mbulge = concatenate([mbulge1, mbulge2])
    xbulge = concatenate([xbulge1, xbulge2])
    ybulge = concatenate([ybulge1, ybulge2])
    zbulge = concatenate([zbulge1, zbulge2])
    vxbulge = concatenate([vxbulge1, vxbulge2])
    vybulge = concatenate([vybulge1, vybulge2])
    vzbulge = concatenate([vzbulge1, vzbulge2])

    m = concatenate([mhalo, mdisk, mbulge])
    x = concatenate([xhalo, xdisk, xbulge])
    y = concatenate([yhalo, ydisk, ybulge])
    z = concatenate([zhalo, zdisk, zbulge])
    vx = concatenate([vxhalo, vxdisk, vxbulge])
    vy = concatenate([vyhalo, vydisk, vybulge])
    vz = concatenate([vzhalo, vzdisk, vzbulge])

if (bulge == False) & (gas == False):
    m = concatenate([mhalo, mdisk])
    x = concatenate([xhalo, xdisk])
    y = concatenate([yhalo, ydisk])
    z = concatenate([zhalo, zdisk])
    vx = concatenate([vxhalo, vxdisk])
    vy = concatenate([vyhalo, vydisk])
    vz = concatenate([vzhalo, vzdisk])

#-------------------------------------------------
#shift to COM

xcom = sum(x*m)/sum(m)
ycom = sum(y*m)/sum(m)
zcom = sum(z*m)/sum(m)
x = x - xcom
y = y - ycom
z = z - zcom

vxcom = sum(vx*m)/sum(m)
vycom = sum(vy*m)/sum(m)
vzcom = sum(vz*m)/sum(m)
vx = vx - vxcom
vy = vy - vycom
vz = vz - vzcom

#-------------------------------------------------
#shapes and ids

pos = np.column_stack((x, y, z))
pos.shape = (-1, 1)

vel = np.column_stack((vx, vy, vz))
vel.shape = (-1, 1)

print('pos.shape: ', pos.shape)
print('vel.shape: ', vel.shape)
print('m.shape: ', m.shape)

if (gas == True) & (bulge == True):
    ids  = arange(0, Ngas + Nhalo + Ndisk + Nbulge, 1)
    hsml = np.zeros(Ngas)

if (bulge == True) & (gas == False):
    N = Nhalo + Ndisk + Nbulge
    ids = arange(0, N, 1)

if (bulge == False) & (gas == False):
    N = Nhalo + Ndisk
    ids = arange(0, N, 1)

print('ids.shape: ', ids.shape)
print('bulge included? ', bulge)
print('gas included? ', gas)
#------------------------------------------------------
#write output

if (gas == True) & (bulge == True):
    print('With gas and bulge')
    write_snapshot(n_part=[Ngas, Nhalo, Ndisk, Nbulge, 0, 0], from_text=False, outfile=output, data_list=[pos, vel, ids, m, u, rho, hsml])

if (bulge == True) & (gas == False):
    print('With bulge but no gas')
    write_snapshot(n_part=[0, Nhalo, Ndisk, Nbulge, 0, 0], from_text=False, outfile=output, data_list=[pos, vel, ids, m])

if (bulge == False) & (gas == False):
    print('Without gas nor bulge')
    write_snapshot(n_part=[0, Nhalo, Ndisk, 0, 0, 0], from_text=False, outfile=output, data_list=[pos, vel, ids, m])
#------------------------------------------------------
