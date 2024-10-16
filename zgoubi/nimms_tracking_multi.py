

from georges_core.sequences import TwissSequence
from georges_core import twiss
import zgoubidoo
from zgoubidoo.commands import *
from zgoubidoo import ureg as _
import pandas as _pd
import numpy as _np
from scipy import constants
import matplotlib.pyplot as plt
import math
import get_closed_orbits
import warnings
from pint.errors import UnitStrippedWarning

import nafflib

warnings.simplefilter('ignore', UnitStrippedWarning)



input_madx = zgoubidoo.sequences.Sequence.from_madx_twiss(
    filename='170724_og_newwp_twissbeta0.prt',
    path='/Users/spansolo/Physics/Zgoubidoo/doo_work/NIMMS_ring'
)

zi = zgoubidoo.Input.from_sequence(sequence=input_madx,
                                   beam=BeamInputDistribution,
                                   with_survey=True,
                                   with_survey_reference=True,
                                   converters={'SBEND': zgoubidoo.converters.sbend_to_zgoubi,
                                               'QUADRUPOLE': zgoubidoo.converters.quadrupole_to_zgoubi,'MULTIPOLE': zgoubidoo.converters.multipole_to_zgoubi},
                                   options={
                                       'SBEND': {'command': Dipole},
                                       'QUADRUPOLE':{'command':Quadrupole}
                                       
                                   })
print(zi.beam)
#just checking output from mad-x
#print(input_madx.betablock)
#print(input_madx.df.head(10))

kin_nom=input_madx.metadata.kinematics
#print('zi',zi)
#generate the beam from the kin data from mad-x


#print('zi from sequence,',zi.from_sequence(input_madx,beam=BeamInputDistribution))

"""
zi_new= zgoubidoo.Input(
    name="NIMMS",
    line=[
        zi.from_sequence(input_madx,beam=BeamInputDistribution),
    ],
)


print('zi_new',zi_new)

"""
zi.XPAS = 1*_.cm #integration step

#scanning over x and y

init_amp_Y=_np.linspace(0,1.78,5)

init_amp_X=_np.linspace(-0.85/2,0.85/2,5)

X,Y=_np.meshgrid(init_amp_X,init_amp_Y)
print('X,Y',X,Y)

y=init_amp_Y*_.cm
x=init_amp_X*_.cm

ref_beam = Objet2("BUNCH", BORO=kin_nom.brho)
#ref_beam = BeamZgoubiDistribution('BUNCH', kinematics=kin_nom, IMAX=2*9999999990)

'''
ref_beam.add(_np.array([[0,0,0,0,1.0]]))
ref_beam.add(_np.array([[0.85,0,0,0,1.0]]))
ref_beam.add(_np.array([[0,0,1.78,0,1.0]]))
ref_beam.add(_np.array([[0.85,0,1.78,0,1.0]]))

'''
for i in range(len(init_amp_Y)):
    for j in range(len(init_amp_X)):
        init_amp_X[j]
        init_amp_Y[i]
        ref_beam.add(_np.array([[init_amp_Y[j],0, init_amp_X[i], 0, 1.0]]))
      
        
#print('refbeam', ref_beam)
nturns=99
zi.replace('BEAM',ref_beam)
#print('beam',zi)
zi+=(Rebelote(NPASS=nturns, K=99))
#making it go faster by using more cores
ref_beam.slices = 5
zr= zgoubidoo.zgoubi.Zgoubi(n_procs=5)(zi).collect()
zr.print('stdout')
#zr= zgoubidoo.Zgoubi()(zi).collect()
points_at_marker = zr.tracks[zr.tracks.LABEL1=='TERARING$START']

print(points_at_marker)

new_y=(list(points_at_marker['Z']))
new_x=(list(points_at_marker['Y']))
print('y from marker',new_y)
print('length',len(new_y))
print('x from marker',new_x)
new_py=(list(points_at_marker['P']))
new_px=(list(points_at_marker['T']))
     

