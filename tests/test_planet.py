from Orbeez.planet import Planet
import numpy as np

def test_planet():
    """
    Tests the proper instantiation of a Planet object and that it integrates correctly
    """

    Planet(1, 1, 1)
    Planet.update_pos(1)

    assert Planet.theta == 1/p*2*np.pi + np.pi/2
    assert Planet.x == 1*np.cos(1/1*2*np.pi + np.pi/2)
    assert Planet.y == 1*np.sin(1/1*2*np.pi + np.pi/2)



