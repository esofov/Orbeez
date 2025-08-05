from planet import Planet
from orbitplot import plot_orbit
import numpy as np
from PIL import Image
import os
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive
from astropy import units as u

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
        plot_orbit(planet_list, directory, name, j, figsize)

    frames = [Image.open(directory+'/'+name+'_'+str(i)+'.jpg') for i in range(increments)]

    frame_1 = frames[0]
    frame_1.save(directory+'/'+name+'.gif', format='GIF', append_images=frames, save_all=True, duration=100, loop=0)

    for j in range(increments):
        os.remove(directory+'/'+name+'_'+str(j)+'.jpg')


def gif_from_archive(system_name: str, directory, name, figsize=(8,8), color_list=None, increments=100):
    data = NasaExoplanetArchive.query_criteria(
        table="ps", 
        select="pl_name, pl_orbsmax, pl_orbper, pl_radj, st_rad", 
        where="hostname='{}' AND default_flag=1".format(system_name), 
    )

    a_list = (data['pl_orbsmax'].to(u.Rsun)/data['st_rad']).value
    p_list = data['pl_orbper'].value
    r_list = (data['pl_radj'].to(u.Rsun)/data['st_rad']).value

    make_orbit_gif(a_list, p_list, r_list, directory=directory, name=name, figsize=figsize, color_list=color_list, increments=increments)

