# Real-Time Vibration-Based Bearing Fault Diagnosis Under Time-Varying Speed Conditions

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S1 (embedded RT FD 배경), S2 (W 설계 근거)
- **플랫폼 태그**: `PL-DESKTOP`
- **실행환경 태그**: `ENV-OTHER` (MacBook Pro M1 Pro; OS·framework·backend 미기재)
- **출처/연도**: IEEE ICIT 2024, pp.1–7, DOI: 10.1109/ICIT58233.2024.10540813
- **저자**: T. Jalonen, M. Al-Sa'd, S. Kiranyaz, M. Gabbouj
- **분석 PDF**: `papers/05_fault_diagnosis_app/reviews/Time_Varying_Speed_W_Processing_분석.pdf`

---

## 두 질문

- **가변 변수**: 없음. W=2000 samples 고정; M(5-block CNN) 단일 고정; H=W (non-overlapping). Speed가 680~2460 RPM으로 변해도 W를 runtime에 조절하지 않는다.
- **트리거**: 없음. Motor speed PSD의 변화 주파수를 offline 분석해 W를 한 번 결정한다. Runtime trigger 없음.

---

## 초록 번역

구름 요소 베어링의 고장을 탐지하는 것은 선제적 유지보수 전략을 구현하고, 예기치 않은 고장으로 인한 경제적·운영상의 피해를 최소화하는 데 중요하다. 그러나 기존의 많은 방법은 엄격하게 통제된 조건에서 개발·시험되므로, 실제 응용에서 마주치는 다양하고 동적인 환경에 적응하는 데 한계가 있다.

본 논문은 여러 noise level과 시간에 따라 변하는 최전속도 조건에서 다양한 베어링 고장을 진단하기 위한 효율적인 실시간 CNN을 제안한다. 또한 설계한 CNN 모델이 효과적인 이유를 설명하기 위한 새로운 Fisher-based spectral separability analysis(SSA) 방법을 제안한다. 실험 결과 accuracy 최대 15.8%p 향상, noise 강건성 유지, processing duration이 acquisition duration보다 약 5배 짧아 실시간으로 동작함을 보였다.

---

## 논문 흐름 + Novelty

### 논리 흐름

1. 기존 bearing FD는 고정 speed·clean data 조건에서 평가되므로 실제 산업 환경의 time-varying speed와 noise에 취약하다는 문제 제기
2. 680~2460 RPM time-varying dataset(Kaist) 사용; speed 변화의 주파수 특성을 NUFT로 분석해 고정 W=2000 결정
3. 두 accelerometer의 raw time-domain vibration을 입력받는 5-block lightweight CNN으로 Normal/Outer/Inner/Ball 분류
4. Clean 및 여러 SNR에서 PIResNet과 성능 비교; MacBook Pro에서 acquisition 대비 inference time 측정
5. Fisher-based SSA와 t-SNE로 class별 분리·혼동 원인을 시간·주파수 관점에서 해석

### Novelty

| # | 내용 | 근거 |
|---|---|---|
| 1 | Time-varying speed + noise를 함께 다루는 lightweight CNN | Introduction, p.1–2 |
| 2 | Acquisition보다 약 5배 빠른 실시간 진단 (C_avg ≈ 20.2 ms < T_acq = 100 ms) | Section II-B, pp.5–6; Figure 6 |
| 3 | Fisher-based SSA — class별 구분되는 frequency band 파악 | Section II-D, pp.3–4; Figure 7 |

---

## W 설계 — Speed 조건과의 관계

### 핵심 결론

이 논문은 회전 주기나 특정 회전 수를 기준으로 W를 정하지 않는다. Motor speed가 시간에 따라 얼마나 빠르게 변하는지를 frequency analysis한 뒤, 그 변화 주파수를 포착할 수 있는 0.1 s의 고정 segment를 선택한다.

**W = 2000 samples, f_s = 20,000 Hz, T_W = 100 ms**

### (W=2000)을 결정한 4단계 과정

| 단계 | 내용 |
|---|---|
| Step 1 | Speed signal에 NUFT 적용 (비균일 sampling interval 대응) |
| Step 2 | Speed PSD에서 주요 변화 = 8 Hz, 9.15 Hz |
| Step 3 | 10 Hz까지 범위 = speed PSD total power의 99.6% → T = 1/10 Hz = 0.1 s |
| Step 4 | W = 20,000 × 0.1 = 2000 samples |

(근거: Section II-B, pp.2–3)

### 원문의 W 선택 논리

- 너무 길면: speed가 segment 안에서 많이 변함 → 복잡성 증가, 학습 sample 수 감소
- 너무 짧으면: 복잡한 vibration morphology 포함 불충분 → class-specific pattern 학습 어려움
- **결론**: speed-change frequency로 100 ms를 절충값으로 선택

### 회전 주기 기반인가?

아니다. 동일한 W=2000이 포함하는 회전 수:
- 680 RPM: (680/60) × 0.1 ≈ **1.13 revolutions**
- 2460 RPM: (2460/60) × 0.1 ≈ **4.10 revolutions**

모델이 회전 수를 정규화한 입력을 사용하지 않는다.

