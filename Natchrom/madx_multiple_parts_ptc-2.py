from cpymad.madx import Madx
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import pandas as pd
import numpy as np
import math
import NAFFlib
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy.ma as ma
import itertools


import helper_functions as hf
import cpymad_helpers as cp

plt.rcParams['figure.figsize'] = [8.0, 5.0]
plt.rcParams['figure.dpi'] = 200
plt.rcParams['savefig.dpi'] = 200

plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 14

plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

plt.rcParams['font.size'] = 10
plt.rcParams['legend.fontsize'] = 8

plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 5
'''
save_folder = 'Plots/'
hf.make_directory(save_folder)
#legend_label = 'Case'
main_label = 'NIMMS'
output_line = 0
'''
#import tfs
madx=Madx()
madx.option(echo=True)

#this prints the crap into a log file so you don't have to see all the PTC info for
#every time you send a particle round
cpymad_logfile = 'cpymad_logfile.log'
madx = cp.cpymad_start(cpymad_logfile)

#calling the mad-x file to be used
#madx.call('NIMMS_og_newwp.txt')
#madx.call('curvedcct_newvals_movedsexts_natural.txt')
#madx.call('Boundaries_split_matched_multiring.madx')
madx.call('Boundaries_split_natural_movedsexts.madx')
#madx.call('corrected_moremulti.madx')
madx.use(sequence='TERARING') #sequence used by the file
#output_line = cp.cpymad_print_output(cpymad_logfile)
madx.input('SELECT,flag=TWISS,COLUMN=keyword, name, s, betx, alfx, mux, bety, alfy, muy, x,')
madx_twiss = madx.twiss(sequence='TERARING', file='nimms_twiss.tfs').dframe()
#before there was no .dframe()

sx1=list(madx.elements['xs1'].knl)
sx2=list(madx.elements['xs2'].knl)
print('sx1',sx1[2])

plt.xlabel('S [m]')
#plt.ylabel('$D_{x}$')
#plt.ylabel(r'$\beta_{x}$')
plt.legend()
#plt.ylabel(r'($\beta_{x}$ - $\beta_{x_split}$)/$\beta_{x}$')
#plt.show()

plt.plot(madx_twiss.s,madx_twiss.mux*360,'-',label='$\mu_x$')
plt.vlines(madx_twiss.loc['xs1.1'].s,0,madx_twiss.loc['xs1.3'].mux *360,label='XSF1,2',color='g',linestyle=':',alpha=0.8)
plt.vlines(madx_twiss.loc['xs2.1'].s,0,madx_twiss.loc['xs2.3'].mux *360,label='XSD1,2',color='r',linestyle=':',alpha=0.8)

plt.savefig('270524_mux_test.pdf')
#plt.show()
#list(madx_twiss)

#initial inputs, ignore
madx.input('ptc_create_universe')
madx.input('ptc_create_layout, time=false,model=2, method=6, nst=5, exact=true')
madx.input('ptc_twiss, closed_orbit, icase=56, no=4, slice_magnets')
madx.input('ptc_end')

ptc_twiss_summary = madx.table['ptc_twiss_summary']
#for k in ptc_twiss_summary.keys():
    #if ptc_twiss_summary[k][0] > 0:
        #print(k + ' = ' + str(ptc_twiss_summary[k][0]))
#list(madx_twiss)
#survey = madx.twiss(sequence='teraring', betx=1, bety=1)
#plt.plot(twiss.s, twiss.betx)
#plt.plot(twiss.s, twiss.bety)
#plt.show()


ptc_twiss = madx.table['ptc_twiss_summary']
#list(ptc_twiss)

#twiss plots!
madx_twiss = madx.twiss(sequence='TERARING', file='nimms_twiss.tfs').dframe()
#list(madx_twiss)

ring_twiss_file = 'nimms_twiss.tfs'
madx_twiss_ring = cp.cpymad_madx_twiss(madx, cpymad_logfile, 'teraring')
cp.cpymad_plot_madx_twiss_block(madx, madx_twiss_ring, 'teraring')
plt.tight_layout()
#plt.show()


#ring survey plots
madx.survey()
mySurvey=madx.table.survey.dframe()
plt.plot(mySurvey.x,mySurvey.z,'o-k')
plt.axis('square')
plt.xlabel('X [m]')
plt.ylabel('Z [m]')
plt.grid()
#plt.show()

