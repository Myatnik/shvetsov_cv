import pyautogui as gui
import cv2
import time
import numpy as np
#from pynput import keyboard #later maybe for normal controls
from skimage import morphology, measure

#all comments for myself so i wont forget what am i even doing through several days of coding

region = (1, 1, 1, 1)
dino_spawn = (1, 1, 1, 1)
labeled_save = None
curr_frame = 0
left_offset = 5
top_offset = 100
wait_to_start = 5
speed_increment = 0.05
increment_interval = 10 #sec
slam_push_interval = 30 #sec
detect_len = 170
slam_len = 130
slam_len_left = 10
top_shrink = 30 #to not detect birds...
last_time_detect = 0
last_time_slam = 0
spawn_show = True
airborn = False
low = False
can_slam = False
mask = np.ones((3,3))

def restart_game():
    global region, dino_spawn, labeled_save, curr_frame, spawn_show, detect_len, slam_len, slam_len_left, last_time_detect, last_time_slam, airborn, low, can_slam

    print("restarting the game...")
    airborn = False
    low = False
    can_slam = False
    gui.hotkey('ctrl', 'r') #reload page
    time.sleep(1) #for page to load properly
    gui.press('space') #start game
    time.sleep(2) #pause for the field to unroll
    detect_len = 170
    slam_len = 130
    slam_len_left = 10
    dino_spawn = gui.locateOnScreen(image_rex, confidence=0.7) #left top corner of dino spawn, to find the field for screenshots
    region = (int(dino_spawn[0]-left_offset), 
              int(dino_spawn[1]-top_offset), 
              700, 
              190)
    labeled_save = None
    curr_frame = 0
    last_time_detect = time.time()
    last_time_slam = time.time()
    slam()
    print("game began")
#
def jump():
    global airborn
    gui.press('space')
    airborn = True
    #print("jumped")
#
def slam():
    global dino_spawn, airborn, can_slam
    gui.click(dino_spawn[0], dino_spawn[1]+300)
    gui.click(dino_spawn[0], dino_spawn[1])
    airborn = False
    can_slam = False
    #print("slammed")
#
def crouch():
    global low
    gui.keyDown('down')
    low = True
    #print("bent down")
#
def stand():
    global low, airborn
    gui.keyUp('down')
    low = False
    airborn = False
    can_slam = False
    #print("stood up")
#

image_rex = cv2.imread("rex.png")

print("---hotkeys(only on cv2 window so far)---\n",
    "Q-exit the game\n",
    "S-show/hide dino spawn\n",
    "---end---\n",
    f"You have {wait_to_start} seconds to open the game window\n")

time.sleep(wait_to_start) #to open the dino game
restart_game()

cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
#cv2.namedWindow("Binary", cv2.WINDOW_GUI_NORMAL)


while True:
    curr_frame += 1
    current_time1 = time.time()
    current_time2 = time.time()
    if detect_len < 400 and current_time1 - last_time_detect >= increment_interval:
        detect_len += int(detect_len * speed_increment)
        slam_len += int(detect_len * speed_increment)
        #print("detection rose\n")
        last_time_detect = current_time1
    if slam_len_left < 35 and current_time2 - last_time_slam >= slam_push_interval:
        slam_len_left += 5
        #print("slam moved right")
        last_time_slam = current_time2


    field = gui.screenshot(region = region)
    result = cv2.cvtColor(np.array(field), cv2.COLOR_RGB2BGR)

    
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    binary = (gray < 100).astype(np.float32)
    binary = morphology.opening(binary, mask)

    labeled = measure.label(binary)

    roi_jump = labeled[top_offset+top_shrink:100 + dino_spawn[3], left_offset + dino_spawn[2]:left_offset + detect_len]
    roi_slam = labeled[top_offset+top_shrink:100 + dino_spawn[3], slam_len_left:left_offset + slam_len]
    roi_crouch = labeled[top_offset+10:top_offset + top_shrink - 1, left_offset + dino_spawn[2] + 10:left_offset + detect_len]
    roi_slam_check = labeled[top_offset+top_shrink:100 + dino_spawn[3], left_offset + dino_spawn[2] + 25:left_offset + slam_len - 5]

    if np.any(roi_jump>0) and not airborn:
        jump()
    #
    if np.all(roi_slam == 0) and airborn and can_slam:
        slam()
    #
    if np.any(roi_crouch > 0) and np.all(roi_jump == 0) and not low and not airborn:
        crouch()
    #
    if np.all(roi_crouch == 0) and low:
        stand()
    #
    if np.any(roi_slam_check > 0) and airborn and not can_slam:
        #print("can slam")
        can_slam = True
    #
    if curr_frame % 60 == 0:
        if labeled_save is not None and np.array_equal(labeled_save, labeled):
            print("crashed! restarting in 5 seconds")
            time.sleep(5)
            restart_game()
        labeled_save = labeled.copy()
    #
    if spawn_show:
        cv2.rectangle(result, (left_offset + dino_spawn[2], top_offset+top_shrink), (left_offset + detect_len, 100 + dino_spawn[3]), (0, 255, 255), 2)
        cv2.rectangle(result, (slam_len_left, top_offset+top_shrink), (left_offset + slam_len, 100 + dino_spawn[3]), (255, 255, 0), 1)
        cv2.rectangle(result, (left_offset + dino_spawn[2] + 10, top_offset+10), (left_offset + detect_len,top_offset + top_shrink - 1), (255, 0, 0), 1)
        cv2.rectangle(result, (left_offset + dino_spawn[2]  + 25,top_offset+top_shrink), (left_offset + slam_len - 5,100 + dino_spawn[3]), (0, 0, 0), 3)
    #
    cv2.imshow("Image", result)
    #cv2.imshow("Binary", binary)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if key == ord('s'):
        spawn_show = not spawn_show
    if key == ord('r'):
        restart_game()
    time.sleep(0.01)
#
