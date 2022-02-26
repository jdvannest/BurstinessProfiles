import pickle,sys
import numpy as np
import matplotlib.pylab as plt
def myprint(string,clear=False):
    if clear:
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K") 
    print(string)

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth
'''
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

data = pickle.load(open('BurstinessData.pickle','rb'))

total = 0
for sim in ['cptmarvel', 'elektra', 'storm', 'rogue']:
    for hnum in data[sim]:
        total+=1

print('Plotting: 0.00%')
done = 0
sm = 100 #smoothing window
for sim in ['cptmarvel', 'elektra', 'storm', 'rogue']:
    for hnum in data[sim]:
        halo = data[sim][hnum]
        f,ax = plt.subplots(1,1,figsize=(10,6))
        ax.set_xlim([0,14])
        snr = np.mean(np.reshape(halo['SNR'],(-1,138)),axis=1)
        bins = np.mean(np.reshape(halo['Bins'][:-1],(-1,138)),axis=1)
        ax.bar(bins,snr,width=bins[1]-bins[0],color='0.75')
        ax2 = ax.twinx()
        ax2.set_ylim([-1,1])
        ax2.plot(halo['Burstiness']['50 Time'],halo['Burstiness']['50 Data'],c='crimson',linewidth=3)
        #ax2.plot(halo['Burstiness']['50 Time'],smooth(halo['Burstiness']['50 Data'],500),c='crimson',linewidth=3)
        #ax2.plot(halo['Burstiness']['50 Time'][np.arange(0,len(halo['Burstiness']['50 Time']),sm)],halo['Burstiness']['50 Data'][np.arange(0,len(halo['Burstiness']['50 Time']),sm)],c='crimson',linewidth=3)

        ax.tick_params(labelsize=15)
        ax.set_xlabel('Time [Gyr]',fontsize=20)
        ax.set_ylabel(r'Supernova Rate [Myr$^{-1}$]',fontsize=20)
        ax2.set_ylabel(r'Burstiness',fontsize=20)
        ax2.tick_params(labelsize=15)
        ax2.set_yticks([-1,-.5,0,.5,1])
        ax2.yaxis.set_label_position("right")
        ax2.yaxis.tick_right()
        ax.set_title(f'{sim} {hnum}',fontsize=25)
        f.savefig(f'Plots/{sim}{hnum}.png',bbox_inches='tight',pad_inches=.1)
        plt.close()
        done+=1
        myprint(f'Plotting: {round(done/total*100,2)}%',clear=True)