from astropy.io import fits
from astropy.wcs import WCS
import matplotlib.pyplot as plt

image = '/home/elismar/Documentos/Fisica/IC/imfit-1.7.1/ngc2992/images/2MASS/NGC2992_2MASS_h-band.fits'

data = fits.getdata(image)
header = fits.getheader(image)

w = WCS(header)

fig = plt.subplot(projection=w)
fig.imshow(data, cmap='cividis')

from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
axins = zoomed_inset_axes(fig, 10, loc=1)
axins.plot([1, 1], [0, 1], color='k')
axins.plot([0, 1], [0, 0], color='k')
axins.text(0.8, 0.8, 'N')
axins.text(0.1, 0.1, 'E')
plt.yticks(visible=False)
plt.xticks(visible=False)
ax = plt.gca()
ax.axes.xaxis.set_visible(False)
ax.axes.yaxis.set_visible(False)

plt.show()
