# -*- coding: utf-8 -*-
from numpy import *
from pygadgetreader import *
import matplotlib.pyplot as plt

### DATA ------------
sn = ('/media/hunter/706885E06885A586/gtr/gtr101/SNAPS/gtr101_2000')
massTable = readheader(sn,'massTable')
m = massTable[2]
n = readheader(sn,'ndisk')
M = zeros(n) + m
S =  readsnap(sn,'pos','disk')
x = S[:,0]
y = S[:,1]
z = S[:,2]

xCOM = (sum(M*x))/sum(M)
yCOM = (sum(M*y))/sum(M)
zCOM = (sum(M*z))/sum(M)
xpos = x-xCOM
ypos = y-yCOM
zpos = z-zCOM
x = xpos
y = ypos
z = zpos
### DATA ------------


def strength(xpos,ypos,mass,Rmin,Rmax,Nbins):
    #mass: array

    #cylindrical radius (isso projeta tudo em um plano, como se sumisse a coordenada z)
    R = sqrt(xpos**2 + ypos**2)

    #angles
    theta = arctan2(ypos,xpos)

    #interval size (intsize) #dividimos a galáxia em vários anéis (Nbisn) (nesse caso, 50 aneis de 0 a 10kpc)
    Rmin = float(Rmin) #kpc
    Rmax = float(Rmax) #kpc ------------- FOR NBINS
    Nbins = float(Nbins)
    dR = (Rmax-Rmin)/Nbins
    Nbins = int(Nbins)
    over = 0*dR #isso dá uma suavizada nos dados, mas geralmente não usamos, por isso tá zero

    #fourier parameters  (listas vazias pra preencher com os parâmetros de cada Nbin)
    a0=[]
    a2=[]
    b2=[]
    radius=[] #raio médio de cada anel

    for i in range(0, Nbins):
        R1 = i * dR
        R2 = R1 + dR #isso aqui vai incrementando pro programa calcular as coisas dentro de cada anel somente

        #condição
        cond = argwhere((R1-over < R) & (R2+over >= R)).flatten() #pega os índices de tudo que tá dentro do anel em questão
        msamp = mass[cond] #cria o array com a massa das partículas que têm os índices capturados anteriormente
        T = theta[cond] #angulos de todas as partículas da condição

        #A0 is the sum of the mass of all particles within the limits "R2-R1"
        A0  = sum(msamp)

        #sum of the mass of all particles within the limits "R2-R1" times cos(2T)
        A2  = sum(msamp*cos(2*T))

        #sum of the mass of all particles within the limits "R2-R1" times sin(2T)
        B2 = sum(msamp*sin(2*T))

        #add to lists (o append coloca uma coisa atrás da outra, em cada ciclo do for, nas listas vazias que criei antes dele)
        a0.append(A0)
        a2.append(A2)
        b2.append(B2)
        radius.append((R1+R2)/2.0)

    #building I2 (com esse parâmetro calculamos o A2)
    I2=[]
    for i in range(0, Nbins):
        i2 = sqrt(a2[i]**2 + b2[i]**2)/a0[i]
        I2.append(i2)

    A2 = max(I2) #força

    return A2, radius, I2

A2, radius, I2 = strength(x,y,M,0,50,50)

#create figure
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,8))

ax1 = plt.subplot(1,1,1)
plt.plot(radius, I2, '-', color='blue', markersize=1)

# y label
ax1.set_ylabel(r'$I_2$', fontsize=15)

# x label
ax1.set_xlabel(r'$R ~({\rm kpc})$', fontsize=15)

#save png
plt.savefig('1.jpg', dpi=500, bbox_inches='tight')
