import os
from transformers import AutoModel
from huggingface_hub import login

# 로그인 (토큰이 필요함)
login(token='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')

# 설정
MODE = 'torchscript'  # 또는 'bfloat16'
SAPIENS_LITE_CHECKPOINT_ROOT = f'/home/jyc/sapiens_lite_host/{MODE}/pretrain/checkpoints'

# 체크포인트 리스트 (필요에 따라 수정 가능)
checkpoints_to_download = [
    'sapiens_0.3b',  # 필요한 경우 다른 체크포인트 추가
]

# 체크포인트 다운로드
for checkpoint in checkpoints_to_download:
    model_name = f'sapiens_0.3b_epoch_1600_torchscript.pt2'  # Hugging Face 모델 이름
    model_path = os.path.join(SAPIENS_LITE_CHECKPOINT_ROOT, checkpoint)

    # 디렉토리 생성
    os.makedirs(model_path, exist_ok=True)

    # 모델 다운로드
    try:
        print(f"Downloading {model_name}...")
        model = AutoModel.from_pretrained(model_name)
        model.save_pretrained(model_path)
    except Exception as e:
        print(f"Error downloading {model_name}: {e}")

print("Download complete.")
