# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # 로컬 영역이 아닌 전역적으로 이미지에 모델을 적용시킬 수 있다면...?
# 
# ## 레이블 된 이미지 생성:

# %%
import cv2
import numpy as np

MIN_CONT_AREA = 20

# --------------------------------

for raw, mask in load():
    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    labled_mask = np.zeros(mask.shape, dtype=np.uint8)

    for cont in contours:
        if cv2.contourArea(cont) >= MIN_CONT_AREA:
            cv2.drawContours(labled_mask, [cont], -1, 1, -1)

        else:
            cv2.drawContours(labled_mask, [cont], -1, 2, -1)

