import os
import numpy as np
from planet import Planet
from PIL import Image
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive
from astropy import units as u
from orbitplot import plot_orbit
import tqdm



def make_orbit_gif(a_list, p_list, r_list, directory, name, figsize=(8,8), num_periods = 1, gif_duration = 10, color_list=None, increments=100, title = False):

    if not len(a_list) == len(p_list) == len(r_list):
        print('Planet arrays not same length')
        return 
    
    if np.any(np.isnan(r_list)):
        print('Query returned some nan planetary radii, setting radii to default value of 0.01')
        indices = np.where(np.isnan(r_list))[0]
        for i in indices:
            r_list[i] = 0.01

    if color_list is None:
        color_list = [None] * len(a_list)
    elif len(color_list) < len(a_list):
        color_list *= int(np.ceil(len(a_list)/len(color_list)))
        

    p_list = np.array(p_list)/max(p_list)

    if np.min(p_list)*increments < 16:
        increments = int(np.ceil(16/np.min(p_list)))

    planet_list = []

    for i in range(len(a_list)):
        entry = Planet(a_list[i], p_list[i], r_list[i], color_list[i])
        planet_list.append(entry)

    print('Generating images...')
    for j in tqdm.tqdm(range(increments)):
        for planet in planet_list:
            planet.update_pos(j/increments*num_periods)
        plot_orbit(planet_list, directory, name, j, figsize, title = title)

    print('Stitching frames...')
    frames = [Image.open(directory+'/'+name+'_'+str(i)+'.jpg') for i in tqdm.tqdm(range(increments))]

    frame_1 = frames[0]
    frame_1.save(directory+'/'+name+'.gif', format='GIF', append_images=frames, save_all=True, duration=gif_duration/increments*1000, loop=0)

    print('Deleting images...')
    for j in tqdm.tqdm(range(increments)):
        os.remove(directory+'/'+name+'_'+str(j)+'.jpg')


def gif_from_archive(system_name: str, directory, figsize=(8,8), num_periods = 1, gif_duration = 10, color_list=None, increments=100, title = False):
    data = NasaExoplanetArchive.query_criteria(
        table="ps", 
        select="pl_name, pl_orbsmax, pl_orbper, pl_radj, st_rad", 
        where="hostname='{}' AND default_flag=1".format(system_name), 
    )

    a_list = (data['pl_orbsmax'].to(u.Rsun)/data['st_rad']).value
    p_list = data['pl_orbper'].value
    r_list = (data['pl_radj'].to(u.Rsun)/data['st_rad']).value

    make_orbit_gif(a_list, p_list, r_list, directory=directory, name=system_name, figsize=figsize, num_periods=num_periods, gif_duration=gif_duration, color_list=color_list, increments=increments, title=title)

