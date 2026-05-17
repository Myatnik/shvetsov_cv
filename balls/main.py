import cv2
import numpy as np
import time
import json
from pathlib import Path
import random

save_path = Path(__file__).parent

cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow("Mask", cv2.WINDOW_GUI_NORMAL)

position = [0, 0]
clicked = False

def on_click(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        #print(f"Clicked at {x}, {y}")
        global position
        global clicked
        position = [x, y]
        clicked = True
#
cv2.setMouseCallback("Image", on_click)
capture = cv2.VideoCapture(0)
lower = None
upper = None

sphere1 = [None, None]
sphere2 = [None, None]
sphere3 = [None, None]
sphere4 = [None, None]

can_play = False

tags = [1, 2, 3, 4]
random.shuffle(tags)
config_path = save_path / "config.json"
if config_path.exists():
    print("Found saved combination")
    with config_path.open("r") as f:
        js = json.load(f)
        sphere1[0] = np.array(js[f"lower{tags[0]}"], dtype = "u1")
        sphere1[1] = np.array(js[f"upper{tags[0]}"], dtype = "u1")
        sphere2[0] = np.array(js[f"lower{tags[1]}"], dtype = "u1")
        sphere2[1] = np.array(js[f"upper{tags[1]}"], dtype = "u1")
        sphere3[0] = np.array(js[f"lower{tags[2]}"], dtype = "u1")
        sphere3[1] = np.array(js[f"upper{tags[2]}"], dtype = "u1")
        sphere4[0] = np.array(js[f"lower{tags[3]}"], dtype = "u1")
        sphere4[1] = np.array(js[f"upper{tags[3]}"], dtype = "u1")
        print(sphere1)
        print(sphere2)
        print(sphere3)
        print(sphere4)
    can_play = True
    print("Press E to start the game or click new colors and press 1/2/3/4 to overwrite existing ones\n",
          "Press Q to exit")
else:
    print("Found no saved colors, cant start the game. Select the colors and press 1/2/3/4 to select them\n",
          "Press Q to exit")
positions = []

playing = False

while True:
    ret, frame = capture.read()
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    key = cv2.waitKey(50) & 0xFF
    #
    if key == ord("q"):
        break
    #
    if clicked:
        if not playing:
            clicked = False
            color = hsv[position[1], position[0]]
            lower = np.clip(color * 0.9, 0, 255).astype("u1")
            upper = np.clip(color * 1.1, 0, 255).astype("u1")
            upper[1] = 255
            upper[2] = 255
        else:
            print("Cant click colors while playing")
    #
    if key == ord("1"):
        if not playing:
            sphere1 = [lower, upper]
            print("Remembered color1. Press W to write down colors when remembered all 4")
        else:
            print("Cant remember colors while playing")
    #
    if key == ord("2"):
        if not playing:
            sphere2 = [lower, upper]
            print("Remembered color2. Press W to write down colors when remembered all 4")
        else:
            print("Cant remember colors while playing")
    #
    if key == ord("3"):
        if not playing:
            sphere3 = [lower, upper]
            print("Remembered color3. Press W to write down colors when remembered all 4")
        else:
            print("Cant remember colors while playing")
    #
    if key == ord("4"):
        if not playing:
            sphere4 = [lower, upper]
            print("Remembered color4. Press W to write down colors when remembered all 4")
        else:
            print("Cant remember colors while playing")
    #
    if key == ord("w"):
        if not playing:
            with (save_path / "config.json").open("w") as f:
                json.dump({
                    "lower1": None if sphere1[0] is None else sphere1[0].tolist(),
                    "upper1": None if sphere1[1] is None else sphere1[1].tolist(),
                    "lower2": None if sphere2[0] is None else sphere2[0].tolist(),
                    "upper2": None if sphere2[1] is None else sphere2[1].tolist(),
                    "lower3": None if sphere3[0] is None else sphere3[0].tolist(),
                    "upper3": None if sphere3[1] is None else sphere3[1].tolist(),
                    "lower4": None if sphere4[0] is None else sphere4[0].tolist(),
                    "upper4": None if sphere4[1] is None else sphere4[1].tolist(),
                    }, f)
            print("Color order saved")
        else:
            print("Cant save colors while playing")
    #
    if key == ord("e"):
        if can_play == True:
            playing = True
            lower = None
            upper = None
            print("Game started. Line 4 color orbs in grid in camera")
        else:
            print("Couldnt start the game. Make sure you have saved color order")
    #
    if lower is not None:
        inr = cv2.inRange(hsv, lower, upper)
        mask = cv2.morphologyEx(inr, cv2.MORPH_CLOSE, np.ones((5, 5), dtype = "u1"))
        cv2.imshow("Mask", inr)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            contour = max(contours, key = cv2.contourArea)
            (x, y), radius = cv2.minEnclosingCircle(contour)
            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius), (1, 255, 255), 4)
                cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 255), -1)
    #
    if playing:
        inr1 = cv2.inRange(hsv, sphere1[0], sphere1[1])
        mask1 = cv2.morphologyEx(inr1, cv2.MORPH_CLOSE, np.ones((5, 5), dtype = "u1"))
        inr2 = cv2.inRange(hsv, sphere2[0], sphere2[1])
        mask2 = cv2.morphologyEx(inr2, cv2.MORPH_CLOSE, np.ones((5, 5), dtype = "u1"))
        inr3 = cv2.inRange(hsv, sphere3[0], sphere3[1])
        mask3 = cv2.morphologyEx(inr3, cv2.MORPH_CLOSE, np.ones((5, 5), dtype = "u1"))
        inr4 = cv2.inRange(hsv, sphere4[0], sphere4[1])
        mask4 = cv2.morphologyEx(inr4, cv2.MORPH_CLOSE, np.ones((5, 5), dtype = "u1"))
        inr = inr1 + inr2 + inr3 + inr4
        cv2.imshow("Mask", inr)
        orderx = [0, 0, 0, 0]
        ordery = [0, 0, 0, 0]
        #
        contours1, _ = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours1) > 0:
            contour1 = max(contours1, key = cv2.contourArea)
            (x1, y1), radius1 = cv2.minEnclosingCircle(contour1)
            orderx[0] = int(x1)
            ordery[0] = int(y1)
            if radius1 > 10:
                cv2.circle(frame, (int(x1), int(y1)), int(radius1), (1, 255, 255), 4)
                cv2.circle(frame, (int(x1), int(y1)), 5, (0, 255, 255), -1)
        #
        contours2, _ = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours2) > 0:
            contour2 = max(contours2, key = cv2.contourArea)
            (x2, y2), radius2 = cv2.minEnclosingCircle(contour2)
            orderx[1] = int(x2)
            ordery[1] = int(y2)
            if radius2 > 10:
                cv2.circle(frame, (int(x2), int(y2)), int(radius2), (1, 255, 255), 4)
                cv2.circle(frame, (int(x2), int(y2)), 5, (0, 255, 255), -1)
        #
        contours3, _ = cv2.findContours(mask3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours3) > 0:
            contour3 = max(contours3, key = cv2.contourArea)
            (x3, y3), radius3 = cv2.minEnclosingCircle(contour3)
            orderx[2] = int(x3)
            ordery[2] = int(y3)
            if radius3 > 10:
                cv2.circle(frame, (int(x3), int(y3)), int(radius3), (1, 255, 255), 4)
                cv2.circle(frame, (int(x3), int(y3)), 5, (0, 255, 255), -1)
        #
        contours4, _ = cv2.findContours(mask4, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours4) > 0:
            contour4 = max(contours4, key = cv2.contourArea)
            (x4, y4), radius4 = cv2.minEnclosingCircle(contour3)
            orderx[3] = int(x4)
            ordery[3] = int(y4)
            if radius4 > 10:
                cv2.circle(frame, (int(x4), int(y4)), int(radius4), (1, 255, 255), 4)
                cv2.circle(frame, (int(x4), int(y4)), 5, (0, 255, 255), -1)
        #
        if orderx[0] < orderx[1] and orderx[2] < orderx[3] and ordery[0] < ordery[2] and ordery[1] < ordery[3]:
            cv2.putText(frame, "correct", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
        

    cv2.imshow("Image", frame)
