import os

import numpy as np
import cv2

class DG_CSD_ErosionDetection:
    """첨성대 벽돌 사이사이에서 침식된 영역을 검사하기 위한 메소드를 담고있는 클래스"""

    def findHoles(frame_bgr):
        """첨성대 벽돌 사이사이에서 침식된 영역(추정)의 마스크 이미지 생성"""

        frame_hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
        # 채도(S)와 밝기(V)가 낮은 영역 : 검은색 영역을 선택
        frame_bin = cv2.inRange(frame_hsv, (  0,  0,  0), (255, 96, 96))
        frame_bin = cv2.morphologyEx(frame_bin, cv2.MORPH_OPEN, (5,5))
        return frame_bin

    def findContoursFromMask(frame_color, mask, area_thresh=32):
        """주어진 마스크로부터 윤곽선 검출을 통해 객체를 찾고, 객체가 위치한 영역을 작은 프레임에 담아 반환.\n
        반환값:
        1. 각 침식영역을 잘라낸 작은 프레임들의 리스트
        2. 바운딩 박스를 표현하기 위한 좌표 리스트
        """

        contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        
        frame_cut_list = []
        box_list = []

        for cont in contours:
            if cv2.contourArea(cont) < area_thresh: continue

            x, y, w, h = cv2.boundingRect(cont)
            cx, cy = x + w/2, y + h/2
            n = max(w,h)
            
            x0, y0 = int(cx - n/2), int(cy - n/2)
            x1, y1 = int(cx + n/2), int(cy + n/2)
            
            frame_cut = np.zeros((n,n,3), dtype=np.uint8)
            frame_cut = frame_color[y0:y1, x0:x1]
            
            if not frame_cut.any(): continue

            frame_cut_list.append(frame_cut.copy())
            box_list.append((x,y,w,h))

        return frame_cut_list, box_list

class DG_ClassWrapper:
    class_list = []

    # 새로운 ML클래스 생성
    def new(class_name:str, label:int,
            is_fixed_shape:bool=False, data_shape:tuple=()):
        """Creates a new class with given name and label value.

        Parameters
        ----------
        class_name : str
            The name of the class.
        label : int
            The value of label.
        is_fixed_shape : bool, optional
            Toggle whether to use fixed data_size or not.
        data_shape : tuple, optional
            The shape of data

        Returns
        -------
        DG_ClassWrapper.DG_Class
        """

        if DG_ClassWrapper.does_class_exist(class_name, label):
            return None

        new_class = DG_ClassWrapper.DG_Class(class_name, label, data_size, is_fixed_size)

        DG_ClassWrapper.class_list.append(new_class)
        return new_class

    def does_class_exist(class_name:str, label:int):
        """중복된 ML클래스가 존재하는지 확인"""
        for c in DG_ClassWrapper.class_list:
            try:
                if c.name == class_name:
                    raise Exception(f"Class with the name '{class_name}' already exists.")
                if c.label == label:
                    raise Exception(f"Class with the label '{label}' already exists.")
            except Exception as err:
                return True
        return False
    
    class DG_Class:
        """ML클래스 인스턴스를 생성하기 위한 클래스"""

        def __init__(self, class_name:str, label:int,
                    is_fixed_shape:bool=False, data_shape:tuple=()):
            self.name = class_name

            self.label = label

            self.data_shape = data_shape
            self.is_fixed_shape = is_fixed_size
            self.samples = []
        
        def addSample(self, data):
            """단일 샘플을 클래스 인스턴스에 등록"""
            if self.is_fixed_shape:
                if data.shape != self.data_shape:
                    raise Exception(f"data.shape does not match with {self.data_shape}")
            self.samples.append(data)
        
        def addSamples(self, data_list):
            """다중 샘플을 클래스 인스턴스에 등록"""
            for data in data_list:
                self.addSample(data)

        def createDataset(self):
            """등록된 샘플들과 레이블을 1:1 대응시켜 반환: returns (x, y)"""
            return self.samples, [self.label]*len(self.samples)

class DG_FileSystem:
    # TODO: 도큐먼트 작성하기
    """파일 입출력과 관련됨."""

    def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
        """유니코드로 이루어진 파일경로를 읽기위한 함수. 동작은 cv2.imread()와 동일하다.\n
        scrapped from: https://cjh5414.github.io/python-with/"""
        try:
            n = np.fromfile(filename, dtype)
            img = cv2.imdecode(n, flags)
            return img
        except Exception as e:
            print(e)
            return None

    def imwrite(filename, img, params=None):
        """유니코드로 이루어진 파일경로를 읽기위한 함수. 동작은 cv2.imwrite()와 동일하다.\n
        scrapped from: https://cjh5414.github.io/python-with/"""
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

    # ------------------------------------------------

    def openImage(path:str):
        """단일 이미지를 열어 BGR 형태의 cv2 이미지로 반환"""
        if not os.path.isfile(path):
            raise Exception(f"Could not open '{path}'. The file does not exist.")
            
        frame = DG_FileSystem.imread(path)

        if (type(frame) == type(None)):
            raise Exception(f"Could not open '{path}' using cv2.")

        return frame
            

    def openImages(path_list:list):
        """다중 이미지를 열어 BGR 형태의 cv2 이미지 리스트로 반환"""
        return [FileOpener.openImage(path) for path in path_list]
    
    def openImagesFromDir(dir_path:str):
        """주어진 폴더에 있는 이미지 파일들을 열어 BGR 형태의 cv2 이미지 리스트로 반환.\n
        단, 각 파일의 경로도 함께 반환한다."""
        if not os.path.isdir(dir_path):
            raise Exception(f"Could not open '{dir_path}': is not a directory.")
        
        file_path_list = []
        frame_list = []
        for file_basename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_basename)
            file_name, file_extension = os.path.splitext(file_path)
            if file_extension.lower() in ['.jpg', '.jpeg', '.png']:
                file_path_list.append(file_path)
                frame_list.append(DG_FileSystem.openImage(file_path))
        return file_path_list, frame_list