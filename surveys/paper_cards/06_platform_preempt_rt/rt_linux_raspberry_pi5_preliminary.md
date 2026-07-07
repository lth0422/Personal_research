# A Preliminary Assessment of the Real-Time Capabilities of Real-Time Linux on Raspberry Pi 5

- **그룹**: 6 platform_preempt_rt
- **출처/연도**: 2024, venue 확인 필요
- **저자**: Wannes Dewit, Antonio Paolillo, Joel Goossens

## 두 질문
- **가변 변수**: 없음. 비교 조건은 stock Linux kernel과 PREEMPT_RT patched kernel.
- **트리거**: 없음. 실험적 scheduling latency benchmarking 논문이며 runtime adaptation을 다루지 않는다.

## Abstract 3줄 요약
- Raspberry Pi 5에서 PREEMPT_RT 적용 Linux의 practical real-time capability를 평가한다.
- cyclictest와 stressor를 사용해 PREEMPT_RT 적용 전후의 scheduling latency와 predictability를 비교한다.
- Real-Time Linux에서 maximum latency가 크게 줄었다고 보고하며, measurement-based RTOS assessment methodology를 장기 목표로 둔다.

## Conclusion 요약
- 결론 섹션의 독립적인 본문은 추출본에서 명확히 확인되지 않았다. abstract와 본문 기준으로는 PREEMPT_RT가 Raspberry Pi 5의 determinism과 worst-case scheduling latency를 개선한다는 preliminary evidence를 제시하지만, Pi Zero 2W로 직접 일반화하면 안 된다.

## 요점
- 플랫폼: Raspberry Pi 5 Model B Rev 1.0, Debian 12, kernel 6.6.21 stock vs PREEMPT_RT.
- 도메인: Real-Time Linux benchmarking, scheduling latency.
- 핵심 방법 (2~3줄): Raspberry Pi 5에서 cyclictest를 stress-ng와 iperf3 부하와 함께 실행해 stock kernel과 PREEMPT_RT kernel의 scheduling latency를 비교한다. extreme stress 조건에서 PREEMPT_RT가 maximum observed latency를 크게 줄였다고 보고한다.
- 정식화/수식 (있으면): cyclictest는 intended wake-up time과 actual wake-up time의 차이를 scheduling latency로 측정한다.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): Pi Zero 2W, TFLite fault diagnosis pipeline, inference/end-to-end latency는 다루지 않는다.
- 내 연구에 쓸 곳: KSC 2026에서 cyclictest + stress-ng 기반 vanilla Linux vs PREEMPT_RT 사전 검증 절차를 정당화하는 근거.
- 인용할 문장 (있으면, 15단어 이내): "294x shorter maximum latency"

## 불확실한 점
- 확인 필요: PDF 안에서 venue가 명확히 확인되지 않았다.
- 확인 필요: 추출본에서 conclusion heading 또는 conclusion 본문이 명확히 잡히지 않아 결론 요약은 abstract와 본문 기준이다.
- 확인 필요: Pi 5 결과를 Pi Zero 2W에 직접 일반화하지 말고, methodology 참고로만 사용해야 한다.
