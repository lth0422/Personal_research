# Development of a Low-Cost Vision-Based Real-Time Displacement System Using Raspberry Pi

- **그룹**: 6 platform_preempt_rt
- **출처/연도**: Engineering Structures 2023
- **저자**: Miaomin Wang, Ki-Young Koo, Chunyu Liu, Fuyou Xu

## 두 질문
- **가변 변수**: image processing configuration. Runtime adaptation variable은 확인되지 않음.
- **트리거**: 없음 또는 offline/system design.

## 요점
- 플랫폼: Raspberry Pi 4 Model B.
- 도메인: vision-based real-time displacement measurement for structural health monitoring.
- 핵심 방법: SBC에서 동작하는 빠른 image processing software를 만들고 Raspberry Pi 기반 low-cost portable displacement measurement system을 구성한다. Long-span suspension bridge field application에서 multipoint structural displacement를 real-time 측정한다.
- 정식화/수식: ZNCC tracking과 Lanczos interpolation 사용. 세부 수식은 확인 필요.

## 내 연구 관점
- 한 줄 gap: Raspberry Pi 실시간 측정 시스템 사례지만 PREEMPT_RT, vibration FD inference, deadline miss/jitter 분석은 다루지 않는다.
- 내 연구에 쓸 곳: SBC 기반 real-time sensing/measurement application 배경.
- 인용할 문장: "Raspberry Pi"

## 불확실한 점
- 확인 필요: 실시간 sampling/update rate, CPU load, latency 수치는 본문 실험표에서 재확인해야 한다.
- 확인 필요: PREEMPT_RT 관련 논문은 아니므로 platform_preempt_rt 그룹 내에서는 low-priority background로만 사용한다.
