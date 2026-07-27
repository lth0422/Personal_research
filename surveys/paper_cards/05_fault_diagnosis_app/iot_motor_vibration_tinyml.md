# IoT Device for Detecting Abnormal Vibrations in Motors Using TinyML

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S3 (경량화 대조군), S4 (E2E pipeline latency 분해 참고)
- **플랫폼 태그**: `PL-MCU`
- **실행환경 태그**: `ENV-OTHER` (OS 미기재; Edge Impulse firmware; TFLite Micro 여부 미명시)
- **출처/연도**: Discover Internet of Things, Vol. 5, 2025, Art. no. 41, DOI 10.1007/s43926-025-00142-4
- **저자**: Stalin Arciniegas, Dulce Rivero, Jefferson Piñan, Elizabeth Diaz, Francklin Rivas
- **분석 MD**: `papers/05_fault_diagnosis_app/reviews/Arciniegas_2025_XIAO_ESP32S3_TinyML_분석.md`

---

## 두 질문

- **가변 변수**: 없음. W=16, H=8, f_s=100 Hz, M(DNN+K-means) 전부 고정.
- **트리거**: 없음. Runtime mode 변경 없음. K-means anomaly score가 threshold를 넘으면 MQTT alert를 보내지만, 이것은 mode selection이 아니라 alert 조건이다.

---

## 초록 번역

본 논문은 MPU6050과 XIAO ESP32S3를 이용해 모터 진동을 edge에서 분석하고, TinyML 기반 이상 감지 결과를 MQTT, Node-RED, Telegram으로 전달하는 IoT 시스템을 제안한다. 실험실 환경에서 96.5% accuracy와 약 300 ms의 sensing-to-alert latency를 보고하며, 저전력 MCU에서도 spectral feature와 neural-network inference를 결합한 상태 감시가 가능하다고 주장한다.

---

## 논문 흐름 + Novelty

### 논리 흐름

1. Cloud 기반 예지보전의 network latency·bandwidth·privacy 문제를 제기하고, edge에서 직접 처리하는 TinyML을 대안으로 제시한다.
2. MPU6050 → ESP32S3 → MQTT → Node-RED → Telegram 순서의 full IoT pipeline을 구성한다.
3. Edge Impulse로 DNN classifier(운전 상태 3-class)와 K-means anomaly detector를 학습·양자화·배포한다.
4. Laboratory 정확도와 inference latency, end-to-end sensing-to-alert latency를 평가하고 2개월 실환경 운용 결과를 추가 보고한다.

### 분류 형태 주의

이 논문은 **베어링 고장 유형(inner/outer/ball 등)을 다중 분류하지 않는다.** DNN은 Stopped/Average Speed/High Speed의 운전 상태를 분류하고, K-means가 비정상 진동을 별도로 탐지한다. 원문 서술에서 DNN output이 3 neurons인데 four labels를 나열하는 모순이 있으나, 운전 상태 3-class + 별도 anomaly detector 구조로 해석하는 것이 가장 일관적이다.

### Novelty

신규 학습 알고리즘보다 **시스템 구현 contribution**이다.

- XIAO ESP32S3에서 FFT, TinyML classification, K-means anomaly detection을 함께 실행
- Edge inference 결과를 MQTT·Node-RED·Telegram alert로 연결한 end-to-end IoT pipeline
- MCU inference latency와 sensing-to-alert E2E latency를 함께 분해·보고

---

## RT 등급: B (확정)

| 판정 항목 | 결과 | 원문 근거 |
|---|---|---|
| 명시적 deadline | X | 없음 |
| RTOS | X | OS 미기재 |
| Deadline miss / p99 / max | X | 미보고 |
| Average inference latency | O | 25 ms, SD 3 ms (Section 7.1.1) |
| E2E latency | O | 약 300 ms |
| Acquisition period (implicit) | △ | T_H=80 ms 계산 가능, deadline 선언 없음 |
| W/H/M runtime 변경 | X | 전부 고정 |

### Deadline 판정: △

