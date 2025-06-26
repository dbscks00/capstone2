import os
import json
import numpy as np
import cv2
from classes_and_palettes import GOLIATH_PALETTE  # 외부에서 import 사용

# 🔹 디렉토리 설정
seg_result_dir = "/home/jyc/sapiens/output_image/sapiens_1b/seg"
edge_output_dir = os.path.join(seg_result_dir, "seg_edge")
colored_output_dir = os.path.join(seg_result_dir, "seg_colored_on_edge")
combined_output_dir = os.path.join(seg_result_dir, "seg_colored_edge_pose")

pose_json_dir = "/home/jyc/sapiens/output_image/sapiens_1b/pose"

# 🔧 디렉토리 생성
os.makedirs(edge_output_dir, exist_ok=True)
os.makedirs(colored_output_dir, exist_ok=True)
os.makedirs(combined_output_dir, exist_ok=True)

# 🔧 skeleton 정의 (예시: COCO나 SAPIENS 일부)
SKELETON = [
    (5, 6),   # shoulders
    (11, 12), # hips
    (5, 11), (6, 12),
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (6, 7), (7, 8)
]

# ✅ 메인 루프: segmentation + pose를 하나의 이미지로
for filename in sorted(os.listdir(seg_result_dir)):
    if not filename.endswith("_seg.npy"):
        continue

    name = filename.replace("_seg.npy", "")
    seg_path = os.path.join(seg_result_dir, filename)
    seg_array = np.load(seg_path)

    # ▶ Edge 추출
    binary_mask = (seg_array > 0).astype(np.uint8) * 255
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    edge_img = np.zeros_like(binary_mask)
    cv2.drawContours(edge_img, contours, -1, 255, thickness=2)

    # ▶ Colored segmentation 생성
    color_mask = np.zeros((*seg_array.shape, 3), dtype=np.uint8)
    for label in np.unique(seg_array):
        if label == 0:
            continue
        if label < len(GOLIATH_PALETTE):
            color = GOLIATH_PALETTE[label]
        else:
            color = [128, 128, 128]
        color_mask[seg_array == label] = color

    edge_overlay = np.zeros_like(color_mask)
    edge_overlay[edge_img > 0] = [255, 255, 255]
    combined = np.clip(color_mask + edge_overlay, 0, 255)

    # ▶ pose 결과 불러오기 (.json)
    json_path = os.path.join(pose_json_dir, f"{name}.json")
    if os.path.exists(json_path):
        with open(json_path) as f:
            data = json.load(f)

        try:
            keypoints = np.array(data["instance_info"][0]["keypoints"])
            scores = np.array(data["instance_info"][0]["keypoint_scores"])
        except (KeyError, IndexError):
            print(f"⚠️ {name}에서 pose 정보가 없습니다.")
            keypoints, scores = None, None

        if keypoints is not None:
            # ▶ Keypoint 원 그리기
            for i, (x, y) in enumerate(keypoints):
                if scores[i] > 0.3:
                    cv2.circle(combined, (int(x), int(y)), 3, (0, 255, 0), -1)  # 초록색

            # ▶ 관절 연결선 그리기
            for i1, i2 in SKELETON:
                if scores[i1] > 0.3 and scores[i2] > 0.3:
                    pt1 = tuple(map(int, keypoints[i1]))
                    pt2 = tuple(map(int, keypoints[i2]))
                    cv2.line(combined, pt1, pt2, (0, 255, 255), 2)  # 노랑색 선

    # ▶ 최종 저장
    save_path = os.path.join(combined_output_dir, f"{name}_seg_colored_edge_pose.png")
    cv2.imwrite(save_path, combined)

print("✅ segmentation + pose skeleton 합성 이미지 저장 완료!")
print(f"저장 위치: {combined_output_dir}")
