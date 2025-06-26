import numpy as np
import cv2
import os
import pandas as pd

# 부위별 class 정의 (GOLIATH 기준)
target_classes = {
    21: 'Torso',
    10: 'Left Upper Arm',
    14: 'Right Upper Arm',
    11: 'Left Upper Leg',
    20: 'Right Upper Leg',
    6:  'Left Lower Arm',
    15: 'Right Lower Arm',
    7:  'Left Lower Leg',
    16: 'Right Lower Leg',
    5:  'Left Hand',
    19: 'Right Hand',
}

# 파일 경로
seg_path = "/home/jyc/sapiens/output_image/sapiens_1b/seg/test/img5.npy"
edge_path = "/home/jyc/sapiens/estimate_muscle/img5_edge.png"

# 로드
seg = np.load(seg_path)
edge = cv2.imread(edge_path, cv2.IMREAD_GRAYSCALE)

# 결과 저장 리스트
results = []

for class_id, class_name in target_classes.items():
    mask = seg == class_id
    num_pixels = np.sum(mask)

    if num_pixels == 0:
        print(f"[Warning] No pixels found for {class_name}")
        continue

    edge_strength = np.sum(edge[mask])
    avg_edge_per_pixel = edge_strength / num_pixels

    results.append({
        "Body Part": class_name,
        "Pixels": num_pixels,
        "Edge Sum": edge_strength,
        "Avg Edge / Pixel": round(avg_edge_per_pixel, 2)
    })

# 정리
df = pd.DataFrame(results).sort_values("Avg Edge / Pixel", ascending=False)
print(df)