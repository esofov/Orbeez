import os
from Orbeez import orbeez

def test_gif_from_archive(directory: str='tests/end-to-end-tests/'):
    """
    End to end test for making .gif animation from Exoplanet Archive entry

    Args:
        directory (str, optional): Path to the directory in which to save the resulting .gif animation.
            Default is end-to-end-tests folder.
    """

    orbeez.gif_from_archive('TRAPPIST-1', directory)
    assert os.path.isfile(directory+'TRAPPIST-1.gif')



test_gif_from_archive()

