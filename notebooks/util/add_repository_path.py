import os
import sys

# ------------------------------------------------
# 정상적인 모듈 import를 위해 레포지토리 경로를
# system.path 에 추가
# ------------------------------------------------

repository_path = os.path.abspath('')
python_path = repository_path + '/python'

sys.path.append(python_path)