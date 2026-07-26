# A Multimodal TinyML-Based Predictive Maintenance Architecture for Industrial IoT in the 6G Era

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S1 (embedded RT FD 대조군), S6 (latency 계층 분리 사례)
- **플랫폼 태그**: `PL-MCU` (진동: nRF52832 Cortex-M4F), 음향: NDP120 ASIC, 열화상: Cortex-M7
- **실행환경 태그**: `ENV-RTOS` (진동 노드: Arduino Mbed OS v4.6.0 — deployment runtime으로만 사용)
- **출처/연도**: Sensors 2026, DOI: 10.3390/s26144536
- **저자**: Carlos Exequiel Garay et al.
- **원문 위치**: `papers/05_fault_diagnosis_app/Multimodal_TinyML_Predictive_Maintenance_Architecture.pdf`
- **재판정 분석**: `papers/05_fault_diagnosis_app/reviews/c326d3e8-b9b9-4102-80aa-397346f9bc38_Garay_2026_Multimodal_TinyML_RT_등급_개인연구.pdf`

---

## 두 질문

- **가변 변수**: 없음. W/H/M 전부 offline 고정. 진동 W=60 samples=6 s, H=W (non-overlapping), M=modality별 고정 모델.
- **트리거**: 진동 anomaly score가 healthy-training 95th percentile 초과 시 anomaly로 판단 (고정 threshold). Fusion probability p ≥ τ이면 cloud event 전송. 어느 것도 runtime W/H/M 변경을 유발하지 않음.

---

## RT 등급: B (확정)

**B 유지 근거 (원문 section/page 기준)**

| 판정 항목 | 결과 | 원문 근거 |
|---|---|---|
| 로컬 fault diagnosis deadline 수치 | X | 논문 전체에 없음 |
| 로컬 추론 tail latency (p99/max) | X | Section 5.1 p.17; Table 4 p.13: median만 보고 |
| 로컬 deadline miss count/rate | X | 없음 |
| p95/p99 측정 | △ cloud path만 | Table 9 p.25: forwarder publish → AWS Lambda 경로만 해당 |
| RTOS RT scheduling 사용 | X | Mbed OS는 deployment runtime, task priority·period·WCET 없음 |
| schedulability 분석 | X | 없음 |
| gateway fusion runtime 동작 | X | Figure 1 caption p.5: "fusion stage is evaluated offline" |

**핵심 패턴**: 로컬 추론이 sample period(100 ms)보다 394배 빠름(254 μs)을 사실상 주장하지만, 이를 deadline으로 정의하거나 miss를 측정하지 않는다. B등급의 전형적 패턴이다.

---

## 핵심 방법 요약

### 시스템 구조 (Figure 1–2, pp.5–7)

```
TinyML sensing nodes
├── 진동: INT8 autoencoder, nRF52832 Cortex-M4F (Nicla Sense ME)
├── 음향: NN classifier, Syntiant NDP120 ASIC (Nicla Voice)
└── 열화상: CNN, OpenMV Cam H7+ (Cortex-M7)
          ↓ (BLE/serial)
Edge-AI gateway: Arduino Portenta H7
  └── decision-level late fusion (logistic regression) ← 현재 prototype에서 offline 분석
          ↓ (Wi-Fi / MQTT)
AWS cloud (storage, digital twin, dashboard, alerting)
```

### W/H 설계 근거 (Section 3.2, p.8; Table 2, p.10)

- 진동 W = 60 samples = 6 s (host cadence 10 Hz)
- W의 근거: skewness·excess kurtosis 같은 고차 통계량의 분산 안정성. 더 짧은 window는 4차 통계량을 불안정하게 만든다고 설명 (FFT 기반 spectral 분석이 아님)
- H = W (non-overlapping). Section 5.5 synchronized evaluation에서 명시; 실제 runtime diagnosis hop 정의는 별도로 없음
- **Yang et al.과의 차이**: Yang은 베어링 characteristic frequency(Δf_min)에서 W를 유도; Garay는 통계량 안정성에서 유도. 목적이 다름.

### 로컬 추론 성능 (Table 4, p.13; Section 5.1, p.17)

| 모델 | Cortex-M4F latency | Flash | F1 |
|---|---|---|---|
| Q8INT FC autoencoder | 254 μs (median, 16,605 calls) | 6056 B | 0.9807 |
| FP32 FC autoencoder | 293 μs | 6640 B | 0.9807 |
| OC-SVM | 7057 μs | 14,584 B | 0.9831 |

### Cloud latency (Table 9, p.25; Section 6.3, pp.24–25)

측정 경로: **Local Mosquitto event → Python forwarder publish → TLS-MQTT → AWS IoT Core → AWS Lambda arrival**

