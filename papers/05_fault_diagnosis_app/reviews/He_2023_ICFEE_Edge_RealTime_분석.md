# He et al. (2023) — ICFEE 기반 비접촉 모터 베어링 진단 분석

> **대상 논문**  
> C. He, P. Han, J. Lu, X. Wang, J. Song, Z. Li, and S. Lu,  
> “Real-Time Fault Diagnosis of Motor Bearing via Improved Cyclostationary Analysis Implemented onto Edge Computing System,”  
> *IEEE Transactions on Instrumentation and Measurement*, Vol. 72, 2023.  
> DOI: 10.1109/TIM.2023.3295476
>
> **개인연구 기준**
>
> $$
> a=(W,H,M), \quad \text{trigger}=q+S
> $$
>
> **분류**  
> 경량화 대조군 Set B  
> 비DL 신호처리 알고리즘의 edge 구현
>
> **RT 등급**  
> B  
> Online MCU implementation과 단계별 실행시간은 보고하지만, explicit deadline, tail latency, miss ratio, schedulability는 다루지 않는다.

---

# 0. 초록 번역

본 논문은 복잡한 산업 환경에서 접촉식 진동 센서 설치가 어렵다는 문제를 고려해, microphone으로 취득한 sound signal에서 motor-bearing fault를 진단하는 improved cyclostationary analysis 방법을 제안한다. 제안한 improved cyclic feature enhancement extraction algorithm을 STM32 기반 edge-computing system에 구현하고, inner-race 및 outer-race fault feature를 MCU에서 계산해 LCD에 표시한다. 다만 보고된 전체 pipeline 시간은 10.294 s로, 1 s acquisition window보다 훨씬 길다.

---

# 1. 논문 논리 흐름과 Novelty

## 1.1 논리 흐름

### 1. 문제 제기

기존 bearing fault diagnosis는 주로 accelerometer 기반 vibration signal을 사용한다. 그러나 harsh environment에서는 accelerometer를 적절한 위치에 설치하기 어렵고, contact sensing 자체가 제약이 될 수 있다.

Sound signal은 microphone으로 비접촉 취득할 수 있지만, vibration signal과 마찬가지로 external noise와 nonstationarity의 영향을 크게 받는다. 기존 envelope analysis나 full-band cyclostationary integration은 weak fault feature가 noise에 묻히거나, fault와 무관한 frequency band까지 포함해 feature contrast가 저하될 수 있다.

또한 많은 fault-diagnosis method가 desktop 또는 upper computer의 postprocessing으로 수행되므로, 저자는 이를 equipment-side MCU로 옮겨 online diagnosis를 구현하려 한다.

**근거:** Section I, pp.1–3.

---

### 2. Improved cyclostationary analysis

## 2.1 표준 cyclostationary analysis의 계산 문제

이론적인 cyclic autocorrelation과 cyclic spectrum은 다음과 같이 정의된다.

$$
R_x(t,\tau)
=
E\left\{
x\left(t-\frac{\tau}{2}\right)^*
x\left(t+\frac{\tau}{2}\right)
\right\}
$$

$$
S_x(\alpha,f)
=
\mathcal{F}_{\tau}
\left\{
R_x(\tau,\alpha)
\right\}
$$

논문은 이러한 식을 직접 계산하면 time-consuming하여 edge-based online diagnosis에 적합하지 않다고 설명한다.

이를 줄이기 위해 STFT 결과의 cross-product를 이용하는 spectral correlation density 계산을 사용한다.

$$
S_x(\alpha,f)
=
\frac{1}{K\lVert w\rVert^2F_s}
\sum_{i=0}^{K-1}
X_w(i,f)
X_w(i,f-\alpha)^*
$$

저자는 이 식이 직접 cyclic autocorrelation spectrum을 계산하는 방식보다 matrix operation을 크게 줄인다고 설명한다.

**근거:** Section III-A, p.4, Equations 1–8.

## 2.2 Spectral coherence와 기존 full-band integration의 한계

Spectral correlation density를 normalization하여 spectral coherence를 계산한다.

$$
\gamma_x(\alpha,f)
=
\frac{S_x(\alpha,f)}
{\sqrt{S_x(0,f)S_x(0,f-\alpha)}}
$$

