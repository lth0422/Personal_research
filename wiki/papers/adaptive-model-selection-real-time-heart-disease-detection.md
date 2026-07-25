# Adaptive Model Selection for Real-Time Heart Disease Detection on Embedded Systems

> 심박수에 따라 CNN 모델 복잡도를 동적으로 조정하는 Adaptive Model Selection(AMS) 프레임워크로 Raspberry Pi 4에서 실시간 심혈관질환 탐지

- **Conference**: RTCSA 2025
- **Tags**: #embedded-ml #neural-network-inference

## Abstract
Real-time cardiovascular disease (CVD) detection on wearable devices presents significant challenges due to the varying heart rate conditions and constrained computational capabilities of embedded systems. Existing approaches often struggle to balance diagnostic accuracy with the strict latency requirements imposed by different heart rate scenarios. In this study, we propose an Adaptive Model Selection (AMS) framework coupled with an anytime Convolutional Neural Network that integrates Residual Blocks, Squeeze-and-Excitation layers, and a Global Attention mechanism. By dynamically adjusting the model's complexity based on real-time heart rate, our solution optimizes diagnostic accuracy while ensuring a timely response. Evaluations conducted with the PhysioNet Database on a Raspberry Pi 4 demonstrate that our model achieves an accuracy of 91.5% with an average inference latency of only 1.33 ms per sample. These outcomes illustrate the effectiveness and practical applicability of our framework for robust, responsive, and accurate on-device ECG monitoring in continuous cardiac care.

웨어러블 기기에서의 실시간 심혈관질환(CVD) 탐지는 다양한 심박수 조건과 임베디드 시스템의 제한된 연산 능력으로 인해 상당한 어려움을 겪는다. 기존 접근법은 서로 다른 심박수 시나리오가 부과하는 엄격한 지연 요구사항과 진단 정확도 사이의 균형을 맞추기 어려웠다. 이 연구는 Residual Block, Squeeze-and-Excitation 레이어, Global Attention 메커니즘을 결합한 anytime CNN과 함께 적응형 모델 선택(AMS) 프레임워크를 제안한다. 실시간 심박수에 따라 모델 복잡도를 동적으로 조정함으로써, 이 솔루션은 적시 응답을 보장하면서 진단 정확도를 최적화한다. PhysioNet 데이터베이스로 Raspberry Pi 4에서 평가한 결과, 샘플당 평균 추론 지연 1.33ms로 91.5%의 정확도를 달성했다. 이 결과는 지속적 심장 관리를 위한 견고하고 반응성 있으며 정확한 온디바이스 ECG 모니터링에 이 프레임워크가 실용적으로 적용 가능함을 보여준다.

## Key Takeaways
- 어떤 문제를 해결하는가: 웨어러블 기기에서 다양한 심박수 조건 하 실시간 심혈관질환 탐지의 정확도-지연 균형 문제
- 어떤 방법을 사용하는가: 심박수에 따라 모델 복잡도를 동적 조정하는 Adaptive Model Selection + anytime CNN(Residual/SE/Global Attention)
- 주요 결과/기여: Raspberry Pi 4에서 91.5% 정확도, 샘플당 평균 1.33ms 추론 지연 달성

## Related
- [[embedded-ml]]
- [[neural-network-inference]]

## Source
- DOI: [10.1109/RTCSA66114.2025.00028](https://doi.org/10.1109/RTCSA66114.2025.00028)

## My Notes
<!-- This section is written only by the user. The LLM must never edit or delete this section. -->
- **Status**: Read
- **Interest**: 6/10
- **Notes**: 시계열 데이터를 사용한 점에서 내가 기존에 하던 것과 유사함을 느끼고 읽음. 모델의 동작에 대해서는 세세히 파악하지 않았으나 모델이 복잡하고 특징적인 논문은 아님. 주요하게 확인해야 할 것은 모델이 HR(심박수)에 따라서 동적으로 선택된다는 것. 이때 각 상황마다 다르게 모델이 선택되는 것이 아니라 동일한 구조에서 중간 과정을 추가/제거 함으로써 모델을 조정함. 앞으로 동적 모델 구조에 참고할만 함. 다만 실시간성에 대한 분석이 부족하다고 느껴짐. utilization을 설명하며 해당 값이 1 이하이면 edf는 schedulable 하다고 설명하는데 U를 계산하기 위한 C(HR) D(HR)에 대한 값과 얻는 과정에 대한 설명이 하나도 없음. 또한 그 외의 테스크들의 C와 T에 대한 설정도 논의된 바 없음. RPI4를 사용하여 보드의 제약도 압도적이라고 생각되지 않음. 단순히 모델을 변형하며 심장 질환 검사를 해봤다는 느낌으로 다가옴.
