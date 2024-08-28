import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import pandas as pd
import numpy as np
import math
import nafflib as NAFFlib 
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy.ma as ma

#our initial amplitudes
#sig_x = (13e-3)
#sig_y = (18e-3)
sig_10x=0.85e-2
sig_10y=1.78e-2
init_amp_x=np.linspace(-sig_10x/2,sig_10x/2,100)#sig_2x,3) #going from 0 to 2sigma for 3 steps in x
init_amp_y=np.linspace(0,sig_10y,100)
X,Y = np.meshgrid(init_amp_x,init_amp_y)
plt.rc('font',size=13)




class resonance_lines(object):
    """
    Adapted from https://pypi.org/project/acc-lib/
    Provide input of ranges in Qx and Qy, the orders and the periodiciy of the resonances
    """

    def __init__(self, Qx_range, Qy_range, orders, periodicity):

        if np.std(Qx_range):
            self.Qx_min = np.min(Qx_range)
            self.Qx_max = np.max(Qx_range)
        else:
            self.Qx_min = np.floor(Qx_range) - 0.05
            self.Qx_max = np.floor(Qx_range) + 1.05
        if np.std(Qy_range):
            self.Qy_min = np.min(Qy_range)
            self.Qy_max = np.max(Qy_range)
        else:
            self.Qy_min = np.floor(Qy_range) - 0.05
            self.Qy_max = np.floor(Qy_range) + 1.05

        self.periodicity = periodicity
        self.orders = orders

        nx, ny = [], []

        for order in np.nditer(np.array(orders)):
            t = np.array(range(-order, order + 1))
            nx.extend(order - np.abs(t))
            ny.extend(t)
        nx = np.array(nx)
        ny = np.array(ny)

        cextr = np.array([nx * np.floor(self.Qx_min) + ny * np.floor(self.Qy_min), \
                          nx * np.ceil(self.Qx_max) + ny * np.floor(self.Qy_min), \
                          nx * np.floor(self.Qx_min) + ny * np.ceil(self.Qy_max), \
                          nx * np.ceil(self.Qx_max) + ny * np.ceil(self.Qy_max)], dtype='int')
        cmin = np.min(cextr, axis=0)
        cmax = np.max(cextr, axis=0)
        res_sum = [range(cmin[i], cmax[i] + 1) for i in range(cextr.shape[1])]
        self.resonance_list = zip(nx, ny, res_sum)

    def plot_resonance(self, figure_object=None, ax=None, interactive=True):
        if (interactive):
            plt.ion()
        if figure_object:
            fig = figure_object
            plt.figure(fig.number)
        else:
            fig = plt.figure()
        if ax is None:
            ax = fig.add_subplot(1, 1, 1)  # create an axes object in the figure
        Qx_min = self.Qx_min
        Qx_max = self.Qx_max
        Qy_min = self.Qy_min
        Qy_max = self.Qy_max
        for resonance in self.resonance_list:
            nx = resonance[0]
            ny = resonance[1]
            for res_sum in resonance[2]:
                if ny:
                    line, = ax.plot([Qx_min, Qx_max], \
                                    [(res_sum - nx * Qx_min) / ny, (res_sum - nx * Qx_max) / ny], color='b')
                else:
                    line, = ax.plot([float(res_sum) / nx, float(res_sum) / nx], [Qy_min, Qy_max], color='g')
                if ny % 2:
                    plt.setp(line, linestyle='--', zorder=1, color='b')  # for skew resonances
                if res_sum % self.periodicity:
                    plt.setp(line, zorder=1, color='r')  # non-systematic resonances
                else:
                    plt.setp(line, zorder=1, linewidth=2.0, color='k')  # systematic resonances
                      # systematic resonances
        if (interactive):
            plt.draw()
        return ax

q_x_1024=list(np.loadtxt('0708_1024_xtunes_alltuned_10microns.txt'))
q_x_2048=list(np.loadtxt('0708_2048_xtunes_alltuned_10microns.txt'))
q_y_1024=list(np.loadtxt('0708_1024_ytunes_alltuned_10microns.txt'))
q_y_2048=list(np.loadtxt('0708_2048_ytunes_alltuned_10microns.txt'))

q_x=q_x_1024+q_x_2048
q_y=q_y_1024+q_y_2048

fig, ax = plt.subplots()

rl = resonance_lines([0.65, 0.75], [0.05, 0.15], [1,2,3,4,5], 1)

ax = rl.plot_resonance(fig, ax=ax, interactive=False)


#diffusion index
D=(np.log10(np.sqrt((np.array(q_x_2048)-(np.array(q_x_1024)))**2 + ((np.array(q_y_2048))-np.array(q_y_1024))**2)))
print('difference',D)
print('shape',np.shape(D))


normalise = matplotlib.colors.Normalize(vmin=-14, vmax=-2)

ax.set_ylim(0.05,0.15)
ax.set_xlim(0.65,0.74)
ax.set_title('Tune Footprint')
plt.plot(0.71,0.085,'go',markersize=1,label='Normal Operation WP')
#plt.plot(0.68,0.13,'bo',markersize=10,label='Extraction WP')
plt.scatter(q_x_1024,q_y_1024,marker='s',c=D,s=5,cmap='jet',norm=normalise)
plt.xlabel('$q_x$')
plt.ylabel('$q_y$')
#plt.xlim([0.705,0.725])
#plt.ylim([0.065,0.12])
plt.colorbar(label='D')
plt.axvline(2/3,color='r')
plt.xlabel('$q_x$')
plt.ylabel('$q_y$')
plt.legend()
plt.savefig('070824_fma_alltuned_10microns.pdf')


plt.clf()
plt.figure(figsize=(8,6))
plt.scatter(X, Y, c=D, s=500, cmap='jet', norm=normalise, marker='s')
plt.xlabel('x/m')
plt.ylabel('y/m')
#plt.xlim([0,0.01])
#plt.ylim([0,0.13])
plt.colorbar(label='D')
#plt.show()
plt.savefig('070824tunediff_alltuned_10microns.pdf')

