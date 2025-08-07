import os
from Orbeez import orbitplot
from Orbeez.planet import Planet
import numpy as np


def test_plot_orbit():
    """
    Tests whether plot_orbit generates a .png file of a single GIF frame
    """
    p = Planet(1, 1, 1, 0, np.pi/2, 'blue')

    orbitplot.plot_orbit([p], directory='tests/', name='test_plot', num=1, figsize=(8, 8))

    assert os.path.isfile('tests/test_plot_1.jpg')