기존 방식은 spectral coherence를 carrier-frequency axis 전체 또는 넓은 범위에서 적분해 enhanced cyclic feature를 얻는다.

$$
S_x^{\mathrm{EES}}(\alpha,f_1,f_2)
=
\int_{f_1}^{f_2}
\left|S(\alpha,f)\right|df
$$

문제는 full-band integration이 fault와 무관한 information과 noise까지 포함한다는 점이다.

**근거:** Section III-A, pp.4–5, Equations 9–10.

## 2.3 제안 ICFEE의 핵심

제안한 ICFEE는 fault feature가 강한 carrier-frequency band만 자동으로 선택한다.

1. Hall signal에서 motor rotation frequency $f_r$를 계산한다.
2. Bearing geometry와 $f_r$로 BPFI와 BPFO를 계산한다.
3. Cyclic-frequency 범위를 $\alpha_O$부터 $\alpha_I$까지 설정한다.
4. Carrier-frequency axis에서 폭 $3\alpha_I$인 rectangular band를 이동시킨다.
5. 각 band의 impulse-factor 기반 information curve $g(f_k)$를 계산한다.
6. $g(f_k)$가 최대인 위치를 $f_2$로 선택한다.
7. 다음과 같이 lower bound를 결정한다.

$$
f_1=f_2-3\alpha_I
$$

8. 선택된 $[f_1,f_2]$에서만 spectral coherence를 적분해 fault feature를 강조한다.

논문의 information curve는 다음 형태다.

$$
g(f_k)
=
\frac{
\sum_{\alpha=\alpha_O}^{\alpha_I}
\left[
\max\left(
\sum_{f=f_k-3\alpha_I}^{f_k}|S(\alpha,f)|
\right)
-
\min\left(
\sum_{f=f_k-3\alpha_I}^{f_k}|S(\alpha,f)|
\right)
\right]
}{
\left[
\sum_{\alpha=\alpha_O}^{\alpha_I}
\sum_{f=f_k-3\alpha_I}^{f_k}
|S(\alpha,f)|
\right]
/
(\alpha_I-\alpha_O)
}
$$

따라서 ICFEE의 주된 novelty는 **full-band integration 대신 fault-sensitive band를 자동 선택해 weak cyclic feature를 강화하는 것**이다.

다만 논문은 ICFEE 자체의 Big-O complexity나 기존 cyclostationary method 대비 runtime 감소율을 별도로 제시하지 않는다. 실제 bottleneck은 여전히 spectral correlation density 계산이다.

**근거:** Section III-A, p.5, Equation 11.

## 2.4 DNN 또는 ML 사용 여부

> **DNN과 ML을 사용하지 않는다.**

Pipeline은 pure signal processing과 physics-based frequency matching으로 구성된다.

```text
Sound + Hall acquisition
        ↓
Rotation-speed calculation
        ↓
BPFI / BPFO prior calculation
        ↓
Spectral correlation density
        ↓
Information curve g(f_k)
        ↓
Selected-band integration
        ↓
Peak frequency와 theoretical prior 비교
        ↓
Inner-race / outer-race fault identification
```

즉 $M$은 trained model이 아니라 fixed signal-processing algorithm인 ICFEE다.

---

### 3. 시스템 구성

## 3.1 Sensor와 signal

| 항목 | 내용 |
|---|---|
| Fault-observation signal | Sound |
| Sensor | PCB377C01 microphone |
| Speed signal | BLDC driver의 hall output |
| Sampling | Sound와 hall 모두 5000 Hz |
| ADC | AD7606, 16-bit |
| Contact sensing | 사용하지 않음 |

Microphone은 BLDC motor drive-end 왼쪽에 설치된다. Hall signal은 별도 tachometer 없이 BLDC driver output에서 얻는다.

## 3.2 Edge hardware

| 항목 | 사양 |
|---|---|
| MCU | STM32F407IGT6 |
| Clock | 168 MHz |
| Internal Flash | 1 MB |
| Internal RAM | 192 KB |
| External SRAM | 2 MB |
| FPU | 사용 |
| DSP library | 사용 가능하다고 기재 |
| Display | 800 × 480 LCD |
| Implementation language | C |
| FPGA or DSP coprocessor | 없음 |
| RTOS | 미기재 |

