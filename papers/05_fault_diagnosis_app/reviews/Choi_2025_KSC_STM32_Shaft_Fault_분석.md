# Choi et al. (2025) — 저비용 MCU 기반 회전기계 축 결함 진단 시스템 분석

> **대상 논문**  
> 최성현, 김서랑, 김태현,  
> “저비용 마이크로컨트롤러 환경에서의 경량 딥러닝 기반 회전기계 축 결함 진단 시스템,”  
> *2025 한국소프트웨어종합학술대회 논문집*, pp. 1434–1436.
>
> **참고**  
> 사용자 프롬프트의 저자명과 원문 저자명이 다르다. 본 문서는 원문 표기인 최성현, 김서랑, 김태현을 따른다.
>
> **개인연구 기준**
>
> $$
> a=(W,H,M), \quad \text{trigger}=q+S
> $$
>
> **분류**  
> 경량화 대조군 Set B  
> 본 연구실 선행연구

---

# 0. 초록

본 연구는 하드웨어 자원이 극도로 제한된 마이크로컨트롤러 환경에서 원시 진동 데이터를 활용한 회전기계 축 결함 진단 시스템을 제안한다. 제안된 시스템은 STM32F401RET6 마이크로컨트롤러 상에서 진동 데이터를 수집하고 경량 딥러닝 모델을 통해 결함을 추론한 뒤, 결과를 LCD 패널에 출력하는 결함 진단 프로세스를 구현하였다. 전체 시스템의 실행 시간은 약 0.8초 이내로, 결함 발생 후 수 초 이내에 결함 상태를 신속하게 탐지할 수 있다. 제안된 경량 딥러닝 모델은 평균 99.25%의 높은 진단 정확도를 달성하여, 자원 제약이 심한 임베디드 시스템 환경에서도 효과적인 결함 진단이 가능함을 입증하였다.

---

# 1. 논문 논리 흐름과 Novelty

기존 cloud 중심 결함 진단은 데이터 전송량 증가와 병목으로 즉각적인 대응이 어렵다는 한계가 있다. 이에 저자는 STM32F401RET6 기반 Nucleo-64 보드가 USB digital accelerometer로 raw vibration을 수집하고, FRFconv-TDSNet으로 shaft fault를 추론한 뒤 LCD에 결과를 표시하는 완전한 MCU-side diagnosis system을 구현한다. 1400 RPM, 16 kHz 조건에서 2048-sample vibration window를 사용하며, Healthy, Looseness, Misalignment 3단계, Unbalance 3단계를 포함한 8-class classification을 수행한다.

Novelty는 새로운 fault-diagnosis algorithm 제안보다는 **기존 경량 모델인 FRFconv-TDSNet을 저비용 MCU에 실제 배포하고 sensing–inference–display pipeline을 통합한 system implementation contribution**에 가깝다. 또한 각 module의 평균, 표준편차, 최소, 최대 실행시간과 전체 Flash 및 SRAM 사용량을 제시했다는 점에서 embedded feasibility validation의 성격이 강하다.

---

# 2. 핵심 수치

| 지표 | 값 | 원문 근거 |
|---|---|---|
| 플랫폼 | STM32 Nucleo-64, STM32F401RET6 | Section 2.1, p.1434 |
| 클럭 | 84 MHz | Table 1, p.1435 |
| RAM | 96 KiB SRAM | Table 1, p.1435 |
| Flash | 512 KiB Flash | Table 1, p.1435 |
| 실행 환경 | RTOS 사용 없음. Bare-metal 여부는 명시하지 않음 | Section 3에서 RTOS 적용을 future work로 제시 |
| X-CUBE-AI version | 미보고 | Section 2.3 |
| 센서 | USB digital accelerometer. 정확한 model명은 미보고 | Section 2.1, 2.4 |
| $f_s$ | 16 kHz | Section 2.2, p.1435 |
| $W$ | 2048 samples | Section 2.2, p.1435 |
| $T_W$ | 128 ms | $2048/16000=0.128$ s |
| $H$ | 미정의 | Overlap, stride, hop 미보고 |
| $T_H$ | 계산 불가 | $H$ 미정의 |
| 결함 유형 | Healthy, Looseness, Misalignment, Unbalance | Table 2, p.1435 |
| 클래스 수 | 8 | H, L, M1–M3, U1–U3 |
| 모델 구조 | FRFconv-TDSNet | Section 2.3 |
| 파라미터 수 | 미보고 | 원문 미기재 |
| INT8 quantization | 미보고 | X-CUBE-AI 변환만 기재 |
| Accuracy | 평균 99.25% | Section 2.3, Figure 3 |
| Inference latency | 평균 555.872 ms | Table 3, p.1436 |
| Inference latency 표준편차 | 0.028 ms | Table 3 |
| Inference latency 최소 | 555.800 ms | Table 3 |
| Inference latency 최대 | 555.910 ms | Table 3 |
| Sensing latency | 평균 151.205 ms | Table 3 |
| Output latency | 평균 56.158 ms | Table 3 |
| End-to-end 평균 latency | 약 763.235 ms | $151.205+555.872+56.158$ |
| Model weight size | 34.50 KiB | Section 2.3 |
| Activation buffer | 32.01 KiB | Section 2.3 |
| 전체 Flash 사용량 | 144.69 KiB, 약 30% | Section 2.4 |
| 전체 SRAM 사용량 | 73.54 KiB, 약 75% | Section 2.4 |
| p99 latency | 미보고 | 원문 미기재 |
| Maximum latency | Module별 최대값 보고 | Table 3 |

