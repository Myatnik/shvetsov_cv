import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label
from scipy import ndimage

def distance(point1, point2):
    dist = ((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)**0.5
    return dist
#

images = []
labeleds = []
centroids = []
data = np.load("out/h_0.npy")
for i in range(100):
    img = np.load(f"out/h_{i}.npy")
    img_labels = label(img)
    img_centroids = ndimage.center_of_mass(img, img_labels, range(1, img_labels.max() + 1))

    images.append(img)
    labeleds.append(img_labels)
    centroids.append(img_centroids)
#

graph1 = []
graph2 = []
graph3 = []

graphs = {1: graph1,
          2: graph2,
          3: graph3}

for i, line in enumerate(centroids[:-1]):
    if i == 0:
        graph1.append(line[0])
        graph2.append(line[1])
        graph3.append(line[2])
    else:
        to_compare = [graph1[-1], graph2[-1], graph3[-1]]
        for cords in line:
            dists = []
            for i in range(3):

                dists.append(distance(cords, to_compare[i]))
            graphs[dists.index(min(dists))+1].append(cords)
#
graph1.append(graph1[0])
graph2.append(graph2[0])
graph3.append(graph3[0])

print(graph1)
print(graph2)
print(graph3)
graph1x = []
graph1y = []
graph2x = []
graph2y = []
graph3x = []
graph3y = []
for xy in graph1:
    graph1x.append(xy[0])
    graph1y.append(xy[1])
for xy in graph2:
    graph2x.append(xy[0])
    graph2y.append(xy[1])
for xy in graph3:
    graph3x.append(xy[0])
    graph3y.append(xy[1])
#

plt.figure()
plt.plot(graph1y, graph1x)
plt.plot(graph2y, graph2x)
plt.plot(graph3y, graph3x)
plt.grid()
plt.show()