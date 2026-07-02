# Real-Time Performance and Response Latency Measurements of Linux Kernels on Single-Board Computers

- **그룹**: 6 platform_preempt_rt
- **출처/연도**: Computers 2021
- **저자**: George K. Adam

## 두 질문
- **가변 변수**: Linux kernel configuration, PREEMPT_RT patch 여부.
- **트리거**: 없음. Offline benchmarking/evaluation.

## 요점
- 플랫폼: Raspberry Pi 3, BeagleBone Black.
- 도메인: Linux real-time performance and response latency measurement on SBCs.
- 핵심 방법: response and periodic task model 기반 measurement software로 user/kernel space latency를 측정하고 standard Linux와 PREEMPT_RT patched kernel을 비교한다. PREEMPT_RT가 worst-case latency를 줄인다고 보고한다.
- 정식화/수식: response latency and periodic task measurement model. 세부 수식은 본문 확인 필요.

## 내 연구 관점
- 한 줄 gap: kernel latency benchmark 중심이며 TFLite vibration FD pipeline latency와 deadline miss는 다루지 않는다.
- 내 연구에 쓸 곳: KSC 2026의 vanilla Linux vs PREEMPT_RT latency distribution 검증 배경.
- 인용할 문장: "PREEMPT_RT patch"

## 불확실한 점
- 확인 필요: 160 us upper bound는 platform/kernel/load 조건과 함께 인용해야 한다.
- 확인 필요: Pi Zero 2W로 직접 일반화하지 않아야 한다.
