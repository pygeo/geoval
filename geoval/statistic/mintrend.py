import os
import cPickle
import numpy as np
from scipy.interpolate import griddata
from scipy.spatial import cKDTree

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
    def __init__(self, lutname, backend='imshow', proj_prop=None):
        """
        Parameters
        ----------
        lutname : str
            name of LUT file derived from mintrend analysis
        backend : str
            backend used for plotting ['imshow','basemap']

        """
        self._lutname = lutname
        self.backend=backend
        self.proj_prop = proj_prop
        self._read_lut()



    def _read_lut(self):
        assert os.path.exists(self._lutname)
        d = cPickle.load(open(self._lutname,'r'))

        # generate array of indices and then use only LUT values that are not NaN
        MEAN, PHIS, CVS  = np.meshgrid(d['means'],d['phis'],d['cvs'])
        msk = ~np.isnan(d['res'])

        # now generate vector from all values that are not None
        #~ print 'CVS: ', CVS.shape, len(d['cvs'])
        #~ print 'means: ', len(d['means'])
        #~ print 'phis: ', len(d['phis'])

        self.cvs = CVS[msk].flatten()
        self.means = MEAN[msk].flatten()
        self.phis = PHIS[msk].flatten()

        self.lut = d['res'][msk].flatten()

    def _interpolate_fast(self, tcvs, tmeans, tphis):
        #http://stackoverflow.com/questions/29974122/interpolating-data-from-a-look-up-table

        # these are the target coordinates
        tcvs = np.asarray(tcvs)
        tmeans = np.asarray(tmeans)
        tphis = np.asarray(tphis)

        coords = np.vstack((tphis, tmeans, tcvs)).T

        xyz = np.vstack((self.phis, self.means, self.cvs)).T
        val = self.lut

        tree = cKDTree(xyz)
        dist, ind = tree.query(coords, k=2)  # take 2 closest LUT points

        # the problem can occur that  an invali index is returned.
        # if this corresponds to the boundary, then this is a hacked fix
        # this seems to be a proble in the cKDTree
        ind[ind==len(val)]=len(val)-1



        print 'ncoords: ', coords.shape
        print 'indx: ', ind.min(), ind.max(), ind.shape
        print 'val: ', val.min(), val.max(), val.shape

        d1,d2 = dist.T
        v1,v2 = val[ind].T

        v = (d1)/(d1 + d2)*(v2 - v1) + v1
        return v




    #~ def _interpolate_slow(self, tcvs, tmeans, tphis, method='linear'):
        #~ """
        #~ interpolate LUT to target using griddata
        #~ for this vectors of the variation coefficient
        #~ and mean is required
#~
        #~ tcvs : ndarray
            #~ list of variations of coefficient to interpolate to
        #~ tmeans : ndarray
            #~ list of mean values to interpolate to
        #~ tphis : ndarray
            #~ list of correlation values (phi)
        #~ method : str
            #~ methods used for interpolation ['cubic','linear']
            #~ for further details see documentation of griddata routine
        #~ """
        #~ tcvs = np.asarray(tcvs)
        #~ tmeans = np.asarray(tmeans)
        #~ tphis = np.asarray(tphis)
#~
#~
#~
        #~ return griddata((self.phis,self.means,self.cvs), self.lut, (tphis[:,None],tmeans[None,:],tcvs[:,None]), method=method)

    def _calc_cv(self, PHI, SLOPE, SIG_R, ME, var_t):
        """
        calculate coefficient of variance
        and return a Data object

        note, that the slope and tvar units need to be consistent (e.g. need to be valid per YEAR)
        see Albedo_mintrend.ipynb for checking

        """

        # now calculate CV for deseasonalized timeseries
        # CV = sig_y / mu_y with
        # sig_y = sqrt(b**2 * var(t) + sig_r^2 / (1-phi**2))

        TMP1 = PHI.mul(PHI).mulc(-1.).addc(1.)
        RIGHT = SIG_R.mul(SIG_R).div(TMP1)
        LEFT = SLOPE.mul(SLOPE).mulc(var_t)
        CV = LEFT.add(RIGHT)
        CV.data = np.sqrt(CV.data)
        CV = CV.div(ME)

        self.CV = CV


    def map_trends(self, SIG_R, ME, PHI, SLOPE, var_t, force=False, time_unit=None):
        """
        STD : GeoData
        ME : GeoData
        """
        assert time_unit is not None, 'Time unit needs to be provided'

        if SIG_R.ndim == 3:
            if SIG_R.nt == 1:
                SIG_R.data = SIG_R.data[0,:,:]
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
        if SLOPE.ndim == 3:
            if SLOPE.nt == 1:
                SLOPE.data = SLOPE.data[0,:,:]
            else:
                assert False

        assert SIG_R.data.ndim == 2
        assert ME.data.ndim == 2
        assert PHI.data.ndim == 2
        assert SLOPE.data.ndim == 2

        # coefficient of variation
        self._calc_cv(PHI, SLOPE, SIG_R, ME, var_t)
        print self.CV.min, self.CV.max


        # mask for valid pixels
        msk = ~self.CV.data.mask

        # vectors which correpond to data that should be interpolated to
        cvs = self.CV.data[msk].flatten()
        means = ME.data[msk].flatten()
        phis = PHI.data[msk].flatten()

        print 'NPixels: ', len(means)

        if hasattr(self, 'X'):
            if force:
                do_calc = True
            else:
                do_calc = False
        else:
            do_calc = True

        if do_calc:
            # interpolation

            z = self._interpolate_fast(cvs, means, phis)

            # map back to original geometry
            tmp = np.ones(ME.nx*ME.ny)*np.nan
            tmp[msk.flatten()] = z
            tmp = tmp.reshape((ME.ny,ME.nx))

            X = GeoData(None, None)
            X._init_sample_object(nt=None, ny=ME.ny, nx=ME.nx, gaps=False)
            X.data = np.ma.array(tmp, mask=tmp != tmp)

            self.X = X
            self.X.unit = 'trend / ' + time_unit
            self.X._trend_unit = time_unit

    def _get_temporal_scaling_factor(self):
        if self.X._trend_unit == 'year':
            scal = 10.
        else:
            assert False, 'Unknown temporal unit. Automatic rescaling not possible'
        return scal


    def draw_trend_map(self, decade=True, ax=None, **kwargs):
        if decade:  # show trends per decade
            scal= self._get_temporal_scaling_factor()
            X = self.X.mulc(scal)
            X.unit = 'trend / decade'
        else:
            X = self.X

        self.M = SingleMap(X, ax=ax, backend=self.backend)
        self.M.plot(proj_prop=self.proj_prop, **kwargs)

    def draw_cv_map(self, ax=None, **kwargs):
        """
        show map of CV, which needs to be calculated before
        """
        self.Mcv = SingleMap(self.CV, ax=ax, backend=self.backend)
        self.Mcv.plot(proj_prop=self.proj_prop, **kwargs)

    def draw_relative_trend(self, M, decade=True, ax=None, **kwargs):
        """
        generate a relative trend map
        the trend mapping needs to have been performed already

        Parameters
        ==========
        M : GeoData
            mean value
        """
        assert ax is not None
        assert hasattr(self, 'X'), 'mintrend has not been preprocessed'

        scal= self._get_temporal_scaling_factor()
        X = self.X.mulc(scal).div(M).mulc(100.)
        X.unit = '% / decade'

        self.Mr = SingleMap(X, ax=ax)
        self.Mr.plot(proj_prop=self.proj_prop, **kwargs)















