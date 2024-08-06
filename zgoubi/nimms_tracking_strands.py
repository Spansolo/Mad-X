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



#Scanning over x and y
ref_beam = Objet2("BUNCH", BORO=input_madx.kinematics.brho)
ref_beam.add(_np.array([[0,0, 0, 0, 1.0]]))
zi.replace('BEAM',ref_beam)

init_amp_y=_np.linspace(0,1.78,10)

init_amp_x=_np.linspace(0,0.85,10)

y=init_amp_y*_.cm
x=init_amp_x*_.cm

X,Y = _np.meshgrid(init_amp_x,init_amp_y)

new_y=[]
new_x=[]
new_px=[]
new_py=[]


nturns=999

#for catching lost particles


for i in range(len(init_amp_y)):
    for j in range(len(init_amp_x)):
        # print('x=',X[i][j])
        # print('y=',Y[i][j])
        init_amp_x[j]
        init_amp_y[i]
        
        ref_beam = Objet2("BUNCH", BORO=input_madx.kinematics.brho)
        coords=_np.array([[x[j].magnitude,0, y[i].magnitude, 0, 1.0]])
        ref_beam.add(coords)
        
    
        print('ref beam with new coords',ref_beam)
        zi.replace('BUNCH',ref_beam)
    
        zi+=(Rebelote(NPASS=nturns, K=99))
        
        zr= zgoubidoo.Zgoubi(n_procs=12)(zi).collect()
        points_at_marker = zr.tracks[zr.tracks.LABEL1=='TERARING$START']
        print(points_at_marker)
        new_y.append(list(points_at_marker['Z']))
        new_x.append(list(points_at_marker['Y']))
        new_py.append(list(points_at_marker['P']))
        new_px.append(list(points_at_marker['T']))
        
#this says, for each initial amplitude (total is # of x amps x # of y amps): if the length of the array doesn't equal the length of the number of turns,
#make a variable var that contains some nans to make up the remaining number of turns,
#so it doesn't look like the array is shorter when the particle is lost
#print('new x', new_x[j])
#print('length',len(new_x[j]))

for i in range(len(init_amp_y)*len(init_amp_x)):
    if len(new_y[i])<(nturns+1):
        var=(_np.empty((nturns+1) - len(new_y[i]), dtype=object))
        var.fill(_np.nan)
        new_y[i].extend(var)
        print('var=',var)
        print('length',_np.shape(var)) #var is fine
    #checking it works
    print('y=',new_y[i])
    print('length',len(new_y[i]))

    if len(new_x[i])<(nturns+1):
        var_2=(_np.empty((nturns+1) - len(new_x[i]), dtype=object))
        var_2.fill(_np.nan)
        new_x[i].extend(var_2)
            

    if len(new_px[i])<(nturns+1):
        var_3=(_np.empty((nturns+1) - len(new_px[i]), dtype=object))
        var_3.fill(_np.nan)
        new_px[i].extend(var_3)
        
    if len(new_py[i])<(nturns+1):
        var_4=(_np.empty((nturns+1) - len(new_py[i]), dtype=object))
        var_4.fill(_np.nan)
        new_py[i].extend(var_4)
            

print('y',new_y)
print('shape',_np.shape(new_y))
print('x',new_x)
print('shape',_np.shape(new_x))



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
    #print(YN[i])
    freq_y.append(_np.abs(_np.fft.fft(YN[i].magnitude)))
    naff_y.append(nafflib.get_tune(new_y[i]))
    freq_x.append(_np.abs(_np.fft.fft(XN[i].magnitude)))
    naff_x.append(nafflib.get_tune(XN[i]))
    myTunes.append(_np.linspace(0,1,(nturns+1)))
    #plt.plot(myTunes[i],freq_y[i])
    plt.plot(myTunes[i],freq_x[i])
    plt.xlim(0,0.5)
    plt.xlabel('Tune')
    plt.ylabel("Amplitude [arb]'")
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



print('qx20484=',_np.array(q_x_2048))
print('shape',_np.shape(q_x_2048))

print('qy2048=',_np.array(q_y_2048))
print('shape',_np.shape(q_y_2048))


print('y tunes',naff_y)
print(len(naff_y))
print('x tunes', 1.-_np.array(naff_x))
print(_np.shape(naff_x))

print('1024 x tunes',1.-_np.array(freq_x_1024))
print(len(freq_x_1024))
print('2048 x tunes', 1.-_np.array(freq_x_2048))
print(len(freq_x_2048))







#tune shift with action
#remember that you need Jx[:,0] for plotting these individually

#plt.scatter(Jx[:,0],_np.array(naff_x))


#Writing turn by turn data to files
#saving the turn data to a file
with open("0508_1024_xtunes_og_zgoubi_1kturns_100.txt","w") as external_file:
    print(*q_x_1024,sep='\n',file=external_file)
external_file.close()
with open("0508_1024_ytunes_og_zgoubi_1kturns_100.txt","w") as external_file:
    print(*q_y_1024,sep='\n',file=external_file)
external_file.close()

with open("0508_2048_xtunes_og_zgoubi_1kturns_100.txt","w") as external_file:
    print(*q_x_2048,sep='\n',file=external_file)
external_file.close()
with open("0508_2048_ytunes_og_zgoubi_1kturns_100.txt","w") as external_file:
    print(*q_y_2048,sep='\n',file=external_file)
external_file.close()


#and amplitude data too

with open("0508_jx_og_zgoubi_1kturns_100.txt","w") as external_file:
    print(*Jx[:,0],sep='\n',file=external_file)
external_file.close()
with open("0508_jy_og_zgoubi_1kturns_100.txt","w") as external_file:
    print(*Jy[:,0],sep='\n',file=external_file)
external_file.close()

