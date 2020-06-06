import numpy as np
import cv2

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