qfSurvey=mySurvey[mySurvey['name'].str.contains('qq1')]
qdSurvey=mySurvey[mySurvey['name'].str.contains('qq2')]
mbSurvey=mySurvey[mySurvey['name'].str.contains('mb')]
sxfSurvey=mySurvey[mySurvey['name'].str.contains('xs1')]
sxdSurvey=mySurvey[mySurvey['name'].str.contains('xs2')]
plt.plot(mySurvey.x,mySurvey.z,'-k', lw=0.3, label='ALL')
plt.scatter(mbSurvey.x,mbSurvey.z, marker='o', color='y', label='Dipole')
mtype='.'
plt.scatter(qfSurvey.x,qfSurvey.z, marker=mtype, color='r', label='QF')
plt.scatter(qdSurvey.x,qdSurvey.z, marker=mtype, color='b', label='QD')
plt.scatter(sxfSurvey.x,sxfSurvey.z, marker=mtype, color='orange', label='SXF')
plt.scatter(sxdSurvey.x,sxdSurvey.z, marker=mtype, color='tab:purple', label='SXD')
plt.legend()

# Custom legend
#legend_elements = [Line2D([0], [0], color='y', label='Dipole'), Line2D([0], [0], color='g', label='QD'), Line2D([0], [0], color='b', label='QF')]
#plt.legend(handles=legend_elements, loc=1)

plt.axis('square')
plt.xlabel('X [m]')
plt.ylabel('Z [m]')
plt.grid()
#plt.show()

#madx_summary_dframe = madx.table['summ'].dframe()
#ptc_summary_dframe = madx.table['ptc_twiss_summary'].dframe()


#track using ptc
#emittances set to those of the NIMMS document
#beta_x at point where alpha = 0 is 1.080519198
#beta_y at point where alpha = 0 is 3.358349842
#((np.sqrt(3.981526824  * 6.565500075e-7))
#((np.sqrt(8.231740397 * 9.379285821e-7))
#5.2524e-6 max emittance
#beam sizes calculated from EMITTANCE (converted from normalised emittances)
#sig_x = 13e-3
#sig_y=18e-3
sig_10x=0.85e-2
sig_10y=1.78e-2
px = []
py = []


#convert to action angles
#just commenting out the initial action angles as I want to calculate them from the amplitudes instead
"""
Jy = -(sig_2y**2)/(2*3.358349842)
phi_y = -np.arctan2(3.358349842*py,sig_2y)
"""

plt.clf()
#Generating x up to 2sigs off axis
#Makes PTC input
#n_=np.linspace(0,0.0001,3)#sig_2x,3) #going from 0 to 2sigma for 3 steps in x
init_amp_x=np.linspace(0,sig_10x,50)#sig_2x,3) #going from 0 to 2sigma for 3 steps in x
init_amp_y=np.linspace(0,sig_10y,50)
X,Y = np.meshgrid(init_amp_x,init_amp_y)
#print(X[0,:])
#print(Y[0,:])
#n=list(X,Y)
#print('X,Y',X,Y)



myString=[]
myPTCParticle=[]
myAmplitudePTC_x=[]
y=[]
x=[]
beta_x=[]
beta_y=[]
turns=[]
s=[]
dx=[]
dy=[]
D=[]
freq_x=[] #overall x frequencies
freq_y=[] #overall y frequencies
freq_x_1024=[]
freq_y_1024=[]
freq_x_2048=[]
freq_y_2048=[]
q_x=[]
q_y=[]
Qx_2048=[]
Qx_1024=[]
Qy_2048=[]
Qy_1024=[]
q_x_1024=[]
q_y_1024=[]
q_x_2048=[]
q_y_2048=[]


myAmplitudePTC_y=[]
myTunesPTC=[]

#First want to write this loop in the python file instead of in an external file
#Have to append the particle each time for different starting values or it'll lump all the data together
#Same with amplitude

for i in range(len(init_amp_y)):
    for j in range(len(init_amp_x)):
        # print('x=',X[i][j])
        # print('y=',Y[i][j])
        s_x = init_amp_x[j]
        s_y = init_amp_y[i]
        print('s_x=',s_x)
        print('s_y=',s_y)
        #print('s_x=',s_x)
        #print('s_y=',s_y)
        #Defining the PTC input parameters with changing x amplitudes
        myString.append('''
        ptc_create_universe;
        ptc_create_layout, time=false, model=2, method=6, nst=5, exact=true;
        PTC_ALIGN;
        PTC_START, X=%s, PX=0, Y=%s, PY=0, T=0, PT=0;
        ptc_track, icase=5, closed_orbit,dump,MAXAPER={0.03,0.01,0.03,0.01},turns=2047,file=ptc_x_track,
        NORM_OUT;
        ptc_track_end;
        ptc_end;
        '''%(s_x,s_y))
        #sense checking to see what I have put into PTC
