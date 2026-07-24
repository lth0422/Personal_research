# A Dual-Microcontroller IoT-Based Real-Time Monitoring System for Predictive Maintenance of Induction Motors

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S1 embedded real-time fault diagnosis, S6 platform/interference
- **플랫폼 태그**: `PL-MCU`
- **실행환경 태그**: `ENV-OTHER`
- **출처/연도**: IEEE International Electronics Symposium, 2025, DOI 10.1109/IES67184.2025.11160991
- **저자**: Ali Husein Alasiry, Haqifal Hanesta Saidya, Ni'am Tamami

## 두 질문
- **가변 변수**: runtime adaptation 없음. Sensor threshold와 10 Hz communication rate가 고정된다.
- **트리거**: ISO 10816-3 vibration zone 및 voltage/current/temperature threshold 초과 시 cloud/Telegram alert.

## Abstract 3줄 요약
- Sensor acquisition과 wireless communication을 두 MCU로 분리한 저비용 motor monitoring system을 제안한다.
- STM32F103이 voltage/current/temperature/vibration을 취득하고 ESP32가 10 Hz로 cloud에 전송한다.
- Calibration, 5-hour bearing-damage test와 end-to-end latency를 평가한다.

## Conclusion 요약
- Acquisition과 communication 분리가 sensor timing interference를 줄이며, RMS vibration threshold가 rear-bearing damage를 구분할 수 있다고 결론짓는다.

## 요점
- 플랫폼: STM32F103C8T6 + ESP32-WROOM-32, UART, Blynk/Telegram.
- 도메인: multi-sensor induction-motor condition monitoring; learned fault classifier는 없다.
- 핵심 방법 (2~3줄): STM32가 deterministic sensing을 담당하고 ESP32가 network/threshold alert를 담당한다. ISO vibration severity 기준으로 abnormal 상태를 판정한다.
- 정식화/수식 (있으면): 10 Hz packets, average end-to-end latency 402 ms.

## 0708 면담 기준 보강
- **실시간성 수준**: acquisition isolation과 평균 cloud latency만 있고 RTOS/deadline/jitter/miss는 없다. `B`.
- **실행시간 가정**: sensing/communication partition의 empirical latency.
- **보장 방식**: threshold와 architectural isolation; formal timing guarantee 없음. 근거: Sections II, III-B, IV.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): AI inference와 `W/H/M` scheduling은 없고 fixed threshold monitoring이다.
- 내 연구에 쓸 곳: sensing task를 network interference에서 분리하는 pipeline architecture와 end-to-end metric 참고.
- 인용할 문장 (있으면, 15단어 이내): "separates sensing and communication processes"

## 불확실한 점
- 확인 필요: "supervisory-control requirements"의 402 ms 허용 기준이 명시적 deadline으로 정의되지 않는다.