f_s=100 Hz, H=8 samples → T_H=80 ms. Inference 25 ms < T_H 80 ms이나 논문은 이를 deadline 기준으로 선언하거나 miss를 측정하지 않는다.

---

## 핵심 수치

| 지표 | 값 |
|---|---|
| 플랫폼 | Seeed XIAO ESP32S3 Sense (Xtensa LX7 dual-core) + MPU6050 |
| 실행환경 | OS 미기재; Edge Impulse firmware; TFLite Micro 여부 미명시 |
| W | 16 samples, f_s=100 Hz → T_W=160 ms |
| H | 8 samples (50% overlap) → T_H=80 ms |
| 양자화 | INT8 (32-bit → INT8) + matrix factorization pruning + Huffman coding |
| Inference latency | 평균 25 ms, SD 3 ms |
| E2E sensing-to-alert | 약 300 ms |
| Accuracy | 실험실 96.5%; 2개월 운용 98% |
| Model size | Flash·RAM 수치 미보고 |

### E2E latency 분해

$$T_{\mathrm{E2E}} = T_{\mathrm{collection}} + T_{\mathrm{inference}} + T_{\mathrm{network+alert}} = 80 + 25 + 195\ \mathrm{ms} \approx 300\ \mathrm{ms}$$

| 구간 | 시간 | 내용 |
|---|---:|---|
| Data collection | 80 ms | MPU6050 vibration sample 확보 |
| Model inference | 25 ms | MCU TinyML inference |
| Network + alert | 195 ms | Wi-Fi, MQTT, Node-RED, Telegram |
| **Total** | **~300 ms** | Sensing 시작부터 alert 생성까지 |

**주의:** FFT·filtering latency가 25 ms inference에 포함되는지, 80 ms collection에 포함되는지 원문이 명확히 분리하지 않는다. 또한 16 samples × (1/100 Hz) = 160 ms가 필요한데 collection 시간이 80 ms로 보고된다 — 이는 steady-state hop interval로 해석하는 것이 자연스럽다.

**개인연구 관점:** inference time만 보면 fast(25 ms)지만, IoT pipeline을 포함한 E2E는 300 ms다. System-level latency 논의에서 "inference가 빠르다고 real-time이 보장되지 않는다"는 근거로 활용할 수 있다.

---

## 세 문장 압축

Arciniegas et al.은 MPU6050, XIAO ESP32S3, Edge Impulse, MQTT, Node-RED, Telegram을 연결한 TinyML 기반 motor-vibration monitoring system을 구현한다. DNN은 운전 상태 3-class를 분류하고 K-means가 abnormal vibration을 별도로 탐지하며, average inference latency 25 ms와 sensing-to-alert latency 약 300 ms를 보고한다. 그러나 W=16·H=8은 고정되어 있고 explicit deadline, p99, deadline miss, runtime q+S mode selection은 다루지 않는다.

## Related Work 영어 한 줄

> Arciniegas et al. integrated FFT-based TinyML inference and K-means anomaly detection with an MQTT–Node-RED alert pipeline on a XIAO ESP32S3, but used a fixed sensing and model configuration without runtime W/H/M adaptation or tail-latency analysis.

---

## 불확실한 점

1. Edge Impulse firmware 내부 runtime이 TFLite Micro인지 여부가 미명시다.
2. Model parameter 수, Flash·RAM 사용량, arena size가 미보고다.
3. FFT·filtering latency가 25 ms inference에 포함되는지 80 ms collection에 포함되는지 불명확하다.
4. 80 ms collection latency와 16-sample window acquisition(160 ms 필요)의 불일치가 원문에서 설명되지 않는다.
5. Inference time 측정 횟수와 warm-up 여부가 미기재다.
6. Maximum, p95, p99 latency와 deadline-miss ratio가 없다.
7. 300 ms E2E latency의 반복 횟수와 SD가 미보고다.
8. Lab accuracy 96.5%와 industrial 98%의 evaluation protocol 차이가 설명되지 않는다.
9. DNN output이 3 neurons인데 four labels를 나열한 원문 서술 모순이 해결되지 않는다.