#print('my string=',myString[8])
#print('size',np.shape(myString[8]))

#Phase space plots
#Calculating action angles
plt.clf()


#This says: for every starting amplitude I have, give me the tracking data from its data frame.
#Add this to the final x values, y values, you name it.
for i in range(len(myString)):
    madx.input(myString[i])
    madx.use(sequence='TERARING')
    #print(madx.table)
    #my particle is taking on the track.obs0001.p0001 dataframe each time, hence why it's
    # inside the loop.
    myPTCParticle.append(madx.table['track.obs0001.p0001'].dframe())
    #print('particle',myPTCParticle[i])

    #my final phase space data of the particle each time
    x.append(list(myPTCParticle[i]['x']))
    y.append(list(myPTCParticle[i]['y']))
    px.append(list(myPTCParticle[i]['px']))
    py.append(list(myPTCParticle[i]['py']))
    turns.append(list(myPTCParticle[i]['turn']))
    
    #print('betax',list(madx.table.twiss.betx))
    #print the betas at the sextupole locations
    #print('betaxi',madx.elements['xs1'].betx)
    #print('betaxj',madx.elements['xs2'].betx)

    #catching lost particles
    dum1=[]
    dum2=[]
    dump1=[]
    dump2=[]

    if len(x[i])<2048:
        #with open("lostpart_%s.txt"%i, "w") as f_out:
            #print('x',x[i], file=f_out, sep=" ")
            #print('px',px[i], file=f_out, sep=" ")
            #print('y',y[i], file=f_out, sep=" ")
            #print('py',py[i], file=f_out, sep=" ")
            #print('#turns',turns[i], file=f_out, sep=" ")
        var = (np.empty(2048 - len(x[i]), dtype=object))
        var.fill(np.nan)
        dum1.extend(var)
        x[i].extend(dum1)
        print('var=',dum1) #var is fine
        print('length',np.shape(dum1)) #var is fine
    #checking it works
    print('x=',x[i])
    print('length',len(x[i])) #DID IT

    if len(y[i])<2048:
        var = (np.empty(2048 - len(y[i]), dtype=object))
        var.fill(np.nan)
        dum2.extend(var)
        y[i].extend(dum2)
        #print('var=',dum2) #var is fine
        #print('length',np.shape(dum2)) #var is fine
    #checking it works
    #print('y=',y[i])
    #print('length',len(y[i])) #DID IT


    if len(px[i])<2048:
        var = (np.empty(2048 - len(px[i]), dtype=object))
        var.fill(np.nan)
        dump1.extend(var)
        px[i].extend(dum1)
        #print('var=',dum1) #var is fine
        #print('length',np.shape(dum1)) #var is fine
    #checking it works
    #print('x=',x[i])
    #print('length',len(x[i])) #DID IT

    if len(py[i])<2048:
        var = (np.empty(2048 - len(py[i]), dtype=object))
        var.fill(np.nan)
        dump2.extend(var)
        py[i].extend(dum2)
        #print('var=',dum2) #var is fine
        #print('length',np.shape(dum2)) #var is fine
    #checking it works
    #print('y=',y[i])
    #print('length',len(y[i])) #DID IT


    #take this out of loop when using
    """
    Jx = 0.5 * ((np.array(x) ** 2) + ((np.array(px)/9.81) ** 2))
    Jy = 0.5 * ((np.array(y) ** 2) + ((np.array(py)/9.81) ** 2))
    phi_x = np.arctan2(np.array(px), np.array(x))
    phi_y = np.arctan2(np.array(py), np.array(y))
    # plotting them
    plt.scatter(x, px)
    plt.xlabel('$x$[m]')
    plt.ylabel('$p_x$[m mrad]')
    #plt.show()
    plt.savefig('150324xpx_split_new_10sig.pdf')
    plt.clf()
    plt.scatter(phi_x, Jx)
    plt.xlabel('$\phi_x$[rad]')
    plt.ylabel('$J_x$')
    #plt.show()
    plt.savefig('150324jxphix_split_new_10sig.pdf')
    plt.clf()
    plt.scatter(phi_y, Jy)
    plt.xlabel('$\phi_y$[rad]')
    plt.ylabel('$J_y$')
    plt.tight_layout()
    #plt.show()
    """
    #myAmplitudePTC_y[i]

    #calculating the tunes
    
    #make sure the i is in the fft otherwise you'll be doing an fft on everything it'll be messy!
    myAmplitudePTC_x.append(np.abs(np.fft.fft(x[i])))
    myAmplitudePTC_y.append(np.abs(np.fft.fft(y[i])))

    #print('amp',myAmplitudePTC_x[i])
    #print('shape',np.shape(myAmplitudePTC_x[i]))

    #proper tunes when using nafflib
    # myNAFF = NAFFlib.get_tune(myPTCParticle[i]['x'])

    #tune plots
    myTunesPTC.append(np.linspace(0, 1, 2048))

    #plt.figure()
    #plt.xlim([0., 0.5])
    #plt.plot(myTunesPTC[i],(np.array(myAmplitudePTC_x[i]))) #,label="%s" %(X[i]))
    #plt.xlabel('qx')
    #plt.ylabel('Amplitude [arb.]')
    #plt.figure()
    #plt.xlim([0., 0.5])
    #plt.plot(myTunesPTC[i],myAmplitudePTC_y[i])#,label="%s" %(Y[i]))
    #plt.xlabel('qy')
    #plt.ylabel('Amplitude [arb.]')
    #plt.legend()
    #plt.plot(myTunesPTC,myAmplitudePTC[1])
    #plt.plot(myTunesPTC,myAmplitudePTC[2])
    #plt.show()


    freq_x.append(NAFFlib.get_tune(np.array(x[i])))
    freq_y.append(NAFFlib.get_tune(np.array(y[i])))
    print('freqx=',freq_x[i])
    print('size',np.size(freq_x[i]))
    #separating the turn data
    #to do: tidy this up later
    freq_x_1024.append(NAFFlib.get_tune(np.array(x[i][0:1024])))  # this gets the fft
    freq_y_1024.append(NAFFlib.get_tune(np.array(y[i][0:1024])))
    freq_x_2048.append(NAFFlib.get_tune(np.array(x[i][1024:2048])))
    freq_y_2048.append(NAFFlib.get_tune(np.array(y[i][1024:2048])))


    Qx_1024=(freq_x_1024) #this finds the max tune
    Qy_1024=(freq_y_1024)

    #last 1000 turns
    Qx_2048=(freq_x_2048)
    Qy_2048=(freq_y_2048)

    if (freq_x[i]<0.004):
        q_x.append(np.nan)
    else:
        q_x.append(1.-np.array(freq_x[i]))
    if (freq_y[i]<0.004):
        q_y.append(np.nan)
    else:
        q_y.append(freq_y[i])

    #just putting it out there, I know this is messy af but it'll have to do for now
    if (freq_x_1024[i]<0.004):
        q_x_1024.append(np.nan)
    else:
        q_x_1024.append(1.-np.array(freq_x_1024[i]))
    if (freq_y_1024[i]<0.004):
        q_y_1024.append(np.nan)
    else:
        q_y_1024.append(freq_y_1024[i])

    if (freq_x_2048[i]< 0.004):
        q_x_2048.append(np.nan)
    else:
        q_x_2048.append(1.-np.array(freq_x_2048[i]))
    if (freq_y_2048[i]<0.004):
        q_y_2048.append(np.nan)
    else:
        q_y_2048.append(freq_y_2048[i])





    print('qx1024=',np.array(q_x_1024[i]))
    print('shape',np.shape(q_x_1024[i]))