Figure 5는 ADC, STM32F407IGT6, external SRAM, LCD를 포함한 full pipeline을 제시한다. 모든 analysis와 display 계산은 MCU에서 수행하며 FPU로 가속한다.

**근거:** Section II, p.3; Section IV-C, p.8; Figures 1, 2, and 5.

---

### 4. 검증 방법

## 4.1 Dataset

공개 dataset이 아니라 자체 experimental test bench에서 sound signal을 수집한다.

- Motor: BLDC motor
- Bearing fault: EDM으로 가공한 1 mm fault
- Fault classes:
  - Inner-race fault
  - Outer-race fault
- Sensor: Microphone
- Speed:
  - Inner-race experiment: 1086 r/min
  - Outer-race experiment: 1138 r/min
- Sampling rate: 5000 Hz
- Signal length: 5000 samples
- Window duration: 1 s

## 4.2 검증 단계

1. Synthetic noisy impulse signal
2. Fourier spectrum
3. Hilbert-envelope spectrum
4. Proposed ICFEE
5. Physical inner-race experiment
6. Physical outer-race experiment
7. STM32 edge implementation
8. Pipeline-stage execution-time measurement

## 4.3 평가 지표

- Fault-frequency visibility
- Harmonic visibility
- Traditional envelope spectrum과의 qualitative comparison
- MCU에서 단계별 execution time
- LCD online visualization

Accuracy, precision, recall, F1, confusion matrix는 보고하지 않는다.

---

## 1.2 Novelty

> **신규 signal-processing method와 MCU edge implementation의 결합 contribution이다.**

### Signal-processing contribution

- Impulse-factor 기반 information curve를 이용해 optimal spectral integration band 선택
- Full-band integration의 irrelevant information과 noise 감소
- Sound signal에서 weak cyclic fault feature 강화

### System contribution

- Sound와 hall signal을 STM32에서 동시 처리
- Rotation speed에 따라 BPFI와 BPFO prior를 online update
- ICFEE 전체 pipeline을 MCU에서 수행
- LCD에 diagnosis spectrum을 표시

### 한계

알고리즘을 MCU에 이식했지만 reported processing time은 acquisition window보다 훨씬 길다. 따라서 implementation contribution은 있으나 periodic real-time guarantee는 입증되지 않는다.

---

# 2. 핵심 수치

## 2.1 기본 파라미터

| 지표 | 값 |
|---|---|
| 플랫폼 | STM32F407IGT6, 168 MHz, 1 MB Flash, 192 KB internal RAM, 2 MB external SRAM |
| 실행 환경 | C implementation, FPU와 MCU DSP library 활용. OS와 RTOS는 미기재 |
| 센서 종류 | PCB377C01 microphone sound signal + BLDC-driver hall signal |
| ADC | AD7606, 16-bit |
| $f_s$ | 5000 Hz |
| $W$ | 5000 samples |
| $T_W$ | 1000 ms |
| $H$ | 미정의 |
| $T_H$ | 계산 불가 |
| Fault classes | Inner race, outer race |
| DNN / ML | 사용하지 않음 |

$$
T_W
=
\frac{W}{f_s}
=
\frac{5000}{5000}
=
1\ \mathrm{s}
$$

---

## 2.2 Pipeline 단계별 실행시간

| 단계 | 실행시간 |
|---|---:|
| 단계 1: Sound 및 hall data acquisition | 1.000 s |
| 단계 2: Hall signal 기반 rotation-speed calculation | 0.001 s |
| 단계 3: Spectral correlation density analysis | 9.196 s |
| 단계 4: Spectral frequency-range guideline $g(f_k)$ 계산 | 0.038 s |
| 단계 5: Enhanced cyclic feature extraction | 0.001 s |
| 단계 6: LCD display | 0.058 s |
| **합계** | **10.294 s** |

Processing만 분리하면 다음과 같다.

$$
T_{\mathrm{processing}}
=
0.001+9.196+0.038+0.001+0.058
=
9.294\ \mathrm{s}
$$

전체 end-to-display latency:

$$
T_{\mathrm{total}}
=
1.000+9.294
=
10.294\ \mathrm{s}
$$

