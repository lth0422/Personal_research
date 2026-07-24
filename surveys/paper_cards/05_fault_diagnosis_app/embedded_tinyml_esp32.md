# Embedded TinyML for Predictive Maintenance: Vibration Analysis on ESP32

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S1 embedded real-time fault diagnosis, S2 adaptive diagnostic fidelity
- **플랫폼 태그**: `PL-MCU`
- **실행환경 태그**: `ENV-OTHER`
- **출처/연도**: International Journal on Computational Modelling Applications, 2025, DOI 10.63503/j.ijcma.2025.114
- **저자**: Shubbham Gupta, Shiv Naresh Shivhare

## 두 질문
- **가변 변수**: offline model choice 1D CNN/CNN-LSTM. 본문 실험의 sampling rate와 window/hop은 고정이다.
- **트리거**: runtime trigger 없음. Accuracy, memory, latency와 energy를 offline 비교해 model을 선택한다.

## Abstract 3줄 요약
- ESP32에서 vibration-based four-class fault diagnosis를 실행하는 TinyML framework를 제안한다.
- ADXL345 custom data와 quantized 1D CNN/CNN-LSTM을 비교한다.
- 1D CNN이 더 작은 resource/latency로 ESP32 deployment에 적합하다고 평가한다.

## Conclusion 요약
- 두 model 모두 실행 가능하지만 1D CNN이 resource-constrained deployment에 더 적합하며, 향후 hybrid edge-cloud와 multimodal sensing을 제안한다.

## 요점
- 플랫폼: ESP32, ADXL345, INT8 deployment; OS/RTOS 명시 없음.
- 도메인: normal/misalignment/imbalance/bearing-worn classification.
- 핵심 방법 (2~3줄): 1 kHz, 10 s recording을 256-sample window와 50% overlap으로 분할한다. 1D CNN은 13 ms, CNN-LSTM은 26 ms inference를 보고한다.
- 정식화/수식 (있으면): fixed `W=256`, `H=128 samples`.

## 0708 면담 기준 보강
- **실시간성 수준**: on-device inference latency만 있고 deadline/jitter/miss/RTOS는 없다. `B`.
- **실행시간 가정**: model별 fixed measured latency.
- **보장 방식**: empirical single latency. 근거: Sections 4-5, Table 4.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): abstract의 "adaptive sampling"과 달리 실험은 1 kHz fixed sampling이며 runtime `W/H/M` adaptation이 없다.
- 내 연구에 쓸 곳: model `M`별 latency/accuracy offline profile 및 고정 `W/H` TinyML 비교군.
- 인용할 문장 (있으면, 15단어 이내): "window sizes set to 256 samples"

## 불확실한 점
- 확인 필요: adaptive sampling의 algorithm, trigger와 평가가 본문에 없어 해당 기능을 구현된 contribution으로 인용하지 않는다.
