# -*- coding: utf-8 -*-
"""
This file is part of GEOVAL.
(c) Alexander Loew
For COPYING and LICENSE details, please refer to the LICENSE file
"""

import sys
sys.path.append('..')

from unittest import TestCase
import unittest

from geoval.core import GeoData
from geoval.statistic.mintrend import MintrendPlot

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
        phis = np.asarray([0.9])
        lut = np.ones((len(phis),len(means), len(cvs)))*np.nan
        lut[0,0,0] = 0.1
        lut[0,0,1] = 0.2
        lut[0,0,2] = np.nan
        lut[0,1,0] = 0.4
        lut[0,1,1] = 0.5
        lut[0,1,2] = 0.6

        #lut = np.asarray([[0.1,0.2,np.nan],[0.4,0.5,0.6]])

        d = {'cvs' : cvs, 'means' : means, 'res' : lut, 'phis' : phis}
        cPickle.dump(d, open(lutname, 'w'))
        return lutname, d

    def test_mintrend_lut_interpolation(self):
        lutname, d = self._generate_sample_lut()
        P = MintrendPlot(lutname)
        self.assertEqual(P._lutname, lutname)

    def test_read_lut(self):
        # check that LUT is read properly
        lutname, d = self._generate_sample_lut()
        P = MintrendPlot(lutname)

        self.assertEqual(len(P.cvs),5)
        self.assertEqual(len(P.means),5)
        self.assertEqual(len(P.lut),5)
        self.assertEqual(list(P.lut), [0.1,0.2,0.4,0.5,0.6])

    def test_interpolate(self):
        lutname, d = self._generate_sample_lut()
        P = MintrendPlot(lutname)
#~
        # first interpolate to same coordinates as given
        # should give same results
        # cvs, means, phis
        z = P._interpolate_fast([1.], [10.], [0.9])
        self.assertEqual(z[0],0.1)

        z = P._interpolate_fast([2.], [10.], [0.9])
        self.assertEqual(z[0],0.2)

        z = P._interpolate_fast([1.], [20.], [0.9])
        self.assertEqual(z[0],0.4)

        z = P._interpolate_fast([2.], [20.], [0.9])
        self.assertEqual(z[0],0.5)

        z = P._interpolate_fast([3.], [20.], [0.9])
        self.assertEqual(z[0],0.6)

        # now check real interpolation
        z = P._interpolate_fast([2.], [15.], [0.9])
        self.assertEqual(z[0],0.35)

        z = P._interpolate_fast([1.], [15.], [0.9])
        self.assertEqual(z[0],0.25)

    #~ def test_plot(self):
        #~ ny = 5
        #~ nx = 3
        #~ STD = GeoData(None, None)
        #~ STD._init_sample_object(nt=None, ny=ny, nx=nx, gaps=True)
        #~ STD.mulc(100.,copy=False)
        ###STD.addc(1.,copy=False)
#~
        #~ ME = GeoData(None, None)
        #~ ME._init_sample_object(nt=None, ny=ny, nx=nx)
        #~ ME.mulc(30.,copy=False)
        ####ME.addc(10.,copy=False)
#~
        #~ lutname, d = self._generate_sample_lut()
        #~ P = MintrendPlot(lutname)
        #~ P.map_trends(STD, ME)
#~
        #~ self.assertTrue(hasattr(P,'X'))


if __name__ == '__main__':
    unittest.main()
