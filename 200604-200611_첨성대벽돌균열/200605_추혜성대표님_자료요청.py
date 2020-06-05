import numpy as np
import cv2

# --------------------------------

def convertColorSpace(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

def threshold(frame):
    # HSV 색공간을 이용. 채도와 밝기가 낮은 곳을 선택함. (==그림자)
    range_lower = (  0,  0,  0)
    range_upper = (255, 96, 92)
    return cv2.inRange(frame, range_lower, range_upper)

def morphology(frame):
    frame = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, (5,5))
    return cv2.morphologyEx(frame, cv2.MORPH_OPEN, (5,5))

# --------------------------------

file_path_list = [
    './res/partial_01.JPG',
    './res/partial_p_01.JPG',
    './res/total_01.JPG'
]

sequence = [
    convertColorSpace,
    threshold,
    morphology
]

# --------------------------------

def model(src, sequence):
    retval = src
    for proc in sequence:
        retval = proc(retval)
    return retval

# %%

import os

# --------------------------------
for file_path in file_path_list:
    original = cv2.imread(file_path)
    result   = model(original, sequence)

    file_name, file_extension = os.path.splitext(os.path.basename(file_path))

    mask_addWeighted = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
    for cont in cv2.findContours(result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]:
        if cv2.contourArea(cont) >= MIN_CONT_AREA:
            cv2.drawContours(mask_addWeighted, [cont], -1, (0,0,255), -1)
        else:
            cv2.drawContours(mask_addWeighted, [cont], -1, (0,128,128), -1)

    cv2.imwrite(f"./out/{file_name}{file_extension}", original)
    cv2.imwrite(f"./out/{file_name}_result{file_extension}", cv2.addWeighted(original, 0.75, mask_addWeighted, 0.75, 0))