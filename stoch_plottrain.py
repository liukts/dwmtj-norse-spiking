import numpy as np
import matplotlib.pyplot as plt

plt.style.use(['science','nature'])

basedir = [
            '230103_s05_fashion_noise0.0_seqnet0200_lif_ep20_lr0.001_T80_alpha100_beta1_pf1e3_bn_initxunif',
            '240610_stochmwleak_s5_fashion_noise0.0_seqnet500_neurmw_ep10_lr0.001_T200_alpha100_beta1_pf1000.0_bn_initxunif',
            '240610_leak_s5_fashion_noise0.0_seqnet500_neurmw_ep10_lr0.001_T400_alpha100_beta1_pf1000.0_bn_initxunif',
            ]
# basedir = [
#             '0131_fashion_ann',
#             ]
lstyle = ['.-','-','-',':',':']
col = ['black','tab:blue','tab:orange','tab:blue','tab:orange']
figacc,axacc = plt.subplots(1,1,figsize=(2.0,1.5))
fignorm,axnorm = plt.subplots(1,1,figsize=(1.8,1.4))
for id,i in enumerate(basedir):
    print(i)
    accs = np.load('./outputs/' + i + '/accuracies.npy')[:10,:]
    epochs = np.linspace(0,9,10)+0.5
    # noise_inj = np.load('./outputs/' + i + '/noise_std_range.npy')
    axacc.plot(epochs,np.mean(accs,axis=1),lstyle[id],color=col[id])
    # axacc.plot(epochs,accs,lstyle[id],color=col[id])
    if id < 3:
        axacc.fill_between(epochs,np.mean(accs,axis=1)-np.std(accs,axis=1),np.mean(accs,axis=1)+np.std(accs,axis=1),alpha=0.3,facecolor=col[id])
    # axnorm.plot(np.mean(accs,axis=1)/np.mean(accs,axis=1)[0],'^-')
# axacc.set_ylim([76,88])
# axacc.set_yticks([84,86,88,90])
axacc.set_xticks([0,2,4,6,8,10])
figacc.savefig('accs_lif.svg')
# fignorm.savefig('accs_normed.svg')