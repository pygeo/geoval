STUFF = "Hello world"  # this is done to avoid this problem: http://stackoverflow.com/questions/8024805/cython-compiled-c-extension-importerror-dynamic-module-does-not-define-init-fu

import numpy as np
cimport numpy as np

from scipy import stats
import multiprocessing

ctypedef np.double_t DTYPE_t  # double type for numpy arrays

"""
Minimum detectable trend analysis

References
----------
* Morin (2011): To know what we cannot know ... doi:10.1029/2010WR009798
"""

def calculate_trend(X):
        """
        generate random time series and return
        significance of trends
        """
        cdef double p, tau
        cdef np.ndarray[DTYPE_t, ndim=1] y,t
        cdef double intercept, trend, sigma
        t = X[0]
        intercept = X[1]
        trend = X[2]
        sigma = X[3]

        # generate timeseries with random normal distributed noise (eq.1, eq 7)
        y = intercept + trend * t + np.random.randn(len(t))*sigma
        # calculate trend using Kendall-Tau method
        tau, p = stats.kendalltau(t,y)
        return p

cdef class Mintrend(object):
    cdef double mean
    cdef double cv
    cdef int N
    cdef object trends  # see here why we use this method: http://stackoverflow.com/questions/21131884/using-cython-to-early-type-class-attributes
    cdef object t

    def __init__(self, np.ndarray[DTYPE_t, ndim=1] t, double mean, double cv, np.ndarray[DTYPE_t, ndim=1] trends, int N):
        """
        Parameters
        ----------
        t : ndarray
            timeseries
        mean : float
            mean of timeseries to be generated
        cv : float
            coefficient of variation of timeseries (std/mean)
        trends : ndarray
            array with trends to be investigated
        N : int
            number of ensembles to be generated
        """
        self.mean = mean
        self.cv = cv
        self.N = N
        self.trends = trends
        self.t = t

    def get_mintrend(self, double thres=0.5, double pthres=0.05):
        """
        calculate minimum detectable trend
        Parameters
        ----------
        thres : float
            parameter specifying the fraction of ensembles that need to show a significant trend
        pthres : float
            significance threshold
        """
        cdef np.ndarray[DTYPE_t, ndim=1] res_trend
        cdef np.ndarray[DTYPE_t, ndim=1] res_frac

        res_trend, res_frac = self._calculate_significant_trend_fractions(pthres)
        tmp = res_trend[res_frac >= thres]
        if len(tmp) > 0:
            return tmp.min()
        else:
            return np.nan

    def _calculate_significant_trend_fractions(self, double pthres):
        """
        returns fraction of cases which showed a significant trend
        """
        cdef np.ndarray[DTYPE_t, ndim=1] trends  # local variable for speed increas
        cdef np.ndarray[DTYPE_t, ndim=1] P

        trends = self.trends
        thetrend = []
        fraction = []  # fraction of trends above significance threshold
        for trend  in trends:
            T = TrendModel(self.t, self.mean, self.cv, trend, self.N)
            # calculate now the significances for the given trend
            P = T.calc_trend_significances()
            thetrend.append(trend)
            fraction.append(float(len(P[P<pthres])) / float(self.N))
        return np.asarray(thetrend), np.asarray(fraction)


cdef class TrendModel(object):

    cdef double mean, cv, trend
    cdef int N
    cdef object t
    cdef double tmean, intercept, sigma
    cdef str method

    def __init__(self, np.ndarray[DTYPE_t, ndim=1] t, double mean, double cv, double trend, int N, method='mann_kendall'):
        """
        Parameters
        ----------
        t : ndarray
            time index as float number (e.g. 1975.5 corresponds to mid of the year 1975)
        trend : float
            note that the trend needs to be in the same unit as the time array
        N : int
            number of realizations to be generated
        """
        self.mean = mean
        self.cv = cv
        self.trend = trend
        self.t = t
        self.N = N
        assert N > 0

        self._set_model_parameters()
        self.method = method

    def _set_model_parameters(self):
        """
        set the statistical model parameters
        """
        cdef np.ndarray[DTYPE_t, ndim=1] t  # local variable for speed increas
        cdef tmp

        t = self.t
        self.tmean = t.mean()
        tmp = self.cv**2. * self.mean**2. - self.trend**2. * t.var()
        self.intercept = self.mean - self.trend * self.tmean  # eq.5
        if tmp <=0.:
            self.sigma = np.nan
        else:
            self.sigma = np.sqrt(tmp)

    def calc_trend_significances(self, nproc=24):
        """
        calculate trend significances for N realizations

        Parameters
        ----------
        nproc : int
            number of processors to use
        """
        cdef int N
        cdef int i
        cdef np.ndarray[DTYPE_t, ndim=1] P

        N = self.N
        P = np.ones(N) * np.nan

        if N > 5:
            do_parallel = True
        else:
            do_parallel = False

        if do_parallel:  # parallel processing
            pool = multiprocessing.Pool(processes=min(nproc,N))
            P = np.asarray(pool.map(calculate_trend, zip([self.t]*N, [self.intercept]*N, [self.trend]*N, [self.sigma]*N     )))  # this runs really in parallel!)
            pool.close()
        else:
            for i in xrange(N):
                P[i] = calculate_trend([self.t, self.intercept, self.trend, self.sigma])
        return P



