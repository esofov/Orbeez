import os
from Orbeez import orbeez

def test_make_orbit_gif(directory: str='tests/end-to-end-tests/'):
    """
    End to end test for making .gif animation from user generated entry

    Args:
        directory (str, optional): Path to the directory in which to save the resulting .gif animation.
            Default is end-to-end-tests folder.
    """

    a_list = [1, 2, 3]
    p_list = [1, 2, 3]
    r_list = [1, 1, 1]

    orbeez.make_orbit_gif(a_list, p_list, r_list, directory, 'planet')
    assert os.path.isfile(directory+'planet.gif')


test_make_orbit_gif()