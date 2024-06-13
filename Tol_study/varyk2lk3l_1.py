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


trackparts = []

myAmplitudePTC_x = []
y = []
px=[]
py=[]
beta_x = []
beta_y = []
s = []
dx = []
dy = []
D = []
freq_x = []  # overall x frequencies
freq_y = []  # overall y frequencies
freq_x_1024 = []
freq_y_1024 = []
freq_x_2048 = []
freq_y_2048 = []
q_x = []
q_y = []
Qx_2048 = []
Qx_1024 = []
Qy_2048 = []
Qy_1024 = []
q_x_1024 = []
q_y_1024 = []
q_x_2048 = []
q_y_2048 = []

survivedparts = []


myAmplitudePTC_y = []
myTunesPTC = []



#import tfs



#madx.option(echo=True)

#this prints the crap into a log file so you don't have to see all the PTC info for
#every time you send a particle round
cpymad_logfile = 'cpymad_logfile.log'

n=12
madxs=np.repeat(Madx(),(n*n))
print(madxs)
print(np.shape(madxs))

sig_7x = (1.3e-3) * 7
sig_7y = (1.8e-3) * 7

#setting initial (x,y) space for beam to be tracked
init_amp_x = np.linspace(0, sig_7x,100) #100)  # sig_2x,3) #going from 0 to 2sigma for 3 steps in x
init_amp_y = np.linspace(0,sig_7y,10) #10)
X, Y = np.meshgrid(init_amp_x, init_amp_y)
#print('X length',np.size(X))


for i in init_amp_y:
    for j in init_amp_x:
        trackparts.append('''
             ptc_create_universe;
             ptc_create_layout, time=false, model=2, method=6, nst=5, exact=true;
             PTC_ALIGN;
             PTC_START, X=%s, PX=0, Y=%s, PY=0, T=0, PT=0;
             ptc_track, icase=5, closed_orbit, dump,recloss=true, MAXAPER={0.03,0.01,0.03,0.01},turns=2047, file=ptc_x_track,
             NORM_OUT, NORM_NO=1;
             ptc_track_end;
             ptc_end;
             ''' % (j, i))






#calling the mad-x file to be used




input=[]
k2L_b=0.1013878507
k3L_b=2.96491034
#k2L=np.linspace(k2L_b,1.5*k2L_b,n)
#k3L=np.linspace(k3L_b,1.5*k3L_b,n)
#S,O=np.meshgrid(k2L,k3L)

k2L=np.linspace(0.0,1.0,n)
k3L=np.linspace(0.0,1.0,n)
S,O=np.meshgrid(k2L,k3L)
print('S',S,'O',O)
print('shape',np.shape(S))






