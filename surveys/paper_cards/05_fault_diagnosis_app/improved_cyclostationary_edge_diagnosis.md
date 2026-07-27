# Real-Time Fault Diagnosis of Motor Bearing via Improved Cyclostationary Analysis Implemented onto Edge Computing System

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S3 (경량화 대조군), 원고 반례 ("online edge 실행 ≠ deadline 충족")
- **플랫폼 태그**: `PL-MCU`
- **실행환경 태그**: `ENV-OTHER` (C implementation, FPU + MCU DSP library; OS·RTOS 미기재)
- **출처/연도**: IEEE Transactions on Instrumentation and Measurement, Vol. 72, 2023, DOI 10.1109/TIM.2023.3295476
- **저자**: Changbo He, Pengpeng Han, Jingfeng Lu, Xiaoxian Wang, Juncai Song, Zhixiong Li, Siliang Lu
- **분석 MD**: `papers/05_fault_diagnosis_app/reviews/He_2023_ICFEE_Edge_RealTime_분석.md`

---

## 두 질문

- **가변 변수**: 없음. W=5000, f_s=5000 Hz, M(ICFEE) 전부 고정. 회전속도에서 BPFI·BPFO prior를 update하지만 W·H·M을 바꾸지 않는다.
- **트리거**: 없음. Hall-derived speed는 fault-frequency prior update에만 쓰이며, mode selection trigger가 아니다.

---

## 초록 번역

본 논문은 접촉식 진동 센서 설치가 어려운 환경을 고려해 microphone으로 취득한 sound signal에서 motor bearing fault를 진단하는 improved cyclostationary analysis 방법을 제안한다. Impulse-factor 기반 information curve로 optimal spectral integration band를 자동 선택하는 ICFEE(Improved Cyclic Feature Enhancement Extraction) algorithm을 STM32F407 edge system에 C로 구현하고, inner-race·outer-race fault feature를 MCU에서 계산해 LCD에 표시한다. 보고된 전체 pipeline 시간은 10.294 s로 1 s acquisition window보다 약 10배 길다.

---

## 논문 흐름 + Novelty

### 논리 흐름

1. Accelerometer 기반 진동 진단의 설치 제약을 제기하고, 비접촉 sound signal을 대안으로 제시한다. 기존 full-band cyclostationary integration이 fault와 무관한 주파수까지 포함해 weak feature contrast를 저하시킨다는 문제도 지적한다.
2. 표준 cyclic autocorrelation의 직접 계산 대신 STFT 결과의 cross-product 기반 spectral correlation density를 사용해 matrix 연산을 줄인다.

$$S_x(\alpha, f) = \frac{1}{K\|w\|^2 F_s} \sum_{i=0}^{K-1} X_w(i,f)\, X_w(i, f-\alpha)^*$$

3. ICFEE는 impulse-factor 기반 information curve $g(f_k)$로 fault-sensitive carrier-frequency band $[f_1, f_2]$를 자동 선택하고 그 band에서만 spectral coherence를 적분해 weak cyclic feature를 강화한다.
4. Hall signal로 rotation speed를 실시간 계산하고 BPFI·BPFO prior를 update한다. ICFEE 전체 pipeline을 STM32F407에서 수행하고 LCD에 diagnosis spectrum을 표시한다.
5. Synthetic signal, inner-race 실험(1086 r/min), outer-race 실험(1138 r/min)에서 전통 envelope spectrum과 qualitative 비교로 검증한다.

### Novelty

신호처리 contribution과 MCU 구현 contribution의 결합이다.

- 신호처리: information curve $g(f_k)$로 optimal band 자동 선택 → full-band integration 대비 weak cyclic feature 강화
- 시스템: sound + hall을 STM32에서 동시 처리, speed-dependent fault prior online update, ICFEE 전체 pipeline MCU 구현

**DNN·ML을 사용하지 않는다.** M은 trained model이 아니라 fixed signal-processing algorithm(ICFEE)이다.

### 개인연구 관점: 반례 포지셔닝

이 논문은 "edge MCU에서 online 실행 = real-time" 이라는 암묵적 주장의 **직접 반례**다. Pipeline이 acquisition period보다 10배 이상 길지만 논문은 이를 deadline miss로 다루지 않는다. 원고에서 "경량화 단독으로는 deadline 충족이 보장되지 않는다"는 주장의 근거로 인용할 수 있다.

또한 Hall-derived speed로 fault frequency prior를 update하는 구조는 machine condition q를 일부 활용하는 선례지만, 이 q가 W·H·M mode selection으로 연결되지 않는다는 점에서 개인연구와 구분된다.

