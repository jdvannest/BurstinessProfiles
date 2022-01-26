import numpy as np

def CumNumber(mass):
    """ Returns the number of stars *above* a given mass, assuming a
        Kroupa01 IMF, .08 < M < 100 Msol, with a total *mass* of 1 Msol
        
        mass - the mass above which you want the total number of stars
    """
    if hasattr(mass, '__len__'):
        mass = np.array(mass)
    else:
        mass = np.array([mass])
    dCumN = np.zeros(len(mass))
    dCumN[mass>0.5] = 0.22038/(-1.3)*(100.**-1.3 - mass[mass>0.5]**-1.3)
    dCumN[mass<=0.5] = 0.22038/(-1.3)*(100.**-1.3 - 0.5**-1.3)
    dCumN[(mass>0.08) & (mass<=0.05)] += 0.22038*2.0/(-0.3)*(0.5**-0.3 - mass[(mass>0.08) & (mass<=0.05)]**-0.3) 
    dCumN[(mass<=0.08)] += 0.22038*2.0/(-0.3)*(0.5**-0.3 - mass[mass<=0.08]**-0.3) 
    
    #if mass > 100.:
    #    return 0
    #if mass > 0.5:
    #    dCumN = 0.22038/(-1.3)*(100.**-1.3 - mass**-1.3)
    #    return dCumN
    #else:
    #    dCumN = 0.22038/(-1.3)*(100.**-1.3 - mass**-1.3)

    #if mass > 0.08:
    #    dCumN += 0.22038*2.0/(-0.3)*(0.5**-0.3 - mass**-0.3)
    #else:
    #    dCumN += 0.22038*2.0/(-0.3)*(0.5**-0.3 - 0.08**-0.3)
                
    return dCumN
