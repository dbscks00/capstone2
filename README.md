<!--
<p align="center">
  <img src="./assets/sapiens_animation.gif" alt="Sapiens" title="Sapiens" width="500"/>
</p>

<p align="center">
   <h2 align="center">Foundation for Human Vision Models</h2>
   <p align="center">
      <a href="https://rawalkhirodkar.github.io/"><strong>Rawal Khirodkar</strong></a>
      ·
      <a href="https://scholar.google.ch/citations?user=oLi7xJ0AAAAJ&hl=en"><strong>Timur Bagautdinov</strong></a>
      ·
      <a href="https://una-dinosauria.github.io/"><strong>Julieta Martinez</strong></a>
      ·
      <a href="https://about.meta.com/realitylabs/"><strong>Su Zhaoen</strong></a>
      ·
      <a href="https://about.meta.com/realitylabs/"><strong>Austin James</strong></a>
      <br>
      <a href="https://www.linkedin.com/in/peter-selednik-05036499/"><strong>Peter Selednik</strong></a>
      .
      <a href="https://scholar.google.fr/citations?user=8orqBsYAAAAJ&hl=ja"><strong>Stuart Anderson</strong></a>
      .
      <a href="https://shunsukesaito.github.io/"><strong>Shunsuke Saito</strong></a>
   </p>
   <h3 align="center">ECCV 2024 - Best Paper Candidate</h3>
</p>

<p align="center">
   <a href='https://about.meta.com/realitylabs/codecavatars/sapiens/'>
      <img src='https://img.shields.io/badge/Sapiens-Page-azure?style=for-the-badge&logo=Google%20chrome&logoColor=white&labelColor=000080&color=007FFF' alt='Project Page'>
   </a>

   <a href="https://arxiv.org/abs/2408.12569">
      <img src='https://img.shields.io/badge/Paper-PDF-green?style=for-the-badge&logo=adobeacrobatreader&logoWidth=20&logoColor=white&labelColor=66cc00&color=94DD15' alt='Paper PDF'>
   </a>

   <a href='https://huggingface.co/collections/facebook/sapiens-66d22047daa6402d565cb2fc'>
      <img src='https://img.shields.io/badge/HuggingFace-Demo-orange?style=for-the-badge&logo=huggingface&logoColor=white&labelColor=FF5500&color=orange' alt='Spaces'>
   </a>

   <a href='https://rawalkhirodkar.github.io/sapiens/'>
      <img src='https://img.shields.io/badge/More-Results-ffffff?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0id2hpdGUiIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCI+PHBhdGggZD0iTTAgMGgyNHYyNEgweiIgZmlsbD0ibm9uZSIvPjxwYXRoIGQ9Ik0xOSAzSDVjLTEuMSAwLTIgLjktMiAydjE0YzAgMS4xLjkgMiAyIDJoMTRjMS4xIDAgMi0uOSAyLTJWNWMwLTEuMS0uOS0yLTItMnpNOSAxN0g3di01aDJ2NXptNCAwaC0ydi03aDJ2N3ptNCAwaC0yVjhoMnY5eiIvPjwvc3ZnPg==&logoColor=white&labelColor=8A2BE2&color=9370DB' alt='Results'>
   </a>
</p>

Sapiens offers a comprehensive suite for human-centric vision tasks (e.g., 2D pose, part segmentation, depth, normal, etc.). The model family is pretrained on 300 million in-the-wild human images and shows excellent generalization to unconstrained conditions. These models are also designed for extracting high-resolution features, having been natively trained at a 1024 x 1024 image resolution with a 16-pixel patch size.

<p align="center">
  <img src="./assets/01.gif" alt="01" title="01" width="400"/>
  <img src="./assets/03.gif" alt="03" title="03" width="400"/>
</p>
<p align="center">
  <img src="./assets/02.gif" alt="02" title="02" width="400"/>
  <img src="./assets/04.gif" alt="04" title="04" width="400"/>
</p>


## 🚀 Getting Started

### Clone the Repository
   ```bash
   git clone https://github.com/facebookresearch/sapiens.git
   export SAPIENS_ROOT=/path/to/sapiens
   ```

### Recommended: Lite Installation (Inference-only)
   For users setting up their own environment primarily for running existing models in inference mode, we recommend the [Sapiens-Lite installation](lite/README.md).\
   This setup offers optimized inference (4x faster) with minimal dependencies (only PyTorch + numpy + cv2).

