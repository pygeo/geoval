"""
produce example like in MORIN (2011), but for albedo
"""

import pyximport; pyximport.install()

from mintrend import *
import cPickle

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# PARAMETERS
N = 1000 # number of ensemble members
t = np.arange(1998,2016,1).astype('float')

trends = np.arange(0.00001,0.0005,0.00001)/10.   # :10 as timestamp is per year!
means = np.linspace(0.01,0.6,30)
cvs = np.linspace(0.01,1.,10)

# processing ...
nmeans = len(means)
ncvs = len(cvs)
MT = np.ones((nmeans,ncvs))*np.nan

for i in xrange(nmeans):
    for j in xrange(ncvs):
        M = Mintrend(t, means[i], cvs[j], trends, N)
        #M = Mintrend(t, 600., 0.2, trends=trends, N=N)
        MT[i,j] = M.get_mintrend()
        print means[i], cvs[j] #, MT[i,j]

# save results
cPickle.dump({'means' : means, 'cvs' : cvs, 'res' : MT},open('results_albedo_' + str(N) + '.pkl','w'))

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
f.savefig('mintrend_contour_albedo_' + str(N) + '.png', dpi=300)
plt.close('all')