---

## RT 등급: B (확정)

| 판정 항목 | 결과 | 원문 근거 |
|---|---|---|
| 명시적 deadline | X | 선언 없음 |
| RTOS 또는 PREEMPT_RT | X | OS·RTOS 미기재 |
| Deadline miss / p99 / max | X | 단계별 단일 실행시간만 보고 |
| Pipeline latency | △ | Total 10.294 s 보고; 반복 횟수·통계량 미보고 |
| Acquisition period T_W | △ | W=5000, f_s=5000 Hz → T_W=1 s; deadline으로 선언 안 함 |
| Pipeline latency < T_W | X | 10.294 s >> 1 s |
| W/H/M runtime 변경 | X | 없음 |

### Deadline 판정: △

T_W=1 s라는 acquisition reference는 존재하나 deadline으로 선언되지 않고 miss가 측정되지 않는다.

---

## 핵심 수치

| 지표 | 값 |
|---|---|
| 플랫폼 | STM32F407IGT6, 168 MHz, 1 MB Flash, 192 KB internal RAM, 2 MB external SRAM |
| 실행 환경 | C, FPU + MCU DSP library; OS·RTOS 미기재 |
| 센서 | PCB377C01 microphone (sound, 비접촉) + BLDC-driver hall signal (speed) |
| ADC | AD7606, 16-bit |
| DNN / ML | 없음 (pure signal processing) |
| f_s | 5000 Hz |
| W | 5000 samples → T_W = 1000 ms |
| H | 미정의 |
| 고장 유형 | Inner race, Outer race (qualitative identification; % accuracy 없음) |

### Pipeline 단계별 실행시간

| 단계 | 실행시간 |
|---|---:|
| 1. Sound + hall acquisition | 1.000 s |
| 2. Rotation-speed calculation | 0.001 s |
| 3. Spectral correlation density | **9.196 s** |
| 4. Information curve $g(f_k)$ 계산 | 0.038 s |
| 5. Enhanced feature extraction | 0.001 s |
| 6. LCD display | 0.058 s |
| **합계** | **10.294 s** |

$$T_{\mathrm{processing}} = 9.294\ \mathrm{s}, \quad T_{\mathrm{total}} = 10.294\ \mathrm{s}$$

$$\frac{T_{\mathrm{total}}}{T_W} = \frac{10.294}{1} \approx 10.3\times \text{ 초과}$$

Spectral correlation density 단계가 전체의 89.3%를 차지한다. 논문은 이를 future optimization 대상으로 인정하며 deadline miss로 다루지 않는다.

**논문의 real-time 근거**: upper computer postprocessing 없이 MCU에서 on-device online processing + LCD display — 엄밀한 periodic deadline satisfaction이 아닌 **현장 online monitoring**의 의미다.

---

## 세 문장 압축

He et al.은 microphone sound와 hall-derived speed를 이용해 optimal integration band를 자동 선택하는 ICFEE cyclostationary analysis를 제안하고 이를 STM32F407 edge system에 구현한다. Inner-race 98 Hz와 outer-race 69 Hz feature를 MCU에서 식별했지만, 1 s acquisition window에 대한 end-to-display latency는 10.294 s였으며 9.196 s가 spectral correlation density 계산에 사용되었다. 이 연구의 real-time은 online edge execution에 가깝고, explicit deadline, p99, miss analysis와 q+S 기반 W/H/M adaptation은 다루지 않는다.

## Related Work 영어 한 줄

> He et al. implemented a speed-informed cyclostationary feature-enhancement pipeline on an STM32F407 for non-contact bearing diagnosis, but its 10.294-s end-to-display latency exceeded the 1-s sensing window and was not evaluated against an explicit deadline or system slack.

---

## 불확실한 점

1. OS·RTOS 사용 여부 (bare metal 추정이나 원문 미기재)
2. 실행시간 측정 도구 (hardware timer, GPIO toggle, oscilloscope 등)
3. 각 단계 실행시간이 1회 측정값인지 반복 평균인지
4. 반복 측정의 SD·max·p99
5. Acquisition과 processing의 DMA overlap·double buffering 여부
6. H·overlap·diagnosis update period 미정의
7. Inner-race와 outer-race 조건에서 실행시간 동일 여부
8. 2 MB external SRAM 실제 사용량과 spectral correlation matrix memory footprint
9. 기존 cyclostationary method 대비 ICFEE runtime 감소율 미보고
10. Healthy condition을 포함한 분류 성능 미보고
11. LCD update 시간이 full spectrum 전송인지 부분 visualization인지
