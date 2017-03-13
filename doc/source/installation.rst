Installation
============

Dependencies
------------

This is a list of dependencies that would need to be installed before the installation of `geoval`. Note that the PIP based and conda based installation procedures described further below are supposed to take care of the dependencies automatically. This was however not yet thoroughly tested. 

- cython
- numpy
- scipy
- netcdf4
- cdo, cdo python bindings
- matplotlib
- dateutil
- basemap
- libgeos-dev
- libproj-dev
- libgdal
- pyshp
- cartopy 

Installation options
--------------------

For the installation of `geoval`, a couple of installation options exist which are listed below. `geoval` installation requires the compilation of dependencies using cython. This is done automatically by the installation if done as described below. 

Conda and PIP base installation is currently not implemented as the author had no time so far to become familar how to compile dependencies in place using these installers. Help welcome!

conda based installation
~~~~~~~~~~~~~~~~~~~~~~~~

TODO conda installation not tested yet, but will work as follows::

    conda install [-n YOURENV] -c conda-forge geoval

pip based installation
~~~~~~~~~~~~~~~~~~~~~~~~

TBD, not properly working yet.

Standard python installation way
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Standard python way for installing packages::

    python setup.py build_ext --inplace
    python setup.py build
    python setup.py install

Assumes that all required dependencies have been installed already.

Installation from source
~~~~~~~~~~~~~~~~~~~~~~~~

The installation from source is useful if you want to contribute to the geoval development::

    git clone https://github.com/pygeo/geoval.git
    cd geoval
    # compile libraries using cython
    python setup.py build_ext --inplace

    # then you still need to set your PYTHONPATH variable
    # accordingly that the module can be found

Assumes that all required dependencies have been installed already.