## 2.1 Window duration과 실행시간 관계

입력 window duration은 다음과 같다.

$$
T_W
=
\frac{W}{f_s}
=
\frac{2048}{16000}
=
0.128\ \mathrm{s}
=
128\ \mathrm{ms}
$$

평균 inference time은

$$
C_{\mathrm{infer}}
=
555.872\ \mathrm{ms}
$$

이므로

$$
C_{\mathrm{infer}}
>
T_W
$$

이다.

전체 평균 pipeline time은

$$
T_{\mathrm{total}}
=
151.205
+
555.872
+
56.158
=
763.235\ \mathrm{ms}
$$

따라서 다음 관계가 성립한다.

$$
T_{\mathrm{total}}
\approx5.96T_W
$$

다만 원문은 $T_W=128$ ms를 deadline 또는 period로 정의하지 않으며, $H$도 보고하지 않는다. 따라서 이 비교는 보고된 sampling configuration으로부터 계산한 사후 해석이다.

## 2.2 Module별 timing

| Module | 평균 | 표준편차 | 최소 | 최대 |
|---|---:|---:|---:|---:|
| Sensing | 151.205 ms | 5.202 ms | 139.016 ms | 167.033 ms |
| Inference | 555.872 ms | 0.028 ms | 555.800 ms | 555.910 ms |
| Output | 56.158 ms | 0.000 ms | 56.158 ms | 56.158 ms |
| **합계** | **763.235 ms** | 합산 통계 미보고 | 합산 최소 미보고 | 합산 최대 미보고 |

원문은 전체 system이 약 0.8 s 이내에 동작한다고 요약한다.

---

# 3. Deadline 판정

## 종합 판정: **△**

| 판정 항목 | 결과 | 원문 근거 |
|---|---|---|
| 명시적 deadline 선언 | X | Deadline $D$를 정의하지 않음 |
| RTOS 또는 PREEMPT_RT | X | 현재 system에는 RTOS가 없으며 future work로 제시 |
| Deadline miss / p99 / max | 부분 O | Module별 max는 보고하지만 p99와 miss ratio는 미보고 |
| 평균 inference latency | O | Table 3에서 555.872 ms 보고 |
| Acquisition period $T_W$ 또는 $T_H$ | △ | $T_W=128$ ms는 계산 가능하지만 $H$와 period는 미정의 |
| $W/H/M$ runtime 변경 | X | Fixed $W$, fixed FRFconv-TDSNet 사용 |

### 판정 근거

Sampling rate와 window size로 acquisition duration은 계산 가능하다. 그러나 이를 deadline으로 선언하지 않고, $H$, job release period, miss ratio를 정의하지 않는다. 따라서 deadline은 **△**가 적절하다.

또한 inference와 전체 pipeline이 $T_W$보다 길지만, 원문은 이를 deadline violation으로 다루지 않고 단순히 약 0.8 s 내 진단이 가능하다고 해석한다.

---

# 4. 한 줄 gap

> Choi et al.은 fixed $W=2048$과 fixed FRFconv-TDSNet을 STM32F401에 배포하지만, machine condition $q$와 system slack $S$에 따라 $W/H/M$을 runtime에 조절하지 않으며 explicit deadline과 miss analysis를 제공하지 않는다.

---

# 5. 세 문장 압축

Choi et al.은 USB digital accelerometer, STM32F401RET6, FRFconv-TDSNet, LCD를 통합한 low-cost MCU shaft-fault diagnosis system을 구현한다. 8-class accuracy 99.25%를 달성했으며 sensing, inference, output을 포함한 평균 end-to-end latency는 약 763 ms이고 전체 memory 사용량은 Flash 144.69 KiB와 SRAM 73.54 KiB다. 그러나 $H$, explicit deadline, p99와 miss ratio, $q+S$ 기반 runtime $W/H/M$ adaptation은 다루지 않는다.

---

# 6. Related Work

> Choi et al. integrated raw-vibration sensing, FRFconv-TDSNet inference, and LCD reporting on an STM32F401 microcontroller, but used a fixed window and model without runtime adaptation to machine condition or system slack and did not evaluate explicit deadline satisfaction.

---

# 7. 불확실한 점

1. X-CUBE-AI version
2. USB digital accelerometer의 정확한 model
3. Bare-metal firmware인지 vendor framework 기반인지
4. $H$, overlap, stride, diagnosis period
5. $W=2048$의 물리적 또는 empirical 선정 근거
6. FRFconv-TDSNet parameter 수와 MACs
7. Quantization 적용 여부
8. Quantization이 PTQ인지 QAT인지
9. Latency 측정 반복 횟수
10. Module별 평균과 표준편차를 계산한 sample 수
11. 전체 end-to-end latency의 직접 측정값과 최대값
12. USB sensing 151.205 ms가 128 ms acquisition duration보다 긴 이유
13. Inference latency에 data copy와 X-CUBE-AI runtime overhead가 포함되는지
14. Healthy 또는 각 fault condition에 따라 inference time이 달라지는지
15. Baseline model과의 accuracy, latency, memory 비교
