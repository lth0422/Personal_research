# Demo: Real-Time Inference on GPU-Based Heterogeneous SoCs with GPU Cache Locking

> 타이밍 예측성을 고려한 캐시 락킹 정책으로 GPU SoC 내 AI 가속기와의 메인 메모리 경합을 줄여 실시간 CNN 추론을 데모

- **Conference**: RTCSA 2025
- **Tags**: #embedded-ml #memory-management

## Abstract
Embedded real-time systems are increasingly turning to GPU-based SoCs to efficiently handle machine learning tasks at the edge. Modern GPU SoCs often feature specialized AI accelerators to enable concurrent CNN inference while maintaining energy efficiency. While this trend typically leads to a general improvement in performance, the integration of multiple AI accelerators presents challenges for building real-time systems, where ensuring timing predictability is a key design goal. On one hand, contention among various computation units over shared memory can introduce non-deterministic timing behaviors. On the other hand, the built-in GPU scheduling mechanism cannot assure that emergent tasks to be executed first, potentially violating real-time constraints. To tackle these challenges, this study introduces a timing predictability-aware cache locking policy to reduce main memory access volume and mitigate main memory contention with AI accelerators. Additionally, a real-time scheduling framework is proposed to bypass the inherent GPU scheduling algorithm.

임베디드 실시간 시스템은 엣지에서 머신러닝 태스크를 효율적으로 처리하기 위해 GPU 기반 SoC를 점점 더 많이 사용하고 있다. 최신 GPU SoC는 흔히 전용 AI 가속기를 탑재해 에너지 효율을 유지하며 동시 CNN 추론을 가능하게 한다. 이런 추세는 전반적인 성능 개선으로 이어지지만, 여러 AI 가속기의 통합은 타이밍 예측성 확보가 핵심 설계 목표인 실시간 시스템 구축에 과제를 낳는다. 한편으로 다양한 연산 유닛 간 공유 메모리 경합이 비결정적 타이밍 동작을 유발할 수 있고, 다른 한편으로 GPU 내장 스케줄링 메커니즘이 긴급 태스크의 우선 실행을 보장하지 못해 실시간 제약을 위반할 수 있다. 이 문제를 해결하기 위해 이 연구는 메인 메모리 접근량을 줄이고 AI 가속기와의 메인 메모리 경합을 완화하는, 타이밍 예측성을 고려한 캐시 락킹 정책을 소개한다. 또한 GPU 내장 스케줄링 알고리즘을 우회하는 실시간 스케줄링 프레임워크를 제안한다.

## Key Takeaways
- 어떤 문제를 해결하는가: GPU SoC 내 여러 AI 가속기 간 메모리 경합 및 GPU 내장 스케줄러의 실시간성 부재 문제
- 어떤 방법을 사용하는가: 타이밍 예측성 인식 캐시 락킹 정책 + GPU 내장 스케줄러를 우회하는 실시간 스케줄링 프레임워크
- 주요 결과/기여: GPU 기반 이기종 SoC에서 실시간 CNN 추론 예측성 개선을 데모로 시연

## Related
- [[embedded-ml]]
- [[memory-management]]

## Source
- DOI: [10.1109/RTCSA66114.2025.00039](https://doi.org/10.1109/RTCSA66114.2025.00039)

## My Notes
<!-- This section is written only by the user. The LLM must never edit or delete this section. -->
- **Status**: Unread
- **Interest**: /10
- **Notes**: 