Window duration과 비교하면

$$
T_{\mathrm{total}}
=
10.294\ \mathrm{s}
>
T_W
=
1\ \mathrm{s}
$$

$$
\frac{T_{\mathrm{total}}}{T_W}
=
10.294
$$

Processing만 비교해도

$$
\frac{T_{\mathrm{processing}}}{T_W}
=
9.294
$$

따라서 새로운 1-second window가 매초 생성된다고 가정하면 단일 MCU가 reported pipeline으로 input stream을 따라갈 수 없다.

또한 total time의 대부분은 spectral correlation density 단계다.

$$
\frac{9.196}{10.294}\times100
\approx89.3\%
$$

**근거:** Section IV-D, p.9; Figure 11.

---

## 2.3 정확도와 fault identification

논문은 percentage accuracy를 보고하지 않는다.

| 조건 | 결과 |
|---|---|
| Simulation, 555 r/min | ICFEE가 50 Hz fault frequency와 harmonics를 명확히 강조 |
| Inner-race fault, 1086 r/min | Theoretical BPFI 98 Hz와 measured enhanced cyclic peak가 일치 |
| Outer-race fault, 1138 r/min | Theoretical BPFO 69 Hz와 measured enhanced cyclic peak가 일치 |

따라서 결과는 **두 실험 조건에서의 qualitative correct identification**이지 statistical classification accuracy가 아니다.

---

# 3. Deadline 판정

## 종합 판정: **△**

| 판정 항목 | 결과 | 원문 근거 |
|---|---|---|
| 명시적 deadline 선언 | X | 특정 deadline $D$를 정의하지 않음 |
| RTOS 또는 PREEMPT_RT | X | OS와 scheduler 미기재 |
| Deadline miss, p99, max 측정 | X | 단계별 단일 실행시간만 보고 |
| 평균 pipeline latency | △ | Total 10.294 s를 보고하지만 반복 횟수와 통계량은 미보고 |
| Acquisition period $T_W$ 또는 $T_H$ | △ | $W=5000$, $f_s=5000$ Hz로 1 s window는 명시되지만 $H$는 없음 |
| Pipeline latency와 acquisition 비교 | 논문은 직접 비교하지 않음 | 보고값으로 계산하면 $10.294>1$ s |
| $W/H/M$ runtime 변경 | X | Fixed $W$와 fixed ICFEE 사용 |

### 판정 근거

1-second acquisition window라는 time reference는 존재한다. 그러나 저자는 이를 deadline으로 선언하지 않고 miss를 측정하지 않는다.

따라서 deadline 기준은 △다. RT grade는 B가 적절하다.

---

# 4. “Real-Time” 주장과 실제 timing 검토

## 4.1 논문의 real-time 근거

논문은 다음 특성을 real-time 또는 online diagnosis의 근거로 사용한다.

- Upper computer에서 postprocessing하지 않음
- MCU가 sensor data를 equipment side에서 직접 처리
- Hall signal로 rotation speed를 online update
- BPFI와 BPFO theoretical prior를 speed에 따라 update
- Analysis result를 LCD에 continuously update
- Manual intervention 없이 full pipeline 수행

즉 논문의 `real-time`은 주로 **on-device online processing과 현장 display**를 의미한다.

## 4.2 Acquisition window와 pipeline latency

$$
T_W=1\ \mathrm{s}
$$

$$
T_{\mathrm{processing}}=9.294\ \mathrm{s}
$$

$$
T_{\mathrm{total}}=10.294\ \mathrm{s}
$$

따라서 가장 자연스러운 periodic-task 해석인

$$
D=T_H=T_W=1\ \mathrm{s}
$$

를 가정하면 deadline을 크게 초과한다.

다만 $H$와 $D$가 원문에 정의되지 않았으므로, 논문 자체가 formal deadline을 위반했다고 단정하기보다는 다음처럼 표현하는 것이 정확하다.

> **The reported pipeline cannot sustain a new non-overlapping 1-second window every second under the measured sequential execution time.**

## 4.3 논문은 초과를 어떻게 정당화하는가

> **정당화하지 않는다.**

Section IV-D는 total time이 10.294 s라고 보고한 뒤, spectral correlation density calculation이 주된 bottleneck이며 future work에서 최적화해야 한다고 인정한다.

