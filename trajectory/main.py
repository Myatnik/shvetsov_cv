import numpy as np
import matplotlib.pyplot as plt

data = np.load("out/h_0.npy")
for i in range(1, 100):
    data += np.load(f"out/h_{i}.npy") #im not sure what the task wanted from me
#

plt.imshow(data)
plt.show()