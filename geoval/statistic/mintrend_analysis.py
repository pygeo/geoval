import pyximport; pyximport.install()

from mintrend import *
import cPickle

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt


t = np.arange(1951,2001,1).astype('float')
N = 10000
trends = np.arange(1.,21.,0.1)

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

cPickle.dump({'means' : means, 'cvs' : cvs, 'res' : MT},open('results_' + str(N) + '.pkl','w'))


# generate plot
levels=np.arange(2.,20,2)
f = plt.figure()
ax = f.add_subplot(111)
CS = ax.contour(means, cvs, MT.T, levels=levels)
plt.clabel(CS, inline=1, fontsize=10)
ax.grid()
ax.set_xlabel('mean value')
ax.set_ylabel('CV')
ax.set_title('minimum detectable trend (N=' + str(N) + ')')
f.savefig('mintrend_contour_' + str(N) + '.png', dpi=300)
plt.close('all')

