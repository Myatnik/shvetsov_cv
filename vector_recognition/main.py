import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.io import imread
from pathlib import Path

save_path = Path(__file__).parent

def extractor(region):
    return np.array([region.area/region.image.size])

def classificator(region, templates):
    features = extractor(region)
    result = ""
    min_d = 10**16
    for symbol, t in templates.items():
        d = ((t - features)**2).sum()**0.5
        if d < min_d:
            result = symbol
            min_d = d
    return result
template = imread("alphabet-small.png")[:, :, :-1]
template = template.sum(2)
binary = template != 765.

labeled = label(binary)
props = regionprops(labeled)

templates = {}
for region, symbol in zip(props, ["8", "O", "A", "B", "1", "W", "X", "*", "/", "-"]):
    templates[symbol] = extractor(region)

#print(templates)

#print(classificator(props[0], templates))


image = imread("alphabet.png")[:, :, :-1]
binary_alphabet = image.mean(2) > 0
alabeled = label(binary_alphabet)
aprops = regionprops(alabeled)
result = {}
image_path = save_path/"out"
image_path.mkdir(exist_ok = True)

#plt.ion()
plt.figure(figsize = (5, 7))

for region in aprops:
    symbol = classificator(region, templates)
    if symbol not in result:
        result[symbol] = 0
    result[symbol] += 1
    plt.cla()
    plt.title(f"Class - '{symbol}'")
    plt.imshow(region.image)
    plt.savefig(image_path/f"image_{region.label}.png")
print(result)

plt.imshow(alabeled)
plt.show()