import numpy as np
import matplotlib.pyplot as plt
import math

# folder to save results
date = "3_25_22"
target_dir1 = ("alpha_Sweeps/")
target_dir2 = ("alpha_sweep_" + date)
target_dir = (target_dir1 + target_dir2)

alpha = np.linspace(20,100,5) #Original Sweep: (20,100,5)

#Graphing Part
accuracy_data = np.load('./outputs/' + target_dir + '/fin_acc.npy')

plt.plot(accuracy_data.T)
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.title(target_dir2)

plt.legend(alpha, loc = "lower right")

plt.savefig('./outputs/' + target_dir + '/' + target_dir2 +'_Accuracy_Graph.png')