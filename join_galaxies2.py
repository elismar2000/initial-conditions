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
Nbulge1s = header['nbulge']

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

#gas:

gas = False
if(Ngas1>0):
    gas=True

if (gas):
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

#bulge:

posbulge1 = readsnap(snapshot1, 'pos', 'bulge')
velbulge1 = readsnap(snapshot1, 'pos', 'bulge')
mbulge1 = readnsnap(snapshot1, 'pos', 'bulge')

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

#gas:

gas = False
if(Ngas2>0):
    gas=True

if (gas):
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

#bulge:

posbulge2 = readsnap(snapshot2, 'pos', 'bulge')
velbulge2 = readsnap(snapshot2, 'pos', 'bulge')
mbulge2 = readnsnap(snapshot2, 'pos', 'bulge')

xbulge2 = posbulge2[:, 0]
ybulge2 = posbulge2[:, 1]
zbulge2 = posbulge2[:, 2]

vxbulge2 = velbulge2[:, 0]
vybulge2 = velbulge2[:, 1]
vzbulge2 = velbulge2[:, 2]

#-------------------------------------------------
#shift positions and velocities:

#dark matter halo:

xhalo2  = xhalo2  + float(Dx)
yhalo2  = yhalo2  + float(Dy)
zhalo2  = zhalo2  + float(Dz)
vxhalo2 = vxhalo2 + float(Dvx)
vyhalo2 = vyhalo2 + float(Dvy)
vzhalo2 = vzhalo2 + float(Dvz)

#gas:

if (gas):
    xgas2  = xgas2  + float(Dx)
    ygas2  = ygas2  + float(Dy)
    zgas2  = zgas2  + float(Dz)
    vxgas2 = vxgas2 + float(Dvx)
    vygas2 = vygas2 + float(Dvy)
    vzgas2 = vzgas2 + float(Dvz)

#disk:

xdisk2  = xdisk2  + float(Dx)
ydisk2  = ydisk2  + float(Dy)
zdisk2  = zdisk2  + float(Dz)
vxdisk2 = vxdisk2 + float(Dvx)
vydisk2 = vydisk2 + float(Dvy)
vzdisk2 = vzdisk2 + float(Dvz)

#bulge:

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

#gas:

if (gas):
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

if (gas):
    m  = concatenate([mgas,  mhalo, mdisk])
    x  = concatenate([xgas,  xhalo,  xdisk])
    y  = concatenate([ygas,  yhalo,  ydisk])
    z  = concatenate([zgas,  zhalo,  zdisk])
    vx = concatenate([vxgas, vxhalo, vxdisk])
    vy = concatenate([vygas, vyhalo, vydisk])
    vz = concatenate([vzgas, vzhalo, vzdisk])

#disk:

Ndisk   = Ndisk1 + Ndisk2
mdisk = concatenate([mdisk1, mdisk2])
xdisk = concatenate([xdisk1, xdisk2])
ydisk = concatenate([ydisk1, ydisk2])
zdisk = concatenate([zdisk1, zdisk2])
vxdisk = concatenate([vxdisk1, vxdisk2])
vydisk = concatenate([vydisk1, vydisk2])
vzdisk = concatenate([vzdisk1, vzdisk2])

#bulge:

Nbulge   = Nbulge1 + Nbulge2
mbulge = concatenate([mbulge1, mbulge2])
xbulge = concatenate([xbulge1, xbulge2])
ybulge = concatenate([ybulge1, ybulge2])
zbulge = concatenate([zbulge1, zbulge2])
vxbulge = concatenate([vxbulge1, vxbulge2])
vybulge = concatenate([vybulge1, vybulge2])
vzbulge = concatenate([vzbulge1, vzbulge2])

#-------------------------------------------------
#shift to COM

#dark matter halo:

xcom = sum(xhalo*mhalo)/sum(mhalo)
ycom = sum(yhalo*mhalo)/sum(mhalo)
zcom = sum(zhalo*mhalo)/sum(mhalo)
xhalo = xhalo - xcom
yhalo = yhalo - ycom
zhalo = zhalo - zcom

vxcom = sum(vxhalo*mhalo)/sum(mhalo)
vycom = sum(vyhalo*mhalo)/sum(mhalo)
vzcom = sum(vzhalo*mhalo)/sum(mhalo)
vxhalo = vxhalo - vxcom
vyhalo = vyhalo - vycom
vzhalo = vzhalo - vzcom

#gas:

if (gas):
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

#disk:

xcom = sum(xdisk*mdisk)/sum(mdisk)
ycom = sum(ydisk*mdisk)/sum(mdisk)
zcom = sum(zdisk*mdisk)/sum(mdisk)
xdisk = xdisk - xcom
ydisk = ydisk - ycom
zdisk = zdisk - zcom

vxcom = sum(vxdisk*mdisk)/sum(mdisk)
vycom = sum(vydisk*mdisk)/sum(mdisk)
vzcom = sum(vzdisk*mdisk)/sum(mdisk)
vxdisk = vxdisk - vxcom
vydisk = vydisk - vycom
vzdisk = vzdisk - vzcom

#bulge:

xcom = sum(xbulge*mbulge)/sum(mbulge)
ycom = sum(ybulge*mbulge)/sum(mbulge)
zcom = sum(zbulge*mbulge)/sum(mbulge)
xbulge = xbulge - xcom
ybulge = ybulge - ycom
zbulge = zbulge - zcom

vxcom = sum(vxbulge*mbulge)/sum(mbulge)
vycom = sum(vybulge*mbulge)/sum(mbulge)
vzcom = sum(vzbulge*mbulge)/sum(mbulge)
vxbulge = vxbulge - vxcom
vybulge = vybulge - vycom
vzbulge = vzbulge - vzcom

#-------------------------------------------------
#shapes and ids

if (gas):
    pos = np.column_stack((x, y, z))
    pos.shape = (-1, 1)

    vel = np.column_stack((vx, vy, vz))
    vel.shape = (-1, 1)

    ids  = arange(0, Ngas + Nhalo + Ndisk + Nbulge, 1)
    hsml = np.zeros(Ngas)

else:
    x = concatenate([xhalo,xdisk])
    y = concatenate([yhalo,ydisk])
    z = concatenate([zhalo,zdisk])

    vx = concatenate([vxhalo,vxdisk])
    vy = concatenate([vyhalo,vydisk])
    vz = concatenate([vzhalo,vzdisk])

    m = concatenate([mhalo, mdisk])
    print('m: ', m)

    pos = np.column_stack((x, y, z))
    pos.shape = (-1, 1)
    print('pos.shape: ', pos.shape)

    vel = np.column_stack((vx, vy, vz))
    vel.shape = (-1, 1)
    print('vel.shape: ', vel.shape)

    N = Nhalo+Ndisk
    ids = arange(0, N, 1)
    print('ids.shape: ', ids.shape)
#------------------------------------------------------
#write output

if (gas):
    write_snapshot(n_part=[Ngas, Nhalo, Ndisk, 0, 0, 0], from_text=False, outfile=output, data_list=[pos, vel, ids, m, u, rho, hsml])
else:
    write_snapshot(n_part=[0, Nhalo, Ndisk, 0, 0, 0], from_text=False, outfile=output, data_list=[pos, vel, ids, m])
#------------------------------------------------------
