import numpy as np
from scipy.optimize import fsolve

class Planet:
    """A class that stores the information for a planet.

    This class keeps track of the orbital distances, relative radii, and the color of each planet that should be plotted in a given system.

    Attributes:
        a (float): semi-major axis for planet in units of stellar radii
        p (float): period for planet in any unit consistent with other planetary orbits
        r (float): radius for planet in units of stellar radii
        e (float): eccentricity for planet
        w (float): argument of periastron for planet in units of radians
        color (str): color which the planet itself (not the orbital circle) will be plotted with
        x (float): x-coordinate defining position of planet along orbit 
        y (float): y-coordinate defining position of planet along orbit
    """
    def __init__(self, a, p, r, e, w, color, planet_r_scale = 25):
        """
        Args:
            a (float): semi-major axis for planet in units of stellar radii
            p (float): period for planet in any unit consistent with other planetary orbits
            r (float): radius for planet in units of stellar radii
            e (float): eccentricity for planet
            w (float): argument of periastron for planet in units of radians
            color (str): color which the planet itself (not the orbital circle) will be plotted with
            planet_r_scale (float, optional): Factor by which to scale up the planet radii. Default is 25.
        """

        self.a = a
        self.p = p
        self.r = r*planet_r_scale
        self.e = e
        self.w = w
        if color is None:
            self.color = 'black'
        else:
            self.color = color
        self.x  = 0
        self.y = self.a

        if self.e > 0:

            focc = -np.pi/2 - self.w
            Eocc = np.arctan2(np.sqrt(1-self.e**2)*np.sin(focc), self.e+np.cos(focc))
            self.Tp = -self.p/(2*np.pi) * (Eocc - self.e*np.sin(Eocc))
        
    def update_pos(self, t):
        """
        Update the position of the planet along its orbit given a timestep.

        Args:
            t (float): timestep defining how far to move planet along orbit
        """
      
        if self.e == 0:

            theta = t/self.p*2*np.pi + np.pi/2
            self.x = self.a*np.cos(theta)
            self.y = self.a*np.sin(theta)

        else:

            E = self.solve_for_E(t)
            f = np.arctan2(np.sqrt(1-self.e**2)*np.sin(E), np.cos(E)-self.e)
            d = self.a*(1-self.e**2)/(1+self.e*np.cos(f))
            self.x = -d*np.cos(self.w+f)
            self.y = -d*np.sin(self.w+f)

    def solve_for_E(self, t):
        """
        Solve or the eccentric anomaly of the planet at a given time t.

        Args:
            t (float): time at which to calculate the eccentric anomaly
        """

        return fsolve(lambda x: x - self.e * np.sin(x) - 2*np.pi / self.p * (t-self.Tp), 2*np.pi / self.p * (t-self.Tp))[0]

        
