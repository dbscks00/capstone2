import os
from PIL import Image

input_dir = '/home/jyc/sapiens/input_image'
target_size = (1024, 768)

for filename in os.listdir(input_dir):
    if filename.lower().endswith(('.jpeg', '.png', '.jpg')):
        original_path = os.path.join(input_dir, filename)

        try:
            with Image.open(original_path) as img:
                img = img.convert('RGB')
                img.thumbnail(target_size, Image.LANCZOS)

                new_img = Image.new('RGB', target_size, (255, 255, 255))
                offset_x = (target_size[0] - img.width) // 2
                offset_y = (target_size[1] - img.height) // 2
                new_img.paste(img, (offset_x, offset_y))

                # .jpg로 저장 (기존 확장자 무시)
                base_name = os.path.splitext(filename)[0]
                new_img_path = os.path.join(input_dir, f"{base_name}.jpg")

                # 항상 덮어쓰기
                new_img.save(new_img_path, format='JPEG', quality=95)
                print(f"{filename} → {base_name}.jpg 저장 완료.")

            # 원본이 .jpg가 아니면 삭제
            if not filename.lower().endswith('.jpg'):
                os.remove(original_path)
                print(f"{filename} 원본 삭제 완료.")
        except Exception as e:
            print(f"{filename} 처리 중 오류: {e}")

print("모든 이미지 변환 및 정리 완료.")
