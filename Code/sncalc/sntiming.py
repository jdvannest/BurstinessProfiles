import numpy as np
import pynbody as pb
from . import starlifetime as slt
from . import imf

def stochexptime(sim, tstart=0, sniimax=40.0):
    """Gives the time of supernova explosion (with stochastic IMF) *relative to t=0 of sim*
    
    If start is 0, assumes supernova times are relative to t=0 of simulation
    If tstart is None, then supernova times are returned relative to the time of the first explosion
    If tstart [yr] > 0, gives the time of supernova explosion relative to tstart, in yr

    sniimax: the maximum mass stars explode as supernova (above sniimax, assume
        they collapse as black holes)
    """

    stochtimes = []
    for i in range(len(sim.s)):
        sns = slt.lifetime(sim.s['hmstars'][i][(sim.s['hmstars'][i]>0) & (sim.s['hmstars'][i]<sniimax)], sim.s['metals'][i])
        # above is time relative to starform time
        sns += sim.s['tform'].in_units('yr')[i] # making relative to t=0
        if tstart is None and len(sns)>0:
            sns -= min(sns)
        elif tstart>0:
            sns -= tstart
            
        stochtimes += list(sns)

    return np.array(stochtimes)

def stochexpbins(sim, dt=1.e6, tstart=0, tmax=1.e9): 
    """Gives the binned time of supernova explosion (with stochastic IMF) *relative to t=0 of sim*

    If tstart>0, shifts the initial time (e.g., the t=0 time) by that much, in years

    returns bins in Gyr and number of SN (divide by bin size to make into rate)
    
    *** for example ***
        tstart=0.5e9, tmax=2.e9, dt=1.e6
        
        This will return the supernova rate between 0.5 Gyr and 2.5 Gyr relative
        to the beginning of the simulation
        
        However, the bins will be returned as 0 to 2 Gyr in 1 Myr increments
    """
    bins = np.arange(0, tmax+dt, dt)
    stochtimes = stochexptime(sim, tstart=tstart)
    vals = []
    for i in range(len(bins)-1):
        vals.append(len(stochtimes[(stochtimes>=bins[i]) & (stochtimes<bins[i+1])]))

    vals, bins =  np.array(vals, dtype=float), np.array(bins)
    return vals, bins/1.e9

def expbins(simbefore, dt=1.e6, tstart=0, tmax=1.e9, sniimax=40.0):
    """Gives the number of supernova explosions in each bin for non-stochastic IMF sim

    If tstart>0, shifts the initial time (e.g., the t=0 time) by that much, in years
    
    tmax - the maximum time to consider (relative to tstart)
    
    returns bins in Gyr and number of SN (divide by bin size to make into rate)

    *** for example ***
        tstart=0.5e9, tmax=2.e9, dt=1.e6
        
        This will return the supernova rate between 0.5 Gyr and 2.5 Gyr relative
        to the beginning of the simulation
        
        However, the bins will be returned as 0 to 2 Gyr in 1 Myr increments
    """
    bins=np.arange(0, tmax+dt, dt)
    alltimes = np.array([])
    allnums = np.array([])
    notbhs = pb.filt.HighPass('tform', '0 Gyr')
    sim = simbefore.s[notbhs]
    ts = np.arange(0, 50.e6+dt, dt)
    for t in np.arange(0, 50.e6+dt, dt):
        mmax = slt.starmass(t, sim['metals'])
        mmax[mmax>sniimax] = sniimax
        mmin = slt.starmass(t+dt, sim['metals'])
        mmin[mmin<8.] = 8.
        nums = (imf.CumNumber(mmin) - imf.CumNumber(mmax))*sim['massform'].in_units('Msol')
        nums[mmax<8.] = 0.
        nums[mmin>sniimax] = 0.
        times = np.array(sim['tform'].in_units('yr')) + t + dt
        alltimes = np.concatenate((alltimes, times))
        allnums = np.concatenate((allnums, nums))
        
    #for i in range(len(sim)):
    #    for t in np.arange(0, 50.e6, dt):
    #        mmax = slt.starmass(t, sim['metals'][i])
    #        if mmax<8:
    #            break
    #        mmin = slt.starmass(t+1.e6, sim['metals'][i])
    #        if mmin>40:
    #            continue
    #        num = (imf.CumNumber(mmin) - imf.CumNumber(mmax))*sim['massform'].in_units('Msol')[i]
    #        time = sim['tform'].in_units('yr')[i] + t
    #        alltimes.append(time)
    #        allnums.append(num)

    alltimes = np.array(alltimes)
    allnums = np.array(allnums)

    if tstart>0:
        alltimes -= tstart

    vals = []
    for i in range(len(bins)-1):
        vals.append(np.sum(allnums[(alltimes>=bins[i]) & (alltimes<bins[i+1])]))
    
    vals, bins =  np.array(vals), np.array(bins)
    return vals, bins/1.e9
    
