from cpymad.madx import Madx
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import pandas as pd
import numpy as np
import math
#import NAFFlib
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy.ma as ma


import helper_functions as hf
import cpymad_helpers as cp

k2L_b=1.6171150435558206
k3L_b=26.82615373
n=12
k2L=np.linspace(0,1.0,n)
k3L=np.linspace(0,1.0,n)
S,O=np.meshgrid(k2L,k3L)
print('S',S,'O',O)
print('shape',np.shape(S))


SMALL_SIZE = 18
MEDIUM_SIZE = 16
BIGGER_SIZE = 16

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=18)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

sur_1=(np.loadtxt('120624_1sthalf_survived_30_natchrom.txt'))
sur_2=(np.loadtxt('120624_2ndhalf_survived_30_natchrom.txt'))
sur_3=(np.loadtxt('120624_3rdhalf_survived_30_natchrom.txt'))
sur_4=(np.loadtxt('120624_4thhalf_survived_30_natchrom.txt'))

boo=[sur_1,sur_2,sur_3,sur_4]
print(len(boo))
print(boo)

#survival plot
plt.clf()
plt.scatter(O,S,marker="s",c=boo,s=900,cmap='turbo')
plt.xlabel('K3L ')
plt.ylabel('K2L ')
plt.colorbar(label='Number of Initial Amplitudes with 100% survival')
plt.show()
plt.savefig('200824_k2lk3l_30natchrom_100.png')

