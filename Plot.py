import pickle,sys,warnings
import numpy as np
import matplotlib.pylab as plt
warnings.filterwarnings("ignore")
def myprint(string,clear=False):
    if clear:
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K") 
    print(string)

def smooth(array,window=10):
    return np.nanmean(np.pad(array,(0,window-len(array)%window),'constant',constant_values=np.NaN).reshape((-1,window)),axis=1)
'''
def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

def smooth(x,window_len=11,window='hanning'):
    #from Serena Sligh
    if window_len<3:
        return x
    s=np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')
    y=np.convolve(w/w.sum(),s,mode='valid')
    return y
'''

data = pickle.load(open('Data/BurstinessData.pickle','rb'))
masses = pickle.load(open('Data/Marvel_DCJL.Masses.pickle','rb'))
tform = pickle.load(open('Data/Marvel.Tform.pickle','rb'))

total = 0
for sim in ['cptmarvel', 'elektra', 'storm', 'rogue']:
    for hnum in data[sim]:
        total+=1

avg_b,med_b,avg_ab,med_ab,mstar,mvir = [[],[],[],[],[],[]]

print('Plotting Profiles: 0.00%')
done = 0
for sim in ['cptmarvel', 'elektra', 'storm', 'rogue']:
    for hnum in data[sim]:
        halo = data[sim][hnum]
        halo['Burstiness']['50 Data'] = np.nan_to_num(halo['Burstiness']['50 Data'],nan=-1)

        #Smooth the Burstiness arrays
        sm_burst = smooth(halo['Burstiness']['50 Data'],10) 
        sm_time = smooth(halo['Burstiness']['50 Time'],10)

        #Determine active burstiness window
        active = np.where(sm_time<max(tform[sim][hnum]['tform']))[0]
        sm_act = sm_burst[active]
        sm_atime = sm_time[active]


        #Plot Smoothed Arrays
        f,ax = plt.subplots(1,1,figsize=(10,6))
        ax.set_xlim([0,14])
        snr = np.mean(np.reshape(halo['SNR'],(-1,138)),axis=1)
        bins = np.mean(np.reshape(halo['Bins'][:-1],(-1,138)),axis=1)
        ax.bar(bins,snr,width=bins[1]-bins[0],color='0.75')
        ax2 = ax.twinx()
        ax2.set_ylim([-1,1])
        #ax2.plot(smooth(halo['Burstiness']['50 Time'],window=200),smooth(halo['Burstiness']['50 Data'],window=200),c='crimson',linewidth=3)
        #ax2.plot(halo['Burstiness']['50 Time'],halo['Burstiness']['50 Data'],c='crimson',linewidth=3)
        ax2.plot(sm_time,sm_burst,c='crimson',linewidth=3)
        #ax2.plot(halo['Burstiness']['50 Time'][np.arange(0,len(halo['Burstiness']['50 Time']),100)],halo['Burstiness']['50 Data'][np.arange(0,len(halo['Burstiness']['50 Time']),sm)],c='crimson',linewidth=3)
        ax.tick_params(labelsize=15)
        ax.set_xlabel('Time [Gyr]',fontsize=20)
        ax.set_ylabel(r'Supernova Rate [Myr$^{-1}$]',fontsize=20)
        ax2.set_ylabel(r'Burstiness',fontsize=20)
        ax2.tick_params(labelsize=15)
        ax2.set_yticks([-1,-.5,0,.5,1])
        ax2.yaxis.set_label_position("right")
        ax2.yaxis.tick_right()
        ax.set_title(f'{sim} {hnum}',fontsize=25)
        f.savefig(f'Plots/Profiles/{sim}{hnum}.png',bbox_inches='tight',pad_inches=.1)
        plt.close()
        done+=1
        myprint(f'Plotting Profiles: {round(done/total*100,2)}%',clear=True)

        #Add Halo's avg burstiness and mass data
        avg_b.append(np.nanmean(sm_burst))
        med_b.append(np.nanmedian(sm_burst))
        avg_ab.append(np.nanmean(sm_act))
        med_ab.append(np.nanmedian(sm_act))
        mstar.append(masses[sim][hnum]['Mstar'])
        mvir.append(masses[sim][hnum]['Mvir'])

