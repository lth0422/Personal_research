# Approaches for Integrating Deep Learning Models for Inference Using AUTOSAR in ECU

> 딥러닝 모델을 양자화해 AUTOSAR 표준 준수 ECU C코드로 변환하는 세 가지 툴체인(TargetLink 수동, Simulink+DL Toolbox, 하이브리드)을 비교

- **Conference**: RTCSA 2025
- **Tags**: #embedded-ml #autonomous-driving

## Abstract
Deep Learning (DL) models are typically deployed on high-computation platforms like GPUs and FPGAs in cloud environments, leading to high latency and network dependency. In contrast, performing deep learning inference on microcontrollers in automotive applications reduces latency, minimizes network dependency, enhances security, and offers a cost-effective solution. This paper investigates the integration of deep learning models into AUTOSAR-compliant C-code for automotive Electronic Control Units (ECUs). Adhering to AUTOSAR standards guarantees compatibility, scalability, maintainability, and efficient resource management. The study emphasizes toolchains that transform deep learning models, initially trained and developed in Python with frameworks such as TensorFlow or PyTorch, or using other tools like MATLAB, into high-quality AUTOSAR-compliant C code, tailored for specific compilers and hardware optimizations. Upon deployment, the deep learning software module within the ECU must satisfy rigorous real-time system requirements. In this paper, we demonstrate the integration of a deep learning model into an ECU, emphasizing automation and seamless incorporation into existing workflows. The workflow setup can be extended to various deep learning models, but we use a simple neural network for estimating the battery's state of health to illustrate the process. The model is trained in Python, quantized for ECU deployment, and converted to AUTOSAR-compliant C-code through three methods: manual implementation with TargetLink, Simulink combined with the Deep Learning Toolbox, and a hybrid approach integrating Simulink-generated code into existing TargetLink logic using S-functions. This comparison focuses on fixed-point scaling and hardware optimization to ensure code efficiency, reliability, and correctness, verified through static code analysis and unit testing. Functional tests in a Software-in-the-Loop (SIL) environment validate system performance and accuracy by comparing results to a physics-based model. Hardware-in-the-Loop (HIL) testing assesses real-time behavior and robustness, ensuring reliable performance with actual hardware components under real-world conditions.

딥러닝 모델은 흔히 클라우드 환경의 GPU·FPGA 같은 고성능 플랫폼에 배포되어 높은 지연과 네트워크 의존성을 낳는다. 반대로 자동차 애플리케이션의 마이크로컨트롤러에서 딥러닝 추론을 수행하면 지연을 줄이고 네트워크 의존성을 최소화하며 보안을 강화하고 비용 효율적인 솔루션을 제공한다. 이 논문은 딥러닝 모델을 자동차 ECU(전자제어장치)의 AUTOSAR 표준 준수 C코드에 통합하는 방법을 연구한다. AUTOSAR 표준 준수는 호환성, 확장성, 유지보수성, 효율적 자원 관리를 보장한다. 연구는 Python에서 TensorFlow·PyTorch 등으로 학습된 딥러닝 모델(또는 MATLAB 등 다른 도구로 개발된 모델)을 특정 컴파일러·하드웨어에 최적화된 고품질 AUTOSAR 준수 C코드로 변환하는 툴체인에 초점을 맞춘다. 배포 후 ECU 내 딥러닝 소프트웨어 모듈은 엄격한 실시간 시스템 요구사항을 만족해야 한다. 이 논문은 자동화와 기존 워크플로 통합을 강조하며 딥러닝 모델을 ECU에 통합하는 사례를 시연한다. 배터리 상태(SOH) 추정을 위한 간단한 신경망을 예시로, Python에서 학습한 모델을 양자화해 ECU 배포용으로 만들고, TargetLink 수동 구현, Simulink+Deep Learning Toolbox, S-function을 이용한 하이브리드 방식 등 세 가지 방법으로 AUTOSAR 준수 C코드로 변환한다. 이 비교는 고정소수점 스케일링과 하드웨어 최적화에 초점을 맞춰 코드 효율성·신뢰성·정확성을 정적 코드 분석과 단위 테스트로 검증한다. SIL(Software-in-the-Loop) 환경의 기능 테스트로 물리 기반 모델과 비교해 시스템 성능·정확도를 검증하고, HIL(Hardware-in-the-Loop) 테스트로 실제 하드웨어에서의 실시간 동작과 견고성을 평가한다.

## Key Takeaways
- 어떤 문제를 해결하는가: 딥러닝 모델을 자동차 ECU의 AUTOSAR 표준 C코드로 통합해 실시간 요구사항을 만족시키는 문제
- 어떤 방법을 사용하는가: 양자화된 DL 모델을 TargetLink 수동/Simulink+DL Toolbox/하이브리드(S-function) 세 방식으로 AUTOSAR C코드 변환, SIL/HIL 검증
- 주요 결과/기여: 배터리 SOH 추정 신경망 사례로 세 툴체인의 코드 효율성·신뢰성·실시간 동작을 비교 검증

## Related
- [[embedded-ml]]
- [[autonomous-driving]]

## Source
- DOI: [10.1109/RTCSA66114.2025.00013](https://doi.org/10.1109/RTCSA66114.2025.00013)

## My Notes
<!-- This section is written only by the user. The LLM must never edit or delete this section. -->
- **Status**: Unread
- **Interest**: /10
- **Notes**: 
