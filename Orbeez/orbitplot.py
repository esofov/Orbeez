import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse


def plot_orbit(planet_list: list, directory: str, name: str, num: int, figsize: tuple, title = False, dpi = 200,star_color='orange'):
    """Plots planetary system

    Plots the plantary system orbits given a list of planets to be saved as a GIF.

    Args:
        planetary_list (list): List of Planet objects representing the planets in the system.
        directory (str): Path to the directory in which to save plots.
        name (str): Name of plot files.
        num (int): Number representing order of plot in .gif animation frames. 
            Follows <name>_<num>.jpg convention.
        figsize (tuple, optional): Plot figure size in units of inches formatted as (width, height). 
            Default is (8, 8)
        title (bool, optional): Binary determiner for plot title to be included in each plot. 
            Default is False.
        dpi (int, optional): Dots per inch to use when saving the plot. 
            If kernel is crashing, try reducing the DPI.
            Default is 200
        star_color (str, optional): matplotlib color to use for the star. 
            Default is 'orange'.
    """
    fig, ax = plt.subplots(figsize = figsize, layout = 'constrained')

    star = plt.Circle((0,0), 1, color = star_color)
    ax.add_patch(star)
    
    aplusrlist = []

    for planet in planet_list:

        aplusrlist.append(planet.a*(1+planet.e)+planet.r)

        if planet.e == 0:
            orb = plt.Circle((0,0), planet.a, edgecolor = 'black', facecolor = 'None')

        else:
            orb = Ellipse((planet.a*planet.e*np.cos(planet.w), planet.a*planet.e*np.sin(planet.w)), 2*planet.a, 2*planet.a*np.sqrt(1-planet.e**2), angle = planet.w*180/np.pi, edgecolor = 'black', facecolor = 'None')

        ax.add_patch(orb)

        planetcircle = plt.Circle((planet.x, planet.y), planet.r, color = planet.color)
        ax.add_patch(planetcircle)

    axislim = max(aplusrlist)*1.1

    ax.set_xlim(-axislim, axislim)
    ax.set_ylim(-axislim, axislim)
    ax.set_aspect('equal')
    ax.axis('off')
    if title:
        ax.set_title(name, fontsize = 20)

    fig.savefig(directory+'/'+name+'_'+str(num)+'.jpg', dpi = dpi)

    plt.close()

def get_star_color(bp_rp):
    """Sets color of star for plots

    Defines the color of the star when passed data queried from Exoplanet Archive given BP/RP from Gaia DR2.

    Args:
        bp_rp (float): Color value pulled from Gaia DR2 with listed Exoplanet Archive Gaia_id using BP/RP.

    Returns:
        str: hexcode color string
    """
    colors = [
        {"min": -3, "max": -0.26,  "color": '#0000ff'},
        {"min": -0.25, "max": -0.038, "color": '#699bff'},
        {"min": -0.037, "max": 0.327, "color": '#00eded'},
        {"min": 0.326, "max": 0.767,  "color": "#F9E400"},
        {"min": 0.768, "max": 0.984, "color": '#ffbe0d'},
        {"min": 0.983, "max": 1.85, "color": '#ff801f'},
        {"min": 1.85, "max": 7.0, "color": '#d40b0b'}
    ]
    for i in range(len(colors)):
        if bp_rp>colors[i]['min'] and bp_rp<colors[i]['max']:
            return colors[i]['color']
    if bp_rp<-3: 
        return '#5b7cff'
    if bp_rp>7.0:
        return '#ffa448'