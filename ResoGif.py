from planet import Planet
from orbitplot import plot_orbit
import numpy as np
from PIL import Image

def make_orbit_gif(a_list, p_list, r_list, directory, name, figsize=(8,8), color_list=None, increments=100):
    if color_list is None:
        color_list = [None] * len(a_list)

    p_list = np.array(p_list)/max(p_list)

    planet_list = []

    for i in range(len(a_list)):
        entry = Planet(a_list[i], p_list[i], r_list[i], color_list[i])
        planet_list.append(entry)

    for j in range(increments):
        for planet in planet_list:
            planet.update_pos(j/increments)
        plot_orbit(planet_list, directory, j, figsize)

    frames = [Image.open(directory+str(i)+'.jpg') for i in range(increments)]

    frame_1 = frames[0]
    frame_1.save(directory+name+'.gif', format='GIF', append_images=frames, save_all=True, duration=100, loop=0)