(진동 수집, feature extraction, MCU inference, sensor→gateway 전송 미포함)

| 지표 | 값 |
|---|---|
| baseline mean | 562.63 ms |
| p95 | 649.59 ms |
| p99 | 662.78 ms |
| cloud 비중 | end-to-end의 79–88% |

---

## 실험 결과 (Section 5, pp.17–23)

- 실험 데이터: 단일 회전기계, 정적 불평형 testbed, 진동/음향/열화상 실수집
- 진동 anomaly 임계값: healthy training 95th percentile (offline 설정, runtime 불변)
- Healthy baseline recalibration: 센서 재장착 후 짧은 재보정으로 F1=0.975 회복 (weight retraining 없음)
- 6G: Wi-Fi/MQTT 실험, 5G/6G 무선망 미사용. "6G 호환"은 roadmap 표현

---

## 내 연구 관점

**유사점 (참고 가능)**
- 실제 저전력 target(Cortex-M4F)에서 inference latency와 memory를 측정하는 방법론 → 본 연구의 Pi Zero 2W mode profiling에서 동일하게 필요
- R_E2E = T_acquisition + T_preprocess + T_queue + T_inference + T_postprocess 구조 분리의 필요성을 반례로 보여줌 (이 논문은 T_inference만 측정)
- Cloud path p99 측정이 로컬 task tail latency가 아님을 명시 → 본 연구에서 측정 계층 구분의 중요성 입증 근거

**결정적 차이**

이 논문은 세 modality의 고정 TinyML pipeline을 센서 노드에서 실행하고 결과를 gateway/cloud로 전달한다. 하지만 기계 상태 q와 scheduling slack S를 동시에 보고 W/H/M 조합을 runtime에 선택하는 것은 다루지 않는다.

| 관점 | Garay et al. | 개인연구 |
|---|---|---|
| Platform | Cortex-M MCU/ASIC/Portenta H7 | Raspberry Pi Zero 2W + PREEMPT_RT |
| Adaptation | 없음 (설치 후 threshold recalibration) | Runtime W/H/M mode selection |
| Condition | anomaly score threshold (고정) | 기계 상태 q (dynamic) |
| System state | 사용 안 함 | S = D − p99(R_recent) |
| Local deadline | 없음 | 명시적으로 정의 예정 |
| Local tail | median만 | p99/max/miss 핵심 |
| Scheduling | 없음 | PREEMPT_RT task interference 분석 |
| Latency p99 | cloud transport | local diagnosis response |

**인용 맥락**: S1 (B등급 대조군), S6 (latency 계층 분리 사례). "edge-first inference가 필요하다고 주장하지만 로컬 task deadline과 tail을 정의·측정하지 않는다"는 맥락에서 인용. 또한 "inference만 빠르다고 전체 fault detection response가 빠른 것이 아니다"의 반례로 활용 가능.

**인용 후보 문장** (Section 6.3, p.24): `"cloud-uplink leg dominates the end-to-end budget"`

---

## 서베이 표 항목

| 항목 | 내용 |
|---|---|
| 가변 변수 | 없음 — W/H/M 전부 offline 고정 |
| 트리거 | anomaly score > 95th percentile threshold (고정값) |
| 플랫폼·환경 | nRF52832 Cortex-M4F, Arduino Mbed OS v4.6.0 (deployment runtime) |
| 보장 수준 | B — 로컬 추론 median만 보고, cloud p99는 전송 경로만 해당 |
| 본 연구와의 gap | W/H/M 고정, q+S trigger 없음, 로컬 deadline·tail 미정의·미측정 |

---

## 세 문장 압축

이 논문은 진동·음향·열화상 세 modality의 TinyML 추론을 센서 노드에서 수행하고 decision-level fusion 결과만 클라우드로 전달하는 멀티모달 예지보전 아키텍처를 다룬다. 각 modality의 W/H/M은 offline에 고정되고 runtime adaptation이 없으며, 측정한 p95/p99는 로컬 진단 task가 아닌 클라우드 전송 경로에 해당한다. 기계 상태 q와 scheduling slack S를 동시에 보고 W/H/M 조합을 선택하는 것은 다루지 않는다.

---

## 불확실한 점

- Mbed OS scheduler 구성(preemptive/cooperative, task priority, thread 목록): 원문에 없음
- Gateway(Portenta H7) OS/runtime: 언급 없음
- Fusion threshold τ: 사용되지만 설정값과 runtime 변경 정책 없음
- H(runtime diagnosis hop): Section 5.5 evaluation에서 6 s로 쓰이지만, 실제 deployment prototype의 runtime cadence 정의는 별도로 없음
