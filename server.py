from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)

# GPU디바이스 설정
# env = os.environ.copy()
# env["CUDA_VISIBLE_DEVICES"] = "3"

INPUT_DIR = '/home/jyc/sapiens/input_image/demo'
OUTPUT_DIR = '/home/jyc/sapiens/output_image/sapiens_1b/seg/demo'
SCRIPT_PATH = '/home/jyc/sapiens/lite/scripts/demo/torchscript/seg.sh'

@app.route('/upload', methods=['POST'])
def upload_image():
    os.makedirs(INPUT_DIR, exist_ok = True)

    # 기존 이미지 삭제부분
    for f in os.listdir(INPUT_DIR):
        os.remove(os.path.join(INPUT_DIR, f))

    files = request.files.getlist('images')
    for f in files:
        f.save(os.path.join(INPUT_DIR, f.filename))

    result = subprocess.run([SCRIPT_PATH], capture_output=True, text=True, cwd=os.path.dirname(SCRIPT_PATH))


    filename = files[0].filename
    result_filename = filename.rsplit('.', 1)[0] + '.jpg'

    return jsonify({
        'status': 'done',
        'stdout': result.stdout,
        'stderr': result.stderr,
        'result_url': f'http://127.0.0.1:5000/results/{result_filename}'
    })

@app.route('/results/<filename>')
def get_result(filename):
    return send_from_directory(OUTPUT_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)