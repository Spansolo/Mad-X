import numpy as np
import matplotlib.pyplot as plt


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

tunes_x=np.loadtxt('1024_xtunes.txt')
tunes_y=np.loadtxt('1024_ytunes.txt')

fig, ax = plt.subplots()

rl = resonance_lines([0.65, 0.75], [0.05, 0.15], [1,2,3,4,5], 1)

ax = rl.plot_resonance(fig, ax=ax, interactive=False)

ax.set_ylim(0,0.15)
ax.set_title('Tune Footprint')
plt.plot(0.72,0.09,'go',markersize=10,label='Normal Operation WP')
plt.plot(0.68,0.13,'bo',markersize=10,label='Extraction WP')
#plt.scatter(tunes_x,tunes_y,color='r')
plt.axvline(2/3,color='r')
plt.xlabel('$q_x$')
plt.ylabel('$q_y$')
plt.legend()
plt.show()


