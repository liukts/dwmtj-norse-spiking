import numpy as np
import matplotlib.pyplot as plt

# folder to save results
target_dir = "T_sweep_1_3_22"

#Graphing Part
accuracy_data = np.load('./outputs/' + target_dir + '/fin_acc.npy')

plt.plot(accuracy_data.T)
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.title(target_dir)

if target_dir == "w2_sweep":
    plt.legend(('w2 = 25e-9', 'w2 = 40e-9', 'w2 = 55e-9', 'w2 = 70e-9', 'w2 = 85e-9', 'w2 = 100e-9'), loc="lower right")
if target_dir == "fp_sweep":
    plt.legend(('fp = 1e9', 'fp = 2e9', 'fp = 3e9', 'fp = 4e9', 'fp = 5e9', 'fp = 6e9', 
    'fp = 7e9', 'fp = 8e9', 'fp = 9e9', 'fp = 10e9'), loc="lower right")
if target_dir == "T_sweep_1_3_22":
    plt.legend(('T = 5', 'T = 10', 'T = 15', 'T = 20', 'T = 25', 'T = 30', 
    'T = 35', 'T = 40', 'T = 45', 'T = 50'), loc="lower right")


plt.savefig('./outputs/' + target_dir + '/' + target_dir +'Accuracy_Graph.png')