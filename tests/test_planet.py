from Orbeez.planet import Planet
import numpy as np
import pytest


def test_planet():
    """
    Tests the proper instantiation of a Planet object and that it integrates correctly
    """

    p = Planet(1, 1, 1, 0, np.pi/2, 'blue')
    p.update_pos(t=1)

    assert p.x == pytest.approx(1*np.cos(1/1*2*np.pi + np.pi/2), abs=1e-3)
    assert p.y == pytest.approx(1*np.sin(1/1*2*np.pi + np.pi/2), abs=1e-3)
