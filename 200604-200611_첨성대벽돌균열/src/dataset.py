import os

import numpy as np
import cv2

try:
    from . import cv2_utf8
except:
    import cv2_utf8

DEFAULT_CLASS_PATH = 'data/class'

def save(x_data:list, y_data:list, class_path:str=DEFAULT_CLASS_PATH) -> None:
    """리스트의 형태로 전달되는 x, y에 대하여, 지정된 경로에 랜덤한 이름의 이미지 파일로 저장됨."""
    for x, y in zip(x_data, y_data):
        label_path = os.path.join(class_path, str(y))
        file_path  = os.path.join(label_path, f"{cv2.getTickCount()}.png")

        if not os.path.exists(label_path):
            os.mkdir(label_path)

        cv2_utf8.imwrite(x, file_path)

def load(class_path:str=DEFAULT_CLASS_PATH) -> 'test, train dataset':
    """save()를 통해 저장한 데이터를 불러와, test, train 두 데이터셋쌍으로 반환"""
    x_data = []
    y_data = []

    if not os.path.exists(class_path):
        raise Exception(f"Path '{class_path}' does not exist.")

    for label_dirname in os.listdir(class_path):
        label_path = os.path.join(class_path, label_dirname)
        if not os.path.isdir(label_path): continue

        label = int(label_dirname)

        for file_basename in os.listdir(label_path):
            file_path = os.path.join(label_path, file_basename)
            if not os.path.isfile(file_path): continue

            frame = cv2_utf8.imread(file_path)
            if type(frame) == type(None): continue
            # if frame.size == 0: continue
            if frame.shape != (28,28,3): continue

            x_data.append(frame)
            y_data.append(label)

    if len(x_data) == 0:
        raise Exception(f"No data in '{class_path}'.")

    x_data = np.array(x_data)
    y_data = np.array(y_data)

    return split_train_test(x_data, y_data)

def split_train_test(x, y, test_ratio=0.2, shuffle=True):
    n_of_data = len(x)

    shuffled_indices = np.random.permutation(n_of_data)
    size_of_test  = int(n_of_data * test_ratio)

    x_shuffled = x[shuffled_indices]
    y_shuffled = y[shuffled_indices]

    x_train = x_shuffled[size_of_test:]
    y_train = y_shuffled[size_of_test:]

    x_test = x_shuffled[:size_of_test]
    y_test = y_shuffled[:size_of_test]

    return (x_train, y_train), (x_test, y_test)