# Towards Low-Latency GPU-Aware Pub/Sub Communication for Real-Time Edge Computing

> CUDA 공유 메모리를 활용해 GPU-호스트 메모리 복사를 없앤 GPU-Aware Pub/Sub 미들웨어 GAPS로 Edge AI 파이프라인 지연을 최대 3.8배 개선

- **Conference**: RTCSA 2025
- **Tags**: #embedded-ml #mobile-edge-computing #memory-management

## Abstract
Real-time Edge AI applications often require efficient GPU-based data processing and communication. Since the applications are typically highly modularized, publish-subscribe (pub/sub) pattern is widely used to deliver data among components. However, existing pub/sub middleware introduces significant latency due to redundant memory copies between GPU and host memory. To address this, we propose GPU-Aware Pub/Sub communication (GAPS), a universal solution that integrates shared CUDA memory with existing pub/sub middleware, such as Zenoh-pico and Iceoryx. GAPS minimizes data transfer latency by enabling GPU memory sharing between publishers and subscribers, eliminating unnecessary memory copies. In our work, we propose an independent shared CUDA memory manager that creates a shared CUDA memory pool for each topic during a topic's initialization. For fine-grained allocation from the pool, we modify Two-Level Segregated Fit (TLSF), a real-time dynamic memory allocator, making it process-safe and capable of managing GPU memory. Additionally, we develop PyGAPS, an extension that accelerates publications of PyTorch tensors, eliminating serialization overhead in AI-driven applications. Our evaluation demonstrates that GAPS significantly reduces end-to-end latency and improves throughput of simplified computer vision pipelines—by up to 1.5× in the segmentation task and 3.8× in the classification task—making it a robust solution for real-time Edge AI.

실시간 Edge AI 애플리케이션은 흔히 효율적인 GPU 기반 데이터 처리와 통신을 요구한다. 이런 애플리케이션은 대개 고도로 모듈화되어 있어, 컴포넌트 간 데이터 전달에 pub/sub(발행-구독) 패턴이 널리 쓰인다. 그러나 기존 pub/sub 미들웨어는 GPU-호스트 메모리 간 불필요한 복사로 인해 상당한 지연을 유발한다. 이를 해결하기 위해 Zenoh-pico, Iceoryx 등 기존 pub/sub 미들웨어에 공유 CUDA 메모리를 통합하는 범용 솔루션 GPU-Aware Pub/Sub 통신(GAPS)을 제안한다. GAPS는 발행자-구독자 간 GPU 메모리 공유를 가능하게 해 불필요한 메모리 복사를 없애고 데이터 전송 지연을 최소화한다. 각 토픽 초기화 시 공유 CUDA 메모리 풀을 생성하는 독립적인 공유 CUDA 메모리 매니저를 제안하며, 풀에서의 세밀한 할당을 위해 실시간 동적 메모리 할당자인 TLSF(Two-Level Segregated Fit)를 프로세스-세이프하게 수정해 GPU 메모리를 관리할 수 있도록 했다. 또한 PyTorch 텐서 발행을 가속화해 AI 기반 애플리케이션의 직렬화 오버헤드를 없애는 확장 PyGAPS를 개발했다. 평가 결과, GAPS는 단순화된 컴퓨터 비전 파이프라인의 종단 간 지연을 크게 줄이고 처리량을 개선했는데, 세그멘테이션 태스크에서 최대 1.5배, 분류 태스크에서 최대 3.8배 개선되어 실시간 Edge AI를 위한 견고한 솔루션임을 입증했다.

## Key Takeaways
- 어떤 문제를 해결하는가: Edge AI pub/sub 미들웨어의 GPU-호스트 메모리 간 불필요한 복사로 인한 지연 문제
- 어떤 방법을 사용하는가: CUDA 공유 메모리 통합 pub/sub GAPS, 프로세스-세이프 TLSF 기반 GPU 메모리 풀 관리, PyTorch 텐서 가속 확장 PyGAPS
- 주요 결과/기여: 컴퓨터 비전 파이프라인 지연 개선 (세그멘테이션 1.5배, 분류 3.8배)

## Related
- [[embedded-ml]]
- [[mobile-edge-computing]]
- [[memory-management]]

## Source
- DOI: [10.1109/RTCSA66114.2025.00018](https://doi.org/10.1109/RTCSA66114.2025.00018)

## My Notes
<!-- This section is written only by the user. The LLM must never edit or delete this section. -->
- **Status**: Unread
- **Interest**: /10
- **Notes**: 
