import numpy as np


class Planet:
    """A class that stores the information for a planet.

    This class keeps track of the orbital distances, relative radii, and the color of each planet that should be plotted in a given system.

    Attributes:
        a (float): semi-major axis for planet in units of stellar radii
        p (float): period for planet in any unit consistent with other planetary orbits
        r (float): radius for planet in units of stellar radii
        color (str): color which the planet itself (not the orbital circle) will be plotted with
        x (float): x-coordinate defining position of planet along orbit 
        y (float): y-coordinate defining position of planet along orbit
    """
    def __init__(self, a, p, r, color):
        """
        Args:
            a (float): semi-major axis for planet in units of stellar radii
            p (float): period for planet in any unit consistent with other planetary orbits
            r (float): radius for planet in units of stellar radii
            color (str): color which the planet itself (not the orbital circle) will be plotted with
        """
        self.a = a
        self.r = r*25
        if color is None:
            self.color = 'black'
        else:
            self.color = color
        self.x  = 0
        self.y = self.a
        self.p = p

    def update_pos(self, t):
        """Update the position of the planet along its orbit given a timestep

        Args:
            t (float): timestep defining how far to move planet along orbit
        """
        theta = t/self.p*2*np.pi + np.pi/2
        self.x = self.a*np.cos(theta)
        self.y = self.a*np.sin(theta)