import numpy as np
import matplotlib.pyplot as plt

# folder to save results
target_dir = "fp_sweep"

#Graphing Part
accuracy_data = np.load('./outputs/' + target_dir + '/fin_acc.npy')

plt.plot(accuracy_data.T)
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.title(target_dir)

if target_dir == "w2_sweep":
    plt.legend(('Iteration 0', 'Iteration 1', 'Iteration 2', 'Iteration 3', 'Iteration 4'))
if target_dir == "fp_sweep":
    plt.legend(('Iteration 0', 'Iteration 1', 'Iteration 2', 'Iteration 3', 'Iteration 4', 'Iteration 5', 
    'Iteration 6', 'Iteration 7', 'Iteration 8', 'Iteration 9'))

plt.savefig('./outputs/' + target_dir + '/' + target_dir +'Accuracy_Graph.png')