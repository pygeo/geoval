# -*- coding: utf-8 -*-
"""
This file is part of GEOVAL.
(c) 2012- Alexander Loew
For COPYING and LICENSE details, please refer to the LICENSE file
"""

import matplotlib
matplotlib.use('Agg')

import sys
sys.path.append('..')

import unittest

from geoval.core import GeoData
from geoval.core.mapping import SingleMap

import tempfile

class TestData(unittest.TestCase):

    def setUp(self):
        self.D = GeoData(None, None)
        self.D._init_sample_object(nt=None, ny=180, nx=360)
        self._tmpdir = tempfile.mkdtemp()

    def test_imshow(self):
        # test simple mapping using imshow only
        S = SingleMap(self.D)
        S.plot()

    def test_basemap(self):
        # test simple mapping using basemap
        S = SingleMap(self.D, backend='imshow')
        S.plot()

    def test_cartopy(self):
        # test simple mapping using cartopy
        S = SingleMap(self.D, backend='cartopy')
        S.plot(proj_prop={'projection' : 'robin'})



if __name__ == '__main__':
    unittest.main()
