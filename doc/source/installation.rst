Installation
============

Dependencies
------------

- cython
- numpy
- scipy
- netcdf4
- cdo, cdo python bindings
- matplotlib
- dateutil
- basemap

libgeos-dev
libproj-dev
libgdal




Installation options
--------------------

For the installation of `geoval` the following options exist:

conda based installation
~~~~~~~~~~~~~~~~~~~~~~~~

TBD still needs to be implemented

pip based installation
~~~~~~~~~~~~~~~~~~~~~~~~

Still problem that shared object binaries do not compile automatically

Installation from source
~~~~~~~~~~~~~~~~~~~~~~~~

The installation from source is useful if you want to contribute to the geoval development::

    git clone https://github.com/pygeo/geoval.git
    cd geoval
    # compile libraries using cython
    python setup_extensions.py build_ext --inplace

    # then you still need to set your PYTHONPATH variable
    # accordingly that the module can be found