### Full Installation
   To replicate our complete training setup, run the provided installation script. \
   This will create a new conda environment named `sapiens` and install all necessary dependencies.

   ```bash
   cd $SAPIENS_ROOT/_install
   ./conda.sh
   ```

   Please download the **original** checkpoints from [hugging-face](https://huggingface.co/facebook/sapiens). \
   You can be selective about only downloading the checkpoints of interest.\
   Set `$SAPIENS_CHECKPOINT_ROOT` to be the path to the `sapiens_host` folder. Place the checkpoints following this directory structure:
   ```plaintext
   sapiens_host/
   ├── detector/
   │   └── checkpoints/
   │       └── rtmpose/
   ├── pretrain/
   │   └── checkpoints/
   │       ├── sapiens_0.3b/
               ├── sapiens_0.3b_epoch_1600_clean.pth
   │       ├── sapiens_0.6b/
               ├── sapiens_0.6b_epoch_1600_clean.pth
   │       ├── sapiens_1b/
   │       └── sapiens_2b/
   ├── pose/
      └── checkpoints/
         ├── sapiens_0.3b/
   └── seg/
   └── depth/
   └── normal/
   ```

## 🌟 Human-Centric Vision Tasks
We finetune sapiens for multiple human-centric vision tasks. Please checkout the list below.

- ###  [Image Encoder](docs/PRETRAIN_README.md) <sup><small><a href="lite/docs/PRETRAIN_README.md" style="color: #FFA500;">[lite]</a></small></sup>
- ### [Pose Estimation](docs/POSE_README.md) <sup><small><a href="lite/docs/POSE_README.md" style="color: #FFA500;">[lite]</a></small></sup>
- ### [Body Part Segmentation](docs/SEG_README.md) <sup><small><a href="lite/docs/SEG_README.md" style="color: #FFA500;">[lite]</a></small></sup>
- ### [Depth Estimation](docs/DEPTH_README.md) <sup><small><a href="lite/docs/DEPTH_README.md" style="color: #FFA500;">[lite]</a></small></sup>
- ### [Surface Normal Estimation](docs/NORMAL_README.md) <sup><small><a href="lite/docs/NORMAL_README.md" style="color: #FFA500;">[lite]</a></small></sup>

## 🎯 Easy Steps to Finetuning Sapiens
Finetuning our models is super-easy! Here is a detailed training guide for the following tasks.
- ### [Pose Estimation](docs/finetune/POSE_README.md)
- ### [Body-Part Segmentation](docs/finetune/SEG_README.md)
- ### [Depth Estimation](docs/finetune/DEPTH_README.md)
- ### [Surface Normal Estimation](docs/finetune/NORMAL_README.md)

## 📈 Quantitative Evaluations
- ### [Pose Estimation](docs/evaluate/POSE_README.md)

## 🤝 Acknowledgements & Support & Contributing
We would like to acknowledge the work by [OpenMMLab](https://github.com/open-mmlab) which this project benefits from.\
For any questions or issues, please open an issue in the repository.\
See [contributing](CONTRIBUTING.md) and the [code of conduct](CODE_OF_CONDUCT.md).

## License
This project is licensed under [LICENSE](LICENSE).\
Portions derived from open-source projects are licensed under [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0).

## 📚 Citation
If you use Sapiens in your research, please consider citing us.
```bibtex
@article{khirodkar2024sapiens,
  title={Sapiens: Foundation for Human Vision Models},
  author={Khirodkar, Rawal and Bagautdinov, Timur and Martinez, Julieta and Zhaoen, Su and James, Austin and Selednik, Peter and Anderson, Stuart and Saito, Shunsuke},
  journal={arXiv preprint arXiv:2408.12569},
  year={2024}
}
```
-->

# Capstone 2 프로젝트
# 🧠 Human Part Segmentation 기반 눈바디 데이터화 프로젝트

본 프로젝트는 인체 부위 분할(Human Part Segmentation) 및 자세 추정(Pose Estimation) 기술을 활용하여 개인의 신체 변화를 자동으로 시각화하고 분석하는 시스템을 구축하는 것을 목표로 합니다. 사용자는 전신 정면 사진을 업로드함으로써 자신의 신체 데이터를 시각적으로 확인하고 변화 추이를 파악할 수 있습니다.

---

## 📌 프로젝트 개요

- **목표**: 눈바디(Body-check) 이미지 기반으로 신체 부위별 변화를 자동 추출하고, GIF 등으로 시각화하여 사용자가 쉽게 피드백 받을 수 있도록 지원
- **핵심 기능**
  - SAPIE 기반 인체 분할
  - Detectron2를 활용한 포즈 추정
  - 부위별 면적 계산을 통한 변화 추정
  - GIF 생성 및 시각화 이미지 저장
- **사용자 흐름**
  1. 정면 전신 사진 업로드
  2. 인체 부위 분할 및 포즈 추정
  3. 부위별 면적 계산 및 시각화
  4. 결과 이미지 및 GIF 저장/확인

---

## 📁 프로젝트 구조

capstone2/
│
├── input_image/ # 사용자 업로드 이미지 폴더
├── output_image/ # 처리된 결과 이미지 저장 폴더
├── seg/ # SAPIE 기반 분할 모듈
├── pose/ # Detectron2 기반 포즈 추정 모듈
├── estimate_muscle/ # 근육량 계산 관련 코드
├── demo/ # 데모 실행 샘플
├── docs/ # 보고서 등 문서 자료
├── image_resize.py # 이미지 크기 정규화 유틸
├── make_gif.py # 결과 이미지 기반 GIF 생성기
├── game.py # 메인 실행 스크립트 (콘솔 기반)
├── server.py # Flask 기반 웹 서버 실행 파일
└── output.gif # 최종 비교 결과를 담은 GIF 파일