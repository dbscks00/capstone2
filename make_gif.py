from PIL import Image
import os

# 이미지 파일 경로 리스트 (순서 중요)
image_paths = [
    "/home/jyc/sapiens/output_image/normal/fat/sapiens_1b/normal/img120.png",
    "/home/jyc/sapiens/output_image/normal/fat/sapiens_1b/normal/img110.png",
    "/home/jyc/sapiens/output_image/normal/fat/sapiens_1b/normal/img105.png",
    "/home/jyc/sapiens/output_image/normal/fat/sapiens_1b/normal/img100.png",
    "/home/jyc/sapiens/output_image/normal/fat/sapiens_1b/normal/img95.png",
    "/home/jyc/sapiens/output_image/normal/fat/sapiens_1b/normal/img90.png",
    "/home/jyc/sapiens/output_image/normal/fat/sapiens_1b/normal/img85.png"
]

# 이미지 열기
images = [Image.open(path) for path in image_paths]

# GIF로 저장
images[0].save(
    "output.gif",             # 저장할 파일명
    save_all=True,            # 모든 프레임 저장
    append_images=images[1:], # 나머지 프레임 추가
    duration=200,             # 각 프레임당 지속 시간 (ms)
    loop=0                    # 0이면 무한 반복
)
