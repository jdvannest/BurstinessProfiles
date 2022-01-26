# Routines from changa, using Raiteri + 1996 fits to Padova SSPs
# Written by Elaad Applebaum, July 2017

import numpy as np

def CoefInit(metals):
    """ Determine coefficients to fit, based on metallicity

        metals - scalar value or array of values
    """

    Z = np.array(metals)
    Z[Z>3.e-2] = 3.e-2
    Z[Z<7.e-5] = 7.e-5
    #Z = np.minimum(metals, 3.e-2)
    #Z = np.maximum(metals, 7.e-5)
    logZ = np.log10(Z)
    a0 = 10.13 + 0.07547*logZ - 0.008084*logZ*logZ;
    a1 = -4.424 - 0.7939*logZ - 0.1187*logZ*logZ;
    a2 = 1.262 + 0.3385*logZ + 0.05417*logZ*logZ;

    return (a0, a1, a2)

def lifetime(mass, metals):
    """ Determine lifetime of star of a given mass and metallicity

        mass - scalar value or array of values
        metals - scalar value or array of values

    """

    if hasattr(mass, '__len__') and hasattr(metals, '__len__'):
        assert len(mass)==len(metals)
    
    logStarMass = np.log10(mass)
    a0, a1, a2 = CoefInit(metals)
    logLtime = a0 + a1*logStarMass + a2*logStarMass*logStarMass
    Ltime = 10**logLtime

    return Ltime

def starmass(dStarLtime, dMetals):
    """ Given a time and metallicity, returns the mass of the star with that lifetime

        dStarLtime - the time (scalar value or array of values) 
        dMetals - the metallicity (scalar value or array of values)

        If dStarLtime is a scalar, dMetals can be either a scalar or an array, where all
        stars of differing metallicities die at the same time. If dStarLtime is an array,
        dMetals must be an array of the same length
    """

    if hasattr(dMetals, '__len__') and hasattr(dStarLtime, '__len__'):
        assert len(dMetals)==len(dStarLtime)
        dStarLtime = np.array(dStarLtime)
        dMetals = np.array(dMetals)
        StarMass = np.zeros(len(dStarLtime))
        StarMass[dStarLtime<=0.0] = np.log10(1000)
    elif hasattr(dMetals, '__len__') and not hasattr(dStarLtime, '__len__'):
        dMetals = np.array(dMetals)
        if dStarLtime<=0.0:
            return np.array([1000]*len(dMetals))
        dStarLtime = np.array([dStarLtime])
        StarMass = np.zeros(len(dMetals))
    elif hasattr(dStarLtime, '__len__') and not hasattr(dMetals, '__len__'):
        temp = np.zeros(len(dStarLtime))
        dMetals = temp + dMetals
        dStarLtime = np.array(dStarLtime)
        StarMass = np.zeros(len(dMetals))
    else:
        StarMass = np.array([0.])
        dStarLtime = np.array([dStarLtime])
        dMetals = np.array([dMetals])
    
    dStarLtime[dStarLtime<=0]=np.log10(1000)

    a0, a1, a2 = CoefInit(dMetals)
    c=a0 - np.log10(dStarLtime)
    b = a1
    a = a2
    d=b*b-4*a*c
    StarMass[d<0.0] = np.log10(1000)
    StarMass[StarMass!=np.log10(1000)] = (-b[StarMass!=np.log10(1000)] -np.sqrt(d[StarMass!=np.log10(1000)]))/(2*a[StarMass!=np.log10(1000)])
    StarMass = 10**StarMass
    return StarMass

