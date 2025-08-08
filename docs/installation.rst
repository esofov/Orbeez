.._installation:

Installation
===============

For Users
+++++++++

``Orbeez`` is registered on ``pip``, and is tested to work in Python>3.10.
To install ``Orbeez``, use the following command:

.. code-block:: bash
	
	$ pip install Orbeez

We recommend installing and running ``Orbeez`` in a ``conda`` virtual
environment. Install ``miniconda`` `here <https://conda.io/miniconda.html>`_, 
then see instructions `here <https://conda.io/docs/user-guide/tasks/manage-environments.html>`_
to learn more about ``conda`` virtual environments.

For Developers
++++++++++++++

``Orbeez`` is not really being developed actively. The following method for 
installing ``Orbeez`` will allow you to use it and make changes to it. 
After cloning the Git repository, run the following command in the top level 
of the repo:

.. code-block:: bash
	
	$ pip install -r requirements.txt
	$ pip install -e . --upgrade

Issues?
+++++++

If you run into any issues installing ``Orbeez``, please create an issue on GitHub.