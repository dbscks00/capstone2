#!/bin/bash

# 작업 디렉토리로 이동
cd ../../.. || exit

# TorchScript 모드 설정
MODE='torchscript'
SAPIENS_CHECKPOINT_ROOT=/home/jyc/sapiens_lite_host
SAPIENS_CHECKPOINT_ROOT=$SAPIENS_CHECKPOINT_ROOT/$MODE

# 입력/출력/세그 경로 설정
INPUT='/home/jyc/sapiens/input_image/aiimage/test'
SEG_DIR="/home/jyc/sapiens/output_image/sapiens_1b/seg/aiimage/ftest"
OUTPUT="/home/jyc/sapiens/output_image/normal/ftest"
MODEL_NAME='sapiens_1b'
CHECKPOINT="$SAPIENS_CHECKPOINT_ROOT/normal/sapiens_1b_normal_render_people_epoch_115_torchscript.pt2"
OUTPUT="$OUTPUT/$MODEL_NAME/normal"

echo "Using checkpoint: $CHECKPOINT"

RUN_FILE='/home/jyc/sapiens/lite/demo/vis_normal.py'
JOBS_PER_GPU=1; TOTAL_GPUS=1; VALID_GPU_IDS=(0)
BATCH_SIZE=8

IMAGE_LIST="${INPUT}/image_list.txt"
find "${INPUT}" -type f \( -iname \*.jpg -o -iname \*.png \) | sort > "${IMAGE_LIST}"

if [ ! -s "${IMAGE_LIST}" ]; then
  echo "No images found. Check your input directory and permissions."
  exit 1
fi

NUM_IMAGES=$(wc -l < "${IMAGE_LIST}")
if ((TOTAL_GPUS > NUM_IMAGES / BATCH_SIZE)); then
  TOTAL_JOBS=$(( (NUM_IMAGES + BATCH_SIZE - 1) / BATCH_SIZE))
  IMAGES_PER_FILE=$((BATCH_SIZE))
  EXTRA_IMAGES=$((NUM_IMAGES - ((TOTAL_JOBS - 1) * BATCH_SIZE)  ))
else
  TOTAL_JOBS=$((JOBS_PER_GPU * TOTAL_GPUS))
  IMAGES_PER_FILE=$((NUM_IMAGES / TOTAL_JOBS))
  EXTRA_IMAGES=$((NUM_IMAGES % TOTAL_JOBS))
fi

export TF_CPP_MIN_LOG_LEVEL=2
echo "Distributing ${NUM_IMAGES} image paths into ${TOTAL_JOBS} jobs."

for ((i=0; i<TOTAL_JOBS; i++)); do
  TEXT_FILE="${INPUT}/image_paths_$((i+1)).txt"
  if [ $i -eq $((TOTAL_JOBS - 1)) ]; then
    tail -n +$((IMAGES_PER_FILE * i + 1)) "${IMAGE_LIST}" > "${TEXT_FILE}"
  else
    head -n $((IMAGES_PER_FILE * (i + 1))) "${IMAGE_LIST}" | tail -n ${IMAGES_PER_FILE} > "${TEXT_FILE}"
  fi
done

for ((i=0; i<TOTAL_JOBS; i++)); do
  GPU_ID=$((i % TOTAL_GPUS))
  CUDA_VISIBLE_DEVICES=${VALID_GPU_IDS[GPU_ID]} python ${RUN_FILE} \
    ${CHECKPOINT} \
    --input "${INPUT}/image_paths_$((i+1)).txt" \
    --seg_dir ${SEG_DIR} \
    --batch-size="${BATCH_SIZE}" \
    --output-root="${OUTPUT}"
  sleep 1
done

wait

rm "${IMAGE_LIST}"
for ((i=0; i<TOTAL_JOBS; i++)); do
  rm "${INPUT}/image_paths_$((i+1)).txt"
done

cd -
echo "Processing complete. Results saved to $OUTPUT"