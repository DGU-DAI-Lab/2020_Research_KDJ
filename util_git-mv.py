from_path = './200604-200611_첨성대벽돌균열/2_정상-비정상-머신러닝적용.ipynb'
to_path   = './200604-200611_첨성대벽돌균열/3_정상-비정상-머신러닝적용.ipynb'

# --------------------------------

import os

# If directory
if os.path.isdir(from_path):
    if not os.path.exists(to_path): os.mkdir(to_path)

    for file_path in os.listdir(from_path):
        from_file_path = os.path.join(from_path, file_path)
        to_file_path   = os.path.join(to_path, file_path)

        os.system(f'git mv "{from_file_path}" "{to_file_path}"')

    os.remove(from_path)

# If file
else:
    os.system(f'git mv "{from_path}" "{to_path}"')

# --------------------------------

print("commit title:", end='\n')
print(f'    Rename "{os.path.basename(from_path)}" -> "{os.path.basename(to_path)}"', end='\n\n')
print("commit description:", end='\n')
print(f'    "{from_path}" -> "{to_path}"', end='\n\n')