# A Physics-Aware Lightweight Transformer Network for Intelligent Bearing Fault Diagnosis Under Variable Operating Conditions

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S2 adaptive diagnostic fidelity
- **플랫폼 태그**: `PL-SBC-SOC`
- **실행환경 태그**: `ENV-LINUX`
- **출처/연도**: Artificial Intelligence for Engineering, 2026, DOI 10.1049/aie2.70014
- **저자**: Ali Sayghe

## 두 질문
- **가변 변수**: offline patch size/tokenization, model depth와 quantization/pruning configuration. Runtime input window는 고정된다.
- **트리거**: bearing geometry, sampling frequency와 minimum characteristic fault frequency가 patch size를 정하는 offline physics trigger다.

## Abstract 3줄 요약
- Variable operating condition에서 lightweight transformer의 generalization과 edge latency를 함께 다룬다.
- Overlapping convolutional patches, physics-guided patch sizing과 amplitude-invariant attention을 제안한다.
- CWRU/Paderborn, A100와 Raspberry Pi 4에서 accuracy와 latency를 baseline과 비교한다.

## Conclusion 요약
- Physics-aware tokenization이 cross-load robustness와 compact edge inference에 기여한다고 결론짓고, operational industrial data와 on-device adaptation을 future work로 둔다.

## 요점
- 플랫폼: Raspberry Pi 4 Model B, Cortex-A72 1.8 GHz, ONNX Runtime 1.16; training은 NVIDIA A100.
- 도메인: bearing fault classification under load/speed variation.
- 핵심 방법 (2~3줄): Fault impulse가 patch boundary에서 잘리지 않도록 50% overlapping Conv-Stem을 사용한다. `f_s/f_min`으로 patch lower bound를 정하고 fixed 1024-sample window를 512-sample hop으로 처리한다.
- 정식화/수식 (있으면): `P*=ceil(f_s/f_min)`; `W=1024`, `H=512`, decision interval 약 43 ms, RPi4 inference 43.6 ms.

## 0708 면담 기준 보강
- **실시간성 수준**: average per-sample inference만 있고 RTOS/deadline/jitter/miss 없음. `B`.
- **실행시간 가정**: fixed model/input의 average latency; Raspberry Pi 4 1000 calls.
- **보장 방식**: empirical latency. 근거: Sections 3.8, 4.3-4.5, 5.2.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): physics로 patch를 offline 설계하지만 runtime `W/H/M`과 system slack을 공동 선택하지 않는다.
- 내 연구에 쓸 곳: arbitrary `W`가 아니라 fault physics가 허용하는 최소 정보 범위를 mode set에 반영해야 한다는 직접 근거.
- 인용할 문장 (있으면, 15단어 이내): "sampling-frequency-guided patch sizing"

## 불확실한 점
- 확인 필요: Section 6.3의 STM32H7 43 ms는 실험 설정 설명이 부족하므로 RPi4 결과와 분리하고 원고 근거로 쓰지 않는다.