즉 저자는 다음 주장을 하지 않는다.

- $T_{\mathrm{total}}<T_W$
- Deadline satisfaction
- Acquisition과 processing의 parallel pipeline
- Double buffering
- DMA overlap
- Deadline miss ratio
- Bounded response time

## 4.4 이 논문에서 real-time의 실제 의미

> **엄밀한 periodic deadline satisfaction보다 online on-device monitoring에 가깝다.**

결과는 약 10.3 s마다 한 번 update되는 것으로 해석될 수 있으며, 1-second window rate를 따라가는 hard 또는 firm real-time system으로 보기는 어렵다.

이 논문은 다음 주장의 직접 근거로 활용할 수 있다.

> **An algorithm may be labelled real-time because it runs online on an edge MCU, even when its end-to-end processing time exceeds the sensing window duration; therefore, edge deployment alone does not establish deadline feasibility.**

---

# 5. 개인연구와의 연결

## 5.1 $q$와의 연결

Hall signal로 얻은 current rotation speed는 machine condition $q$에 해당한다.

이를 이용해 다음 theoretical fault frequencies를 runtime에 update한다.

$$
f_{\mathrm{BPFI}}
=
\frac{n_rf_r}{2}
\left(
1+\frac{D_1}{D_2}\cos\alpha
\right)
$$

$$
f_{\mathrm{BPFO}}
=
\frac{n_rf_r}{2}
\left(
1-\frac{D_1}{D_2}\cos\alpha
\right)
$$

그러나 $q$는 **fault prior parameter update**에만 사용된다. $W$, $H$, $M$을 바꾸는 mode-selection trigger는 아니다.

## 5.2 한 줄 gap

> He et al.은 speed-derived machine condition $q$로 fault-frequency prior를 update하지만, system slack $S$를 보지 않고 fixed $W=5000$과 fixed ICFEE를 사용하며, reported 10.294 s pipeline을 deadline-aware하게 조절하지 않는다.

---

# 6. 세 문장 압축

He et al.은 microphone sound와 hall-derived speed를 이용해 optimal integration band를 자동 선택하는 ICFEE cyclostationary analysis를 제안하고 이를 STM32F407 edge system에 구현한다. Inner-race 98 Hz와 outer-race 69 Hz feature를 MCU에서 식별했지만, 1 s acquisition window에 대한 end-to-display latency는 10.294 s였으며 9.196 s가 spectral correlation density calculation에 사용되었다. 따라서 이 연구의 real-time은 online edge execution에 가깝고, explicit deadline, p99, miss analysis와 $q+S$ 기반 $W/H/M$ adaptation은 제공하지 않는다.

---

# 7. Related Work 영어 한 줄

> He et al. implemented a speed-informed cyclostationary feature-enhancement pipeline on an STM32F407 for non-contact bearing diagnosis, but its 10.294-s end-to-display latency exceeded the 1-s sensing window and was not evaluated against an explicit deadline or system slack.

---

# 8. 불확실한 점

1. STM32F407이 bare-metal firmware, RTOS, 또는 vendor scheduler 중 무엇을 사용하는지
2. DSP library의 정확한 이름과 version
3. 실행시간 측정에 사용한 timer, cycle counter, GPIO, oscilloscope 등 measurement tool
4. Figure 11의 각 실행시간이 1회 측정값인지 반복 평균인지
5. Execution-time standard deviation, maximum, p95, p99
6. Acquisition과 processing을 overlap하는 DMA 또는 double-buffering 사용 여부
7. 다음 1-second window를 acquisition하는 동안 이전 window를 처리하는 pipeline 구조 여부
8. $H$, overlap, diagnosis update period
9. Inner-race와 outer-race condition에서 execution time이 동일한지
10. 2 MB external SRAM의 실제 사용량
11. Spectral-correlation matrix dimensions와 memory footprint
12. 기존 cyclostationary method 대비 ICFEE의 runtime 감소율
13. Healthy condition을 포함한 classification performance
14. 반복 experiment 수와 statistical accuracy
15. LCD update가 모든 spectrum point를 전송하는 시간인지 일부 visualization만 포함하는지
