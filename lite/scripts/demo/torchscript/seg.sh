#!/bin/bash

cd ../../.. || exit

# 체크포인트 루트 경로 설정
SAPIENS_CHECKPOINT_ROOT='/home/jyc/sapiens_lite_host/torchscript/seg'

MODE='torchscript' ## original. no optimizations (slow). full precision inference.
# MODE='bfloat16' ## A100 gpus. faster inference at bfloat16

#----------------------------set your input and output directories----------------------------------------------
# 테스트용
INPUT='/home/jyc/sapiens/input_image/aiimage/test'  # 입력 이미지 경로
OUTPUT="/home/jyc/sapiens/output_image/sapiens_1b/seg/aiimage/ftest"  # 출력 이미지 경로

#데모용
#INPUT='/home/jyc/sapiens/input_image/demo'  # 입력 이미지 경로
#OUTPUT="/home/jyc/sapiens/output_image/sapiens_1b/seg/demo"  # 출력 이미지 경로

#--------------------------MODEL CARD---------------
MODEL_NAME='sapiens_1b'
CHECKPOINT="$SAPIENS_CHECKPOINT_ROOT/sapiens_1b_goliath_best_goliath_mIoU_7994_epoch_151_$MODE.pt2"

# OUTPUT="$OUTPUT/$MODEL_NAME/seg"

##-------------------------------------inference-------------------------------------
RUN_FILE='/home/jyc/sapiens/lite/demo/vis_seg.py'

## number of inference jobs per gpu, total number of gpus and gpu ids
JOBS_PER_GPU=1; TOTAL_GPUS=1; VALID_GPU_IDS=(3)

BATCH_SIZE=8

# Find all images and sort them, then write to a temporary text file
IMAGE_LIST="${INPUT}/image_list.txt"
find "${INPUT}" -type f \( -iname \*.jpg -o -iname \*.png \) | sort > "${IMAGE_LIST}"

# Check if image list was created successfully
if [ ! -s "${IMAGE_LIST}" ]; then
  echo "No images found. Check your input directory and permissions."
  exit 1
fi

# Count images and calculate the number of images per text file
NUM_IMAGES=$(wc -l < "${IMAGE_LIST}")
if ((TOTAL_GPUS > NUM_IMAGES / BATCH_SIZE)); then
  TOTAL_JOBS=$(( (NUM_IMAGES + BATCH_SIZE - 1) / BATCH_SIZE))
  IMAGES_PER_FILE=$((BATCH_SIZE))
  EXTRA_IMAGES=$((NUM_IMAGES - ((TOTAL_JOBS - 1) * BATCH_SIZE)))
else
  TOTAL_JOBS=$((JOBS_PER_GPU * TOTAL_GPUS))
  IMAGES_PER_FILE=$((NUM_IMAGES / TOTAL_JOBS))
  EXTRA_IMAGES=$((NUM_IMAGES % TOTAL_JOBS))
fi

export TF_CPP_MIN_LOG_LEVEL=2
echo "Distributing ${NUM_IMAGES} image paths into ${TOTAL_JOBS} jobs."

# Divide image paths into text files for each job
for ((i=0; i<TOTAL_JOBS; i++)); do
  TEXT_FILE="${INPUT}/image_paths_$((i+1)).txt"
  if [ $i -eq $((TOTAL_JOBS - 1)) ]; then
    # For the last text file, write all remaining image paths
    tail -n +$((IMAGES_PER_FILE * i + 1)) "${IMAGE_LIST}" > "${TEXT_FILE}"
  else
    # Write the exact number of image paths per text file
    head -n $((IMAGES_PER_FILE * (i + 1))) "${IMAGE_LIST}" | tail -n ${IMAGES_PER_FILE} > "${TEXT_FILE}"
  fi
done

# Run the process on the GPUs, allowing multiple jobs per GPU
for ((i=0; i<TOTAL_JOBS; i++)); do
  GPU_ID=$((i % TOTAL_GPUS))
  echo "Using checkpoint: ${CHECKPOINT}"  # 추가된 디버깅 출력
  CUDA_VISIBLE_DEVICES=${VALID_GPU_IDS[GPU_ID]} python ${RUN_FILE} \
    ${CHECKPOINT} \
    --input "${INPUT}/image_paths_$((i+1)).txt" \
    --batch-size="${BATCH_SIZE}" \
    --output-root="${OUTPUT}" 
  sleep 1
done

# Wait for all background processes to finish
wait

# Remove the image list and temporary text files
rm "${IMAGE_LIST}"
for ((i=0; i<TOTAL_JOBS; i++)); do
  rm "${INPUT}/image_paths_$((i+1)).txt"
done

# Go back to the original script's directory
cd -

echo "Processing complete."
echo "Results saved to $OUTPUT"
