import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.collections import LineCollection

def wavelength_to_rgb(wavelength, gamma=1, t1=0, t2=0, At=1):
    ''' taken from http://www.noah.org/wiki/Wavelength_to_RGB_in_Python
    This converts a given wavelength of light to an
    approximate RGB color value. The wavelength must be given
    in nanometers in the range from 380 nm through 750 nm
    (789 THz through 400 THz).

    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    Additionally alpha value set to 0.5 outside range
    '''
    wavelength = float(wavelength)
    
    
    if 380-t1 <= wavelength < 380:
        attenuation = 0.3 * (wavelength - 380 + t1) / t1
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
        A = ((wavelength-380+t1) / t1) * (1-At) + At
    elif 380 <= wavelength < 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
        A = 1
    elif 440 <= wavelength < 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
        A = 1
    elif 490 <= wavelength < 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
        A = 1
    elif 510 <= wavelength < 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
        A = 1
    elif 580 <= wavelength < 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
        A = 1
    elif 645 <= wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
        A = 1
    elif 750 < wavelength <= 750 + t2:
        attenuation = 0.3 * (750 + t2 - wavelength) / t2
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
        A = ((750 + t2 - wavelength) / t2) * (1-At) + At
    else:
        R = 0.0
        G = 0.0
        B = 0.0
        A = At
        
    return (R, G, B, A)

def get_spectral_cmap(clim, At):
    clim=[clim[0]-1, clim[1]+1]
    if clim[0] < 380:
        t1 = 380 - clim[0]
    else:
        t1=0
    if clim[1] > 750:
        t2 = clim[1] - 750
    else:
        t2=0
        
    norm = plt.Normalize(*clim)
    wl = np.arange(clim[0], clim[1]+1)
    colorlist = list(zip(norm(wl), [wavelength_to_rgb(w, t1=30, t2=30, At=At) for w in wl]))
    spectralmap = LinearSegmentedColormap.from_list("spectrum", colorlist)
    return spectralmap

def spectral_fill(ax, x, y, At=1):   
    xlim = [min(x), max(x)]
    ylim = ax.get_ylim()
    yz = [ylim[0], ylim[1]]
    Xs, Ys = np.meshgrid(x, yz)
    extent = (xlim[0], xlim[1], ylim[0], ylim[1])
    
    clim = [349, 781]
    norm = plt.Normalize(*clim)
    wl = np.arange(clim[0], clim[1]+1)
    colorlist = list(zip(norm(wl), [wavelength_to_rgb(w, t1=30, t2=30, At=At) for w in wl]))
    spectralmap = LinearSegmentedColormap.from_list("spectrum", colorlist)

    ax.imshow(Xs, clim=clim, extent=extent, cmap=spectralmap, aspect='auto', alpha=0.9)
    ax.fill_between(x, y, ylim[1], color='w')
    
def spectral_line(ax, x, y, linestyle='solid', linewidth=2):
    cols = np.linspace(0,1,len(x))
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    
    rgba_list = list([wavelength_to_rgb(w, t1=30, t2=30, At=1) for w in x])

    lc = LineCollection(segments, color=rgba_list, linestyle=linestyle, linewidth=linewidth)
    lc.set_array(cols)
    ax.add_collection(lc)