#print(q_y_1024)
#print(q_x_2048)
#print(np.array(q_y_2048))

Jx = 0.5 * ((np.array(x) ** 2) +((np.array(px)/9.81) ** 2))
Jy = 0.5 * ((np.array(y) ** 2) + ((np.array(py)/9.81) ** 2))


"""
foo_x=(1/np.sin(3*np.pi*np.array(q_x_1024)))*np.cos(3*(np.pi*np.array(q_x_1024) - np.abs(madx_twiss.loc['xs1.2'].mux*360 - madx_twiss.loc['xs1.4'].mux*360)))
print('foox',foo_x)
print('shape',np.shape(foo_x))

foo_y=(1/np.sin(3*np.pi*np.array(q_x_1024)))*np.cos(3*(np.pi*np.array(q_x_1024) - np.abs(madx_twiss.loc['xs2.1'].mux*2*np.pi - madx_twiss.loc['xs2.3'].mux*2*np.pi)))
print('fooy',foo_y)
print('shape',np.shape(foo_y))

bar_x=(1/np.sin(np.pi*np.array(q_x_1024)))*(1/np.sin(np.pi*np.array(q_x_1024)))*3*np.cos(np.pi*np.array(q_x_1024) - np.abs(madx_twiss.loc['xs1.2'].mux*360 - madx_twiss.loc['xs1.4'].mux*360))
print('barx', bar_x)
print('shape', np.shape(bar_x))

bar_y=(1/np.sin(np.pi*np.array(q_x_1024)))*(1/np.sin(np.pi*np.array(q_x_1024)))*3*np.cos(np.pi*np.array(q_x_1024) - np.abs(madx_twiss.loc['xs2.1'].mux*360 - madx_twiss.loc['xs2.3'].mux*360))
print('bary', bar_y)
print('shape', np.shape(bar_y))


a_xx=((1/16*np.pi)*(list(sx1)[2]*list(sx2)[2])*6.6*(foo_x + bar_x)*(foo_y + bar_y))

plt.clf()
print('a_xx',a_xx)
print('shape',np.shape(a_xx))
print(np.array(q_x))
print('shape',np.shape(q_x))
plt.plot(q_x_1024, a_xx)
#plt.savefig('270524_tuneshiftamp_test.pdf')
"""
#uncomment when done with detuning amp plots

