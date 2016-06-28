import os
import cPickle
import numpy as np
from scipy.interpolate import griddata
"""
Minimum trend analysis
"""

class MintrendPlot(object):
    """
    class for plotting minimum trend analysis results
    """
    def __init__(self,lutname):
        """
        Parameters
        ----------
        lutname : str
            name of LUT file derived from mintrend analysis

        """
        self._lutname = lutname
        self._read_lut()

    def _read_lut(self):
        assert os.path.exists(self._lutname)
        d = cPickle.load(open(self._lutname,'r'))

        # generate array of indices and then use only LUT values that are not NaN
        CVS, MEAN = np.meshgrid(d['cvs'],d['means'])
        msk = ~np.isnan(d['res'])

        # now generate vector from all values that are not None
        self.cvs = CVS[msk].flatten()
        self.means = MEAN[msk].flatten()
        self.lut = d['res'][msk].flatten()

    def _interpolate(self, tcvs, tmeans, method='linear'):
        """
        interpolate LUT to target using griddata
        for this vectors of the variation coefficient
        and mean is required

        tcvs : ndarray
            list of variations of coefficient to interpolate to
        tmeans : ndarray
            list of mean values to interpolate to
        method : str
            methods used for interpolation ['cubic','linear']
            for further details see documentation of griddata routine
        """
        tcvs = np.asarray(tcvs)
        tmeans = np.asarray(tmeans)
        return griddata((self.means,self.cvs), self.lut, (tmeans[None,:],tcvs[:,None]), method=method)

    def plot(self, STD, ME):
        """
        STD : GeoData
        ME : GeoData
        """

        assert STD.data.ndim == 2
        assert ME.data.ndim == 2

        CV = STD.div(ME)

        print STD.data

        assert False


        #~ remove masked values

        #~ flatten

        #~ interpolate


        #~ generate map








