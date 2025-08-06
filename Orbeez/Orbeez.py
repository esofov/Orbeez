import os
import numpy as np
from planet import Planet
from PIL import Image
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive
from astropy import units as u
from orbitplot import plot_orbit, get_star_color
import tqdm
from astroquery.gaia import Gaia



def make_orbit_gif(a_list, p_list, r_list, directory, name, figsize=(8,8), num_periods = 1, gif_duration = 10, color_list=None,star_color='orange', num_frames=100, title = False, dpi = 200):

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

    if np.min(p_list)*num_frames < 16:
        num_frames = int(np.ceil(16/np.min(p_list)))

    planet_list = []

    for i in range(len(a_list)):
        entry = Planet(a_list[i], p_list[i], r_list[i], color_list[i])
        planet_list.append(entry)

    print('Generating images...')
    for j in tqdm.tqdm(range(num_frames)):
        for planet in planet_list:
            planet.update_pos(j/num_frames*num_periods)
        plot_orbit(planet_list, directory, name, j, figsize, title = title, dpi = dpi, star_color=star_color)

    print('Stitching frames...')
    frames = [Image.open(directory+'/'+name+'_'+str(i)+'.jpg') for i in tqdm.tqdm(range(num_frames))]

    frame_1 = frames[0]
    frame_1.save(directory+'/'+name+'.gif', format='GIF', append_images=frames, save_all=True, duration=gif_duration/num_frames*1000, loop=0)

    print('Deleting images...')
    for j in tqdm.tqdm(range(num_frames)):
        os.remove(directory+'/'+name+'_'+str(j)+'.jpg')


def gif_from_archive(system_name: str, directory, figsize=(8,8), num_periods = 1, gif_duration = 10, color_list=None, num_frames=100, title = False, dpi = 200):
    data = NasaExoplanetArchive.query_criteria(
        table="ps", 
        select="pl_name, pl_orbsmax, pl_orbper, pl_radj, st_rad, gaia_id",
        where="hostname='{}' AND default_flag=1".format(system_name),
    )

    data.sort('pl_orbper')

    a_list = (data['pl_orbsmax'].to(u.Rsun)/data['st_rad']).value
    p_list = data['pl_orbper'].value
    r_list = (data['pl_radj'].to(u.Rsun)/data['st_rad']).value

    gaiaid=data['gaia_id'][0].split()[2]
    query = f"SELECT bp_rp FROM gaiadr2.gaia_source WHERE source_id = {gaiaid}"
    job = Gaia.launch_job(query)
    bp_rp= job.get_data()['bp_rp'][0]

    star_color=get_star_color(bp_rp)
    

    make_orbit_gif(a_list, p_list, r_list, directory=directory, name=system_name, figsize=figsize, num_periods=num_periods, gif_duration=gif_duration, color_list=color_list, star_color=star_color, num_frames=num_frames, title=title, dpi=dpi)

