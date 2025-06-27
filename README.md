# 👤 Human Part Segmentation 기반 눈바디 데이터화 시스템

본 프로젝트는 인체 부위 분할(Human Part Segmentation) 및 자세 추정(Pose Estimation) 기술을 기반으로, 별도의 센서 없이도 **단일 카메라 이미지만으로 신체 변화를 자동 분석하고 시각화**할 수 있는 시스템을 구현하는 것을 목표로 합니다.  
사용자는 일반적인 스마트폰 또는 카메라를 통해 촬영한 전신 이미지를 업로드함으로써, **신체 부위별 변화**, **자세 분석**, **시각적 비교(GIF 생성)** 등을 손쉽게 확인할 수 있습니다.
![4in1 요약 이미지](https://github.com/dbscks00/capstone2/blob/main/output_image/summary_4in1/img5_4in1.jpg?raw=true)


---

## 🧩 프로젝트 개요

- **프로젝트명**: Human Part Segmentation을 활용한 눈바디의 데이터화
- **소속**: 중앙대학교 캡스톤디자인 Team 2
- **팀원**: 성의인, 전윤찬, 지승후
- **개발기간**: 2024년 3월 ~ 6월

---

## 🎯 목표 및 필요성

- 기존 눈바디는 **주관적 판단**에 의존하여 비교 기준이 모호하고 부정확함
- **고가의 3D 스캐너/체성분 장비 없이**, 단순한 이미지 입력만으로 정량적 변화 분석이 가능한 시스템 제안
- 누구나 쉽게 사용할 수 있고, **비접촉/저비용/자동화된 헬스케어 기술**로의 확장 가능성 확보

---

## ⚙️ 시스템 구성

1. **입력**: 사용자 정면 전신 이미지
2. **AI 분석 (서버)**:
   - 인체 부위 분할 (Segmentation)
   - 자세 추정 (Pose Estimation)
   - Depth Estimation (깊이 분석)
   - Surface Normal Estimation (표면 방향 분석)
3. **시각화**:
   - 부위별 면적 강조 이미지
   - 자세 skeleton 이미지
   - 시계열 비교용 GIF 자동 생성
4. **출력**:
   - `output_image/` 폴더에 결과 저장

---

## 🧠 사용된 주요 기술

| 기술 요소 | 설명 |
|-----------|------|
| Semantic Segmentation | SAPIENS 기반 인체 부위 분할, 28개 클래스 기준 |
| Pose Estimation       | Detectron2 기반의 포즈 추정 |
| Depth & Normal Estimation | OpenCV 기반 후처리 (선택적) |
| Python/OpenCV         | 전체 파이프라인 구현 및 시각화 |

---

## 🗂️ 프로젝트 구조

```bash
capstone2/             
├── input_image/         # 사용자 입력 이미지
├── output_image/        # 처리된 출력 이미지
├── seg/                 # 인체 부위 분할(Segmentation) 관련 
├── pose/                # 자세 추정(Pose Estimation) 관련 
├── estimate_muscle/     # 28개의 class를 5개로 재분할
├── engine/              # 추론 및 파이프라인 엔진
├── demo/                # 데모 실행 스크립트
├── server.py            # 웹 서버 실행 파일
├── make_gif.py          # 이미지 시퀀스를 GIF로 변환
├── image_resize.py      # 이미지 전처리 도구
├── README.md            # 프로젝트 설명서
└── LICENSE              # 라이선스 정보
```
