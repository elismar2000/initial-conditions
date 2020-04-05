from astropy.table import Table
import numpy as np
import matplotlib.pyplot as plt
from lmfit import Model, Parameters

t_path = '/home/elismar/Documentos/Fisica/IC/GalMer/inflow/Tabelas_GalMer/tables_arp245_orbit1'
t = Table.read(t_path, 1)

gal = t['GAL'] == 1
part = t['P_TYPE'][gal] == 1

#star particles
x = t['X'][gal][part]
y = t['Y'][gal][part]
z = t['Z'][gal][part]
m = t['MASS'][gal][part]

#bulge particles:
x_bulge = x[48000:59999]
y_bulge = y[48000:59999]
z_bulge = z[48000:59999]
m_bulge = m[48000:59999]

#calculating center of mass
def cm(x, y, z, m):
    mass = np.sum(m)
    x_cm = np.sum(x*m)/mass
    y_cm = np.sum(y*m)/mass
    z_cm = np.sum(z*m)/mass
    return x_cm, y_cm, z_cm

xcm_all, ycm_all, zcm_all = cm(t['X'][gal], t['Y'][gal], t['Z'][gal], t['MASS'][gal])

#calculating distances from cm
def distance(position):
    cm = np.array([xcm_all, ycm_all, zcm_all])
    distance = np.sqrt(np.sum(np.square(position - cm)))
    return distance

#====================================
#STAR PARTICLES DISTRIBUTION
#====================================
plot1 = False
if plot1:
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x[0:48000], y[0:48000], 'k,')
    ax.plot(x[48000:59999], y[48000:59999], 'b,')
    ax.plot(xcm_all, ycm_all, 'o', color='yellow')
    plt.show()

#====================================
#MODELS
#====================================
def model_galmer(r, M_bulge, r_bulge):
    return (3 * M_bulge / (4 * np.pi * r_bulge**3)) * (1 + (r**2 / r_bulge**2))**(-5/2)

def model_galstep(r, mass, a):
    return (mass / (2 * np.pi)) * (a / (r * (r + a)**3))

plot2 = True
if plot2:
    r = np.linspace(0, 7.1, 1000)
    M_bulge = 2.3e+10 #solar masses
    r_bulge = 2.0 #kpc
    a_bulge = 1.5
    rho_bulge_galmer = model_galmer(r, M_bulge, r_bulge)
    rho_bulge_galstep = model_galstep(r, M_bulge, a_bulge)

    fig, axs = plt.subplots(1, 3, figsize=(40, 40), sharex=True)
    axs[0].plot(r, rho_bulge_galmer, label='galmer model')
    axs[0].set_title('GalMer model')
    axs[0].text(2.5, 5e+8, 'Mass = %1.3f' %M_bulge)
    axs[0].text(2.5, 4.5e+8, 'Radius = %1.3f' %r_bulge)
    axs[0].set_xlabel('r (Kpc)')
    axs[0].set_ylabel(r'$rho (M \odot / kpc^3)$')

    axs[1].plot(r, rho_bulge_galstep, label='galstep model')
    axs[1].set_title('Galstep model')
    axs[1].set_xlabel('r (Kpc)')
    axs[1].set_ylabel(r'$rho (M \odot / kpc^3)$')

#====================================
#CALCULATING DISTANCES FROM CENTER OF MASS
#====================================

bulge_positions = np.vstack((x_bulge, y_bulge, z_bulge))
distances = np.zeros(np.size(bulge_positions, axis=1))
for i in range(np.size(bulge_positions, axis=1)):
    distances[i] = distance(bulge_positions[:, i])

#====================================
#CALCULATING DENSITIES FOR EACH SPHERICAL SHELL
#====================================

dr = (distances.max()  - distances.min()) / 100
radii = np.arange(distances.min(), distances.max(), dr)
bulge_particles_mass = m_bulge[0] * 2.25e+9
rho = np.zeros_like(radii)
i = 0
for r in radii:
    particles = (distances > r) & (distances < r + dr)
    n = np.sum(particles)
    rho[i] = n * bulge_particles_mass / (4 * np.pi * (r + dr)**2 * dr)
    i += 1

#=====================================
#FITTING MODELS TO DATA
#=====================================

model = Model(model_galstep)
params = Parameters()
params.add('mass', value=2.3e+10)
params.add('a', value=1.5)
#params = model.make_params(mass=2.3e+10, a=3.0)
result_galstep = model.fit(rho, params, r=radii)


print(result_galstep.fit_report())

#=====================================

if plot2:
    axs[2].plot(radii, rho, '.')
    axs[2].plot(radii, result_galstep.best_fit, 'r-', label='best fit for galstep model')
    axs[2].text(1.5, 0.8e+9, 'mass = %1.3i' %result_galstep.values['mass'])
    axs[2].text(1.5, 0.75e+9, 'a = %1.3i' %result_galstep.values['a'])
    axs[2].set_title('Galstep model fitting')
    axs[2].set_xlabel('r (Kpc)')
    axs[2].set_ylabel(r'$rho (M \odot / kpc^3)$')

    plt.legend(loc=0)
    plt.show()
