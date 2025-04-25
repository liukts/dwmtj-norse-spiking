import numpy as np
import matplotlib.pyplot as plt

plt.style.use(['science','nature'])

# basedir = [
#             '230103_s05_fashion_noise0.0_seqnet0200_lif_ep20_lr0.001_T80_alpha100_beta1_pf1e3_bn_initxunif',
#             '230103_s05_fashion_noise0.0_seqnet0200_neur_ep20_lr0.001_T80_alpha100_beta1_pf1e3_bn_initxunif',
#             '230103_s05_fashion_noise0.0_seqnet0500_neur_ep20_lr0.001_T80_alpha100_beta1_pf1e3_bn_initxunif',
#             ]
basedir_def = [
            '240401_fashion_default_1','240401_fashion_default_2','240401_fashion_default_3','240401_fashion_default_4','240401_fashion_default_5',
            ]
basedir_dwmtj = [
            '240430_fashion_dwmtj_1','240430_fashion_dwmtj_2','240430_fashion_dwmtj_3','240430_fashion_dwmtj_4','240430_fashion_dwmtj_5','240430_fashion_dwmtj_6',
            ]
basedir_dwmtjnoise = [
            '240430_fashion_dwmtjnoise_1','240430_fashion_dwmtjnoise_2','240430_fashion_dwmtjnoise_3','240430_fashion_dwmtjnoise_4','240430_fashion_dwmtjnoise_5','240430_fashion_dwmtjnoise_6',
            ]
lstyle = ['.-','-','-',':',':']
col = ['black','tab:blue','tab:orange','tab:blue','tab:orange']
figacc,axacc = plt.subplots(1,1,figsize=(1.5,1.15))
fignorm,axnorm = plt.subplots(1,1,figsize=(1.8,1.4))

accs_def = []
for id,i in enumerate(basedir_def):
    print(i)
    accs_def.append(np.load('./outputs/' + i + '/accuracies.npy'))

epochs = np.linspace(0,np.shape(accs_def[0])[0]-1,np.shape(accs_def[0])[0])+1
accs_def = np.concatenate(accs_def).reshape((len(accs_def),-1)).T
axacc.plot(epochs,np.mean(accs_def,axis=1),'k--')
axacc.fill_between(epochs,np.mean(accs_def,axis=1)-np.std(accs_def,axis=1),np.mean(accs_def,axis=1)+np.std(accs_def,axis=1),color='black',alpha=0.3,linewidth=0.0)
np.savetxt('accs_def.csv',accs_def)

# accs_dwmtj = []
# for id,i in enumerate(basedir_dwmtj):
#     print(i)
#     accs_dwmtj.append(np.load('./outputs/' + i + '/accuracies.npy'))

# accs_dwmtj = np.concatenate(accs_dwmtj).reshape((len(accs_dwmtj),-1)).T
# axacc.plot(epochs,np.mean(accs_dwmtj,axis=1),'s-')
# axacc.fill_between(epochs,np.mean(accs_dwmtj,axis=1)-np.std(accs_dwmtj,axis=1),np.mean(accs_dwmtj,axis=1)+np.std(accs_dwmtj,axis=1),alpha=0.3,linewidth=0.0,color='tab:blue')
# np.savetxt('accs_dwmtj.csv',accs_dwmtj)

# accs_dwmtjnoise = []
# for id,i in enumerate(basedir_dwmtjnoise):
#     print(i)
#     accs_dwmtjnoise.append(np.load('./outputs/' + i + '/accuracies.npy'))

# accs_dwmtjnoise = np.concatenate(accs_dwmtjnoise).reshape((len(accs_dwmtjnoise),-1)).T
# axacc.plot(epochs,np.mean(accs_dwmtjnoise,axis=1),'^-',color='tab:orange')
# axacc.fill_between(epochs,np.mean(accs_dwmtjnoise,axis=1)-np.std(accs_dwmtjnoise,axis=1),np.mean(accs_dwmtjnoise,axis=1)+np.std(accs_dwmtjnoise,axis=1),alpha=0.3,linewidth=0.0,color='tab:orange')
# np.savetxt('accs_dwmtjnoise.csv',accs_dwmtjnoise)

accs_if = np.array([71.2,72.0,74.1,75.5,77.2,77.9,78.2,78.3,78.6,79.1])
fill_if = np.array([2.4,2.2,2.5,2.1,1.5,1.6,1.0,1.05,1.1,0.9])
axacc.plot(epochs,accs_if,'--',color='tab:purple')
axacc.fill_between(epochs,accs_if-fill_if,accs_if+fill_if,alpha=0.3,linewidth=0.0,color='tab:purple')
print(np.mean(fill_if))
axacc.set_xlim([-0.5,11])
axacc.set_xticks([0,2,4,6,8,10])
figacc.savefig('autoreset_accs.svg')
# fignorm.savefig('accs_normed.svg')