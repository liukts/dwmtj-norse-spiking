import numpy as np
import matplotlib.pyplot as plt
import math


# folder to save results
date = "06_13_22"
target_dir1 = "I_Sweeps/"
target_dir2 = ("I_sweep_" + date)
target_dir = (target_dir1 + target_dir2)

fin_acc = np.load('./outputs/' + 'I_Sweeps/' + 'I_sweep_06_13_22' + '/fin_acc.npy')

I = np.linspace(60e-6, 120e-6, 7) #7
EPOCHS = 5         # number of iterations
SEED = 2    


#Multiple Seed Graphing
epochs = np.linspace(0, EPOCHS-1, EPOCHS)

legend = []
for ii in range(0, len(I)):
    legend.append(str(math.floor((I[ii])/1e-6)) + "e-6")
avg = []
sum = 0

#Averaging Part
for ii in range(len(I)):
    for jj in range (0, EPOCHS):
        sum = 0
        for kk in range(0, SEED):
            sum += fin_acc[kk][ii][jj]
        avg.append(sum/SEED)
avg = np.reshape(avg, (len(I), EPOCHS))

#Graphing Part
for f in range(0, len(I)):
    plt.plot(avg[f].T)
    
for f in range(0, len(I)):  
    plt.fill_between(epochs, avg[f]-np.std(avg[f]), avg[f]+np.std(avg[f]), alpha = 0.2)

plt.ylabel('Accuracy (%)')
plt.xlabel('Epoch')
plt.title('Current_Average')
plt.legend(legend, loc = "lower right")
plt.savefig('./outputs/' + target_dir + '/' + target_dir2 +'_Accuracy_Graph_2.png')
