import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

"""
Minimum detectable trend analysis

References
----------
* Morin (2011): To know what we cannot know ... doi:10.1029/2010WR009798
"""

class Mintrend(object):
    def __init__(self, t, mean, cv, trends=None, N=1000):
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


    def get_mintrend(self, thres=0.5, pthres=0.05):
        """
        calculate minimum detectable trend
        Parameters
        ----------
        thres : float
            parameter specifying the fraction of ensembles that need to show a significant trend
        pthres : float
            significance threshold
        """

        self._res_trend, self._res_frac = self._calculate_significant_trend_fractions(pthres)
        #~ print ''
        #~ print 'Trend: ', self._res_trend
        #~ print 'Frac: ', self._res_frac
        #~ print 'Selection: ', self._res_trend[self._res_frac>= thres]
        return self._res_trend[self._res_frac >= thres].min()


    def _calculate_significant_trend_fractions(self, pthres):
        """
        returns fraction of cases which showed a significant trend
        """
        thetrend = []
        fraction = []  # fraction of trends above significance threshold
        for trend  in self.trends:
            T = TrendModel(self.t, self.mean, self.cv, trend, self.N)
            # calculate now the significances for the given trend
            P = T.calc_trend_significances()
            thetrend.append(trend)
            fraction.append(float(len(P[P<pthres])) / float(self.N))
        return np.asarray(thetrend), np.asarray(fraction)


class TrendModel(object):
    def __init__(self, t, mean, cv, trend, N, method='mann_kendall'):
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
        self._set_trend_model()

    def _set_trend_model(self):
        if self.method == 'spearman':
            self._trend_estimate = self._spearman_correlation
        elif self.method == 'mann_kendall':
            self._trend_estimate = self._mann_kendall_correlation
        elif self.method == 'pearson':
            self._trend_estimate = self._pearson_correlation

    def _set_model_parameters(self):
        """
        set the statistical model parameters
        """
        self.tmean = self.t.mean()
        self.intercept = self.mean - self.trend * self.tmean  # eq.5
        self.sigma = np.sqrt(self.cv**2. * self.mean**2. - self.trend**2. * self.t.var())
        #~ print 'CV: ', self.cv
        #~ print 'Tmean: ', self.tmean
        #~ print 'intercept: ', self.intercept
        #~ print 'sigma: ', self.sigma  # note that the values in the paper in eq.7 seem to be wrong!
        #~ print 'trend: ', self.trend

    def calc_trend_significances(self):
        """
        calculate trend significances for N realizations
        """
        P = np.ones(self.N) * np.nan
        for i in xrange(self.N):
            p = self._calculate_trend()
            P[i] = p
        return P

    def _calculate_trend(self):
        """
        generate random time series and return
        significance of trends
        """

        # generate timeseries with random normal distributed noise (eq.1, eq 7)
        y = self.intercept + self.trend * self.t + np.random.randn(len(self.t))*self.sigma

        # calculate trend using specified method
        p = self._trend_estimate(self.t, y)
        return p

    def _pearson_correlation(self, t, y):
        assert False
        return p

    def _mann_kendall_correlation(self, t, y):
        tau, p = stats.kendalltau(t,y)
        return p

    def _spearman_correlation(self, t, y):
        assert False
        return p


plt.close('all')




t = np.arange(1951,2001,1)
N = 10
trends = np.arange(1.,21.,0.1)  # todo: do faster by Newton itteration --> not all trends need to be calculated

means = np.linspace(100.,1000.,20)
cvs = np.linspace(0.1,1.,10)

nmeans = len(means)
ncvs = len(cvs)

MT = np.ones((nmeans,ncvs))*np.nan

for i in xrange(nmeans):

    for j in xrange(ncvs):
        M = Mintrend(t, means[i], cvs[j], trends=trends, N=N)
        #M = Mintrend(t, 600., 0.2, trends=trends, N=N)
        MT[i,j] = M.get_mintrend()
        print means[i], cvs[j] #, MT[i,j]


# generate plot
levels=np.arange(2.,20,2)
f = plt.figure()
ax = f.add_subplot(111)
CS = ax.contour(means, cvs, MT.T, levels=levels)
plt.clabel(CS, inline=1, fontsize=10)
ax.grid()
ax.set_xlabel('mean value')
ax.set_ylabel('CV')
ax.set_title('minimum detectable trend')


plt.show()


#~ T = TrendModel(t, 600., 0.2, 10./10., N)  # todo 10mm/decade ...
#~ P = T.calc_trend_significances()
#~
#~ pthres = 0.05
#~ print 'Fraction: ', len(P[P<pthres]) / float(N)


