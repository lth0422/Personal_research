# Demystifying NVIDIA GPU Internals to Enable Reliable GPU Management

> NVIDIA GPU 내부 동작을 리버스엔지니어링해 기존 실시간 GPU 관리 기법 3가지의 결함을 규명

- **Conference**: RTAS 2024
- **Tags**: #resource-management #embedded-ml

## Abstract
As GPU-dependent artificial intelligence and machine learning workloads increasingly come to embedded, safety-critical systems-such as self-driving cars-real-time predictability for GPU-using tasks becomes essential. This paper identifies flaws in three different real-time GPU management approaches that are largely the result of incomplete information about NVIDIA GPU internals. Details concerning this missing information are elucidated via experiments. Based on this information, key rules of GPU scheduling are identified and shown necessary for safe GPU management.

자율주행차 등 임베디드 안전critical 시스템에서 GPU 의존적 AI/ML 워크로드가 늘어나면서, GPU를 사용하는 태스크의 실시간 예측성이 중요해지고 있다. 이 논문은 NVIDIA GPU 내부 동작에 대한 불완전한 정보로 인해 발생하는, 기존 실시간 GPU 관리 기법 3가지의 결함을 규명한다. 실험을 통해 누락된 정보를 상세히 밝히고, 이를 바탕으로 안전한 GPU 관리를 위해 필요한 GPU 스케줄링의 핵심 규칙을 도출한다.

## Key Takeaways
- 어떤 문제를 해결하는가: NVIDIA GPU 내부 동작 정보 부족으로 인해 기존 실시간 GPU 관리 기법들이 갖는 결함
- 어떤 방법을 사용하는가: 실험 기반 리버스엔지니어링으로 GPU 내부 스케줄링 동작을 규명
- 주요 결과/기여: 안전한 실시간 GPU 관리를 위한 핵심 스케줄링 규칙 도출

## Related
- [[resource-management]]
- [[embedded-ml]]

## Source
- DOI: [10.1109/RTAS61025.2024.00031](https://doi.org/10.1109/RTAS61025.2024.00031)

## My Notes
<!-- This section is written only by the user. The LLM must never edit or delete this section. -->
- **Status**: Unread
- **Interest**: /10
- **Notes**: 
