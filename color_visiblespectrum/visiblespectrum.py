import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.collections import LineCollection

def lam2rgba(wavelength, gamma=1, t1=30, t2=30, At=1):
    '''
    Function to generate a RGBA values corresponding to visible light
    
    Inputs
    - wavelength : wavelength of light in nm
    - gamma : gamma value
    - t1 : range in nm of fadein before 380nm
    - t2 : range in nm of fadeout after 750nm
    - At : alpha value of the colors outside [380, 750]nm
    
    Outputs
    - (R,G,B,A) : list element with R, G, B and A values
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

def spectral_cmap(clim, At):
    '''
    Function to generate a colormap object that span the colors of visible light
    
    Inputs
    - clim : wavelength range in nm to generate colormap between [lam_min, lam_max]
    - At : alpha value of the range outside [380, 750]
    
    Outputs
    - spectralmap : colormap objects based on lookup tables using linear segments.
    '''
    
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
    colorlist = list(zip(norm(wl), [lam2rgba(w, t1=30, t2=30, At=At) for w in wl]))
    spectralmap = LinearSegmentedColormap.from_list("spectrum", colorlist)
    return spectralmap

def spectral_fill(ax, x, y, At=1):
    '''
    Function that adds a fill based on the visible light colormap between the lower ylim and a curve. This function should be called after the ylim has been set.
    
    Inputs
    - ax : pyplot axis object
    - x : wavelength array
    - y : spectrum array
    - At : parameter that sets the alpha value of the range outside [380, 750]
    
    Outputs
    - Adds an image to the plot axis with vertical lines corresponding to the visible light colormap
    - Adds a white fill between the spectrum and upper ylim
    '''
    
    xlim = [min(x), max(x)]
    ylim = ax.get_ylim()
    yz = [ylim[0], ylim[1]]
    Xs, Ys = np.meshgrid(x, yz)
    extent = (xlim[0], xlim[1], ylim[0], ylim[1])
    
    clim = [349, 781]
    norm = plt.Normalize(*clim)
    wl = np.arange(clim[0], clim[1]+1)
    colorlist = list(zip(norm(wl), [lam2rgba(w, t1=30, t2=30, At=At) for w in wl]))
    spectralmap = LinearSegmentedColormap.from_list("spectrum", colorlist)

    ax.imshow(Xs, clim=clim, extent=extent, cmap=spectralmap, aspect='auto', alpha=0.9)
    ax.fill_between(x, y, ylim[1], color='w')
    
def spectral_line(ax, x, y, linestyle='solid', linewidth=2):
    '''
    Function that plots a spectrum with a gradient color correponding to the visible light colormap
    
    Inputs
    - ax : pyplot axis object
    - x : wavelength array
    - y : spectrum array
    
    Outputs
    - Adds a LineCollection object to the plot axis with lines correponding to the input spectrum
    - The color of each line is based on the RGBA value of its starting point
    '''
    cols = np.linspace(0,1,len(x))
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    
    rgba_list = list([lam2rgba(w, t1=30, t2=30, At=1) for w in x])

    lc = LineCollection(segments, color=rgba_list, linestyle=linestyle, linewidth=linewidth)
    lc.set_array(cols)
    ax.add_collection(lc)