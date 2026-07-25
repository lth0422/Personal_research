# RTiL: Real-Time Inference of Large Language Models on Memory-Constrained GPU Devices

> 경량 LLM과 강력한 LLM의 협업 추론으로 메모리 제한 GPU 기기에서 실시간 LLM 추론을 구현하는 RTiL

- **Conference**: RTCSA 2024
- **Tags**: #embedded-ml #neural-network-inference #memory-management

## Abstract
While large language models (LLMs) are usually deployed on powerful servers, there is growing interest in deploying them on local machines for better real-time performance, service stability, privacy, and flexibility. Unfortunately, the GPU memory on local machines is often insufficient to accommodate the entire LLM. Although running an LLM on such a GPU device is still possible by swapping data between the limited GPU memory and the abundant main memory, the slow speed of data swapping significantly hampers inference time, rendering it impractical in reality. In this paper, we propose RTiL, a systematic solution to address the above challenge. RTiL utilizes collaborative inference, which combines a lightweight LLM with the default powerful LLM. The lightweight LLM generates output tokens, which are then validated for quality by the powerful LLM. This approach allows RTiL to significantly speed up inference while maintaining the same output quality as when using the powerful LLM alone. Additionally, by delegating part of the inference workload to the CPU and optimizing data movement between main and GPU memory, we further enhance the efficiency of the inference process. Furthermore, we extend RTiL to handle requests with real-time requirements, enabling it to meet such demands by slightly trading off output quality. Through extensive experiments, we demonstrate notable improvements in inference efficiency and the ability to fulfill real-time requirements while minimizing degradation in output quality.

LLM은 보통 강력한 서버에 배포되지만, 실시간 성능·서비스 안정성·프라이버시·유연성을 위해 로컬 머신에 배포하려는 관심이 커지고 있다. 그러나 로컬 머신의 GPU 메모리는 흔히 전체 LLM을 담기에 부족하다. 제한된 GPU 메모리와 풍부한 메인 메모리 사이에서 데이터를 스왑함으로써 LLM 실행이 가능하긴 하지만, 스왑 속도가 느려 추론 시간이 크게 저해되어 실용적이지 못하다. 이 논문은 이 문제를 해결하는 체계적 해법 RTiL을 제안한다. RTiL은 경량 LLM과 기본 강력 LLM을 결합하는 협업 추론을 활용한다. 경량 LLM이 출력 토큰을 생성하면, 강력 LLM이 그 품질을 검증한다. 이 접근으로 RTiL은 강력 LLM 단독 사용과 동일한 출력 품질을 유지하면서 추론 속도를 크게 높인다. 또한 추론 워크로드 일부를 CPU에 위임하고 메인-GPU 메모리 간 데이터 이동을 최적화해 추론 효율을 더욱 높인다. 나아가 RTiL을 실시간 요구사항이 있는 요청까지 처리하도록 확장해, 출력 품질을 약간 희생하며 그 요구를 만족시킨다. 광범위한 실험을 통해 추론 효율의 뚜렷한 개선과, 출력 품질 저하를 최소화하며 실시간 요구사항을 만족시키는 능력을 입증했다.

## Key Takeaways
- 어떤 문제를 해결하는가: 로컬(온디바이스) GPU 메모리 제약으로 인한 LLM 실시간 추론의 속도 저하 문제
- 어떤 방법을 사용하는가: 경량 LLM과 강력 LLM의 협업 추론(생성-검증), CPU 워크로드 위임과 메모리 이동 최적화
- 주요 결과/기여: 출력 품질 저하를 최소화하며 추론 효율을 크게 개선, 실시간 요구사항 대응까지 확장

## Related
- [[embedded-ml]]
- [[neural-network-inference]]
- [[memory-management]]

## Source
- DOI: [10.1109/RTCSA62462.2024.00013](https://doi.org/10.1109/RTCSA62462.2024.00013)

## My Notes
<!-- This section is written only by the user. The LLM must never edit or delete this section. -->
- **Status**: Unread
- **Interest**: /10
- **Notes**: 
