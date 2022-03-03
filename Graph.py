import numpy as np
import matplotlib.pyplot as plt

# folder to save results (Copy from main)
date = "3_3_22_2ndEpoch15_42_44"
target_dir = ("T_sweep_" + date)

#Array of the variable you swept (Copy from main)
var = np.linspace(42,44,2)

#Graphing Part
accuracy_data = np.load('./outputs/' + target_dir + '/fin_acc.npy')

plt.plot(accuracy_data.T)
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.title(target_dir)

plt.legend(var, loc = "lower right")


plt.savefig('./outputs/' + target_dir + '/' + target_dir +'_Accuracy_Graph.png')