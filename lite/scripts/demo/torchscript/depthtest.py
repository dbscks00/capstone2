import cv2
import numpy as np
import os
import sys
from collections import defaultdict
import pandas as pd
from glob import glob

# classes_and_palettes.py가 위치한 경로 추가
sys.path.append("/home/jyc/sapiens/lite/demo")
from classes_and_palettes import ORIGINAL_GOLIATH_CLASSES, ORIGINAL_GOLIATH_PALETTE

# 사용자 환경에서의 경로 (최신 경로로 수정)
seg_dir = "/home/jyc/sapiens/output_image/sapiens_1b/seg/seg_test"
depth_dir = "/home/jyc/sapiens/output_image/sapiens_1b/depth/depth_test"

# 카메라 파라미터 (가정 값)
fx, fy = 600, 600
cx, cy = 320, 240

# 클래스 이름 매핑 생성
class_map = {i: name for i, name in enumerate(ORIGINAL_GOLIATH_CLASSES)}
PALETTE = {tuple(rgb): idx for idx, rgb in enumerate(ORIGINAL_GOLIATH_PALETTE)}

# 컬러 마스크를 클래스 인덱스로 변환하는 함수
def convert_rgb_mask_to_index(mask_rgb):
    h, w, _ = mask_rgb.shape
    index_mask = np.zeros((h, w), dtype=np.uint8)
    for rgb, cls_id in PALETTE.items():
        match = np.all(mask_rgb == rgb, axis=-1)
        index_mask[match] = cls_id
    return index_mask

# 결과 저장용 리스트
results = []
summary = []
pixel_details = []

# Segmentation 결과가 .jpg 또는 .png일 수 있으므로 둘 다 처리
seg_paths = sorted(glob(os.path.join(seg_dir, "*.jpg")) + glob(os.path.join(seg_dir, "*.png")))
depth_paths = sorted(glob(os.path.join(depth_dir, "*.npy")))

# base name 추출 (확장자 없이 매칭)
seg_dict = {os.path.splitext(os.path.basename(p))[0]: p for p in seg_paths}
depth_dict = {os.path.splitext(os.path.basename(p))[0]: p for p in depth_paths}

# 자동 매칭된 파일 목록
matched_keys = set(seg_dict.keys()) & set(depth_dict.keys())
print(f"총 매칭된 이미지 쌍 수: {len(matched_keys)}")

for base_name in sorted(matched_keys):
    seg_path = seg_dict[base_name]
    depth_path = depth_dict[base_name]

    seg = cv2.imread(seg_path, cv2.IMREAD_UNCHANGED)
    depth = np.load(depth_path)

    # 컬러 마스크를 인덱스 마스크로 변환
    if len(seg.shape) == 3:
        seg = convert_rgb_mask_to_index(seg)

    total_scaled_area = 0.0
    class_scale_areas = {}
    unique_classes = np.unique(seg)
    for cls_id in unique_classes:
        if cls_id == 0 or cls_id not in class_map:
            continue

        mask = (seg == cls_id)
        pixel_count = np.sum(mask)
        avg_depth = np.mean(depth[mask])
        scale_area = np.sum((depth[mask] / fx) * (depth[mask] / fy))
        total_scaled_area += scale_area
        class_scale_areas[cls_id] = scale_area

        results.append({
            "Image": base_name,
            "Class ID": cls_id,
            "Class Name": class_map.get(cls_id, f"Class {cls_id}"),
            "Pixel Count": pixel_count,
            "Average Depth": round(avg_depth, 4),
            "Scaled Area (relative unit)": round(scale_area, 6)
        })

    for cls_id, scale_area in class_scale_areas.items():
        percentage = (scale_area / total_scaled_area * 100) if total_scaled_area > 0 else 0.0
        pixel_details.append({
            "Image": base_name,
            "Class ID": cls_id,
            "Class Name": class_map.get(cls_id, f"Class {cls_id}"),
            "2D Pixel Count": np.sum(seg == cls_id),
            "Scaled Area (2.5D)": round(scale_area, 6),
            "Percentage of Body Area": round(percentage, 2)
        })

    summary.append({
        "Image": base_name,
        "Total Scaled Area": round(total_scaled_area, 6)
    })

results_df = pd.DataFrame(results)
sum_df = pd.DataFrame(summary)
detail_df = pd.DataFrame(pixel_details)

results_df.to_csv("segmentation_depth_analysis.csv", index=False)
sum_df.to_csv("segmentation_depth_summary.csv", index=False)
detail_df.to_csv("segmentation_depth_pixel_details.csv", index=False)

print("분석 완료: segmentation_depth_analysis.csv, segmentation_depth_summary.csv, segmentation_depth_pixel_details.csv 저장됨")
