# Real-Time Multitasking of Deep Neural Networks With Nvidia Tensorrt

> DNN을 청크 단위로 쪼개 고정우선순위 제한선점 스케줄링으로 GPU 가속 요청을 스케줄링해 다중 DNN 추론의 타이밍 예측성을 확보

- **Conference**: RTSS 2025
- **Tags**: #neural-network-inference #embedded-ml

## Abstract
Graphics processing units (GPUs) are often employed to accelerate the inference of deep neural networks (DNNs) in cyber-physical systems to implement advanced perception and control functionalities. Frameworks for GPU-accelerated DNN inference typically aim at maximizing the processing throughput rather than focusing on providing a predictable timing behavior, which is crucial for time-sensitive cyber-physical systems. This work proposes a framework for GPU-accelerated inference of DNNs on GPU-based embedded platforms in multitasking scenarios, which provides enhanced timing predictability using a design-time optimization procedure of the DNN workload and a specialized method to schedule the GPU acceleration requests of the DNNs at runtime based on fixed-priority limited-preemptive scheduling. Fine-grained control of the inference is achieved by splitting the DNNs into smaller chunks, which are then scheduled using a specialized real-time scheduling mechanism. Experimental results on commercial embedded platforms report significant improvements in terms of schedulability.

GPU는 CPS(사이버물리시스템)에서 고급 인지·제어 기능을 구현하기 위해 DNN 추론을 가속하는 데 흔히 사용된다. GPU 가속 DNN 추론 프레임워크는 대개 처리량 최대화를 목표로 하며, 시간에 민감한 CPS에 필수적인 예측 가능한 타이밍 동작 제공에는 초점을 두지 않는다. 이 연구는 멀티태스킹 시나리오에서 GPU 기반 임베디드 플랫폼 위 DNN GPU 가속 추론을 위한 프레임워크를 제안하며, DNN 워크로드의 설계 시점 최적화 절차와 고정우선순위 제한선점 스케줄링 기반의 런타임 GPU 가속 요청 스케줄링 기법을 통해 향상된 타이밍 예측성을 제공한다. DNN을 더 작은 청크로 분할해 전용 실시간 스케줄링 메커니즘으로 스케줄링함으로써 추론에 대한 세밀한 제어를 달성한다. 상용 임베디드 플랫폼에서의 실험 결과 스케줄가능성 측면에서 뚜렷한 개선을 보고했다.

## Key Takeaways
- 어떤 문제를 해결하는가: GPU 가속 DNN 추론 프레임워크가 처리량에만 집중해 타이밍 예측성을 제공하지 못하는 문제
- 어떤 방법을 사용하는가: DNN을 청크로 분할하고 고정우선순위 제한선점 스케줄링으로 GPU 가속 요청을 런타임 스케줄링
- 주요 결과/기여: 상용 임베디드 GPU 플랫폼에서 다중 DNN 태스크 스케줄가능성 대폭 개선

## Related
- [[neural-network-inference]]
- [[embedded-ml]]

## Source
- DOI: [10.1109/RTSS66672.2025.00037](https://doi.org/10.1109/RTSS66672.2025.00037)

## My Notes
<!-- This section is written only by the user. The LLM must never edit or delete this section. -->
- **Status**: Unread
- **Interest**: /10
- **Notes**: 
