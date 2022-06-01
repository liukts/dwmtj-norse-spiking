import numpy as np
import matplotlib.pyplot as plt
import math

w2 = np.linspace(25e-9,100e-9,2)
epochs = np.linspace(1, 20, 20)

num_acc = 5
avg = []

acc1 = np.load('./outputs/' + 'w2_Sweeps/' + 'w2_sweep_4_4_22_#1' + '/fin_acc.npy')
acc2 = np.load('./outputs/' + 'w2_Sweeps/' + 'w2_sweep_4_4_22_#2' + '/fin_acc.npy')
acc3 = np.load('./outputs/' + 'w2_Sweeps/' + 'w2_sweep_4_4_22_#3' + '/fin_acc.npy')
acc4 = np.load('./outputs/' + 'w2_Sweeps/' + 'w2_sweep_4_5_22_#4' + '/fin_acc.npy')
acc5 = np.load('./outputs/' + 'w2_Sweeps/' + 'w2_sweep_4_5_22_#5' + '/fin_acc.npy')

#Averaging Part
for ii in range(0,2):
    for jj in range (0, 20):
        avg.append((acc1[ii][jj] + acc2[ii][jj] + acc3[ii][jj] + acc4[ii][jj] + acc5[ii][jj])/num_acc)

avg = np.reshape(avg, (len(w2), 20))
std1 = np.std(avg[0])
std2 = np.std(avg[1])

#Graphing Part
legend = []
for ii in range(0, len(w2)):
    legend.append(str(math.ceil((w2[ii])/1e-9)) + "e-9")

plt.plot(epochs, avg[0])
plt.plot(epochs, avg[1])

plt.fill_between(epochs, avg[0]-std1, avg[0]+std1, alpha = 0.2)
plt.fill_between(epochs, avg[1]-std2, avg[1]+std2, alpha = 0.2)

plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.title('w2_Average')

plt.legend(legend, loc = "lower right")

plt.savefig('./outputs/' + 'w2_Sweeps/' + 'w2_Average_Graph.png')