### Speed가 변할 때 (W)도 변하는가?

변하지 않는다. 모든 speed·class 조건에 W=2000 고정.

### Angular resampling / speed compensation을 하는가?

하지 않는다. NUFT는 speed signal의 변화 주파수를 offline 분석하는 데만 쓰인다. CNN 입력은 (2000 × 2) raw vibration (housing B x, y 방향). Speed 신호 자체는 CNN 입력에 포함되지 않는다.

### H (진단 주기)

H = W = 2000 → T_H = 100 ms (non-overlapping stride)

논문은 runtime task model의 period 또는 deadline으로 H를 공식 정의하지 않는다.
개인연구식 표기: **a = (W=2000, H=2000, M=fixed CNN)**

---

## RT 등급: B (확정)

| 판정 항목 | 결과 | 원문 근거 |
|---|---|---|
| 명시적 deadline 수치 | X | T_acq=100 ms를 deadline이라고 명시하지 않음 |
| RTOS 또는 RT-Linux | X | MacBook Pro, OS 미기재 |
| Deadline miss 측정 | X | 없음 |
| Tail latency (p99/max) | X | 미보고 |
| Average latency | O | C_avg = 20.2 ms ± 0.36 ms (Monte Carlo, 10회 × 1000 samples) |
| W/H/M runtime 변경 | X | 전부 고정 |

**real-time의 의미**: acquisition-rate보다 빠른 empirical throughput. Formal deadline guarantee 아님.

---

## Processing Time 수치

| 지표 | 값 |
|---|---|
| C_avg | **20.2 ms** |
| σ | **0.36 ms** |
| Test samples per rep. | 1,000 |
| Repetitions | 10 |
| p99 / max | 미보고 |
| T_acq | 100 ms (= W/f_s) |
| C_avg / T_acq | 0.202 (약 20.2%) |
| T_acq / C_avg | ≈ 4.95 ("약 5배 빠르다") |

Deadline 관점 해석 (개인연구): T=D=100 ms로 가정하면 S_avg = 100 - 20.2 = **79.8 ms**. 그러나 원문이 deadline이라고 명시하지 않고 max/p99 비교 없음.

**주의**: M1 Pro Desktop 측정값 → Pi Zero 2W 후보 latency로 직접 사용 불가. W=2000에서만 측정 → C(W) scaling 관계 알 수 없음.

---

## 개인연구와의 연결

### 이 논문에서 가져올 수 있는 근거

**(W)는 단순히 고정 sample count로 선택할 것이 아니라, machine condition이 변하는 time scale보다 충분히 짧아 segment 내부의 nonstationarity를 제한해야 한다.**

→ W(q) ≤ f(speed-change rate) 형태의 mode 설계로 확장:
- Speed/load 변화가 빠름 → 짧은 W (nonstationarity 감소)
- Speed/load가 안정적 → 긴 W (진단 정보 확보)
- System slack 부족 → 짧은 W 또는 가벼운 M

즉 W_t = π_W(q_t, S_t)

### 이 논문이 하지 않은 것

Condition dynamics가 runtime에 변할 때 (W)를 바꾸는 것이 아니라, 전체 dataset의 speed dynamics를 분석해 하나의 고정 (W)를 선택한다. 이것이 Jalonen et al.과 개인연구의 핵심 gap이다.

---

## 세 문장 압축

이 논문은 680~2460 RPM으로 속도가 변하고 noise가 존재하는 환경에서 두 채널 raw vibration을 이용해 네 가지 bearing state를 분류하는 lightweight CNN을 제안한다. Motor speed PSD의 주요 변화가 8 Hz와 9.15 Hz에 있음을 근거로 10 Hz 역수인 100 ms의 고정 window (W=2000)을 선택하며, angular resampling이나 runtime (W) 변경은 수행하지 않는다. MacBook Pro에서 평균 20.2 ms로 100 ms acquisition보다 약 5배 빠르지만, (q+S) 기반 (W/H/M) 선택과 p99·deadline·miss·scheduling 분석은 다루지 않는다.

## Related Work 영어 한 줄

> Jalonen et al. selected a fixed 100-ms vibration window from the spectral rate of rotational-speed variation and achieved 20.2 ms inference on an M1 Pro, but did not adapt the window at runtime or analyse deadline misses under system interference.

---

## 불확실한 점

1. Inference가 M1 CPU, integrated GPU, Neural Engine 중 어디서 실행되었는지 확인 불가
2. DL framework 및 version 확인 불가
3. Timing batch size 및 warm-up 여부 확인 불가
4. Exact maximum 및 p99 inference time 미보고
5. Continuous runtime에서 acquisition과 inference가 병렬인지 순차인지 확인 불가
6. W=2000 이외의 window에서 accuracy와 latency 미평가 — C(W) 관계 미지
7. Speed NUFT의 10 Hz threshold를 window duration으로 직접 대응시키는 이론적 정당화 제한적
8. Segment duration 100 ms가 deadline이라고 명시되지 않음
9. Angular resampling 미사용 시 RPM 변화에 따른 spectral smearing 크기 미분석
