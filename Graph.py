import numpy as np
import matplotlib.pyplot as plt

# folder to save results
date = "2_3_22_Epoch15"
target_dir = ("T_sweep_" + date)

#Array of the variable you swept
var = np.linspace(36,45,10)

#Graphing Part
accuracy_data = np.load('./outputs/' + target_dir + '/fin_acc.npy')

plt.plot(accuracy_data.T)
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.title(target_dir)

plt.legend(var, loc = "lower right")


plt.savefig('./outputs/' + target_dir + '/' + target_dir +'_Accuracy_Graph.png')