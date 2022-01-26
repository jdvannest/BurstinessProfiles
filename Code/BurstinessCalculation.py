import argparse,pickle,pynbody,pymp,sncalc,sys
import numpy as np
def myprint(string,clear=False):
    if clear:
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K") 
    print(string)
def BurstinessCalculation(snr,bins,binning=50):
    """ Takes SNR and Bins from sncalc.sntiming.expbins and 
    returns the Burstiness Profile for a given binning 
    binning should be given in Myr """

    snr_mean = np.empty(len(snr)-binning)
    snr_std = np.empty(len(snr)-binning)
    snr_time = np.empty(len(snr)-binning)
    snr_mean[:] = np.NaN
    snr_std[:] = np.NaN
    snr_time[:] = np.NaN

    j = 0
    while j<len(snr_mean):
        snr_mean[j] = np.mean(snr[0+j:binning+j])
        snr_std[j] = np.std(snr[0+j:binning+j])
        snr_time[j] = np.mean(bins[0+j:binning+1+j])
        j+=1

    burstiness = (snr_std/snr_mean-1)/(snr_std/snr_mean+1)
    return burstiness,snr_time

parser = argparse.ArgumentParser()
parser.add_argument("-s","--simulation",
                    choices=['cptmarvel','elektra','storm','rogue','h148','h229','h242','h329'])
parser.add_argument("-n","--numproc",required=True,type=int)
args = parser.parse_args()

#Load in simulation info from config files
Sims = pickle.load(open('SimulationInfo.pickle','rb'))

#Load in datafile
try:
    Datafile = pickle.load(open('../BurstinessData.pickle','rb'))
    print('Datafile Loaded.')
except:
    print('No Datafile found, writing new one...')
    Datafile = {}
    for sim in Sims:
        Datafile[sim] = {}

#Load in simulation
print(f'Loading {args.simulation}...')
s = pynbody.load(Sims[args.simulation]['path'])
s.physical_units()
h = s.halos()
myprint(f'{args.simulation} loaded.',clear=True)

#Begin parallelized analysis
print(f'\tAnalyzing {len(Sims[args.simulation]["halos"])} halos: 0.00%')
SimData = pymp.shared.dict()
prog=pymp.shared.array((1,),dtype=int)
with pymp.Parallel(args.numproc) as pl:
    for i in pl.xrange(len(Sims[args.simulation]['halos'])):
        halonum = Sims[args.simulation]['halos'][i]
        current={}
        halo = h[halonum]

        snr,bins = sncalc.sntiming.expbins(halo,tmax=13.8e9)
        current['SNR'] = snr
        current['Bins'] = bins
        current['Burstiness'] = {}
        for binning in [10,50,100,500,1000,3000]:
            b,t = BurstinessCalculation(snr,bins,binning)
            current['Burstiness'][str(binning)+' Data'] = b
            current['Burstiness'][str(binning)+' Time'] = t

        myprint(f'\tAnalyzing {len(Sims[args.simulation]["halos"])} halos: '+
                f'{round(float(prog[0]+1)/float(len(Sims[args.simulation]["halos"]))*100,2)}%',clear=True)
        SimData[str(halonum)] = current
        prog[0]+=1
        del current

#Copy data over from shared dictionary to Datafile
for halo in Sims[args.simulation]['halos']:
    Datafile[args.simulation][halo] = SimData[halo]

#Write out updated Datafile
out = open('../BurstinessData.pickle','wb')
pickle.dump(Datafile,out)
out.close()
print('Datafile updated.')