#for each value of k2L, k3L, write a new mad-x input
for i in range(len(k2L)):
    for j in range(len(k3L)):
        input.append(f"""
    

    
        //first fringe section's multipoles 
        
        ml1: multipole, knl:={{0,0,0.05174218354271365*{S[i][j]},-8.372324917950808*{O[i][j]}}},ksl:={{0,0,-0.07263117346686897,-21.215649834527493}}; 
        ml2: multipole, knl:={{0,0,-0.034065730930271695*{S[i][j]},2.6898872860353067*{O[i][j]}}},ksl:={{0,0,0.056507135241667755,32.57063641883827}};
        ml3: multipole, knl:={{0,0,0.06646817983770664*{S[i][j]},17.287433892273967*{O[i][j]}}},ksl:={{0,0,-0.10597414179840726,7.432180570843474}};
        ml4: multipole, knl:={{0,0,0.352750743663756*{S[i][j]},-3.0421770342941983*{O[i][j]}}},ksl:={{0,0,-0.37104782498225947,-8.21570372039009}};
        ml5: multipole, knl:={{0,0,0.47498251053833934*{S[i][j]},-4.375496704937848*{O[i][j]}}},ksl:={{0,0,-0.4694815362341481,5.624059916576834}};
        ml6: multipole, knl:={{0,0,0.49643450235109765*{S[i][j]},7.763195893588152*{O[i][j]}}},ksl:={{0,0,-0.5017009412586334,10.781604909016647}};
        ml7: multipole, knl:={{0,0,0.48712627023359817*{S[i][j]},10.888537369657392*{O[i][j]}}},ksl:={{0,0,-0.49417404440613294,6.937288464151968}};
        ml8: multipole, knl:={{0,0,0.44890333399252197*{S[i][j]},7.63908745734465*{O[i][j]}}},ksl:={{0,0,-0.44916680180224283,1.0152619424878002}};
        ml9: multipole, knl:={{0,0,0.3875798208639547*{S[i][j]},3.1067299798023247*{O[i][j]}}},ksl:={{0,0,-0.3791655910317315,-3.330702279495824}};
        ml10: multipole, knl:={{0,0,0.3150680425187353*{S[i][j]},-0.2665133025966837*{O[i][j]}}},ksl:={{0,0, -0.3084118141262903,-4.555217116812375}};
        ml11: multipole, knl:={{0,0,0.24256334100884006*{S[i][j]},-1.8462210386698623*{O[i][j]}}},ksl:={{0,0,-0.23375855197587353,-4.230935418780664}};
        ml12: multipole, knl:={{0,0,0.1780807885573016*{S[i][j]},-2.119895382809879*{O[i][j]}}},ksl:={{0,0,-0.16910561223486864,-2.892974958274154}};
        ml13: multipole, knl:={{0,0,0.1244089213823894*{S[i][j]},-1.5261527287102792*{O[i][j]}}},ksl:={{0,0,-0.11717149093759363,-1.4217977410285414}};
        ml14: multipole, knl:={{0,0,0.0845357880367623*{S[i][j]},-1.06779671508994*{O[i][j]}}},ksl:={{0,0,-0.0786757291059749,-0.4437617819636255}};
        ml15: multipole,knl:={{0,0,0.05494531715746322*{S[i][j]},-0.39344361167681385*{O[i][j]}}},ksl:={{0,0,-0.051149329571618364,0.1687149152040626}};
        
        
        //last fringe section's multipoles
        mr1: multipole, knl:={{0,0,0.02713694484568402*{S[i][j]},-1.2936016279373141*{O[i][j]}}},ksl:={{0,0,-0.03344811125350078,0.3946180910150646}}; 
        mr2: multipole, knl:={{0,0,0.0440841249262118*{S[i][j]},-2.280054616832684*{O[i][j]}}},ksl:={{0,0,-0.053133966642882106,-0.16141143700218524}}; 
        mr3: multipole, knl:={{0,0,0.07051957143778219*{S[i][j]},-3.544812754109982*{O[i][j]}}},ksl:={{0,0,-0.08283029509911753,-1.0992798451903418}}; 
        mr4: multipole, knl:={{0,0,0.11032588842186483*{S[i][j]},-5.060189392855733*{O[i][j]}}},ksl:={{0,0,-0.1250211570309426,-2.4382447054985343}}; 
        mr5: multipole, knl:={{0,0,0.16591004699232917*{S[i][j]},-6.1131828154731265*{O[i][j]}}},ksl:={{0,0,-0.18259297556526147,-3.9882331338816437}}; 
        mr6: multipole, knl:={{0,0,0.23765168616680823*{S[i][j]},-5.89328341128801*{O[i][j]}}},ksl:={{0,0,-0.25471726169479,-4.8793045858383035}}; 
        mr7: multipole, knl:={{0,0,0.32020753516304046*{S[i][j]},-3.32088024946798*{O[i][j]}}},ksl:={{0,0,-0.33643742042440183,-4.01666933726846}}; 
        mr8: multipole, knl:={{0,0,0.39978985917936455*{S[i][j]},2.392874819257562*{O[i][j]}}},ksl:={{0,0,-0.41472165093118935,-0.5513512414339089}}; 
        mr9: multipole, knl:={{0,0,0.4599121858239861*{S[i][j]},9.830049910439003*{O[i][j]}}},ksl:={{0,0,-0.47242373581535324,5.190809514258742}}; 
        mr10: multipole, knl:={{0,0,0.48670963538385487*{S[i][j]},14.48350220391324*{O[i][j]}}},ksl:={{0,0,-0.4929292905384712,10.536192075427977}}; 
        mr11: multipole, knl:={{0,0,0.4802019251060581*{S[i][j]},8.814120334162714*{O[i][j]}}},ksl:={{0,0,-0.4715227766089816,9.767833603678932}}; 
        mr12: multipole, knl:={{0,0,0.4476311097985487*{S[i][j]},-6.993217367582879*{O[i][j]}}},ksl:={{0,0,-0.41913225377098845,-1.7104943599701177}}; 
        mr13: multipole, knl:={{0,0,0.2678222342819212*{S[i][j]},5.197598700165096*{O[i][j]}}},ksl:={{0,0,-0.2782721848409969,-10.176931517429368}}; 
        mr14: multipole, knl:={{0,0,-0.004522667005111972*{S[i][j]},21.358825707619463*{O[i][j]}}},ksl:={{0,0,0.0012165603561003467,22.85652291891122}}; 
        mr15: multipole, knl:={{0,0,-0.020153183321378252*{S[i][j]},8.214400077814053*{O[i][j]}}},ksl:={{0,0,0.04026690620079324,19.653038676087824}}; 
        
        
        //boundary multipoles
        
        
        mbo1: multipole, knl:={{0,0,0.003724355597701272*{S[i][j]},0.44943051046317695*{O[i][j]}}},ksl:={{0,0,-0.0034457329750667742,0.4787436975257266}}; 
        mbo2: multipole, knl:={{0,0,0.0040040440910900435*{S[i][j]},0.43214984147359753*{O[i][j]}}},ksl:={{0,0,-0.0037098205166518675,0.4418203903712419}}; 
        mbo3: multipole, knl:={{0,0,0.004078097394653043*{S[i][j]},0.46657263713367186*{O[i][j]}}},ksl:={{0,0,-0.0038975410030415198,0.4337586906802744}}; 
        mbo4: multipole, knl:={{0,0,0.0044210333458859*{S[i][j]},0.41600887540187964*{O[i][j]}}},ksl:={{0,0,-0.003913917709995806,0.46465277115380954}}; 
        mbo5: multipole, knl:={{0,0,0.0045206482116777425*{S[i][j]},0.4729389594335212*{O[i][j]}}},ksl:={{0,0,-0.004032233835416338,0.45095452165222766}}; 
        mbo6: multipole, knl:={{0,0,0.00457659558775221*{S[i][j]},0.49526941001657865*{O[i][j]}}},ksl:={{0,0,-0.003903982631920891,0.45299038929971785}}; 
        mbo7: multipole, knl:={{0,0,0.003485460699226455*{S[i][j]},0.6252678326284868*{O[i][j]}}},ksl:={{0,0,-0.0027811448628870354,0.45162888247751254}}; 
        mbo8: multipole, knl:={{0,0,-0.0005799035931314371*{S[i][j]},0.7146379209316773*{O[i][j]}}},ksl:={{0,0,0.0016036948079864537,0.524486093400065}}; 
        mbo9: multipole, knl:={{0,0,-0.015011873374487008*{S[i][j]},0.876093225669636*{O[i][j]}}},ksl:={{0,0,0.015753042152805406,0.8140085711544095}}; 
        mbo10: multipole, knl:={{0,0,-0.04936665185661155*{S[i][j]},-0.825778301144271*{O[i][j]}}},ksl:={{0,0,0.04918572465726452,0.5990480829763275}}; 
        mbo11: multipole, knl:={{0,0,-0.09939105458109962*{S[i][j]},-10.972861180747143*{O[i][j]}}},ksl:={{0,0,0.10196686389300934,-3.831896442560623}}; 
        mbo12: multipole, knl:={{0,0,-0.1368044217572699*{S[i][j]},-30.729903255724512*{O[i][j]}}},ksl:={{0,0,0.14520977194176288,-18.29242669168161}}; 
        mbo13: multipole, knl:={{0,0,-0.2763787931949364*{S[i][j]},-17.329146889756405*{O[i][j]}}},ksl:={{0,0,0.2284931512076435,-27.212275268826247}}; 
        mbo14: multipole, knl:={{0,0,-0.48953749144164366*{S[i][j]},18.516007074259708*{O[i][j]}}},ksl:={{0,0,0.41107185666149254,15.574943053656362}}; 
        mbo15: multipole, knl:={{0,0,-0.3296960807450906*{S[i][j]},15.117632114961257*{O[i][j]}}},ksl:={{0,0,0.2887619043716814,36.578706390551595}}; 
        
        //second boundary
        
        mbo1_2: multipole, knl:={{0,0,0.1650319702242267*{S[i][j]},-8.050387904219651*{O[i][j]}}},ksl:={{0,0,-0.11421390435504508,-13.57804422284358}}; 
        mbo2_2: multipole, knl:={{0,0,-0.26841431875308464*{S[i][j]},10.195481104983644*{O[i][j]}}},ksl:={{0,0,0.32657939771313116,35.41817356446289}}; 
        mbo3_2: multipole, knl:={{0,0,-0.3302175847180019*{S[i][j]},13.430469651332496*{O[i][j]}}},ksl:={{0,0,0.31530579119224006,-3.3784960588622606}}; 
        mbo4_2: multipole, knl:={{0,0,-0.1430750140697533*{S[i][j]},-16.251017206331273*{O[i][j]}}},ksl:={{0,0,0.14926964880576327,-23.27966398915956}}; 
        mbo5_2: multipole, knl:={{0,0,-0.06435033044418849*{S[i][j]},-20.44727691759517*{O[i][j]}}},ksl:={{0,0,0.08990604774289358,-9.00662356939925}}; 
        mbo6_2: multipole, knl:={{0,0,-0.04274971496272812*{S[i][j]},-7.720216336434085*{O[i][j]}}},ksl:={{0,0,0.05291270595914753,-0.5273248519834437}}; 
        mbo7_2: multipole, knl:={{0,0,-0.019815804046223646*{S[i][j]},-1.5636154622043417*{O[i][j]}}},ksl:={{0,0,0.02179223540004597,0.8083510150126835}}; 
        mbo8_2: multipole, knl:={{0,0,-0.005375381475609387*{S[i][j]},0.01832353370760056*{O[i][j]}}},ksl:={{0,0,0.005383021181269883,0.6178874942867795}}; 
        mbo9_2: multipole, knl:={{0,0,0.0004962190524573627*{S[i][j]},0.42104798696310275*{O[i][j]}}},ksl:={{0,0,-0.0009314948112840501,0.4665948546657393}}; 
        mbo10_2: multipole, knl:={{0,0,0.0026599463927766635*{S[i][j]},0.4562761375517129*{O[i][j]}}},ksl:={{0,0, -0.00292400045788297,0.4371616053881111}}; 
        mbo11_2: multipole, knl:={{0,0,0.00324337577680284*{S[i][j]},0.48140691410014147*{O[i][j]}}},ksl:={{0,0,-0.0034927832011887234,0.42726407731445637}}; 
        mbo12_2: multipole, knl:={{0,0,0.003507569855725236*{S[i][j]},0.4490111603326956*{O[i][j]}}},ksl:={{0,0,-0.003566893346988717,0.4322854159416494}}; 
        mbo13_2: multipole, knl:={{0,0,0.0033708230203965826*{S[i][j]},0.452957871679303*{O[i][j]}}},ksl:={{0,0,-0.003445566785277617,0.47927307016920184}}; 
        mbo14_2: multipole, knl:={{0,0,0.0035529302780353497*{S[i][j]},0.4122174776877115*{O[i][j]}}},ksl:={{0,0,-0.0035351720346672296,0.43392189193232766}}; 
        mbo15_2: multipole, knl:={{0,0,0.0034317119372752167*{S[i][j]},0.45713652583212616*{O[i][j]}}},ksl:={{0,0,-0.0034648518530029475,0.4197193017665418}}; 
        
        
        
        //body multipoles
        
        
        //first F
        multib1: multipole, knl:={{0,0,0.1505689259736886*{S[i][j]},17.75144206893953*{O[i][j]}}},ksl:={{0,0,-0.13092323063887223,20.78711738579513}};
        
        //Ds 
        multib2: multipole, knl:={{0,0,0.351167188415951*{S[i][j]},19.342531089728393*{O[i][j]}}},ksl:={{0,0,-0.3579388536444811,20.038205570287516}}; 
        multib3: multipole, knl:={{0,0,0.35148370142516405*{S[i][j]},18.366205030108937*{O[i][j]}}},ksl:={{0,0,-0.35799926788086217,18.84620564891376}}; 
        multib4: multipole, knl:={{0,0,0.3488506308072991*{S[i][j]},19.70912127552942*{O[i][j]}}},ksl:={{0,0,-0.36069269704172185,18.03594062135351}}; 
        
        //last F 
        multib5: multipole, knl:={{0,0,0.1260156597463035*{S[i][j]},18.563674803630832*{O[i][j]}}},ksl:={{0,0,-0.12291886570171466,20.83508502171123}}; 
        
        
        
        
        teracell1: sequence, refer=entry, l:=lcell1;
        //1st 14 sbends section
        
        ml1.1:ml1, at:=0;
        mb1_1.1:mb_1, at:=0;
        ml2.1:ml2, at:=e_1/14;
        mb1_2.1:mb_1, at:=e_1/14;
        ml3.1:ml3, at:=2*e_1/14;
        mb1_3.1:mb_1, at:=2*e_1/14;
        ml4.1:ml4, at:=3*e_1/14;
        mb1_4.1:mb_1, at:=3*e_1/14;
        ml5.1:ml5, at:=4*e_1/14;
        mb1_5.1:mb_1, at:=4*e_1/14;
        ml6.1:ml6, at:=5*e_1/14;
        mb1_6.1:mb_1, at:=5*e_1/14;
        ml7.1:ml7, at:=6*e_1/14;
        mb1_7.1:mb_1, at:=6*e_1/14;
        ml8.1:ml8, at:=7*e_1/14;
        mb1_8.1:mb_1, at:=7*e_1/14;
        ml9.1:ml9, at:=8*e_1/14;
        mb1_9.1:mb_1, at:=8*e_1/14;
        ml10.1:ml10, at:=9*e_1/14;
        mb1_10.1:mb_1, at:=9*e_1/14;
        ml11.1:ml11, at:=10*e_1/14;
        mb1_11.1:mb_1, at:=10*e_1/14;
        ml12.1:ml12, at:=11*e_1/14;
        mb1_12.1:mb_1, at:=11*e_1/14;
        ml13.1:ml13, at:=12*e_1/14;
        mb1_13.1:mb_1, at:=12*e_1/14;
        ml14.1:ml14, at:=13*e_1/14;
        mb1_14.1:mb_1, at:=13*e_1/14;
        
        
        //main body of magnet
        //first proper magnet chunk (focusing)
        mb1.1:mb1, at:=e_1;
        b1.1:multib1, at:=e_1 + lbf_n/2;
        mb2.1:mb1, at:=e_1+lbf_n/2;
        
        //boundary region (F)
        mbo1.1:mbo1, at:=lbf-lbf_fr;
        mbf_1.1:mb_f, at:=lbf-lbf_fr;
        mbo2.1: mbo2, at:=lbf-lbf_fr*6/7;
        mbf_2.1:mb_f, at:=lbf-lbf_fr*6/7;
        mbo3.1: mbo3, at:=lbf-lbf_fr*5/7;
        mbf_3.1:mb_f, at:=lbf-lbf_fr*5/7;
        mbo4.1: mbo4, at:=lbf-lbf_fr*4/7;
        mbf_4.1:mb_f, at:=lbf-lbf_fr*4/7;
        mbo5.1: mbo5, at:=lbf-lbf_fr*3/7;
        mbf_5.1:mb_f, at:=lbf-lbf_fr*3/7;
        mbo6.1: mbo6, at:=lbf-lbf_fr*2/7;
        mbf_6.1:mb_f, at:=lbf-lbf_fr*2/7;
        mbo7.1: mbo7, at:=lbf-lbf_fr/7;
        mbf_7.1:mb_f, at:=lbf-lbf_fr/7;
        
        
        //boundary region (D)
        mbo8.1: mbo8, at:=lbf;
        mbd_1.1:mb_d, at:=lbf;
        mbo9.1: mbo9, at:=lbf+lbf_fr/7;
        mbd_2.1:mb_d, at:=lbf+lbf_fr/7;
        mbo10.1: mbo10, at:=lbf+2*lbf_fr/7;
        mbd_3.1:mb_d, at:=lbf+2*lbf_fr/7;
        mbo11.1: mbo11, at:=lbf+3*lbf_fr/7;
        mbd_4.1:mb_d, at:=lbf+3*lbf_fr/7;
        mbo12.1: mbo12, at:=lbf+4*lbf_fr/7;
        mbd_5.1:mb_d, at:=lbf+4*lbf_fr/7;
        mbo13.1: mbo13, at:=lbf+5*lbf_fr/7;
        mbd_6.1:mb_d, at:=lbf+5*lbf_fr/7;
        mbo14.1: mbo14, at:=lbf+6*lbf_fr/7;
        mbd_7.1:mb_d, at:=lbf+6*lbf_fr/7;
        
        //second magnet chunk (defocusing)
        mb3.1:mb2, at:=lbf+lbf_fr;
        b2.1:multib2, at:=lbf+lbf_fr+lbd_n/2;
        mb4.1:mb2, at:=lbf+lbf_fr+lbd_n/2;
        
        //third magnet chunk (defocusing)
        b3.1:multib3, at:=lbf+lbf_fr+lbd_n;
        mb5.1:mb3, at:=lbf+lbf_fr+lbd_n;
        b4.1:multib4, at:=lbf+lbf_fr+lbd_n+lbd_n/2;
        mb6.1:mb3, at:=lbf+lbf_fr+lbd_n+lbd_n/2;
        
        //boundary region (D)
        mbo1_2.1: mbo1_2, at:=lbf+lbf+lbf-lbf_fr;
        mbd_8.1:mb_d, at:=lbf+lbf+lbf-lbf_fr;
        mbo2_2.1: mbo2_2, at:=lbf+lbf+lbf-lbf_fr*6/7;
        mbd_9.1:mb_d, at:=lbf+lbf+lbf-lbf_fr*6/7;
        mbo3_2.1: mbo3_2, at:=lbf+lbf+lbf-lbf_fr*5/7;
        mbd_10.1:mb_d, at:=lbf+lbf+lbf-lbf_fr*5/7;
        mbo4_2.1: mbo4_2, at:=lbf+lbf+lbf-lbf_fr*4/7;
        mbd_11.1:mb_d, at:=lbf+lbf+lbf-lbf_fr*4/7;
        mbo5_2.1: mbo5_2, at:=lbf+lbf+lbf-lbf_fr*3/7;
        mbd_12.1:mb_d, at:=lbf+lbf+lbf-lbf_fr*3/7;
        mbo6_2.1: mbo6_2, at:=lbf+lbf+lbf-lbf_fr*2/7;
        mbd_13.1:mb_d, at:=lbf+lbf+lbf-lbf_fr*2/7;
        mbo7_2.1: mbo7_2, at:=lbf+lbf+lbf-lbf_fr*1/7;
        mbd_14.1:mb_d, at:=lbf+lbf+lbf-lbf_fr*1/7;
        
        //boundary region (F)
        mbo8_2.1:mbo8_2, at:=lbf+lbf+lbd;
        mbf_8.1:mb_f, at:=lbf+lbf+lbd;
        mbo9_2.1:mbo9_2, at:=lbf+lbf+lbd+lbf_fr/7;
        mbf_9.1:mb_f, at:=lbf+lbf+lbd+lbf_fr/7;
        mbo10_2.1:mbo10_2, at:=lbf+lbf+lbd+2*lbf_fr/7;
        mbf_10.1:mb_f, at:=lbf+lbf+lbd+2*lbf_fr/7;
        mbo11_2.1:mbo11_2, at:=lbf+lbf+lbd+3*lbf_fr/7;
        mbf_11.1:mb_f, at:=lbf+lbf+lbd+3*lbf_fr/7;
        mbo12_2.1:mbo12_2, at:=lbf+lbf+lbd+4*lbf_fr/7;
        mbf_12.1:mb_f, at:=lbf+lbf+lbd+4*lbf_fr/7;
        mbo13_2.1:mbo13_2, at:=lbf+lbf+lbd+5*lbf_fr/7;
        mbf_13.1:mb_f, at:=lbf+lbf+lbd+5*lbf_fr/7;
        mbo14_2.1:mbo14_2, at:=lbf+lbf+lbd+6*lbf_fr/7;
        mbf_14.1:mb_f, at:=lbf+lbf+lbd+6*lbf_fr/7;
        
        
        //last chunk (focusing)
        mb7.1:mb4, at:=lbf+lbf+lbd+lbf_fr;
        b5.1:multib5, at:=lbf+lbf+lbd+lbf_fr+lbf_n/2;
        mb8.1:mb4, at:=lbf+lbf+lbd+lbf_fr+lbf_n/2;
        
        L=lbd+lbf+lbf+lbd;
        
        //2nd 14 sbends section
        mr1.1:mr1, at:=L-e_1;
        mb2_1.1:mb_4, at:=L-e_1;
        mr2.1:mr2, at:=L-13*e_1/14;
        mb2_2.1:mb_4, at:=L-13*e_1/14;
        mr3.1:mr3, at:=L-12*e_1/14;
        mb2_3.1:mb_4, at:=L-12*e_1/14;
        mr4.1:mr4, at:=L-11*e_1/14;
        mb2_4.1:mb_4, at:=L-11*e_1/14;
        mr5.1:mr5, at:=L-10*e_1/14;
        mb2_5.1:mb_4, at:=L-10*e_1/14;
        mr6.1:mr6, at:=L-9*e_1/14;
        mb2_6.1:mb_4, at:=L-9*e_1/14;
        mr7.1:mr7, at:=L-8*e_1/14;
        mb2_7.1:mb_4, at:=L-8*e_1/14;
        mr8.1:mr8, at:=L-7*e_1/14;
        mb2_8.1:mb_4, at:=L-7*e_1/14;
        mr9.1:mr9, at:=L-6*e_1/14;
        mb2_9.1:mb_4, at:=L-6*e_1/14;
        mr10.1:mr10, at:=L-5*e_1/14;
        mb2_10.1:mb_4, at:=L-5*e_1/14;
        mr11.1:mr11, at:=L-4*e_1/14;
        mb2_11.1:mb_4, at:=L-4*e_1/14;
        mr12.1:mr12, at:=L-3*e_1/14;
        mb2_12.1:mb_4, at:=L-3*e_1/14;
        mr13.1:mr13, at:=L-2*e_1/14;
        mb2_13.1:mb_4, at:=L-2*e_1/14;
        mr14.1:mr14, at:=L-e_1/14;
        mb2_14.1:mb_4, at:=L-e_1/14;
        mr15.1:mr15, at:=L;
        
        qq1a.1:qq1, at:=lbd+lbf+lbf+lbd+0.25+dq;
        xs1.1:xs1, at:=lbd+lbf+lbf+lbd+0.25+dq+3*lquad;
        
        //p1:marker, at=lcell-d2*3./4.;
        //p2:marker, at=lcell-d2/2.;
        //p3:marker, at=lcell-d2/4.;
        qq1b.1:qq1, at:=lcell1-0.25 -lquad -dq;
        xs2.1:xs2, at:=lcell1-0.25 -lquad -dq + 3*lquad;
        
        endsequence;
        
        
        
        
        teracell2: sequence, refer=entry, l:=lcell2;
        //1st 14 sbends section
        ml1.2:ml1, at:=0;
        mb1_1.2:mb_1, at:=0;
        ml2.2:ml2, at:=e_1/14;
        mb1_2.2:mb_1, at:=e_1/14;
        ml3.2:ml3, at:=2*e_1/14;
        mb1_3.2:mb_1, at:=2*e_1/14;
        ml4.2:ml4, at:=3*e_1/14;
        mb1_4.2:mb_1, at:=3*e_1/14;
        ml5.2:ml5, at:=4*e_1/14;
        mb1_5.2:mb_1, at:=4*e_1/14;
        ml6.2:ml6, at:=5*e_1/14;
        mb1_6.2:mb_1, at:=5*e_1/14;
        ml7.2:ml7, at:=6*e_1/14;
        mb1_7.2:mb_1, at:=6*e_1/14;
        ml8.2:ml8, at:=7*e_1/14;
        mb1_8.2:mb_1, at:=7*e_1/14;
        ml9.2:ml9, at:=8*e_1/14;
        mb1_9.2:mb_1, at:=8*e_1/14;
        ml10.2:ml10, at:=9*e_1/14;
        mb1_10.2:mb_1, at:=9*e_1/14;
        ml11.2:ml11, at:=10*e_1/14;
        mb1_11.2:mb_1, at:=10*e_1/14;
        ml12.2:ml12, at:=11*e_1/14;
        mb1_12.2:mb_1, at:=11*e_1/14;
        ml13.2:ml13, at:=12*e_1/14;
        mb1_13.2:mb_1, at:=12*e_1/14;
        ml14.2:ml14, at:=13*e_1/14;
        mb1_14.2:mb_1, at:=13*e_1/14;
        
        
        //main body of magnet
        //first proper magnet chunk (focusing)
        mb1.2:mb1, at:=e_1;
        b1.2:multib1, at:=e_1 + lbf_n/2;
        mb2.2:mb1, at:=e_1+lbf_n/2;
        
        //boundary region (F)
        mbo1.2:mbo1, at:=lbf-lbf_fr;
        mbf_1.2:mb_f, at:=lbf-lbf_fr;
        mbo2.2: mbo2, at:=lbf-lbf_fr*6/7;
        mbf_2.2:mb_f, at:=lbf-lbf_fr*6/7;
        mbo3.2: mbo3, at:=lbf-lbf_fr*5/7;
        mbf_3.2:mb_f, at:=lbf-lbf_fr*5/7;
        mbo4.2: mbo4, at:=lbf-lbf_fr*4/7;
        mbf_4.2:mb_f, at:=lbf-lbf_fr*4/7;
        mbo5.2: mbo5, at:=lbf-lbf_fr*3/7;
        mbf_5.2:mb_f, at:=lbf-lbf_fr*3/7;
        mbo6.2: mbo6, at:=lbf-lbf_fr*2/7;
        mbf_6.2:mb_f, at:=lbf-lbf_fr*2/7;
        mbo7.2: mbo7, at:=lbf-lbf_fr/7;
        mbf_7.2:mb_f, at:=lbf-lbf_fr/7;
        
        
        //boundary region (D)
        mbo8.2: mbo8, at:=lbf;
        mbd_1.2:mb_d, at:=lbf;
        mbo9.2: mbo9, at:=lbf+lbf_fr/7;
        mbd_2.2:mb_d, at:=lbf+lbf_fr/7;
        mbo10.2: mbo10, at:=lbf+2*lbf_fr/7;
        mbd_3.2:mb_d, at:=lbf+2*lbf_fr/7;
        mbo11.2: mbo11, at:=lbf+3*lbf_fr/7;
        mbd_4.2:mb_d, at:=lbf+3*lbf_fr/7;
        mbo12.2: mbo12, at:=lbf+4*lbf_fr/7;
        mbd_5.2:mb_d, at:=lbf+4*lbf_fr/7;
        mbo13.2: mbo13, at:=lbf+5*lbf_fr/7;
        mbd_6.2:mb_d, at:=lbf+5*lbf_fr/7;
        mbo14.2: mbo14, at:=lbf+6*lbf_fr/7;
        mbd_7.2:mb_d, at:=lbf+6*lbf_fr/7;
        
        //second magnet chunk (defocusing)
        mb3.2:mb2, at:=lbf+lbf_fr;
        b2.2:multib2, at:=lbf+lbf_fr+lbd_n/2;
        mb4.2:mb2, at:=lbf+lbf_fr+lbd_n/2;
        
        //third magnet chunk (defocusing)
        b3.2:multib3, at:=lbf+lbf_fr+lbd_n;
        mb5.2:mb3, at:=lbf+lbf_fr+lbd_n;
        b4.2:multib4, at:=lbf+lbf_fr+lbd_n+lbd_n/2;
        mb6.2:mb3, at:=lbf+lbf_fr+lbd_n+lbd_n/2;
        
        //boundary region (D)
        mbo1_2.2: mbo1_2, at:=lbf+lbf+lbf-lbf_fr;
        mbd_8.2:mb_d, at:=lbf+lbf+lbf-lbf_fr;
        mbo2_2.2: mbo2_2, at:=lbf+lbf+lbf-lbf_fr*6/7;
        mbd_9.2:mb_d, at:=lbf+lbf+lbf-lbf_fr*6/7;
        mbo3_2.2: mbo3_2, at:=lbf+lbf+lbf-lbf_fr*5/7;
        mbd_10.2:mb_d, at:=lbf+lbf+lbf-lbf_fr*5/7;
        mbo4_2.2: mbo4_2, at:=lbf+lbf+lbf-lbf_fr*4/7;
        mbd_11.2:mb_d, at:=lbf+lbf+lbf-lbf_fr*4/7;
        mbo5_2.2: mbo5_2, at:=lbf+lbf+lbf-lbf_fr*3/7;
        mbd_12.2:mb_d, at:=lbf+lbf+lbf-lbf_fr*3/7;
        mbo6_2.2: mbo6_2, at:=lbf+lbf+lbf-lbf_fr*2/7;
        mbd_13.2:mb_d, at:=lbf+lbf+lbf-lbf_fr*2/7;
        mbo7_2.2: mbo7_2, at:=lbf+lbf+lbf-lbf_fr*1/7;
        mbd_14.2:mb_d, at:=lbf+lbf+lbf-lbf_fr*1/7;
        
        //boundary region (F)
        mbo8_2.2:mbo8_2, at:=lbf+lbf+lbd;
        mbf_8.2:mb_f, at:=lbf+lbf+lbd;
        mbo9_2.2:mbo9_2, at:=lbf+lbf+lbd+lbf_fr/7;
        mbf_9.2:mb_f, at:=lbf+lbf+lbd+lbf_fr/7;
        mbo10_2.2:mbo10_2, at:=lbf+lbf+lbd+2*lbf_fr/7;
        mbf_10.2:mb_f, at:=lbf+lbf+lbd+2*lbf_fr/7;
        mbo11_2.2:mbo11_2, at:=lbf+lbf+lbd+3*lbf_fr/7;
        mbf_11.2:mb_f, at:=lbf+lbf+lbd+3*lbf_fr/7;
        mbo12_2.2:mbo12_2, at:=lbf+lbf+lbd+4*lbf_fr/7;
        mbf_12.2:mb_f, at:=lbf+lbf+lbd+4*lbf_fr/7;
        mbo13_2.2:mbo13_2, at:=lbf+lbf+lbd+5*lbf_fr/7;
        mbf_13.2:mb_f, at:=lbf+lbf+lbd+5*lbf_fr/7;
        mbo14_2.2:mbo14_2, at:=lbf+lbf+lbd+6*lbf_fr/7;
        mbf_14.2:mb_f, at:=lbf+lbf+lbd+6*lbf_fr/7;
        
        
        //last chunk (focusing)
        mb7.2:mb4, at:=lbf+lbf+lbd+lbf_fr;
        b5.2:multib5, at:=lbf+lbf+lbd+lbf_fr+lbf_n/2;
        mb8.2:mb4, at:=lbf+lbf+lbd+lbf_fr+lbf_n/2;
        L=lbd+lbf+lbf+lbd;
        
        //2nd 14 sbends section
        mr1.2:mr1, at:=L-e_1;
        mb2_1.2:mb_4, at:=L-e_1;
        mr2.2:mr2, at:=L-13*e_1/14;
        mb2_2.2:mb_4, at:=L-13*e_1/14;
        mr3.2:mr3, at:=L-12*e_1/14;
        mb2_3.2:mb_4, at:=L-12*e_1/14;
        mr4.2:mr4, at:=L-11*e_1/14;
        mb2_4.2:mb_4, at:=L-11*e_1/14;
        mr5.2:mr5, at:=L-10*e_1/14;
        mb2_5.2:mb_4, at:=L-10*e_1/14;
        mr6.2:mr6, at:=L-9*e_1/14;
        mb2_6.2:mb_4, at:=L-9*e_1/14;
        mr7.2:mr7, at:=L-8*e_1/14;
        mb2_7.2:mb_4, at:=L-8*e_1/14;
        mr8.2:mr8, at:=L-7*e_1/14;
        mb2_8.2:mb_4, at:=L-7*e_1/14;
        mr9.2:mr9, at:=L-6*e_1/14;
        mb2_9.2:mb_4, at:=L-6*e_1/14;
        mr10.2:mr10, at:=L-5*e_1/14;
        mb2_10.2:mb_4, at:=L-5*e_1/14;
        mr11.2:mr11, at:=L-4*e_1/14;
        mb2_11.2:mb_4, at:=L-4*e_1/14;
        mr12.2:mr12, at:=L-3*e_1/14;
        mb2_12.2:mb_4, at:=L-3*e_1/14;
        mr13.2:mr13, at:=L-2*e_1/14;
        mb2_13.2:mb_4, at:=L-2*e_1/14;
        mr14.2:mr14, at:=L-e_1/14;
        mb2_14.2:mb_4, at:=L-e_1/14;
        mr15.2:mr15, at:=L;
        
        
        qq2a.2:qq2, at:=lbd+lbf+lbf+lbd+0.25+dq;
        
        //ES1, at:=0.25, from=qq2a.2;
        //MS1, at:=-0.25, from=qq2b.2;
        
        //p1:marker, at=lquad/2., from=qq2;
        //p3:marker, at=0.8, from=p1;
        //p4:marker, at=0.8, from=p3;
        //p5:marker, at=-0.8, from=p2;
        //p2:marker, at=lcell2-0.25 -lquad -dq;
        qq2b.2:qq2, at:=lcell2-0.25 -lquad -dq;
        endsequence;
        
        teracell3: sequence, refer=entry, l:=lcell3;
        //1st 14 sbends section
        ml1.3:ml1, at:=0;
        mb1_1.3:mb_1, at:=0;
        ml2.3:ml2, at:=e_1/14;
        mb1_2.3:mb_1, at:=e_1/14;
        ml3.3:ml3, at:=2*e_1/14;
        mb1_3.3:mb_1, at:=2*e_1/14;
        ml4.3:ml4, at:=3*e_1/14;
        mb1_4.3:mb_1, at:=3*e_1/14;
        ml5.3:ml5, at:=4*e_1/14;
        mb1_5.3:mb_1, at:=4*e_1/14;
        ml6.3:ml6, at:=5*e_1/14;
        mb1_6.3:mb_1, at:=5*e_1/14;
        ml7.3:ml7, at:=6*e_1/14;
        mb1_7.3:mb_1, at:=6*e_1/14;
        ml8.3:ml8, at:=7*e_1/14;
        mb1_8.3:mb_1, at:=7*e_1/14;
        ml9.3:ml9, at:=8*e_1/14;
        mb1_9.3:mb_1, at:=8*e_1/14;
        ml10.3:ml10, at:=9*e_1/14;
        mb1_10.3:mb_1, at:=9*e_1/14;
        ml11.3:ml11, at:=10*e_1/14;
        mb1_11.3:mb_1, at:=10*e_1/14;
        ml12.3:ml12, at:=11*e_1/14;
        mb1_12.3:mb_1, at:=11*e_1/14;
        ml13.3:ml13, at:=12*e_1/14;
        mb1_13.3:mb_1, at:=12*e_1/14;
        ml14.3:ml14, at:=13*e_1/14;
        mb1_14.3:mb_1, at:=13*e_1/14;
        
        
        //main body of magnet
        //first proper magnet chunk (focusing)
        mb1.3:mb1, at:=e_1;
        b1.3:multib1, at:=e_1 + lbf_n/2;
        mb2.3:mb1, at:=e_1+lbf_n/2;
        
        //boundary region (F)
        mbo1.3:mbo1, at:=lbf-lbf_fr;
        mbf_1.3:mb_f, at:=lbf-lbf_fr;
        mbo2.3: mbo2, at:=lbf-lbf_fr*6/7;
        mbf_2.3:mb_f, at:=lbf-lbf_fr*6/7;
        mbo3.3: mbo3, at:=lbf-lbf_fr*5/7;
        mbf_3.3:mb_f, at:=lbf-lbf_fr*5/7;
        mbo4.3: mbo4, at:=lbf-lbf_fr*4/7;
        mbf_4.3:mb_f, at:=lbf-lbf_fr*4/7;
        mbo5.3: mbo5, at:=lbf-lbf_fr*3/7;
        mbf_5.3:mb_f, at:=lbf-lbf_fr*3/7;
        mbo6.3: mbo6, at:=lbf-lbf_fr*2/7;
        mbf_6.3:mb_f, at:=lbf-lbf_fr*2/7;
        mbo7.3: mbo7, at:=lbf-lbf_fr/7;
        mbf_7.3:mb_f, at:=lbf-lbf_fr/7;
        
        
        //boundary region (D)
        mbo8.3: mbo8, at:=lbf;
        mbd_1.3:mb_d, at:=lbf;
        mbo9.3: mbo9, at:=lbf+lbf_fr/7;
        mbd_2.3:mb_d, at:=lbf+lbf_fr/7;
        mbo10.3: mbo10, at:=lbf+2*lbf_fr/7;
        mbd_3.3:mb_d, at:=lbf+2*lbf_fr/7;
        mbo11.3: mbo11, at:=lbf+3*lbf_fr/7;
        mbd_4.3:mb_d, at:=lbf+3*lbf_fr/7;
        mbo12.3: mbo12, at:=lbf+4*lbf_fr/7;
        mbd_5.3:mb_d, at:=lbf+4*lbf_fr/7;
        mbo13.3: mbo13, at:=lbf+5*lbf_fr/7;
        mbd_6.3:mb_d, at:=lbf+5*lbf_fr/7;
        mbo14.3: mbo14, at:=lbf+6*lbf_fr/7;
        mbd_7.3:mb_d, at:=lbf+6*lbf_fr/7;
        
        //second magnet chunk (defocusing)
        mb3.3:mb2, at:=lbf+lbf_fr;
        b2.3:multib2, at:=lbf+lbf_fr+lbd_n/2;
        mb4.3:mb2, at:=lbf+lbf_fr+lbd_n/2;
        
        //third magnet chunk (defocusing)
        b3.3:multib3, at:=lbf+lbf_fr+lbd_n;
        mb5.3:mb3, at:=lbf+lbf_fr+lbd_n;
        b4.3:multib4, at:=lbf+lbf_fr+lbd_n+lbd_n/2;
        mb6.3:mb3, at:=lbf+lbf_fr+lbd_n+lbd_n/2;
        
        //boundary region (D)
        mbo1_2.3: mbo1_2, at:=lbf+lbf+lbf-lbf_fr;
        mbd_8.3:mb_d, at:=lbf+lbf+lbf-lbf_fr;
        mbo2_2.3: mbo2_2, at:=lbf+lbf+lbf-lbf_fr*6/7;
        mbd_9.3:mb_d, at:=lbf+lbf+lbf-lbf_fr*6/7;
        mbo3_2.3: mbo3_2, at:=lbf+lbf+lbf-lbf_fr*5/7;
        mbd_10.3:mb_d, at:=lbf+lbf+lbf-lbf_fr*5/7;
        mbo4_2.3: mbo4_2, at:=lbf+lbf+lbf-lbf_fr*4/7;
        mbd_11.3:mb_d, at:=lbf+lbf+lbf-lbf_fr*4/7;
        mbo5_2.3: mbo5_2, at:=lbf+lbf+lbf-lbf_fr*3/7;
        mbd_12.3:mb_d, at:=lbf+lbf+lbf-lbf_fr*3/7;
        mbo6_2.3: mbo6_2, at:=lbf+lbf+lbf-lbf_fr*2/7;
        mbd_13.3:mb_d, at:=lbf+lbf+lbf-lbf_fr*2/7;
        mbo7_2.3: mbo7_2, at:=lbf+lbf+lbf-lbf_fr*1/7;
        mbd_14.3:mb_d, at:=lbf+lbf+lbf-lbf_fr*1/7;
        
        //boundary region (F)
        mbo8_2.3:mbo8_2, at:=lbf+lbf+lbd;
        mbf_8.3:mb_f, at:=lbf+lbf+lbd;
        mbo9_2.3:mbo9_2, at:=lbf+lbf+lbd+lbf_fr/7;
        mbf_9.3:mb_f, at:=lbf+lbf+lbd+lbf_fr/7;
        mbo10_2.3:mbo10_2, at:=lbf+lbf+lbd+2*lbf_fr/7;
        mbf_10.3:mb_f, at:=lbf+lbf+lbd+2*lbf_fr/7;
        mbo11_2.3:mbo11_2, at:=lbf+lbf+lbd+3*lbf_fr/7;
        mbf_11.3:mb_f, at:=lbf+lbf+lbd+3*lbf_fr/7;
        mbo12_2.3:mbo12_2, at:=lbf+lbf+lbd+4*lbf_fr/7;
        mbf_12.3:mb_f, at:=lbf+lbf+lbd+4*lbf_fr/7;
        mbo13_2.3:mbo13_2, at:=lbf+lbf+lbd+5*lbf_fr/7;
        mbf_13.3:mb_f, at:=lbf+lbf+lbd+5*lbf_fr/7;
        mbo14_2.3:mbo14_2, at:=lbf+lbf+lbd+6*lbf_fr/7;
        mbf_14.3:mb_f, at:=lbf+lbf+lbd+6*lbf_fr/7;
        
        
        //last chunk (focusing)
        mb7.3:mb4, at:=lbf+lbf+lbd+lbf_fr;
        b5.3:multib5, at:=lbf+lbf+lbd+lbf_fr+lbf_n/2;
        mb8.3:mb4, at:=lbf+lbf+lbd+lbf_fr+lbf_n/2;
        L=lbd+lbf+lbf+lbd;
        
        
        //2nd 14 sbends section
        mr1.3:mr1, at:=L-e_1;
        mb2_1.3:mb_4, at:=L-e_1;
        mr2.3:mr2, at:=L-13*e_1/14;
        mb2_2.3:mb_4, at:=L-13*e_1/14;
        mr3.3:mr3, at:=L-12*e_1/14;
        mb2_3.3:mb_4, at:=L-12*e_1/14;
        mr4.3:mr4, at:=L-11*e_1/14;
        mb2_4.3:mb_4, at:=L-11*e_1/14;
        mr5.3:mr5, at:=L-10*e_1/14;
        mb2_5.3:mb_4, at:=L-10*e_1/14;
        mr6.3:mr6, at:=L-9*e_1/14;
        mb2_6.3:mb_4, at:=L-9*e_1/14;
        mr7.3:mr7, at:=L-8*e_1/14;
        mb2_7.3:mb_4, at:=L-8*e_1/14;
        mr8.3:mr8, at:=L-7*e_1/14;
        mb2_8.3:mb_4, at:=L-7*e_1/14;
        mr9.3:mr9, at:=L-6*e_1/14;
        mb2_9.3:mb_4, at:=L-6*e_1/14;
        mr10.3:mr10, at:=L-5*e_1/14;
        mb2_10.3:mb_4, at:=L-5*e_1/14;
        mr11.3:mr11, at:=L-4*e_1/14;
        mb2_11.3:mb_4, at:=L-4*e_1/14;
        mr12.3:mr12, at:=L-3*e_1/14;
        mb2_12.3:mb_4, at:=L-3*e_1/14;
        mr13.3:mr13, at:=L-2*e_1/14;
        mb2_13.3:mb_4, at:=L-2*e_1/14;
        mr14.3:mr14, at:=L-e_1/14;
        mb2_14.3:mb_4, at:=L-e_1/14;
        mr15.3:mr15, at:=L;
        
        qq1a.3:qq1, at:=lbd+lbf+lbf+lbd+0.25+dq;
        xs1.3:xs1, at:=lbd+lbf+lbf+lbd+0.25+dq+3*lquad;
        
        
        //p1:marker, at=lcell3-d2*3./4.;
        //p2:marker, at=lcell3-d2/2.;
        //p3:marker, at=lcell3-d2/4.;
        qq1b.3:qq1, at:=lcell3-0.25 -lquad -dq;
        xs2.3:xs2, at:=lcell3-0.25 -lquad -dq+3*lquad;
        
        endsequence;
        
        teracell4: sequence, refer=entry, l:=lcell4;
        //1st 14 sbends section
        ml1.4:ml1, at:=0;
        mb1_1.4:mb_1, at:=0;
        ml2.4:ml2, at:=e_1/14;
        mb1_2.4:mb_1, at:=e_1/14;
        ml3.4:ml3, at:=2*e_1/14;
        mb1_3.4:mb_1, at:=2*e_1/14;
        ml4.4:ml4, at:=3*e_1/14;
        mb1_4.4:mb_1, at:=3*e_1/14;
        ml5.4:ml5, at:=4*e_1/14;
        mb1_5.4:mb_1, at:=4*e_1/14;
        ml6.4:ml6, at:=5*e_1/14;
        mb1_6.4:mb_1, at:=5*e_1/14;
        ml7.4:ml7, at:=6*e_1/14;
        mb1_7.4:mb_1, at:=6*e_1/14;
        ml8.4:ml8, at:=7*e_1/14;
        mb1_8.4:mb_1, at:=7*e_1/14;
        ml9.4:ml9, at:=8*e_1/14;
        mb1_9.4:mb_1, at:=8*e_1/14;
        ml10.4:ml10, at:=9*e_1/14;
        mb1_10.4:mb_1, at:=9*e_1/14;
        ml11.4:ml11, at:=10*e_1/14;
        mb1_11.4:mb_1, at:=10*e_1/14;
        ml12.4:ml12, at:=11*e_1/14;
        mb1_12.4:mb_1, at:=11*e_1/14;
        ml13.4:ml13, at:=12*e_1/14;
        mb1_13.4:mb_1, at:=12*e_1/14;
        ml14.4:ml14, at:=13*e_1/14;
        mb1_14.4:mb_1, at:=13*e_1/14;
        
        
        //main body of magnet
        //first proper magnet chunk (focusing)
        mb1.4:mb1, at:=e_1;
        b1.4:multib1, at:=e_1 + lbf_n/2;
        mb2.4:mb1, at:=e_1+lbf_n/2;
        
        //boundary region (F)
        mbo1.4:mbo1, at:=lbf-lbf_fr;
        mbf_1.4:mb_f, at:=lbf-lbf_fr;
        mbo2.4: mbo2, at:=lbf-lbf_fr*6/7;
        mbf_2.4:mb_f, at:=lbf-lbf_fr*6/7;
        mbo3.4: mbo3, at:=lbf-lbf_fr*5/7;
        mbf_3.4:mb_f, at:=lbf-lbf_fr*5/7;
        mbo4.4: mbo4, at:=lbf-lbf_fr*4/7;
        mbf_4.4:mb_f, at:=lbf-lbf_fr*4/7;
        mbo5.4: mbo5, at:=lbf-lbf_fr*3/7;
        mbf_5.4:mb_f, at:=lbf-lbf_fr*3/7;
        mbo6.4: mbo6, at:=lbf-lbf_fr*2/7;
        mbf_6.4:mb_f, at:=lbf-lbf_fr*2/7;
        mbo7.4: mbo7, at:=lbf-lbf_fr/7;
        mbf_7.4:mb_f, at:=lbf-lbf_fr/7;
        
        
        //boundary region (D)
        mbo8.4: mbo8, at:=lbf;
        mbd_1.4:mb_d, at:=lbf;
        mbo9.4: mbo9, at:=lbf+lbf_fr/7;
        mbd_2.4:mb_d, at:=lbf+lbf_fr/7;
        mbo10.4: mbo10, at:=lbf+2*lbf_fr/7;
        mbd_3.4:mb_d, at:=lbf+2*lbf_fr/7;
        mbo11.4: mbo11, at:=lbf+3*lbf_fr/7;
        mbd_4.4:mb_d, at:=lbf+3*lbf_fr/7;
        mbo12.4: mbo12, at:=lbf+4*lbf_fr/7;
        mbd_5.4:mb_d, at:=lbf+4*lbf_fr/7;
        mbo13.4: mbo13, at:=lbf+5*lbf_fr/7;
        mbd_6.4:mb_d, at:=lbf+5*lbf_fr/7;
        mbo14.4: mbo14, at:=lbf+6*lbf_fr/7;
        mbd_7.4:mb_d, at:=lbf+6*lbf_fr/7;
        
        //second magnet chunk (defocusing)
        mb3.4:mb2, at:=lbf+lbf_fr;
        b2.4:multib2, at:=lbf+lbf_fr+lbd_n/2;
        mb4.4:mb2, at:=lbf+lbf_fr+lbd_n/2;
        
        //third magnet chunk (defocusing)
        b3.4:multib3, at:=lbf+lbf_fr+lbd_n;
        mb5.4:mb3, at:=lbf+lbf_fr+lbd_n;
        b4.4:multib4, at:=lbf+lbf_fr+lbd_n+lbd_n/2;
        mb6.4:mb3, at:=lbf+lbf_fr+lbd_n+lbd_n/2;
        
        //boundary region (D)
        mbo1_2.4: mbo1_2, at:=lbf+lbf+lbf-lbf_fr;
        mbd_8.4:mb_d, at:=lbf+lbf+lbf-lbf_fr;
        mbo2_2.4: mbo2_2, at:=lbf+lbf+lbf-lbf_fr*6/7;
        mbd_9.4:mb_d, at:=lbf+lbf+lbf-lbf_fr*6/7;
        mbo3_2.4: mbo3_2, at:=lbf+lbf+lbf-lbf_fr*5/7;
        mbd_10.4:mb_d, at:=lbf+lbf+lbf-lbf_fr*5/7;
        mbo4_2.4: mbo4_2, at:=lbf+lbf+lbf-lbf_fr*4/7;
        mbd_11.4:mb_d, at:=lbf+lbf+lbf-lbf_fr*4/7;
        mbo5_2.4: mbo5_2, at:=lbf+lbf+lbf-lbf_fr*3/7;
        mbd_12.4:mb_d, at:=lbf+lbf+lbf-lbf_fr*3/7;
        mbo6_2.4: mbo6_2, at:=lbf+lbf+lbf-lbf_fr*2/7;
        mbd_13.4:mb_d, at:=lbf+lbf+lbf-lbf_fr*2/7;
        mbo7_2.4: mbo7_2, at:=lbf+lbf+lbf-lbf_fr*1/7;
        mbd_14.4:mb_d, at:=lbf+lbf+lbf-lbf_fr*1/7;
        
        //boundary region (F)
        mbo8_2.4:mbo8_2, at:=lbf+lbf+lbd;
        mbf_8.4:mb_f, at:=lbf+lbf+lbd;
        mbo9_2.4:mbo9_2, at:=lbf+lbf+lbd+lbf_fr/7;
        mbf_9.4:mb_f, at:=lbf+lbf+lbd+lbf_fr/7;
        mbo10_2.4:mbo10_2, at:=lbf+lbf+lbd+2*lbf_fr/7;
        mbf_10.4:mb_f, at:=lbf+lbf+lbd+2*lbf_fr/7;
        mbo11_2.4:mbo11_2, at:=lbf+lbf+lbd+3*lbf_fr/7;
        mbf_11.4:mb_f, at:=lbf+lbf+lbd+3*lbf_fr/7;
        mbo12_2.4:mbo12_2, at:=lbf+lbf+lbd+4*lbf_fr/7;
        mbf_12.4:mb_f, at:=lbf+lbf+lbd+4*lbf_fr/7;
        mbo13_2.4:mbo13_2, at:=lbf+lbf+lbd+5*lbf_fr/7;
        mbf_13.4:mb_f, at:=lbf+lbf+lbd+5*lbf_fr/7;
        mbo14_2.4:mbo14_2, at:=lbf+lbf+lbd+6*lbf_fr/7;
        mbf_14.4:mb_f, at:=lbf+lbf+lbd+6*lbf_fr/7;
        
        
        //last chunk (focusing)
        mb7.4:mb4, at:=lbf+lbf+lbd+lbf_fr;
        b5.4:multib5, at:=lbf+lbf+lbd+lbf_fr+lbf_n/2;
        mb8.4:mb4, at:=lbf+lbf+lbd+lbf_fr+lbf_n/2;
        
        
        L=lbd+lbf+lbf+lbd;
        
        //2nd 14 sbends section
        mr1.4:mr1, at:=L-e_1;
        mb2_1.4:mb_4, at:=L-e_1;
        mr2.4:mr2, at:=L-13*e_1/14;
        mb2_2.4:mb_4, at:=L-13*e_1/14;
        mr3.4:mr3, at:=L-12*e_1/14;
        mb2_3.4:mb_4, at:=L-12*e_1/14;
        mr4.4:mr4, at:=L-11*e_1/14;
        mb2_4.4:mb_4, at:=L-11*e_1/14;
        mr5.4:mr5, at:=L-10*e_1/14;
        mb2_5.4:mb_4, at:=L-10*e_1/14;
        mr6.4:mr6, at:=L-9*e_1/14;
        mb2_6.4:mb_4, at:=L-9*e_1/14;
        mr7.4:mr7, at:=L-8*e_1/14;
        mb2_7.4:mb_4, at:=L-8*e_1/14;
        mr8.4:mr8, at:=L-7*e_1/14;
        mb2_8.4:mb_4, at:=L-7*e_1/14;
        mr9.4:mr9, at:=L-6*e_1/14;
        mb2_9.4:mb_4, at:=L-6*e_1/14;
        mr10.4:mr10, at:=L-5*e_1/14;
        mb2_10.4:mb_4, at:=L-5*e_1/14;
        mr11.4:mr11, at:=L-4*e_1/14;
        mb2_11.4:mb_4, at:=L-4*e_1/14;
        mr12.4:mr12, at:=L-3*e_1/14;
        mb2_12.4:mb_4, at:=L-3*e_1/14;
        mr13.4:mr13, at:=L-2*e_1/14;
        mb2_13.4:mb_4, at:=L-2*e_1/14;
        mr14.4:mr14, at:=L-e_1/14;
        mb2_14.4:mb_4, at:=L-e_1/14;
        mr15.4:mr15, at:=L;
        
        qq2a.4:qq2, at:=lbd+lbf+lbf+lbd+0.25+dq;
        
        
        //p1:marker, at=lquad/2., from=qq2;
        //p3:marker, at=0.8, from=p1;
        //p4:marker, at=0.8, from=p3;
        //p5:marker, at=-0.8, from=p2;
        //p2:marker, at=lcell4-0.25 -lquad -dq;
        qq2b.4:qq2, at:=lcell4-0.25 -lquad -dq;
        endsequence;
        
        teraring: sequence, refer=entry, l:=circum;
        start_machine: marker, at:=0.;
        teracell1, at:=0.;
        teracell2, at:=lcell1;
        teracell3, at:=lcell1+lcell2;
        teracell4, at:=lcell1+lcell2+lcell3;
        endsequence;
        
        
        !call, file='PR_qq1qq2_ok.elex';
        !call, file='PR_qq1qq2_ok.dbx';
        
        !call, file='PR_qq1qq2_ok.seqx';
        
        MC6 = 11.174670;    ! Stripped Carbon6+ rest mass (GeV)
        T  = 0.430*12;      ! Total kinetic energy; 430 MeV/u (GeV)
        DEGREE:=PI/180.0;   ! For readability
        
        
        eg   := MC6+T;           !total energy
        bg   := eg/MC6;         !gamma
        en   := 3.75e-06;       !normalised emittance of injected beam
        
        
        exnPIMMS = 0.7E-6;
        eynPIMMS = 1E-6;
        
        
        BEAM,   MASS=MC6,       ! Fully stripped carbon beam
                CHARGE=6,
                ENERGY=eg,
                exn=5.0E-6,    ! normalised horizontal emittance [m]
                eyn=3.3E-6,
            npart=2E10,
        ; 
"""
    )