#saving the turn data to a file
with open("2905_1024_xtunes_split_rem_redist_nat.txt","w") as external_file:
    print(*q_x_1024,sep='\n',file=external_file)
external_file.close()
with open("2905_1024_ytunes_split_rem_redist_nat.txt","w") as external_file:
    print(*q_y_1024,sep='\n',file=external_file)
external_file.close()

with open("2905_2048_xtunes_split_rem_redist_nat.txt","w") as external_file:
    print(*q_x_2048,sep='\n',file=external_file)
external_file.close()
with open("2905_2048_ytunes_split_rem_redist_nat.txt","w") as external_file:
    print(*q_y_2048,sep='\n',file=external_file)
external_file.close()


#and amplitude data too

with open("2905_jx_split_rem_redist_nat.txt","w") as external_file:
    print(*Jx[:,0],sep='\n',file=external_file)
external_file.close()
with open("2905_jy_split_rem_redist_nat.txt","w") as external_file:
    print(*Jy[:,0],sep='\n',file=external_file)
external_file.close()

"""









#commenting out a copy of this just in case I mess up
for i in range(len(init_amp_x)):
    myString.append('''
        ptc_create_universe;
        ptc_create_layout, time=false, model=2, method=6, nst=5, exact=true;
        PTC_ALIGN;
        PTC_START, X=%s, PX=0, Y=0, PY=0, T=0, PT=0;
        ptc_track, icase=5, closed_orbit, dump,recloss=true, MAXAPER={0.02,0.01,0.02,.01},turns=1023, file=ptc_x_track,
        NORM_OUT, NORM_NO=1;
        ptc_track_end;
        ptc_end;
        '''%(init_amp_x[i]))
        '''%(init_amp_y[i]))
    print(init_amp_x
        '''%(init_amp_y[i]))
    print(init_amp_xrint(init_amp_x[i])
print('string',myString[2])
print('size',np.shape(myString[2]))








#crap, ignore
plt.clf()
fig,ax=plt.subplots()
#ax.set_aspect('equal')

#Zm=ma.masked_invalid(D)
#plt.imshow(Zm,origin='lower',interpolation='none',extent=[np.min(q_x_1024),np.max(q_x_1024),np.min(q_y_1024),np.max(q_y_1024)],aspect='auto',cmap='turbo')
tunes=ax.pcolormesh([X,Y],shading='auto',cmap='turbo')
#tunes=ax.scatter(X,Y,c=D,cmap='turbo',)
plt.xlabel('$x$')
plt.ylabel('$y$')
#cbar = fig.colorbar(tunes, ax=ax, label="D")
plt.colorbar(label='D',cmap='turbo')
plt.show()

"""




