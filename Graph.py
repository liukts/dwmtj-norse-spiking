import numpy as np
import matplotlib.pyplot as plt
import math

# folder to save results (Copy from main)
date = "3_21_22"
target_dir1 = ("w2_Sweeps/")
target_dir2 = ("w2_sweep_" + date)

#Array of the variable you swept (Copy from main)
var = np.linspace(25e-9,100e-9,6)
legend = []

for ii in range(0, len(var)):
    legend.append(str(math.ceil(var[ii]/1e-9)) + "e-9")

#Graphing Part
accuracy_data = np.load('./outputs/' + target_dir1 + '/' + target_dir2 + '/fin_acc.npy')

plt.plot(accuracy_data.T, label= legend)
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.title(target_dir2)

plt.legend(loc = "lower right")


plt.savefig('./outputs/' + target_dir1 + '/' + target_dir2 + '/' + target_dir2 +'_Accuracy_Graph.png')