import matplotlib.pyplot as plt


def plot_orbit(planet_list: list, directory: str, name: str, num: int, figsize: tuple, title = False, dpi = 200,star_color='orange'):

    fig, ax = plt.subplots(figsize = figsize, layout = 'constrained')

    star = plt.Circle((0,0), 1, color = star_color)
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
    if title:
        ax.set_title(name, fontsize = 20)

    fig.savefig(directory+'/'+name+'_'+str(num)+'.jpg', dpi = dpi)

    plt.close()

def get_star_color(bp_rp):
    colors = [
        {"min": -3, "max": -0.26,  "color": '#a200ff'},
        {"min": -0.25, "max": -0.038, "color": '#0092ed'},
        {"min": -0.037, "max": 0.327, "color": '#00eded'},
        {"min": 0.326, "max": 0.767,  "color": '#57ed00'},
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