#defining aperture
adj_y=[]
adj_x=[]
adj_px=[]
adj_py=[]
for i in range(len(new_y)):
    if len(new_y)<(nturns+1) or new_y[i] > 0.03 or new_py[i] > 0.01 or new_y[i]< -1 or new_x[i] > 0.03 or new_px[i] > 0.01:
        adj_y.append(_np.nan)
        adj_x.append(_np.nan)
        adj_py.append(_np.nan)
        adj_px.append(_np.nan)
    
    else:
        adj_y.append(new_y[i])
        adj_x.append(new_x[i])
        adj_px.append(new_px[i])
        adj_py.append(new_py[i])
        '''
        var=(_np.empty((nturns+1) - len(new_y[i]), dtype=object))
        var.fill(_np.nan)
        new_y[i].extend(var)
        print('var=',var)
        print('length',_np.shape(var)) #var is fine
        '''
    
    
    #checking it works
print('y=',new_y)
print('length',len(new_y))
print('adjusted y=',adj_y)
print('length',len(adj_y))

print('x=',new_x)
print('length',len(new_x))
print('adjusted x=',adj_x)
print('length',len(adj_x))

print('px=',new_px)
print('length',len(new_px))
print('adjusted px=',adj_px)
print('length',len(adj_px))

print('py=',new_py)
print('length',len(new_py))
print('adjusted py=',adj_py)
print('length',len(adj_py))


#separating the data



    
reshapey=_np.array(adj_y).reshape((nturns+1),len(init_amp_X)*len(init_amp_Y))
reshapex=_np.array(adj_x).reshape((nturns+1),len(init_amp_X)*len(init_amp_Y))
reshapepy=_np.array(adj_py).reshape((nturns+1),len(init_amp_X)*len(init_amp_Y))
reshapepx=_np.array(adj_px).reshape((nturns+1),len(init_amp_X)*len(init_amp_Y))
print(reshapey)


print('y reshaped',(reshapey.T))

print(_np.shape(reshapey.T))

print('x reshaped',(reshapex.T))

print(_np.shape(reshapex.T))
print('py reshaped',(reshapepy.T))

print(_np.shape(reshapey.T))

print('px reshaped',(reshapepx.T))

print(_np.shape(reshapex.T))

new_x=reshapex.T
new_y=reshapey.T
new_px=reshapepx.T
new_py=reshapepy.T

#normalised coordinates


#normalised phase space
XN=(new_x/_np.sqrt((input_madx.betablock['BETA11'])))
PXN=(new_px*_np.sqrt(input_madx.betablock['BETA11']))+ (_np.array(new_x)*(input_madx.betablock['ALPHA11']))/_np.sqrt((input_madx.betablock['BETA11']))*(_.meter**0.5)**2


print('XN',XN)
print('PXN',PXN)


PHIXN=_np.arctan2(PXN,XN*(_.meter**0.5)**2)
print('PHIXN',PHIXN)

YN=(new_y/_np.sqrt((input_madx.betablock['BETA22'])))
PYN=(new_py*_np.sqrt(input_madx.betablock['BETA22']))+ (_np.array(new_y)*(input_madx.betablock['ALPHA22']))/_np.sqrt((input_madx.betablock['BETA22']))*(_.meter**0.5)**2
PHIYN=_np.arctan2(PYN,YN*(_.meter**0.5)**2)
print('YN',YN.magnitude)
print('len',len(YN))

#action angles
Jy = 0.5 * ((YN.magnitude**2) + (PYN.magnitude/9.81)**2)
Jx =  0.5 * ((XN.magnitude**2) + (PXN.magnitude/9.81)**2)
print('Jy',Jy, 'Jx',Jx, 'len',(len(Jy)))
#plt.scatter(PHIYN,Jy)

#tunes
myTunes=[]
naff_y=[]
freq_y=[]
freq_x=[]
naff_x=[]
freq_x_1024=[]
freq_y_1024=[]
freq_x_2048=[]
freq_y_2048=[]
q_x_1024=[]
q_y_1024=[]
q_x_2048=[]
q_y_2048=[]

