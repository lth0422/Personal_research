# Evaluating Real-Time Pattern Recognition in Autonomous Systems on COTS Hardware

- **그룹**: 6 platform_preempt_rt
- **출처/연도**: M.Sc. thesis 2025
- **저자**: Akshay Jitendrabhai Vaghasiya

## 두 질문
- **가변 변수**: real-time extension/configuration, workload condition.
- **트리거**: offline benchmarking under workload and timing constraints.

## 요점
- 플랫폼: Raspberry Pi platform.
- 도메인: real-time object detection/pattern recognition for autonomous systems.
- 핵심 방법: Xenomai 3, Xenomai 4, PREEMPT-RT를 Raspberry Pi object detection workload에서 비교하고 latency, jitter, responsiveness, deadline 유지 능력을 평가한다.
- 정식화/수식: 확인 필요.

## 내 연구 관점
- 한 줄 gap: pattern recognition/object detection 중심이며 vibration FD pipeline과 Pi Zero 2W/PREEMPT_RT 조건은 별도 검증이 필요하다.
- 내 연구에 쓸 곳: PREEMPT_RT와 Xenomai 비교 배경, COTS hardware에서 inference workload를 timing 측면으로 평가하는 사례.
- 인용할 문장: "latency, jitter"

## 불확실한 점
- 확인 필요: thesis 문헌이므로 원고 인용 전 공개성, bibliographic status, 실험 platform 세부조건을 확인해야 한다.
- 확인 필요: Raspberry Pi model, object detection model, exact workload, deadline/miss 결과는 본문에서 재확인해야 한다.
