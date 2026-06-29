# Generalized self-cueing real-time attention scheduling with intermittent inspection and image resizing

- **그룹**: 2 input_adaptive
- **출처/연도**: Real-Time Systems 2023
- **저자**: Shengzhong Liu, Xinzhe Fu, Yigong Hu, Maggie Wigness, Philip David, Shuochao Yao, Lui Sha, Tarek Abdelzaher

## 두 질문
- **가변 변수**: object inspection frequency, target image size, task batching
- **트리거**: object criticality, object motion/location uncertainty, object size, workload

## 요점
- 플랫폼: NVIDIA Jetson Xavier, embedded GPU
- 도메인: autonomous driving 기반 visual machine perception
- 핵심 방법: self-cueing으로 object region을 추적하고, full-frame inspection 사이에 object별 partial inspection을 scheduling한다. GBPB 알고리즘은 intermittent inspection, image resizing, batching을 함께 결정해 generalized uncertainty를 줄인다.
- 정식화/수식: location uncertainty와 resizing으로 인한 accuracy degradation factor를 함께 고려하는 generalized system uncertainty 최소화 문제로 정식화한다.

## 내 연구 관점
- 한 줄 gap: criticality와 uncertainty 기반으로 resizing과 inspection frequency를 조절하지만, 기계 결함 상태의 anomaly score와 system slack을 함께 쓰는 vibration FD scheduling은 아니다.
- 내 연구에 쓸 곳: 본 연구의 `W + H + M` 중 `입력 크기 + 검사 빈도`에 가까운 vision-domain 비교군으로 활용 가능하다.
- 인용할 문장: 없음