#sense checking the input, the length of the input and the splitting of the input data into half
print(input)
print(len(input))
n_q=int((len(input))/4)
n_half=int(len(input)/2)

sp_1=input[:n_q]
sp_2=input[n_q:n_half]
sp_3=input[n_half:3*n_q]
sp_4=input[3*n_q:]

#print(sp_1)

#print(sp_2)

#print(sp_3)
#print(sp_4)







lostparts = []

#this says, for every value of k2L, k3L we have, call the mad-x file to be used and input that string
#so if we have e.g. 4x4 grid points, we should have 16 strings
for g in range(len(sp_1)):
    #print(string[g])
    madxs[g] = cp.cpymad_start(cpymad_logfile)
    madxs[g].call('Boundaries_split_matched_multiring.madx')
    madxs[g].input(sp_1[g])
    madxs[g].use(sequence='TERARING')
    myPTCParticle = []
    x = []
    test=[]
    #this says, for every grid point, track our input particles (so if we have 4x4 particles,
    # we have 16 total particles) and get its tracking data
    for f in range(len(trackparts)):
        madxs[g].input(trackparts[f])
        myPTCParticle.append(madxs[g].table['track.obs0001.p0001'].dframe())
        x.append(list(myPTCParticle[f]['x']))
        #print('xs1', (madxs[g].elements['xs1'].knl)) #checking it put in the sextupole strengths right
        #print('xs2', (madxs[g].elements['xs2'].knl))

        #if the length of e.g. the x positions of the particle is less than 2048 then it's been lost
        if len(x[f]) < 2048:
            lostparts.append(0)
        #otherwise it survived
        else:
            lostparts.append(1)


print('lost parts',lostparts)
print('lost parts shape',np.shape(lostparts))

#reshape our lost particles into the same shape as our original k2L,k3L data points
foo = np.reshape(lostparts,(len(sp_1),np.size(X)))
#print('reshaped',np.shape(foo))
boo=[]

#count number of nonzero particles (so the ones that survived)
for b in range(len(foo)):
    #print('foo',foo[b])
    boo.append(np.count_nonzero(foo[b]))
    #print('how many survived',boo[b])

print('boo',boo)
print(np.shape(boo))


with open("120624_1sthalf_survived_30_natchrom.txt","w") as external_file:
    print(*boo,sep='\n',file=external_file)
external_file.close()



'''
#survival plot
plt.clf()
plt.scatter(O,S,marker="s",c=boo,s=500)
plt.xlabel('K3L ')
plt.ylabel('K2L ')
plt.colorbar(label='Number survived')
plt.show()
plt.savefig('110624k2lk3l_test.png')
'''
