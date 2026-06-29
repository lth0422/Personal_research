# On Exploring Image Resizing for Optimizing Criticality-based Machine Perception

- **그룹**: 2 input_adaptive
- **출처/연도**: IEEE RTCSA 2021
- **저자**: Yigong Hu, Shengzhong Liu, Tarek Abdelzaher, Maggie Wigness, Philip David

## 두 질문
- **가변 변수**: 입력 segment size, resizing level, 대응 inference model size
- **트리거**: criticality, frame interval 기반 load, offline profiling된 accuracy/time profile

## 요점
- 플랫폼: NVIDIA Jetson AGX Xavier, embedded GPU
- 도메인: autonomous driving 기반 visual machine perception
- 핵심 방법: frame을 segment로 나눈 뒤 criticality에 따라 segment resize와 model choice를 결정한다. 덜 중요한 segment는 작은 입력과 작은 모델로 처리해 response time과 deadline miss를 줄이고, 중요한 segment에는 더 높은 fidelity를 배정한다.
- 정식화/수식: perception task의 input size와 model choice를 quality/latency trade-off point로 보고, frame interval 내 deadline miss 여부와 normalized accuracy를 비교한다.

## 내 연구 관점
- 한 줄 gap: vision perception의 입력 크기 조절과 criticality scheduling을 다루지만, 진동 fault diagnosis의 window size, machine condition, system slack 결합은 다루지 않는다.
- 내 연구에 쓸 곳: related work의 input-adaptive perception 비교군. 입력 크기 조절이 latency/accuracy trade-off를 만드는 선행 사례로 활용 가능하다.
- 인용할 문장: 없음

