import numpy as np
import cv2
import os

def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    """유니코드로 이루어진 파일경로를 읽기위한 함수. 동작은 cv2.imread()와 동일하다.\n
    scrapped from: https://jangjy.tistory.com/337"""
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None

def imwrite(filename, img, params=None):
    """유니코드로 이루어진 파일경로를 읽기위한 함수. 동작은 cv2.imwrite()와 동일하다.\n
    scrapped from: https://jangjy.tistory.com/337"""
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)
        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
                return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
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
    'res/partial_01.JPG',
    'res/partial_p_01.JPG',
    'res/total_01.JPG'
]

sequence = [
    convertColorSpace,
    threshold,
    morphology
]


cwd = os.path.dirname(os.path.dirname(__file__)) # == ../
file_path_list = [os.path.join(cwd, file_path) for file_path in file_path_list]

# --------------------------------

def model(src, sequence):
    retval = src
    for proc in sequence:
        retval = proc(retval)
    return retval

# %%

MIN_CONT_AREA = 20

# --------------------------------
for file_path in file_path_list:
    original = imread(file_path)
    result   = model(original, sequence)

    file_name, file_extension = os.path.splitext(os.path.basename(file_path))

    mask_addWeighted = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
    for cont in cv2.findContours(result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]:
        if cv2.contourArea(cont) >= MIN_CONT_AREA:
            cv2.drawContours(mask_addWeighted, [cont], -1, (0,0,255), -1)
        else:
            cv2.drawContours(mask_addWeighted, [cont], -1, (0,128,128), -1)

    output_dir = os.path.join(cwd, 'out')
    imwrite(f"{output_dir}/{file_name}{file_extension}", original)
    imwrite(f"{output_dir}/{file_name}_result{file_extension}", cv2.addWeighted(original, 0.75, mask_addWeighted, 0.75, 0))