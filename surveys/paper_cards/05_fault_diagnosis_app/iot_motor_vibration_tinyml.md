# IoT Device for Detecting Abnormal Vibrations in Motors Using TinyML

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S1 embedded real-time fault diagnosis, S6 platform/interference
- **플랫폼 태그**: `PL-MCU`
- **실행환경 태그**: `ENV-OTHER`
- **출처/연도**: Discover Internet of Things, 2025, DOI 10.1007/s43926-025-00142-4
- **저자**: Stalin Arciniegas, Dulce Rivero, Jefferson Piñan, Elizabeth Diaz, Francklin Rivas

## 두 질문
- **가변 변수**: runtime 적응 변수는 없다. Fixed FFT/model/alert pipeline을 사용한다.
- **트리거**: offline 설정한 anomaly threshold를 넘으면 MQTT/Node-RED/Telegram alert를 생성한다.

## Abstract 3줄 요약
- Resource-constrained IoT node에서 spectral feature와 TinyML을 결합한 motor vibration anomaly detection을 제안한다.
- XIAO ESP32S3에서 local inference하고 MQTT를 통해 alert pipeline에 연결한다.
- Laboratory와 industrial operation에서 accuracy, inference time, end-to-end alert latency를 평가한다.

## Conclusion 요약
- Edge inference와 IoT alerting의 실용성을 보였지만 Wi-Fi latency, industrial noise, multi-motor scalability가 한계라고 정리한다.

## 요점
- 플랫폼: Seeed XIAO ESP32S3, ADXL345, Edge Impulse, MQTT/Node-RED/Telegram.
- 도메인: motor vibration anomaly detection.
- 핵심 방법 (2~3줄): 100 Hz sampling, 16-sample FFT와 50% overlap으로 feature를 만들고 quantized TinyML classifier를 실행한다. 평균 inference 25 ms, collection-to-alert 약 300 ms를 보고한다.
- 정식화/수식 (있으면): fixed `W=16`, hop `H=8 samples`.

## 0708 면담 기준 보강
- **실시간성 수준**: mean inference와 end-to-end latency만 있다. RTOS/deadline/jitter/miss 없음, `B`.
- **실행시간 가정**: fixed pipeline의 평균 latency.
- **보장 방식**: empirical mean latency와 deployment observation. 근거: Sections 5-6, Table 2.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): network disturbance를 관찰하지만 이를 local mode selection이나 schedulability에 반영하지 않는다.
- 내 연구에 쓸 곳: inference-only가 아닌 sensing-to-alert latency와 connectivity interference를 분리해야 한다는 S1/S6 사례.
- 인용할 문장 (있으면, 15단어 이내): "300 ms from data collection to alert generation"

## 불확실한 점
- 확인 필요: abstract 96.5% laboratory accuracy와 conclusion 98% two-month result의 protocol이 달라 직접 비교하지 않는다.
