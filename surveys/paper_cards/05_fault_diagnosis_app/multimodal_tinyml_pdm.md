# A Multimodal TinyML-Based Predictive Maintenance Architecture for Industrial IoT in the 6G Era

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S1 embedded real-time fault diagnosis, S4 deadline-aware AI inference, S6 platform/interference
- **플랫폼 태그**: `PL-MCU`
- **실행환경 태그**: `ENV-RTOS`
- **출처/연도**: Sensors, 2026, DOI 10.3390/s26144536
- **저자**: Carlos Exequiel Garay et al.

## 두 질문
- **가변 변수**: runtime mode 변수는 없다. Offline model variant와 per-installation healthy threshold recalibration을 비교한다.
- **트리거**: per-window reconstruction-error threshold가 anomaly를 판단하며, deployment shift가 확인되면 healthy baseline을 재보정한다.

## Abstract 3줄 요약
- Vibration, acoustic, thermography를 local TinyML node에서 처리하고 gateway/cloud로 연결하는 multimodal PdM architecture를 제안한다.
- Cortex-M4F에서 다섯 vibration anomaly models의 F1, latency와 memory를 실제 target 기준으로 비교한다.
- Cloud uplink latency가 end-to-end budget을 지배함을 보이고 edge-first inference의 필요성을 주장한다.

## Conclusion 요약
- INT8 autoencoder를 vibration default로 선택하고 multimodal fusion은 redundancy에 유용하다고 평가하며, 6G는 실제 radio 검증이 아닌 roadmap임을 명시한다.

## 요점
- 플랫폼: Arduino Nicla Sense ME nRF52832, Arduino Mbed OS, Nicla Voice/NDP120, OpenMV H7+, Portenta H7, Wi-Fi/MQTT/AWS.
- 도메인: multimodal motor predictive maintenance/anomaly detection.
- 핵심 방법 (2~3줄): Vibration은 10 Hz data의 non-overlap 6 s window에서 10 statistical features를 만든다. Target MCU median latency와 stack/Flash를 비교하고 confidence late fusion 및 cloud latency decomposition을 수행한다.
- 정식화/수식 (있으면): vibration `W=60 samples=6 s`, `H=W`; Q8INT autoencoder median 254 us.

## 0708 면담 기준 보강
- **실시간성 수준**: target latency와 cloud mean/std/p95/p99를 측정하지만 local deadline/miss는 없다. soft/best-effort `B`.
- **실행시간 가정**: model-dependent measured latency; system-level WCET는 없다.
- **보장 방식**: empirical target benchmark와 latency decomposition. 근거: Sections 5.1, 6.3, Tables 4/9.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): network delay를 측정하지만 local `W/H/M`을 slack에 따라 전환하거나 PREEMPT_RT를 비교하지 않는다.
- 내 연구에 쓸 곳: target-specific `M` profiling과 inference/cloud latency 분해, 고정 6 s `W/H` 대조군.
- 인용할 문장 (있으면, 15단어 이내): "cloud-uplink leg dominates the end-to-end budget"

## 불확실한 점
- 확인 필요: Acoustic/thermal dataset의 intra-session leakage와 single-machine scope 때문에 fusion 수치를 일반화하지 않는다.
