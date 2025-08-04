import matplotlib.pyplot as plt


def plot_orbit(planet_list: list, directory: str, num: int, figsize: tuple):

    fig, ax = plt.subplots(figsize = figsize)

    star = plt.Circle((0,0), 1, color = 'orange')
    ax.add_patch(star)

    for planet in planet_list:

        orb = plt.Circle((0,0), planet.a, edgecolor = 'black', facecolor = 'None')
        ax.add_patch(orb)

        planetcircle = plt.Circle((planet.x, planet.y), planet.r, color = planet.color)
        ax.add_patch(planetcircle)

    ax.set_aspect('equal')
    ax.axis('off')

    fig.savefig(directory+str(num)+'.jpg')

    plt.close()