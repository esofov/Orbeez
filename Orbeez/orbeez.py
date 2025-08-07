import os
import numpy as np
from Orbeez.planet import Planet
from PIL import Image
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive
from astropy import units as u
from Orbeez.orbitplot import plot_orbit, get_star_color
import tqdm
from astroquery.gaia import Gaia



def make_orbit_gif(a_list, p_list, r_list, directory, name, e_list = None, w_list = None, figsize=(8,8), num_periods = 1, gif_duration = 10.0, color_list=None, star_color='orange', num_frames=100, title = False, dpi = 200, planet_r_scale = 25):
    """Makes a .gif animation of the orbits of the input planetary system.

    Generates a .gif animation of the orbits of planets in a system architecture defined by the user.

    Args:
        a_list (array_like): List of semimajor axis values for the planets in the system, in units of stellar radii.
        p_list (array_like): List of orbital period values for the planets in the system, in any consistent units.
        r_list (array_like): List of planetary radii values for the planets in the system, in units of stellar radii.
        directory (str): Path to the directory in which to save the resulting .gif animation.
        name (str): Name of the resulting .gif animation.
        e_list (array_like, optional): List of eccentricity values for the planets in the system. If None, default
            initializes the eccentricities of all planets to 0. Default is None.
        w_list (array_like, optional): List of arguments of periastron for the planets in the system, in units of
            radians. If None, default initializes the arguments of periastron of all planets to pi/2. Default is None.
        figsize (tuple, optional): Size of the .gif animation in units of inches. Formatted as (width, height).
            Default is (8,8).
        num_periods (int, optional): Number of periods of the outermost planet to animate. Default is 1.
        gif_duration (float, optional): Duration of the whole .gif animation in seconds. Default is 10 seconds.
        color_list (array_like, optional): List of matplotlib colors to loop through when plotting the planets.
            Default is None, which sets the planets to be black.
        star_color (str, optional): matplotlib color to use for the star. Default is orange.
        num_frames (int, optional): Number of frames to use in the .gif animation. More frames will make the
            animation more smooth, but will slow down the creation process. Too many frames may cause the kernel
            to crash when making the .gif. Default is 100.
        title (bool, optional): Whether or not to include the name as a title above the animation. Default is False.
        dpi (int, optional): Dots per inch to use when saving the frames. If the kernel is crashing, try reducing the
            dpi. Default is 200.
        planet_r_scale (float, optional): Factor by which to scale up the planet radii. Default is 25.
    """

    if e_list is None or w_list is None:

        e_list = [0]*len(a_list)
        w_list = [np.pi/2]*len(a_list)
        

    if not len(a_list) == len(p_list) == len(r_list) == len(e_list) == len(w_list):
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
        entry = Planet(a_list[i], p_list[i], r_list[i], e_list[i], w_list[i], color_list[i], planet_r_scale = planet_r_scale)
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


def gif_from_archive(system_name, directory, figsize=(8,8), num_periods = 1, gif_duration = 10.0, color_list=None, num_frames=100, title = False, dpi = 200, planet_r_scale = 25):
     
    """Generates gif of exoplanet system with user entered name from NASA Exoplanet Archive.

    Generates a .gif animation of the orbits of planets in a system architecture defined by data pulled from the Exoplanet Archive chosen by the user by passing the name of a host star.

    Args:
        system_name (str): Name of the exoplanet system as found in NASA exoplanet Archive.
        directory (str): Directory where you would like the gif to be saved.
        figsize (tuple, optional): Size of the .gif animation in units of inches. Formatted as (width, height).
            Default is (8,8).
        num_periods (int, optional): Number of periods of the outermost planet to animate. Default is 1.
        gif_duration (float, optional): Duration of the whole .gif animation in seconds. Default is 10 seconds.
        color_list (list, optional): List of matplotlib colors to loop through when plotting the planets.
            Default is None, which sets the planets to be black.
        num_frames (int, optional): Number of frames to use in the .gif animation. More frames will make the
            animation more smooth, but will slow down the creation process. Too many frames may cause the kernel
            to crash when making the .gif. Default is 100.
        title (bool, optional): Whether or not to include the name as a title above the animation. Default is False.
        dpi (int, optional): Dots per inch to use when saving the frames. If the kernel is crashing, try reducing the
            dpi. Default is 200.
        planet_r_scale (float, optional): Factor by which to scale up the planet radii. Default is 25.
    """
    
    data = NasaExoplanetArchive.query_criteria(
        table="ps", 
        select="pl_name, pl_orbsmax, pl_orbper, pl_radj, pl_orbeccen, pl_orblper, st_rad, gaia_id",
        where="hostname='{}' AND default_flag=1".format(system_name),
    )

    data.sort('pl_orbper')

    a_list = (data['pl_orbsmax'].to(u.Rsun)/data['st_rad']).value
    p_list = data['pl_orbper'].value
    r_list = (data['pl_radj'].to(u.Rsun)/data['st_rad']).value
    e_list = (data['pl_orbeccen']).value
    w_list = (data['pl_orblper']).value * np.pi/180

    i = np.where(np.isnan(e_list))[0]
    e_list[i] = 0
    w_list[i] = np.pi/2

    if np.any(np.isnan(w_list)):
        print('Some nan arguments of periastron, setting to pi/2.')
        i = np.where(np.isnan(w_list))[0]
        w_list[i] = np.pi/2

    if np.all(np.isnan(a_list)):
        print('No semi-major axes available.')
        return
    
    if np.all(np.isnan(p_list)):
        print('No periods available.')
        return
    
    if np.any(np.isnan(a_list) & np.isnan(p_list)):
        print('One planet has no semi-major axis and no period.')
        return

    if np.any(np.isnan(a_list)):
        i = np.where(~np.isnan(a_list))[0][0]
        p0 = p_list[i]
        a0 = a_list[i]
        j = np.where(np.isnan(a_list))[0]
        a_list[j] = (p_list[j]/p0)**(2/3) * a0

    if np.any(np.isnan(p_list)):
        i = np.where(~np.isnan(p_list))[0][0]
        p0 = p_list[i]
        a0 = a_list[i]
        j = np.where(np.isnan(p_list))[0]
        p_list[j] = (a_list[j]/a0)**(3/2) * p0

    gaiaid=data['gaia_id'][0].split()[2]
    query = f"SELECT bp_rp FROM gaiadr2.gaia_source WHERE source_id = {gaiaid}"
    job = Gaia.launch_job(query)
    bp_rp= job.get_data()['bp_rp'][0]

    star_color=get_star_color(bp_rp)
    

    make_orbit_gif(a_list, p_list, r_list, directory=directory, name=system_name, e_list = e_list, w_list = w_list, figsize=figsize, num_periods=num_periods, gif_duration=gif_duration, color_list=color_list, star_color=star_color, num_frames=num_frames, title=title, dpi=dpi, planet_r_scale = planet_r_scale)

