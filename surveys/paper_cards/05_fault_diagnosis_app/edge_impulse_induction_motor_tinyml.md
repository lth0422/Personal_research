# Real-Time Fault Detection in Induction Motors Using TinyML: An Evaluation of the Edge Impulse Platform

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S1 embedded real-time fault diagnosis, S2 adaptive diagnostic fidelity
- **플랫폼 태그**: `PL-MCU`
- **실행환경 태그**: `ENV-OTHER`
- **출처/연도**: IEEE Latin Conference on IoT, 2025, DOI 10.1109/LCIoT64881.2025.11118459
- **저자**: Joao Pedro B. Lima

## 두 질문
- **가변 변수**: offline sampling window/rate, feature transform, ANN architecture와 INT8 quantization.
- **트리거**: runtime adaptation 없음. EON Tuner가 offline accuracy/resource metric으로 configuration을 선택한다.

## Abstract 3줄 요약
- Edge Impulse로 broken rotor bar vibration classifier를 만들어 low-power MCU에 배포하는 과정을 평가한다.
- Arduino Nano 33 BLE의 nRF52840에서 one-bar와 four-bar binary models를 시험한다.
- Quantization은 four-bar model latency를 크게 줄였지만 subtle one-bar fault accuracy를 훼손했다.

## Conclusion 요약
- Edge Impulse가 TinyML deployment를 단순화하지만 fault difficulty에 따라 quantization의 accuracy/latency trade-off가 달라짐을 확인한다.

## 요점
- 플랫폼: Arduino Nano 33 BLE, nRF52840 Cortex-M4 64 MHz, 256 kB RAM.
- 도메인: induction-motor broken rotor bar detection.
- 핵심 방법 (2~3줄): 18 s, 7.6 kHz records를 2 s로 자른 뒤 1 s windows를 사용한다. Four-bar model은 250 Hz/500 ms increment, one-bar model은 1 kHz/250 ms increment를 offline 선정한다.
- 정식화/수식 (있으면): four-bar FP32 27 ms에서 INT8 1 ms; one-bar FP32 39 ms이나 quantization 시 accuracy 저하.

## 0708 면담 기준 보강
- **실시간성 수준**: target MCU latency/RAM/Flash는 측정하지만 RTOS/deadline/jitter/miss는 없다. `B`.
- **실행시간 가정**: configuration/model별 measured inference latency.
- **보장 방식**: 없음. 60% confidence 아래는 `Uncertain`으로 표시하는 fallback만 있다. 근거: Sections II-D/E, III.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): 여러 `W/H/M` 후보를 탐색하지만 runtime q/S에 따라 전환하지 않는다.
- 내 연구에 쓸 곳: mode profile 생성과 quantization이 subtle fault utility를 악화시킬 수 있다는 S2 근거.
- 인용할 문장 (있으면, 15단어 이내): "trade-offs between model complexity and hardware constraints"

## 불확실한 점
- 확인 필요: one-bar quantization 전 accuracy가 본문 위치에 따라 95.8%/97.4%로 달라 원고 인용 전 Table III 조건을 재확인한다.
