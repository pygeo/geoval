import pyximport; pyximport.install()

from mintrend import *


import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt


#~ plt.close('all')




t = np.arange(1951,2001,1).astype('float')
N = 5
trends = np.arange(1.,21.,0.1)  # todo: do faster by Newton itteration --> not all trends need to be calculated

means = np.linspace(100.,1000.,20)
cvs = np.linspace(0.1,1.,10)

nmeans = len(means)
ncvs = len(cvs)

MT = np.ones((nmeans,ncvs))*np.nan

for i in xrange(nmeans):

    for j in xrange(ncvs):
        M = Mintrend(t, means[i], cvs[j], trends, N)
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
f.savefig('mintrend_contour.png', dpi=300)
plt.close('all')

#~ plt.show()


#~ T = TrendModel(t, 600., 0.2, 10./10., N)  # todo 10mm/decade ...
#~ P = T.calc_trend_significances()
#~
#~ pthres = 0.05
#~ print 'Fraction: ', len(P[P<pthres]) / float(N)


