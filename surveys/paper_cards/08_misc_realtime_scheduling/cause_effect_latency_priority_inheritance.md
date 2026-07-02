# Optimizing End-to-End Latency of Sporadic Cause-Effect Chains Using Priority Inheritance

- **그룹**: 8 misc_realtime_scheduling
- **출처/연도**: RTSS 2023
- **저자**: Yue Tang, Xu Jiang, Nan Guan, Songran Liu, Xiantong Luo, Wang Yi

## 두 질문
- **가변 변수**: dynamic priority inheritance behavior, buffer manipulation protocol.
- **트리거**: data propagation in sporadic cause-effect chains.

## 요점
- 플랫폼: automotive benchmarks and randomly generated workload.
- 도메인: end-to-end latency of cause-effect chains under fixed-priority scheduling.
- 핵심 방법: Dynamic Priority Inheritance Protocol을 제안해 communicating jobs 사이의 propagation delay가 task relative priority에 덜 의존하도록 한다. DPI-B는 buffer manipulation protocol과 결합해 determinism도 고려한다.
- 정식화/수식: maximum reaction time and maximum data age for cause-effect chains.

## 내 연구 관점
- 한 줄 gap: control/data-chain latency 이론이며 vibration FD W/H/M, anomaly trigger, PREEMPT_RT inference는 다루지 않는다.
- 내 연구에 쓸 곳: Rx -> Inference -> Tx pipeline의 end-to-end latency 개념 배경으로 제한적 활용 가능.
- 인용할 문장: "end-to-end latency"

## 불확실한 점
- 확인 필요: DPI/DPI-B의 latency improvement 수치는 automotive benchmark 조건과 random workload 설정을 확인해야 한다.
