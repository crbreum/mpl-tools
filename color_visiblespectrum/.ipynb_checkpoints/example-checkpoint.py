import numpy as np
import matplotlib.pyplot as plt

from visiblespectrum import *

# Create wavelength and spectrum arrays
wavelengths = np.linspace(200, 1000, 1000)
spectrum = np.sin(wavelengths*0.1)**2 * np.exp(-2e-5*(wavelengths-600)**2)


# ----------------------------------------------------------------------------
fig, ax = plt.subplots(1, 1, figsize=(6, 3), tight_layout=True)

spectral_line(ax, wavelengths, spectrum)

ax.set_xlabel('Wavelength (nm)')
ax.set_ylabel('Intensity')
ax.grid()
ax.tick_params(axis='both', direction='in', grid_alpha=0.3, top=True, right=True)
ax.set_xlim(200,1000)
ax.set_ylim(0,1)

plt.show()


# ----------------------------------------------------------------------------
fig, ax = plt.subplots(1, 1, figsize=(6, 3), tight_layout=True)

ax.plot(wavelengths, spectrum, color='black', linewidth=2)

ax.set_xlabel('Wavelength (nm)')
ax.set_ylabel('Intensity')
ax.grid()
ax.tick_params(axis='both', direction='in', grid_alpha=0.3, top=True, right=True)
ax.set_xlim(200,1000)
ax.set_ylim(0,1)

spectral_fill(ax, wavelengths, spectrum, At=1)

plt.show()