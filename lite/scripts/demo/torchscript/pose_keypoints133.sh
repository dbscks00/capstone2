#!/bin/bash

cd ../../.. || exit
SAPIENS_CHECKPOINT_ROOT='/home/jyc/sapiens_lite_host/torchscript/pose'

MODE='torchscript' ## original. no optimizations (slow). full precision inference.
# MODE='bfloat16' ## A100 gpus. faster inference at bfloat16

SAPIENS_CHECKPOINT_ROOT=$SAPIENS_CHECKPOINT_ROOT

#----------------------------set your input and output directories----------------------------------------------
INPUT='/home/jyc/sapiens/input_image'  # 입력 이미지 경로
OUTPUT="/home/jyc/sapiens/output_image"  # 출력 이미지 경로

#--------------------------MODEL CARD---------------
MODEL_NAME='sapiens_1b' 
CHECKPOINT=$SAPIENS_CHECKPOINT_ROOT/sapiens_1b_coco_best_coco_AP_821_torchscript.pt2
# MODEL_NAME='sapiens_0.6b'; CHECKPOINT=$SAPIENS_CHECKPOINT_ROOT/pose/checkpoints/sapiens_0.6b/sapiens_0.6b_coco_wholebody_best_coco_wholebody_AP_695_$MODE.pt2
# MODEL_NAME='sapiens_1b'; CHECKPOINT=$SAPIENS_CHECKPOINT_ROOT/pose/checkpoints/sapiens_1b/sapiens_1b_coco_wholebody_best_coco_wholebody_AP_727_$MODE.pt2
# MODEL_NAME='sapiens_2b'; CHECKPOINT=$SAPIENS_CHECKPOINT_ROOT/pose/checkpoints/sapiens_2b/sapiens_2b_coco_wholebody_best_coco_wholebody_AP_745_$MODE.pt2

OUTPUT="$OUTPUT/$MODEL_NAME/pose"

#DETECTION_CONFIG_FILE='../pose/demo/mmdetection_cfg/rtmdet_m_640-8xb32_coco-person_no_nms.py'
#DETECTION_CHECKPOINT=$SAPIENS_CHECKPOINT_ROOT/detector/checkpoints/rtmpose/rtmdet_m_8xb32-100e_coco-obj365-person-235e8209.pth

#---------------------------VISUALIZATION PARAMS--------------------------------------------------
LINE_THICKNESS=3 ## line thickness of the skeleton
RADIUS=6 ## keypoint radius
KPT_THRES=0.3 ## confidence threshold

##-------------------------------------inference-------------------------------------
RUN_FILE='demo/vis_pose.py'



## number of inference jobs per gpu, total number of gpus and gpu ids
# JOBS_PER_GPU=1; TOTAL_GPUS=8; VALID_GPU_IDS=(0 1 2 3 4 5 6 7)
JOBS_PER_GPU=1; TOTAL_GPUS=1; VALID_GPU_IDS=(0)

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
TOTAL_JOBS=$(( (NUM_IMAGES + BATCH_SIZE - 1) / BATCH_SIZE )) # 전체 작업 수 계산
IMAGES_PER_JOB=$(( (NUM_IMAGES + TOTAL_JOBS - 1) / TOTAL_JOBS )) # 각 작업당 이미지 수 계산

export TF_CPP_MIN_LOG_LEVEL=2
echo "Distributing ${NUM_IMAGES} image paths into ${TOTAL_JOBS} jobs."

# Divide image paths into text files for each job
for ((i=0; i<TOTAL_JOBS; i++)); do
  TEXT_FILE="${INPUT}/image_paths_$((i+1)).txt"
  START_LINE=$((i * IMAGES_PER_JOB + 1))
  END_LINE=$(( (i + 1) * IMAGES_PER_JOB ))

  # 이미지 수가 전체 이미지 수를 초과하지 않도록 조정
  if (( END_LINE > NUM_IMAGES )); then
    END_LINE=$NUM_IMAGES
  fi

  # head 와 tail을 사용하여 이미지 목록 추출
  head -n ${END_LINE} "${IMAGE_LIST}" | tail -n $((END_LINE - START_LINE + 1)) > "${TEXT_FILE}"
done

# Run the process on the GPUs, allowing multiple jobs per GPU
for ((i=0; i<TOTAL_JOBS; i++)); do
  GPU_ID=$((i % TOTAL_GPUS))
  CUDA_VISIBLE_DEVICES=${VALID_GPU_IDS[GPU_ID]} python ${RUN_FILE} ${CHECKPOINT} \
    --num_keypoints 17 \
    --batch-size ${BATCH_SIZE} \
    --input "${INPUT}/image_paths_$((i+1)).txt" \
    --output-root="${OUTPUT}" \
    --radius ${RADIUS} \
    --kpt-thr ${KPT_THRES}
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
