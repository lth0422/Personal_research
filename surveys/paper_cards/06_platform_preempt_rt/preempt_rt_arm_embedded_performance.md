# Performance Assessment of Linux Kernels with PREEMPT_RT on ARM-Based Embedded Devices

- **그룹**: 6 platform_preempt_rt
- **출처/연도**: Electronics 2021, 10, 1331
- **저자**: George K. Adam, Nikos Petrellis, Lambros T. Doulos

## 두 질문
- **가변 변수**: 없음. 비교 조건은 Linux kernel/distribution의 PREEMPT_RT 적용 여부.
- **트리거**: 없음. 실험적 latency evaluation 논문이며 runtime adaptation을 다루지 않는다.

## 요점
- 플랫폼: Raspberry Pi 3, BeagleBone AI.
- 도메인: ARM-based embedded Linux real-time performance evaluation.
- 핵심 방법 (2~3줄): PREEMPT_RT가 적용된 Linux kernel과 default kernel의 real-time latency를 비교한다. cyclictest와 별도 response/periodic task measurement modules를 사용해 user/kernel space latency, maximum sustained frequency, cyclictest latency를 측정한다.
- 정식화/수식 (있으면): response task의 worst-case response latency를 event arrival부터 task가 running state로 전환되어 결과를 내는 시점까지의 시간으로 정의한다.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): Pi Zero 2W, TFLite inference pipeline, vibration fault diagnosis deadline miss는 다루지 않는다.
- 내 연구에 쓸 곳: PREEMPT_RT 적용 여부를 먼저 cyclictest와 latency distribution으로 검증해야 한다는 실험 방법 근거.
- 인용할 문장 (있으면, 15단어 이내): "worst-case latencies are reduced"

## 불확실한 점
- 확인 필요: 150 us upper bound, 118 us average maximum latency 등 수치는 platform/kernel/distribution 조건별로 나뉘므로 manuscript 인용 전 Table 4와 관련 figure를 재확인해야 한다.
