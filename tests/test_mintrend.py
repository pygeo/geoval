# -*- coding: utf-8 -*-
"""
This file is part of GEOVAL.
(c) Alexander Loew
For COPYING and LICENSE details, please refer to the LICENSE file
"""

from unittest import TestCase
import unittest

from geoval.core import GeoData
from geoval.statistic import MintrendPlot

import os
import cPickle
import numpy as np

import tempfile

from nose.tools import assert_raises



class TestTrend(unittest.TestCase):

    def setUp(self):
        self.D = GeoData(None, None)
        self.D._init_sample_object(nt=1000, ny=1, nx=1)
        self._tmpdir = tempfile.mkdtemp()

    def _generate_sample_lut(self):
        lutname = tempfile.mktemp(suffix='.pkl')

        cvs = np.asarray([1.,2.,3.])
        means = np.asarray([10.,20.])
        lut = np.asarray([[0.1,0.2,0.3],[0.4,0.5,0.6]])

        d = {'cvs' : cvs, 'means' : means, 'res' : lut}
        cPickle.dump(d, open(lutname, 'w'))
        return lutname, d

    def test_mintrend_lut_interpolation(self):

        lutname, d = self._generate_sample_lut()

        P = MintrendPlot(lutname)
        self.assertEqual(P._lutname, lutname)

    def test_read_lut(self):
        lutname, d = self._generate_sample_lut()
        P = MintrendPlot(lutname)
        P._read_lut()



if __name__ == '__main__':
    unittest.main()
