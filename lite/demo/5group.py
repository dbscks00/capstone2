import os
import numpy as np
from PIL import Image
from collections import defaultdict

# classes_and_palettes.py에서 ORIGINAL_GOLIATH_CLASSES 불러오기
from classes_and_palettes import ORIGINAL_GOLIATH_CLASSES as class_names

# ✅ 5개 그룹 매핑 정의
class_to_group = {
    'Torso': 'Torso',
    'Upper_Clothing': 'Torso',
    'Lower_Clothing': 'Torso',

    'Right_Upper_Arm': 'Right_Arm',
    'Right_Lower_Arm': 'Right_Arm',
    'Right_Hand': 'Right_Arm',

    'Left_Upper_Arm': 'Left_Arm',
    'Left_Lower_Arm': 'Left_Arm',
    'Left_Hand': 'Left_Arm',

    'Right_Upper_Leg': 'Right_Leg',
    'Right_Lower_Leg': 'Right_Leg',
    'Right_Foot': 'Right_Leg',

    'Left_Upper_Leg': 'Left_Leg',
    'Left_Lower_Leg': 'Left_Leg',
    'Left_Foot': 'Left_Leg',
}

# ✅ class id → group 매핑 테이블 작성
class_id_to_group = {}
for class_id, class_name in enumerate(class_names):
    group = class_to_group.get(class_name, 'Other')
    class_id_to_group[class_id] = group

# ✅ segmentation mask 결과 저장 폴더 (seg.sh의 output 경로 그대로 사용)
OUTPUT_DIR = '/home/jyc/sapiens/output_image/sapiens_1b/seg/aiimage'

# ✅ 폴더 내 png 파일 중 첫번째 선택
mask_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.png')]
if not mask_files:
    raise FileNotFoundError(f"No mask PNG files found in {OUTPUT_DIR}")

mask_path = os.path.join(OUTPUT_DIR, mask_files[0])
print(f"Using segmentation mask file: {mask_path}")

# ✅ segmentation mask 읽어오기
mask_img = Image.open(mask_path)
seg_mask = np.array(mask_img)

# ✅ 그룹별 픽셀 카운트
group_pixel_count = defaultdict(int)

unique_classes = np.unique(seg_mask)
for class_id in unique_classes:
    count = np.sum(seg_mask == class_id)
    group = class_id_to_group.get(class_id, 'Other')
    group_pixel_count[group] += count

total_pixels = seg_mask.size

# ✅ 결과 출력
print("\n===== Grouped Segmentation Result =====")
for group in ['Torso', 'Right_Arm', 'Left_Arm', 'Right_Leg', 'Left_Leg']:
    count = group_pixel_count[group]
    ratio = 100 * count / total_pixels
    print(f"Group: {group}, Pixel Count: {count}, Ratio: {ratio:.2f}%")

# ✅ Other 그룹도 출력
if 'Other' in group_pixel_count:
    count = group_pixel_count['Other']
    ratio = 100 * count / total_pixels
    print(f"Group: Other, Pixel Count: {count}, Ratio: {ratio:.2f}%")
