import cv2
import numpy as np
from skimage import measure
import matplotlib.pyplot as plt

image = cv2.imread("balls_and_rects.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
binary = gray.astype(np.float32)
labeled = measure.label(binary)

rects = {}
circs = {}

contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for i, cnt in enumerate(contours):
    x, y, w, h = cv2.boundingRect(cnt)
    area = image[y:y+h, x:x+w]
    center = f"{area[int(h/2)][int(w/2)][0]}:{area[int(h/2)][int(w/2)][1]}:{area[int(h/2)][int(w/2)][2]}"
    if area[0][0].all() == np.array([0, 0, 0]).all():
        if center in circs:
            circs[center] += 1
        else:
            circs[center] = 1
    else:
        if center in rects:
            rects[center] += 1
        else:
            rects[center] = 1
    
rect_colors = 0
circ_colors = 0
for i in rects:
    rect_colors += rects[i]
for i in circs:
    circ_colors += circs[i]

print(f"You have {labeled.max()} shapes in total")
print(f"Rectangles have {rect_colors} colors, circles have {circ_colors} colors")