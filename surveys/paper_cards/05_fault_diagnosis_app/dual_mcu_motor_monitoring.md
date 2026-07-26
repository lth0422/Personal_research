# A Dual-Microcontroller IoT-Based Real-Time Monitoring System for Predictive Maintenance of Induction Motors

- **그룹**: 5 fault_diagnosis_app (배경 참고용 — ML 없음, RT 스케줄링 없음)
- **연구 섹션**: 해당 없음 (S1~S6 어느 섹션과도 직접 비교 불가. 단순 IoT monitoring 논문)
- **플랫폼 태그**: `PL-MCU`
- **실행환경 태그**: `ENV-OTHER` (STM32/ESP32 OS·RTOS 이름과 version 원문 미기재)
- **출처/연도**: IEEE International Electronics Symposium 2025, pp. 164–171
- **DOI**: 10.1109/IES67184.2025.11160991
- **저자**: Ali Husein Alasiry, Haqifal Hanesta Saidya, Ni'am Tamami
- **원문 위치**: `papers/05_fault_diagnosis_app/Dual-Microcontroller_Real-Time_Induction_Motor_Monitoring.pdf`
- **재판정 분석**: `papers/05_fault_diagnosis_app/reviews/Alasiry_2025_Dual_MCU_RT_재판정_개인연구.pdf`

---

## 두 질문

- **가변 변수**: 없음. W/H/M 변경 없음. 센서 threshold와 10 Hz communication rate 고정.
- **트리거**: 각 측정값이 사전 정의 threshold(ISO 10816-3 진동, ±10% 전압·전류, 125°C 온도) 초과 시 ESP32가 Blynk cloud + Telegram alert 전송.

---

## RT 등급: B (확정)

**B 유지 + 서베이 매트릭스 수정 필요**

| 판정 항목 | 결과 | 원문 근거 |
|---|---|---|
| 로컬 deadline 수치 | X | 없음 |
| RTOS 사용 | X | STM32·ESP32 모두 OS/RTOS 이름·version 미기재, pp.1–4 |
| task priority / preemption | X | 없음 |
| sensing period를 task deadline으로 정의 | X | 10 Hz transmission만 명시; deadline 문장 없음, Abstract p.1 |
| schedulability / utilization 분석 | X | 없음 |
| WCET bound | X | 없음 |
| p99 / jitter / deadline miss | X | 없음 |
| AI/ML 모델 | X | threshold + ISO 표준 기반 판정, ML 없음 |

**시스템 scheduling △ 재판정: X로 수정 권고**

기존 매트릭스의 △는 dual-MCU 분리를 scheduling으로 간주한 결과지만, 원문 확인 결과 이는 **architectural/functional isolation**에 불과하다. scheduling policy, priority assignment, timing analysis, bounded interference 중 어느 것도 제시하지 않는다. 서베이 프로토콜 매트릭스에서 Alasiry의 시스템 scheduling 열을 △ → X로 수정해야 한다.

---

## 핵심 방법 요약

### 시스템 구조

```
STM32F103C8T6 (Blue Pill)
├── 3상 전압 (ZMPT101B + 58.9 Hz RC LPF): ADC, peak/RMS 계산
├── 3상 전류 (ACS712-30A): midpoint 보정, channel당 10 sample 평균
├── 온도 (PT100 + MAX31865): SPI read
└── 3축 진동 (ADXL335): analog read, RMS velocity 계산
       ↓ (UART, Serial2)
ESP32-WROOM-32
├── UART string parsing
├── Blynk virtual pin V0–V9 전송 (10 Hz packet)
├── threshold 평가 (ISO 10816-3, ±10%, 125°C)
└── Telegram alert
       ↓ (Wi-Fi / MQTT)
Blynk cloud → mobile UI visualization
```

### 이상 판정 기준 (threshold 기반, ML 없음)

| 물리량 | 기준 | 출처 |
|---|---|---|
| 3상 전압 | 198 V ≤ V ≤ 242 V (nominal ±10%) | Section II |
| 3상 전류 | rated current ±10% | Section II |
| 온도 | T ≤ 125°C | Insulation class F |
| 진동 | RMS velocity ≤ 0.71 mm/s (Good) / 0.72–1.80 (Satisfactory) ... | ISO 10816-3, Table I |

