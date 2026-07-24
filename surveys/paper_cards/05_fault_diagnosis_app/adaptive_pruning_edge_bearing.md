# Edge-Oriented Bearing Fault Diagnosis via Triple-Lightweight Network With Adaptive Pruning

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S1 embedded real-time fault diagnosis, S2 adaptive diagnostic fidelity
- **플랫폼 태그**: `PL-HET-SOC`
- **실행환경 태그**: `ENV-LINUX`
- **출처/연도**: IEEE Transactions on Instrumentation and Measurement, 2026, DOI 10.1109/TIM.2026.3699722
- **저자**: Zhaokang Zhan, Siqi Zhang, Jiacan Xu, Dazhong Ma

## 두 질문
- **가변 변수**: training 중 pruning group/rate와 network structure; deployment 후 model은 고정된다.
- **트리거**: dependency graph와 trainable importance threshold가 training 중 redundant structure를 제거한다.

## Abstract 3줄 요약
- Edge bearing diagnosis를 위해 construction, feature extraction, pruning의 세 단계에서 model을 경량화한다.
- Recursive inference, frequency-domain multiscale convolution과 dependency-aware adaptive pruning을 결합한다.
- CWRU와 Jetson Xavier NX physical test bench에서 accuracy, complexity와 latency를 평가한다.

## Conclusion 요약
- APTL-net이 model size와 edge latency를 줄이면서 benchmark accuracy를 유지하며, variable-speed/field validation은 추가 과제로 남는다.

## 요점
- 플랫폼: NVIDIA Jetson Xavier NX, JetPack 5.1.2, Ubuntu 계열, TensorRT 8.5.1.7.
- 도메인: bearing fault classification under speed/domain shift.
- 핵심 방법 (2~3줄): Training graph를 병렬화하되 inference는 recursive하게 실행하고, FDD multiscale feature와 adaptive structural pruning을 사용한다. Pruning은 runtime input에 따른 conditional execution이 아니다.
- 정식화/수식 (있으면): total latency baseline 20.18 ms에서 pruning 16.36 ms; TensorRT deployment 16.588 ms.

## 0708 면담 기준 보강
- **실시간성 수준**: forward/preprocessing latency와 10-minute online test는 있으나 deadline/jitter/p99/miss 없음. `B`.
- **실행시간 가정**: fixed deployed model의 repeated average latency.
- **보장 방식**: empirical latency와 controlled test; schedulability 보장 없음. 근거: Section IV-D/E, Tables V/VIII.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): adaptive pruning은 training-time이며 machine condition/slack에 따른 runtime `M` 선택이 아니다.
- 내 연구에 쓸 곳: HET-SoC/Linux에서 lightweight `M` profile과 preprocessing 포함 latency 측정 비교군.
- 인용할 문장 (있으면, 15단어 이내): "excluding preprocessing"

## 불확실한 점
- 확인 필요: Table V의 pipeline latency와 Table VIII의 deployment latency는 runtime configuration이 달라 직접 혼합하지 않는다.
