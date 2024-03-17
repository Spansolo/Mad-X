import numpy as np
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
init_amp_x=np.linspace(0,sig_10x/5,50)#sig_2x,3) #going from 0 to 2sigma for 3 steps in x
init_amp_y=np.linspace(0,sig_10y/5,50)
X,Y = np.meshgrid(init_amp_x,init_amp_y)
plt.rc('font',size=13)

q_x_1024_1=list(np.loadtxt('1403_1024_xtunes_new_2sig.txt'))
q_x_2048_1=list(np.loadtxt('1403_2048_xtunes_new_2sig.txt'))
q_y_1024_1=list(np.loadtxt('1403_1024_ytunes_new_2sig.txt'))
q_y_2048_1=list(np.loadtxt('1403_2048_ytunes_new_2sig.txt'))
"""
q_x_1024_2=list(np.loadtxt('1503_1024_xtunes_5k.txt'))
q_x_2048_2=list(np.loadtxt('1503_2048_xtunes_5k.txt'))
q_y_1024_2=list(np.loadtxt('1503_1024_ytunes_5k.txt'))
q_y_2048_2=list(np.loadtxt('1503_2048_ytunes_5k.txt'))

q_x_1024_3=list(np.loadtxt('1503_1024_xtunes_7.5k.txt'))
q_x_2048_3=list(np.loadtxt('1503_2048_xtunes_7.5k.txt'))
q_y_1024_3=list(np.loadtxt('1503_1024_ytunes_7.5k.txt'))
q_y_2048_3=list(np.loadtxt('1503_2048_ytunes_7.5k.txt'))

q_x_1024_4=list(np.loadtxt('1503_1024_xtunes_.txt'))
q_x_2048_4=list(np.loadtxt('1503_2048_xtunes_new_1sig.txt'))
q_y_1024_4=list(np.loadtxt('1503_1024_ytunes_new_1sig.txt'))
q_y_2048_4=list(np.loadtxt('1503_2048_ytunes_new_1sig.txt'))

q_x_1024_5=list(np.loadtxt('0403_1024_xtunes_10k_test.txt'))
q_x_2048_5=list(np.loadtxt('0403_2048_xtunes_10k_test.txt'))
q_y_1024_5=list(np.loadtxt('0403_1024_ytunes_10k_test.txt'))
q_y_2048_5=list(np.loadtxt('0403_2048_ytunes_10k_test.txt'))

q_x_1024_2=list(np.loadtxt('1024_x_tunes_k2l_2.txt'))
q_x_2048_2=list(np.loadtxt('2048_xtunes_k2l_2.txt'))
q_y_1024_2=list(np.loadtxt('1024_ytunes_k2l_2.txt'))
q_y_2048_2=list(np.loadtxt('2048_ytunes_k2l_2.txt'))

q_x_1024= q_x_1024_1 + q_x_1024_2 + q_x_1024_3 + q_x_1024_4 
q_x_2048=q_x_2048_1 + q_x_2048_2 + q_x_2048_3 + q_x_2048_4  
q_y_1024=q_y_1024_1 + q_y_1024_2 + q_y_1024_3 + q_y_1024_4 
q_y_2048=q_y_2048_1 + q_y_2048_2 + q_y_2048_3 + q_y_2048_4 
"""
q_x_1024=q_x_1024_1
q_y_1024=q_y_1024_1
q_x_2048=q_x_2048_1
q_y_2048=q_y_2048_1



#diffusion index
D=(np.log10(np.sqrt((np.array(q_x_2048)-(np.array(q_x_1024)))**2 + ((np.array(q_y_2048))-np.array(q_y_1024))**2)))
print('difference',D)
print('shape',np.shape(D))



#tune diffusion plot
plt.clf()
plt.scatter(X,Y,marker="s",c=D,s=500,cmap='jet')
plt.xlabel('x/m')
plt.ylabel('y/m')
#plt.xlim([0,0.01])
#plt.ylim([0,0.018])
plt.colorbar(label='D')
#plt.show()
plt.savefig('150324tunediff_new_2sig.pdf')

#FMA plot
plt.clf()
plt.scatter(q_x_1024,q_y_1024,marker='s',c=D,s=5,cmap='jet')
plt.xlabel('$q_x$')
plt.ylabel('$q_y$')
plt.xlim([0.72,0.722])
#plt.ylim([0.089,0.0915])
plt.colorbar(label='D')
#plt.show()
plt.savefig('150324fma_new_2sig.pdf')
"""



Jx=list(np.loadtxt('2802_jx_multi_test.txt'))
Jy=list(np.loadtxt('2802_jy_multi_test.txt'))




#tune shift with amplitude plots


plt.clf()
fig,ax=plt.subplots()
ax.scatter((np.array(Jx)),q_x)
#plt.ylim(1.7212,1.7213)
plt.xlabel('$Jx$')
#plt.xlim(0.85*10**-3,0.85*10**-2)
#ax.set_xticklabels([1,2,3,4,5,6,7,8,9,10])
#ax.set_xticks([init_amp_x])
plt.ylabel('$q_x$')
plt.tight_layout()
plt.show()
plt.savefig('2802_xqx_multi_test.pdf')
plt.clf()

print(np.gradient(q_x)/np.gradient(2*np.array(Jx)))

plt.scatter(Jx[:,0], q_x)
plt.xlabel('$J_x$[m]')
plt.ylabel('$q_x$')
plt.tight_layout()
plt.show()
#plt.savefig('3103_jyqy_10.pdf')
plt.clf()

"""