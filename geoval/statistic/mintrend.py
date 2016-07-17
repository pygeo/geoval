import os
import cPickle
import numpy as np
from scipy.interpolate import griddata
from geoval.core import GeoData
from geoval.core.mapping import SingleMap
"""
Minimum trend analysis
"""

class MintrendPlot(object):
    """
    class for plotting minimum trend analysis results
    Note that the minimum trend analysis look up table
    needs to be preprocessed using a spearate program
    and that also the STDV and MEAN (timstd, timmean)
    are required for plotting final data
    """
    def __init__(self, lutname):
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

    def _interpolate(self, tcvs, tmeans, tphis, method='linear'):
        """
        interpolate LUT to target using griddata
        for this vectors of the variation coefficient
        and mean is required

        tcvs : ndarray
            list of variations of coefficient to interpolate to
        tmeans : ndarray
            list of mean values to interpolate to
        tphis : ndarray
            list of correlation values (phi)
        method : str
            methods used for interpolation ['cubic','linear']
            for further details see documentation of griddata routine
        """
        tcvs = np.asarray(tcvs)
        tmeans = np.asarray(tmeans)
        tphis = np.asarray(tphis)

        return griddata((self.phis,self.means,self.cvs,self.phis), self.lut, (tphis[:,None],tmeans[None,:],tcvs[:,None]), method=method)

    def map_trends(self, STD, ME, PHI):
        """
        STD : GeoData
        ME : GeoData
        """

        if STD.ndim == 3:
            if STD.nt == 1:
                STD.data = STD.data[0,:,:]
            else:
                assert False
        if ME.ndim == 3:
            if ME.nt == 1:
                ME.data = ME.data[0,:,:]
            else:
                assert False
        if PHI.ndim == 3:
            if PHI.nt == 1:
                PHI.data = PHI.data[0,:,:]
            else:
                assert False


        assert STD.data.ndim == 2
        assert ME.data.ndim == 2
        assert PHI.data.ndim == 2

        hier weiter ...


        cv or std ??? caluclation of CV still usefull ??? what is stored in LUT generation ???

        # coefficient of variation
        CV = STD.div(ME)

        # mask for valid pixels
        msk = ~CV.data.mask

        # vectors which correpond to data that should be interpolated to
        cvs = CV.data[msk].flatten()
        means = ME.data[msk].flatten()
        phis = PHI.data[msk].flatten()

        print 'NPixels: ', len(means)


        if True:
            # interpolation
            z = np.ones(len(means))*np.nan
            if True:
                for i in xrange(len(z)):
                    if i % 1000 == 0:
                        print i
                    z[i] = self._interpolate([cvs[i]], [means[i]], [phis[i]])  # could be probably done more efficient
            else:
                z = self._interpolate(cvs, means, phis)

            # map back to original geometry
            tmp = np.ones(ME.nx*ME.ny)*np.nan
            tmp[msk.flatten()] = z
            tmp = tmp.reshape((ME.ny,ME.nx))

            X = GeoData(None, None)
            X._init_sample_object(nt=None, ny=ME.ny, nx=ME.nx, gaps=False)
            X.data = np.ma.array(tmp, mask=tmp != tmp)

            self.X = X



    def draw_map(self, **kwargs):
        self.M = SingleMap(self.X)
        self.M.plot(**kwargs)












