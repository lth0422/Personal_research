# Compressing VAE-Based Out-of-Distribution Detectors for Embedded Deployment

> 양자화·프루닝·지식증류를 결합해 VAE 기반 OOD(분포 외) 탐지기를 경량화하고 Jetson Nano에서 실시간 추론을 구현

- **Conference**: RTCSA 2024
- **Tags**: #embedded-ml #neural-network-inference

## Abstract
Out-of-distribution (OOD) detectors can act as safety monitors in embedded cyber-physical systems by identifying samples outside a machine learning model's training distribution to prevent potentially unsafe actions. However, OOD detectors are often implemented using deep neural networks, which makes it difficult to meet real-time deadlines on embedded systems with memory and power constraints. We consider the class of variational autoencoder (VAE) based OOD detectors where OOD detection is performed in latent space, and apply quantization, pruning, and knowledge distillation. These techniques have been explored for other deep models, but no work has considered their combined effect on latent space OOD detection. While these techniques increase the VAE's test loss, this does not correspond to a proportional decrease in OOD detection performance and we leverage this to develop lean OOD detectors capable of real-time inference on embedded CPUs and GPUs. We propose a design methodology that combines all three compression techniques and yields a significant decrease in memory and execution time while maintaining AUROC for a given OOD detector. We demonstrate this methodology with two existing OOD detectors on a Jetson Nano and reduce GPU and CPU inference time by 20% and 28% respectively while keeping AUROC within 5% of the baseline.

OOD(분포 외) 탐지기는 머신러닝 모델의 학습 분포를 벗어난 샘플을 식별해 잠재적으로 위험한 행동을 막는 임베디드 CPS의 안전 모니터 역할을 할 수 있다. 그러나 OOD 탐지기는 흔히 심층 신경망으로 구현되어, 메모리·전력이 제한된 임베디드 시스템에서 실시간 데드라인을 만족시키기 어렵다. 이 논문은 잠재 공간에서 OOD 탐지를 수행하는 VAE 기반 탐지기 계열을 대상으로 양자화, 프루닝, 지식증류를 적용한다. 이 세 기법을 잠재 공간 OOD 탐지에 결합 적용한 효과를 다룬 연구는 이전에 없었다. 이 기법들이 VAE의 테스트 손실을 늘리지만 OOD 탐지 성능 저하는 그에 비례하지 않는다는 점을 활용해, 임베디드 CPU·GPU에서 실시간 추론이 가능한 경량 OOD 탐지기를 개발했다. 세 압축 기법을 모두 결합하는 설계 방법론을 제안해, 주어진 OOD 탐지기의 AUROC를 유지하면서 메모리와 실행 시간을 크게 줄였다. Jetson Nano에서 기존 OOD 탐지기 2종에 이 방법론을 적용해, AUROC를 베이스라인 대비 5% 이내로 유지하면서 GPU·CPU 추론 시간을 각각 20%, 28% 줄였다.

## Key Takeaways
- 어떤 문제를 해결하는가: DNN 기반 OOD 탐지기가 임베디드 시스템의 메모리·전력 제약 하에서 실시간 데드라인을 만족하기 어려운 문제
- 어떤 방법을 사용하는가: 양자화, 프루닝, 지식증류를 결합한 VAE 잠재공간 OOD 탐지기 압축 방법론
- 주요 결과/기여: Jetson Nano에서 AUROC 5% 이내 유지하며 GPU/CPU 추론 시간 20%/28% 감소

## Related
- [[embedded-ml]]
- [[neural-network-inference]]

## Source
- DOI: [10.1109/RTCSA62462.2024.00015](https://doi.org/10.1109/RTCSA62462.2024.00015)

## My Notes
<!-- This section is written only by the user. The LLM must never edit or delete this section. -->
- **Status**: Unread
- **Interest**: /10
- **Notes**: 
