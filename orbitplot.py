import matplotlib.pyplot as plt


def plot_orbit(planet_list: list, directory: str, name: str, num: int, figsize: tuple):

    fig, ax = plt.subplots(figsize = figsize, layout = 'constrained')

    star = plt.Circle((0,0), 1, color = 'orange')
    ax.add_patch(star)
    
    aplusrlist = []

    for planet in planet_list:

        aplusrlist.append(planet.a+planet.r)

        orb = plt.Circle((0,0), planet.a, edgecolor = 'black', facecolor = 'None')
        ax.add_patch(orb)

        planetcircle = plt.Circle((planet.x, planet.y), planet.r, color = planet.color)
        ax.add_patch(planetcircle)

    axislim = max(aplusrlist)*1.1

    ax.set_xlim(-axislim, axislim)
    ax.set_ylim(-axislim, axislim)
    ax.set_aspect('equal')
    ax.axis('off')

    fig.savefig(directory+'/'+name+'_'+str(num)+'.jpg', dpi = 200)

    plt.close()