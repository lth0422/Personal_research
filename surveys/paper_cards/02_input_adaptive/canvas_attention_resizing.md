# Algorithms for Canvas-based Attention Scheduling with Resizing

- **그룹**: 2 input_adaptive
- **출처/연도**: IEEE RTAS 2024
- **저자**: Yigong Hu, Ila Gokarn, Shengzhong Liu, Archan Misra, Tarek Abdelzaher

## 두 질문
- **가변 변수**: focus locale size, resizing size, canvas packing decision
- **트리거**: object deadline, spatial size, workload, offline accuracy-resize profile

## 요점
- 플랫폼: NVIDIA Jetson AGX Xavier, embedded GPU
- 도메인: surveillance video 기반 visual machine perception
- 핵심 방법: focus locale을 fixed-size canvas frame에 packing하는 attention scheduling을 다룬다. 기존 quantized size 제약을 완화하고, arbitrary size object와 resizing을 포함한 spatiotemporal schedulability bound와 scheduling algorithm을 제안한다.
- 정식화/수식: object의 spatial volume과 inspection deadline을 함께 고려한 schedulability condition을 사용하고, resizing은 accuracy/resource trade-off를 조절하는 변수로 들어간다.

## 내 연구 관점
- 한 줄 gap: deadline-aware input resizing과 schedulability를 다루지만, vision canvas packing 문제이며 vibration window size, hop size, model selection의 fault diagnosis 문제와는 도메인이 다르다.
- 내 연구에 쓸 곳: deadline-aware inference + input size 조절의 강한 비교군. 본 연구의 window-size 제약과 deadline 제약을 설명할 때 관련연구로 활용 가능하다.
- 인용할 문장: 없음

