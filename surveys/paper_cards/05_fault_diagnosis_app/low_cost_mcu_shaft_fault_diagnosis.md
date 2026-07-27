# 저비용 마이크로컨트롤러 환경에서의 경량 딥러닝 기반 회전기계 축 결함 진단 시스템

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S3 (경량화 대조군), KCC 2026·본 연구의 직전 baseline
- **플랫폼 태그**: `PL-MCU`
- **실행환경 태그**: `ENV-BAREMETAL` (RTOS 사용 없음; bare-metal 여부 명시 없으나 RTOS future work로 제시)
- **출처/연도**: 2025 한국소프트웨어종합학술대회 논문집, pp.1434–1436
- **저자**: 최성현, 김서랑, 김태현
- **분석 MD**: `papers/05_fault_diagnosis_app/reviews/Choi_2025_KSC_STM32_Shaft_Fault_분석.md`

---

## 두 질문

- **가변 변수**: 없음. W=2048, f_s=16 kHz, M(FRFconv-TDSNet) 전부 고정.
- **트리거**: 없음. Runtime mode selection 없음.

---

## 초록

본 연구는 하드웨어 자원이 극도로 제한된 마이크로컨트롤러 환경에서 원시 진동 데이터를 활용한 회전기계 축 결함 진단 시스템을 제안한다. STM32F401RET6에서 진동 데이터를 수집하고 경량 딥러닝 모델로 결함을 추론한 뒤 결과를 LCD 패널에 출력하는 프로세스를 구현하였다. 전체 시스템 실행 시간은 약 0.8초 이내이며 평균 99.25%의 진단 정확도를 달성하였다.

---

## 논문 흐름 + Novelty

Cloud 중심 결함 진단의 전송 지연·병목 문제를 제기하고, USB digital accelerometer, STM32F401RET6, FRFconv-TDSNet, LCD를 통합한 완전한 MCU-side diagnosis system을 구현한다. 새로운 fault-diagnosis algorithm 제안이 아닌 **기존 경량 모델 FRFconv-TDSNet을 저비용 MCU에 실제 배포하고 sensing–inference–display pipeline을 통합한 system implementation + embedded feasibility validation**이 contribution이다. Module별 평균·SD·min·max 실행시간과 Flash·SRAM 사용량을 정량 보고한다.

---

## RT 등급: B (확정)

| 판정 항목 | 결과 | 원문 근거 |
|---|---|---|
| 명시적 deadline | X | 선언 없음 |
| RTOS 또는 PREEMPT_RT | X | RTOS 없음, future work로 제시 |
| Deadline miss / p99 | X | miss ratio·p99 미보고 |
| Module별 max latency | 부분 O | Table 3에 sensing max 167 ms, inference max 555.910 ms 보고 |
| Acquisition period T_W | △ | T_W=128 ms 계산 가능, deadline으로 미선언 |
| W/H/M runtime 변경 | X | 없음 |

### Deadline 판정: △

$f_s=16\ \mathrm{kHz}$, $W=2048$ → $T_W=128\ \mathrm{ms}$. 그러나 sensing 단독 평균(151 ms)이 이미 T_W를 초과하며, inference(556 ms)까지 합산하면 T_total ≈ 5.96 T_W다. 논문은 이를 deadline miss로 다루지 않고 "약 0.8 s 이내"로 요약한다.

---

## 핵심 수치

| 지표 | 값 | 원문 위치 |
|---|---|---|
| 플랫폼 | STM32 Nucleo-64, STM32F401RET6 | Section 2.1 |
| 클럭 | 84 MHz | Table 1 |
| RAM | 96 KiB | Table 1 |
| Flash | 512 KiB | Table 1 |
| 실행 환경 | RTOS 없음 (bare-metal 추정); X-CUBE-AI | Section 3 |
| X-CUBE-AI version | 미보고 | — |
| 센서 | USB digital accelerometer (model명 미보고) | Section 2.1 |
| f_s | 16 kHz | Section 2.2 |
| W | 2048 samples | Section 2.2 |
| T_W | 128 ms | 계산값 |
| H | 미정의 | — |
| 결함 유형 | Healthy, Looseness, Misalignment(×3), Unbalance(×3) | Table 2 |
| 클래스 수 | 8 | — |
| 모델 | FRFconv-TDSNet | Section 2.3 |
| 파라미터 수 | 미보고 | — |
| Quantization | X-CUBE-AI 변환 사용; bit-width 미기재 | Section 2.3 |
| Accuracy | 평균 99.25% | Section 2.3 |
| Model weights | 34.50 KiB | Section 2.3 |
| Activation buffer | 32.01 KiB | Section 2.3 |
| 전체 Flash 사용 | 144.69 KiB (약 30%) | Section 2.4 |
| 전체 SRAM 사용 | 73.54 KiB (약 75%) | Section 2.4 |

### Module별 실행시간 (Table 3)

| Module | 평균 | SD | 최소 | 최대 |
|---|---:|---:|---:|---:|
| Sensing | 151.205 ms | 5.202 ms | 139.016 ms | 167.033 ms |
| Inference | 555.872 ms | 0.028 ms | 555.800 ms | 555.910 ms |
| Output | 56.158 ms | 0.000 ms | 56.158 ms | 56.158 ms |
| **E2E 합계** | **763.235 ms** | — | — | — |

$$T_{\mathrm{total}} \approx 763\ \mathrm{ms} \approx 5.96\,T_W$$

**Sensing jitter(SD 5.202 ms)**: USB accelerometer 인터페이스에서 발생. Inference와 Output은 SD가 거의 0으로 결정론적이다. Jitter의 원인은 sensing 단계에 집중되어 있다.

**Sensing 151 ms > T_W 128 ms**: USB 취득 오버헤드 때문으로 추정되나 원문에 설명 없음.

---

## 세 문장 압축

Choi et al.은 USB digital accelerometer, STM32F401RET6, FRFconv-TDSNet, LCD를 통합한 low-cost MCU shaft-fault diagnosis system을 구현하고 sensing·inference·output module별 실행시간을 정량 보고한다. 8-class accuracy 99.25%를 달성했으며 평균 E2E latency는 약 763 ms이고 전체 memory 사용량은 Flash 144.69 KiB, SRAM 73.54 KiB다. 그러나 H, explicit deadline, p99, miss ratio, q+S 기반 runtime W/H/M adaptation은 다루지 않으며 RTOS 적용은 future work로 남겼다.

## Related Work 영어 한 줄

> Choi et al. integrated raw-vibration sensing, FRFconv-TDSNet inference, and LCD reporting on an STM32F401 microcontroller, but used a fixed window and model without runtime W/H/M adaptation, and the 763-ms end-to-end latency was not evaluated against an explicit deadline.

---

## 불확실한 점

1. X-CUBE-AI version 미보고
2. USB digital accelerometer 정확한 model명 미보고
3. Bare-metal firmware인지 vendor HAL framework인지 미명시
4. Quantization bit-width 미기재 (INT8 여부 불확실)
5. Quantization PTQ·QAT 구분 미기재
6. H·overlap·stride·diagnosis period 미정의
7. W=2048 선정 근거 미기재
8. FRFconv-TDSNet parameter 수·MACs 미보고
9. Latency 측정 반복 횟수 미기재
10. Sensing 151 ms > T_W 128 ms인 이유 미설명 (USB overhead 추정)
11. E2E 최대·p99 latency 미보고
12. Baseline model 대비 accuracy·latency·memory 비교 없음