halfturns=int(0.5*(nturns+1))
#testing this is fine
#print('halfturns',halfturns)
#print('splitting up the turn data',_np.array(XN[0][0:halfturns]))

for i in range(len(YN)):
    print('YN[i]',YN[i])
    freq_y.append(_np.abs(_np.fft.fft(YN[i].magnitude)))
    naff_y.append(nafflib.get_tune(YN[i]))
    freq_x.append(_np.abs(_np.fft.fft(XN[i].magnitude)))
    print('freq_x',freq_x[i])
    print('shape',_np.shape(freq_x[i]))
    naff_x.append(nafflib.get_tune(XN[i]))
    myTunes.append(_np.linspace(0,1,(nturns+1)))
    #plt.plot(myTunes[i],freq_y[i])
    #plt.plot(myTunes[i],freq_x[i])
    #plt.xlim(0,0.5)
    #plt.xlabel('Tune')
    #plt.ylabel("Amplitude [arb]'")
    freq_x_1024.append(nafflib.get_tune(XN[i][0:halfturns]))  # this gets the fft
    freq_y_1024.append(nafflib.get_tune(YN[i][0:halfturns]))
    freq_x_2048.append(nafflib.get_tune(XN[i][halfturns:(nturns+1)]))
    freq_y_2048.append(nafflib.get_tune(YN[i][halfturns:(nturns+1)]))
    
    
    #just putting it out there, I know this is messy af but it'll have to do for now
    if (freq_x_1024[i]<0.004):
        q_x_1024.append(_np.nan)
    else:
        q_x_1024.append(1.-_np.array(freq_x_1024[i]))
    if (freq_y_1024[i]<0.004):
        q_y_1024.append(_np.nan)
    else:
        q_y_1024.append(freq_y_1024[i])

    if (freq_x_2048[i]< 0.004):
        q_x_2048.append(_np.nan)
    else:
        q_x_2048.append(1.-_np.array(freq_x_2048[i]))
    if (freq_y_2048[i]<0.004):
        q_y_2048.append(_np.nan)
    else:
        q_y_2048.append(freq_y_2048[i])





print('qx1024=',_np.array(q_x_1024))
print('shape',_np.shape(q_x_1024))

print('qy1024=',_np.array(q_y_1024))
print('shape',_np.shape(q_y_1024))



print('qx2048=',_np.array(q_x_2048))
print('shape',_np.shape(q_x_2048))

print('qy2048=',_np.array(q_y_2048))
print('shape',_np.shape(q_y_2048))


print('y tunes',naff_y)
print(len(naff_y))
print('x tunes', 1.-_np.array(naff_x))
print(_np.shape(naff_x))

print('1024 x tunes',_np.array(q_x_1024))
print(len(q_x_1024))
print('2048 x tunes', _np.array(q_x_2048))
print(len(q_x_2048))

#saving the turn data to a file

with open("1610_1024_xtunes_og_zgoubi_100turns_25.txt","w") as external_file:
    print(*q_x_1024,sep='\n',file=external_file)
external_file.close()
with open("1610_1024_ytunes_og_zgoubi_100turns_25.txt","w") as external_file:
    print(*q_y_1024,sep='\n',file=external_file)
external_file.close()

with open("1610_2048_xtunes_og_zgoubi_100turns_25.txt","w") as external_file:
    print(*q_x_2048,sep='\n',file=external_file)
external_file.close()
with open("1610_2048_ytunes_og_zgoubi_100turns_25.txt","w") as external_file:
    print(*q_y_2048,sep='\n',file=external_file)
external_file.close()


#and amplitude data too

with open("1610_jx_og_zgoubi_100turns_25.txt","w") as external_file:
    print(*Jx[:,0],sep='\n',file=external_file)
external_file.close()
with open("1610_jy_og_zgoubi_100turns_25.txt","w") as external_file:
    print(*Jy[:,0],sep='\n',file=external_file)
external_file.close()
