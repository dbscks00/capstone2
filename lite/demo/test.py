import cv2
import mediapipe as mp

# 사용자 키 입력 받기
USER_HEIGHT_CM = float(input("📏 키(cm)를 입력하세요: "))

# Mediapipe Pose 초기화
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(static_image_mode=True)

# 이미지 불러오기
image_path = "/mnt/data/test1.jpg"
image = cv2.imread(image_path)
image_height, image_width = image.shape[:2]

# Mediapipe로 포즈 추출
results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

# 어깨 너비 계산 및 시각화
if results.pose_landmarks:
    landmarks = results.pose_landmarks.landmark
    left_shoulder = landmarks[11]  # 좌측 어깨
    right_shoulder = landmarks[12]  # 우측 어깨

    # 픽셀 거리 계산
    pixel_dist = ((left_shoulder.x - right_shoulder.x) ** 2 +
                  (left_shoulder.y - right_shoulder.y) ** 2) ** 0.5
    pixel_dist *= image_height  # 정규화된 좌표 → 실제 픽셀 거리 변환

    # 실측 변환 (키 기반 비율)
    pixel_per_cm = image_height / USER_HEIGHT_CM
    shoulder_width_cm = pixel_dist / pixel_per_cm

    # 🎨 어깨 좌표를 이미지에 표시
    left_x, left_y = int(left_shoulder.x * image_width), int(left_shoulder.y * image_height)
    right_x, right_y = int(right_shoulder.x * image_width), int(right_shoulder.y * image_height)

    # 어깨 위치에 원 그리기
    cv2.circle(image, (left_x, left_y), 5, (0, 255, 0), -1)
    cv2.circle(image, (right_x, right_y), 5, (0, 255, 0), -1)

    # 어깨를 잇는 선 그리기
    cv2.line(image, (left_x, left_y), (right_x, right_y), (0, 255, 0), 2)

    # 어깨 너비 텍스트 표시
    cv2.putText(image, f"Shoulder Width: {shoulder_width_cm:.2f} cm", 
                (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # 결과 이미지 저장
    output_path = "/home/jyc/sapiens/input_image"
    cv2.imwrite(output_path, image)
    print(f"✅ 결과 이미지 저장 완료: {output_path}")

else:
    print("⚠️ 포즈를 감지하지 못했습니다. 다른 사진을 사용해 보세요.")
