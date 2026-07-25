# RT-Swap: Addressing GPU Memory Bottlenecks for Real-Time Multi-DNN Inference

> CPU 메모리로 GPU 메모리를 확장하는 스왑 스케줄링 프레임워크 RT-Swap으로 다중 DNN 실시간 추론의 GPU 메모리 병목을 해소

- **Conference**: RTAS 2024
- **Tags**: #memory-management #neural-network-inference #embedded-ml

## Abstract
The increasing complexity and memory demands of Deep Neural Networks (DNNs) for real-time systems pose new significant challenges, one of which is the GPU memory capacity bottleneck, where the limited physical memory inside GPUs impedes the deployment of sophisticated DNN models. This paper presents, to the best of our knowledge, the first study of addressing the GPU memory bottleneck issues, while simultaneously ensuring the timely inference of multiple DNN tasks. We propose RT-Swap, a real-time memory management framework, that enables transparent and efficient swap scheduling of memory objects, employing the relatively larger CPU memory to extend the available GPU memory capacity, without compromising timing guarantees. We have implemented RT-Swap on top of representative machine-learning frameworks, demonstrating its effectiveness in making significantly more DNN task sets schedulable at least 72% over existing approaches even when the task sets demand up to 96.2% more memory than the GPU's physical capacity.

실시간 시스템을 위한 DNN의 복잡도와 메모리 요구량이 늘면서 새로운 문제가 발생하는데, 그중 하나가 GPU 메모리 용량 병목으로, GPU 내부의 제한된 물리 메모리가 정교한 DNN 모델 배포를 가로막는다. 이 논문은 다중 DNN 태스크의 적시 추론을 보장하면서 동시에 GPU 메모리 병목 문제를 다루는 최초의 연구를 제시한다. 저자들은 상대적으로 더 큰 CPU 메모리를 활용해 GPU 메모리 용량을 확장하는, 타이밍 보장을 저해하지 않는 투명하고 효율적인 스왑 스케줄링 프레임워크 RT-Swap을 제안한다. 대표적인 머신러닝 프레임워크 위에 RT-Swap을 구현해, GPU 물리 용량보다 최대 96.2% 더 많은 메모리를 요구하는 태스크셋에서도 기존 기법 대비 최소 72% 더 많은 DNN 태스크셋을 스케줄 가능하게 만드는 효과를 입증했다.

## Key Takeaways
- 어떤 문제를 해결하는가: 다중 DNN 실시간 추론에서 GPU 물리 메모리 용량 한계로 인한 병목 문제
- 어떤 방법을 사용하는가: CPU 메모리를 활용해 GPU 메모리를 확장하는 실시간 스왑 스케줄링 프레임워크 RT-Swap
- 주요 결과/기여: GPU 용량 초과 96.2% 요구 상황에서도 기존 대비 스케줄 가능 태스크셋 72% 이상 증가

## Related
- [[memory-management]]
- [[neural-network-inference]]
- [[embedded-ml]]

## Source
- DOI: [10.1109/RTAS61025.2024.00037](https://doi.org/10.1109/RTAS61025.2024.00037)

## My Notes
<!-- This section is written only by the user. The LLM must never edit or delete this section. -->
- **Status**: Unread
- **Interest**: /10
- **Notes**: 
