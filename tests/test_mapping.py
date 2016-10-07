# -*- coding: utf-8 -*-
"""
This file is part of GEOVAL.
(c) 2012- Alexander Loew
For COPYING and LICENSE details, please refer to the LICENSE file
"""

from unittest import TestCase
import unittest

from geoval.core import GeoData
from geoval.core.mapping import SingleMap
#~ from geoval.region import RegionPolygon

#~ import os
#~ import scipy as sc
#~ import matplotlib.pylab as pl
#~ import numpy as np
#~ from scipy import stats
#~ from dateutil.rrule import rrule
#~ from dateutil.rrule import MONTHLY
#~ import datetime

import tempfile

from nose.tools import assert_raises

#~ import matplotlib.pyplot as plt

class TestData(unittest.TestCase):

    def setUp(self):
        self.D = GeoData(None, None)
        self.D._init_sample_object(nt=None, ny=180, nx=360)
        self._tmpdir = tempfile.mkdtemp()

    def test_imshow(self):
        pass





if __name__ == '__main__':
    unittest.main()
