import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label
from skimage.morphology import (opening)

data = np.load("stars.npy")
data_labeled = label(data)

struct = np.ones((3, 3))
data_processed = opening(data, struct)
processed_labeled = label(data_processed)

print(data_labeled.max() - processed_labeled.max())

plt.plot()
plt.imshow(data)
plt.show()