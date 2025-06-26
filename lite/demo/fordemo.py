import os
import cv2
import numpy as np

# 경로 설정
input_dir = "/home/jyc/sapiens/input_image"
seg_dir = "/home/jyc/sapiens/output_image/sapiens_1b/seg/"
depth_dir = "/home/jyc/sapiens/output_image/sapiens_1b/depth"
pose_dir = "/home/jyc/sapiens/output_image/sapiens_1b/pose"

output_dir = "/home/jyc/sapiens/output_image/sapiens_1b/summary_4in1"
os.makedirs(output_dir, exist_ok=True)

print("🔄 4-in-1 이미지 생성 중...")

# 이미지 루프
for filename in sorted(os.listdir(input_dir)):
    if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    name = os.path.splitext(filename)[0]

    # 이미지 경로 설정
    original_path = os.path.join(input_dir, filename)
    seg_path = os.path.join(seg_dir, f"{name}.jpg")
    depth_path = os.path.join(depth_dir, f"{name}.jpg")
    pose_path = os.path.join(pose_dir, f"{name}.jpg")  # ✅ pose는 이미지로 처리

    # 원본 이미지 로드
    original = cv2.imread(original_path)
    if original is None:
        print(f"❌ 원본 로딩 실패: {original_path}")
        continue

    # 세그멘테이션 이미지 로드
    seg = cv2.imread(seg_path)
    if seg is None:
        print(f"⚠️ seg 없음: {seg_path}")
        seg = np.zeros_like(original)

    # 뎁스 이미지 로드
    depth = cv2.imread(depth_path)
    if depth is None:
        print(f"⚠️ depth 없음: {depth_path}")
        depth = np.zeros_like(original)

    # 포즈 이미지 로드 (JSON X)
    pose_img = cv2.imread(pose_path)
    if pose_img is None:
        print(f"⚠️ pose 이미지 없음: {pose_path}")
        pose_img = np.zeros_like(original)

    # 크기 통일
    target_size = (512, 512)
    original = cv2.resize(original, target_size)
    seg = cv2.resize(seg, target_size)
    depth = cv2.resize(depth, target_size)
    pose_img = cv2.resize(pose_img, target_size)

    # 2x2 결합
    top = cv2.hconcat([original, seg])
    bottom = cv2.hconcat([depth, pose_img])
    final = cv2.vconcat([top, bottom])

    # 저장
    save_path = os.path.join(output_dir, f"{name}_4in1.jpg")
    cv2.imwrite(save_path, final)
    print(f"✅ 저장 완료: {save_path}")

print("🎉 모든 4-in-1 이미지 생성 완료!")
