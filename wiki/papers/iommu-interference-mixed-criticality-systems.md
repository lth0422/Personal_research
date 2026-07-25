# Beyond the Bermuda Triangle of Contention: IOMMU Interference in Mixed Criticality Systems

> Arm SMMUv2 IOMMU 내부 구조를 리버스엔지니어링해, IOTLB 경합이 DMA 트랜잭션 지연을 최대 1.79배까지 유발함을 실측

- **Conference**: RTCSA 2025
- **Tags**: #mixed-criticality #resource-management #memory-management

## Abstract
As Mixed Criticality Systems (MCSs) evolve, they increasingly integrate heterogeneous computing platforms that combine general-purpose processors with specialized accelerators such as AI engines, Graphics Processing Units (GPUs), and high-speed networking interfaces. This heterogeneity introduces challenges, as Direct Memory Access (DMA)-capable devices act as independent bus masters that directly access shared memory. Ensuring both security and timing predictability in such environments is critical. The Input-Output Memory Management Unit (IOMMU) addresses these concerns by enforcing memory isolation and access control. While prior work has examined the IOMMU from a security perspective, highlighting sidechannel vulnerabilities rooted in shared caching structures, these same architectural resources can also undermine system safety by introducing timing unpredictability due to shared resources contention. In time-sensitive workloads, such interference can hinder the system's ability to meet real-time guarantees. In this work, we analyze IOMMU contention using the Xilinx UltraScale+ ZCU104 platform, which integrates an Arm SMMUv2-compliant IOMMU. We reverse-engineer the IOMMU's internal translation structures and use microbenchmarking to demonstrate how shared components, particularly the IOTLB, introduce measurable latency under concurrent DMA activity. Our results show that translation can induce DMA transaction delays that can arise up to 1.79×. These findings emphasize the need to consider IOMMU-induced contention when designing real-time MCS workloads on modern embedded platforms.

혼합 크리티컬리티 시스템(MCS)이 발전하면서 범용 프로세서와 AI 엔진, GPU, 고속 네트워킹 인터페이스 같은 전용 가속기를 결합한 이기종 컴퓨팅 플랫폼 통합이 늘고 있다. 이런 이기종성은 DMA 지원 기기들이 독립적인 버스 마스터로서 공유 메모리에 직접 접근한다는 과제를 낳는다. 이런 환경에서 보안과 타이밍 예측성을 동시에 보장하는 것이 중요하다. IOMMU(Input-Output Memory Management Unit)는 메모리 격리와 접근 제어를 강제해 이를 해결한다. 기존 연구는 IOMMU를 주로 보안 관점(공유 캐싱 구조에 뿌리를 둔 사이드채널 취약점)에서 다뤘지만, 동일한 아키텍처 자원이 공유 자원 경합으로 인한 타이밍 비예측성을 유발해 시스템 안전성도 저해할 수 있다. 시간에 민감한 워크로드에서는 이런 간섭이 실시간 보장 충족을 방해할 수 있다. 이 연구는 Arm SMMUv2 준수 IOMMU가 탑재된 Xilinx UltraScale+ ZCU104 플랫폼으로 IOMMU 경합을 분석한다. IOMMU의 내부 변환 구조를 리버스엔지니어링하고, 마이크로벤치마킹을 통해 IOTLB 등 공유 컴포넌트가 동시 DMA 활동 하에서 측정 가능한 지연을 유발함을 보인다. 결과는 변환 과정이 DMA 트랜잭션 지연을 최대 1.79배까지 유발할 수 있음을 보여준다. 이는 최신 임베디드 플랫폼에서 실시간 MCS 워크로드를 설계할 때 IOMMU로 인한 경합을 고려해야 함을 시사한다.

## Key Takeaways
- 어떤 문제를 해결하는가: 이기종 가속기(AI 엔진, GPU 등)를 통합한 MCS에서 IOMMU 공유 자원 경합이 유발하는 타이밍 비예측성
- 어떤 방법을 사용하는가: Arm SMMUv2 IOMMU 내부 변환 구조 리버스엔지니어링 + 마이크로벤치마킹 실측
- 주요 결과/기여: IOTLB 경합으로 인한 DMA 트랜잭션 지연 최대 1.79배 실증, MCS 설계 시 IOMMU 경합 고려 필요성 제기

## Related
- [[mixed-criticality]]
- [[resource-management]]
- [[memory-management]]

## Source
- DOI: [10.1109/RTCSA66114.2025.00027](https://doi.org/10.1109/RTCSA66114.2025.00027)

## My Notes
<!-- This section is written only by the user. The LLM must never edit or delete this section. -->
- **Status**: Unread
- **Interest**: /10
- **Notes**: 
