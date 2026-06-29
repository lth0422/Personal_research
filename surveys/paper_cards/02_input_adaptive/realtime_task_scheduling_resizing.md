# Real-time task scheduling with image resizing for criticality-based machine perception

- **그룹**: 2 input_adaptive
- **출처/연도**: Real-Time Systems 2022
- **저자**: Yigong Hu, Shengzhong Liu, Tarek Abdelzaher, Maggie Wigness, Philip David

## 두 질문
- **가변 변수**: segment resize size, segment merge decision, YOLO input size
- **트리거**: criticality, LiDAR 기반 distance cue, frame interval 기반 load

## 요점
- 플랫폼: NVIDIA Jetson AGX Xavier, embedded GPU
- 도메인: autonomous driving 기반 visual machine perception
- 핵심 방법: LiDAR point cloud로 빠르게 image segment를 만들고, noisy segmentation을 보정하기 위해 segment merge와 resizing을 함께 결정한다. downstream detector는 YOLOv5이며, 여러 입력 크기의 네트워크를 사용한다.
- 정식화/수식: resize-merge scheduling problem으로 표현하고, 선택된 segment의 크기와 merge 여부를 정해 frame interval 내 처리하도록 한다.

## 내 연구 관점
- 한 줄 gap: 입력 크기와 scheduling을 연결하지만 vision segment와 LiDAR cue에 초점이 있으며, vibration window의 물리 정보 보존 제약이나 PREEMPT_RT/MCU-SBC 비교는 다루지 않는다.
- 내 연구에 쓸 곳: input resizing이 단순 모델 최적화가 아니라 scheduling decision variable이 될 수 있음을 보이는 관련연구로 활용 가능하다.
- 인용할 문장: 없음