print('Making Master Plots...')
f,ax = plt.subplots(1,1,figsize=(6,6))
ax.scatter(mstar,avg_b,c='k')
ax.set_ylim([-1,1])
#ax.set_xlim([1,1])
ax.semilogx()
ax.set_xlabel(r'Log[M$_*]$',fontsize=15)
ax.set_ylabel('Mean Burstiness',fontsize=15)
f.savefig('Plots/MeanBurstinessVsStellarMass.png',bbox_inches='tight',pad_inches=.1)

f,ax = plt.subplots(1,1,figsize=(6,6))
ax.scatter(mstar,med_b,c='k')
ax.set_ylim([-1,1])
#ax.set_xlim([1,1])
ax.semilogx()
ax.set_xlabel(r'Log[M$_*]$',fontsize=15)
ax.set_ylabel('Median Burstiness',fontsize=15)
f.savefig('Plots/MedianBurstinessVsStellarMass.png',bbox_inches='tight',pad_inches=.1)

f,ax = plt.subplots(1,1,figsize=(6,6))
ax.scatter(mvir,avg_b,c='k')
ax.set_ylim([-1,1])
#ax.set_xlim([1,1])
ax.semilogx()
ax.set_xlabel(r'Log[M$_{vir}]$',fontsize=15)
ax.set_ylabel('Mean Burstiness',fontsize=15)
f.savefig('Plots/MeanBurstinessVsVirialMass.png',bbox_inches='tight',pad_inches=.1)

f,ax = plt.subplots(1,1,figsize=(6,6))
ax.scatter(mvir,med_b,c='k')
ax.set_ylim([-1,1])
#ax.set_xlim([1,1])
ax.semilogx()
ax.set_xlabel(r'Log[M$_{vir}]$',fontsize=15)
ax.set_ylabel('Median Burstiness',fontsize=15)
f.savefig('Plots/MedianBurstinessVsVirialMass.png',bbox_inches='tight',pad_inches=.1)

#Active
f,ax = plt.subplots(1,1,figsize=(6,6))
ax.scatter(mstar,avg_ab,c='k')
ax.set_ylim([-1,1])
#ax.set_xlim([1,1])
ax.semilogx()
ax.set_xlabel(r'Log[M$_*]$',fontsize=15)
ax.set_ylabel('Mean Active Burstiness',fontsize=15)
f.savefig('Plots/MeanActiveBurstinessVsStellarMass.png',bbox_inches='tight',pad_inches=.1)

f,ax = plt.subplots(1,1,figsize=(6,6))
ax.scatter(mstar,med_ab,c='k')
ax.set_ylim([-1,1])
#ax.set_xlim([1,1])
ax.semilogx()
ax.set_xlabel(r'Log[M$_*]$',fontsize=15)
ax.set_ylabel('Median Active Burstiness',fontsize=15)
f.savefig('Plots/MedianActiveBurstinessVsStellarMass.png',bbox_inches='tight',pad_inches=.1)

f,ax = plt.subplots(1,1,figsize=(6,6))
ax.scatter(mvir,avg_ab,c='k')
ax.set_ylim([-1,1])
#ax.set_xlim([1,1])
ax.semilogx()
ax.set_xlabel(r'Log[M$_{vir}]$',fontsize=15)
ax.set_ylabel('Mean Active Burstiness',fontsize=15)
f.savefig('Plots/MeanActiveBurstinessVsVirialMass.png',bbox_inches='tight',pad_inches=.1)

f,ax = plt.subplots(1,1,figsize=(6,6))
ax.scatter(mvir,med_ab,c='k')
ax.set_ylim([-1,1])
#ax.set_xlim([1,1])
ax.semilogx()
ax.set_xlabel(r'Log[M$_{vir}]$',fontsize=15)
ax.set_ylabel('Median ActiveBurstiness',fontsize=15)
f.savefig('Plots/MedianActiveBurstinessVsVirialMass.png',bbox_inches='tight',pad_inches=.1)

myprint('Done',clear=True)