### Latency 측정 (Table II, p.4; Section III, p.4)

측정 구간: **STM32 serial monitor에서 sensor value 변화 표시 시점 → Blynk mobile UI 동일 변화 표시 시점**

(STM32 local sensing·처리, UART, ESP32 parsing·Wi-Fi, Blynk cloud, mobile rendering 포함)

| 측정 | 값 |
|---|---|
| 5회 개별 delay | 358, 466, 430, 395, 359 ms |
| 평균 | 401.6 ms |
| 범위 | 358–466 ms |

이 401.6 ms는 deadline이 아닌 **measured communication delay**다. 논문 스스로 "high-speed control loop에는 부적합"하다고 밝힌다(Section III, p.4). 0.5 s 이하면 timely update로 평가하지만 이를 deadline으로 정의하거나 miss를 측정하지 않는다.

### Dual-MCU isolation 주장 (검증 없음)

STM32를 analog acquisition 전용으로 배치해 wireless overhead가 sampling을 방해하지 않도록 한다고 주장한다. 그러나 single-MCU 대비 sampling jitter 비교, ADC timing 비교, UART backlog 분석, priority·execution trace 중 어느 것도 없다. 설계 설명과 정성적 주장만 있다.

### 실험 결과 (Section II–III, pp.2–7)

- 정상 모터: Mean V_RMS,total = 0.356 mm/s, SD = 0.164 mm/s
- Rear-bearing 손상 모터: Mean V_RMS,total = 0.939 mm/s, SD = 0.304 mm/s
- ISO 10816-3 허용 기준 0.71 mm/s 초과 → 진동만 구분 가능 (전압·전류·온도는 차이 없음)
- 비용: BOM USD 35 미만, firmware 57 kB

---

## 내 연구 관점

**이 논문은 본 연구의 비교군이 아니다.** AI inference, W/H/M 변수, scheduling, RT 보장 중 어느 것도 없다. 인용 필요성이 낮다.

**참고 가능한 구조적 아이디어**: sensing task와 network task를 물리적으로 분리하면 timing interference를 줄일 수 있다는 아키텍처 개념. 단, 본 연구에서는 이를 PREEMPT_RT task isolation로 소프트웨어적으로 구현한다.

**인용 맥락**: 인용하더라도 "IoT 기반 상태 모니터링은 threshold 기반 단순 판정과 cloud visualization latency에 집중하며, ML inference, W/H/M scheduling, deadline 보장을 다루지 않는다"는 대조군 문장에서 1줄 정도.

---

## 서베이 표 항목

| 항목 | 내용 |
|---|---|
| 가변 변수 | 없음 — threshold·sampling rate 고정 |
| 트리거 | ISO/±10% threshold 초과 시 cloud alert |
| 플랫폼·환경 | STM32F103 + ESP32, OS/RTOS 미확인, bare metal 추정 |
| 보장 수준 | B — 평균 cloud latency 측정만, deadline·tail 없음 |
| 본 연구와의 gap | ML 없음, W/H/M 없음, scheduling 없음, RT 보장 없음 |

---

## 세 문장 압축

이 논문은 STM32와 ESP32를 분리해 sensing과 network 간섭을 줄이고 유도전동기의 전압·전류·온도·진동을 cloud에 10 Hz로 전송하는 저비용 IoT monitoring 시스템을 다룬다. ML 없이 ISO 표준 threshold 기반으로 이상을 판정하며, 측정한 latency는 cloud 시각화 지연의 평균값이고 deadline 정의와 tail 측정이 없다. W/H/M 선택, 기계 상태 q와 slack S 기반 runtime 적응, RT scheduling 중 어느 것도 다루지 않는다.

---

## 불확실한 점

- STM32·ESP32의 정확한 OS/RTOS 이름과 bare metal 여부: 원문 전체에 미기재
- 401.6 ms 측정의 정확한 clock source와 timestamp 방법: 불명
- UART baud rate와 packet format byte 수: 불명
- STM32→ESP32 UART 전송 지연 단독 측정: 없음
