# Thota et al. (2025) — TinyML 기반 분산 베어링 고장 분류 분석

> **대상 논문**  
> Y. R. Thota, M. Afshar, S. Boden, B. Dunlap, B. Akin, and T. Nikoubin,  
> “TinyML Enabled Real-Time Bearing Fault Classification in Motors Using Vibration Signals,”  
> *ACM/IEEE Great Lakes Symposium on VLSI*, 2025.
>
> **원문 DOI**
>
> `10.1145/3716368.3735272`
>
> 사용자 프롬프트에 적힌 DOI `10.1145/3716375.3736246`과 다르다.
>
> **개인연구 기준**
>
> $$
> a=(W,H,M), \quad \text{trigger}=q+S
> $$
>
> **분류**  
> 경량화 대조군 Set B
>
> **RT 등급**  
> B

---

# 0. 초록 번역

본 논문은 불규칙하고 비정상적인 진동을 발생시키는 distributed bearing fault를 분류하기 위해 raw 3축 vibration을 직접 입력하는 lightweight 1D CNN TinyML framework를 제안한다. 3000 RPM과 다섯 load 조건에서 healthy, lubrication failure, contamination, flaking, electrical erosion, composite fault의 여섯 상태를 분류하며, 1D CNN이 feature-engineered DNN보다 높은 accuracy를 보였다고 보고한다. Edge Impulse를 통해 ESP32 계열 MCU에 배포한 결과를 제시하지만, latency와 memory 수치는 원문 내부에서 서로 모순된다.

---

# 1. 논문 논리 흐름과 Novelty

## 1.1 논리 흐름

### 1. 문제 제기

기존 bearing diagnosis는 RMS, kurtosis, FFT, PSD, STFT, CWT와 같은 handcrafted feature에 의존한다. 이러한 방식은 domain expertise가 필요하고, load, speed, noise가 달라질 때 generalization이 제한될 수 있다.

Distributed fault는 localized defect와 달리 넓은 표면에 걸쳐 발생하며 irregular, nonstationary vibration을 만든다. 따라서 저자는 다음 두 접근을 비교한다.

- Statistical 및 spectral feature를 입력하는 fully connected DNN
- Raw triaxial vibration을 직접 입력하는 1D CNN

VLSI와 embedded 관점에서는 다음 제약을 강조한다.

- MCU RAM과 Flash
- Inference latency
- Cloud 의존성
- On-device autonomous diagnosis
- Low-power deployment 가능성

다만 실제 energy, power, clock cycle, memory bandwidth는 측정하지 않는다.

**근거:** Section 1–2, pp.1–2.

---

### 2. 시스템 구성

## 2.1 Data source와 sensor

- Dataset: Afshar et al.의 distributed bearing fault dataset
- Motor: 3 hp induction motor
- Speed 범위: 500–3000 RPM
- Load: 0%, 25%, 50%, 75%, 100%
- 본 논문 사용 조건: 3000 RPM과 다섯 load
- Sensor: ADXL354C MEMS triaxial accelerometer
- Mounting: Motor drive end
- Signal: Raw $x$, $y$, $z$ vibration

**근거:** Section 3.1, p.3; Figures 1–3.

## 2.2 Deployment pipeline

```text
ADXL354C triaxial vibration dataset
        ↓
Fixed-window segmentation
        ↓
Path A: statistical + spectral features
        ↓
Fully connected DNN

Path B: raw x/y/z signals
        ↓
1D CNN
        ↓
Edge Impulse conversion and deployment
        ↓
ESP-EYE, ESP32 benchmark
```

논문은 Edge Impulse를 deployment tool로 사용한다. TFLite Micro는 literature review에서 일반 TinyML runtime으로 언급되지만, 실제 deployment runtime이 TFLite Micro인지 EON Compiler 기반 runtime인지 명확히 밝히지 않는다.

## 2.3 MCU와 실행 환경

| 항목 | 원문 내용 |
|---|---|
| Board | Espressif ESP-EYE |
| MCU family | ESP32 |
| CPU clock | 미보고 |
| On-chip RAM | 미보고 |
| Board Flash capacity | 미보고 |
| FPU | 미보고 |
| Deployment tool | Edge Impulse |
| OS 또는 RTOS | 미보고 |
| Inference runtime | 미보고 |
| Live motor-mounted deployment | 수행하지 않음. Future work로 제시 |

Table 2는 `Deployment Summary on ESP 32`라고 표기하고, Section 4는 Espressif ESP-EYE에서 측정했다고 설명한다. 그러나 Conclusion은 motor-mounted hardware의 direct implementation을 future work로 둔다. 따라서 MCU에서 model benchmark는 수행했지만, live sensor-to-diagnosis system을 motor에 장착한 검증은 아니다.

**근거:** Section 3, p.3; Section 4–5, pp.4–5; Table 2.

---

### 3. 모델 설계와 경량화

## 3.1 Feature-engineered DNN

원문이 기술한 구조:

$$
7500
\rightarrow
3000
\rightarrow
1000
\rightarrow
500
\rightarrow
250
\rightarrow
75
\rightarrow
25
\rightarrow
6
$$

- Activation: ReLU
- Output: 6-class softmax
- Loss: categorical cross entropy
- Optimizer: Adam
- Input: statistical and spectral features라고 설명

다만 앞 절에서 열거한 engineered feature 수는 7500차원에 훨씬 못 미치므로, `7500-dimensional feature vector`라는 서술은 내부적으로 불명확하다.

이 구조를 문자 그대로 계산하면 약 2615만 개 weight가 필요하며, INT8 기준 약 26 MB로 Section 4의 quantized DNN Flash 25.0 MB와 대체로 일치한다. 이 parameter 수는 논문이 직접 보고한 값이 아니라 구조로부터 계산한 값이다.

## 3.2 Raw-signal 1D CNN

Figure 6과 Section 3.3.2의 구조:

```text
Input: 7500 values
        ↓
Reshape: 30 columns
        ↓
Conv1D / Pool
16 filters, kernel 5
        ↓
Dropout 0.25
        ↓
Conv1D / Pool
8 filters, kernel 3
        ↓
Dropout 0.25
        ↓
Conv1D / Pool
8 filters, kernel 3
        ↓
Flatten
        ↓
Dense 32
        ↓
Dense 16
        ↓
Softmax 6 classes
```

정확한 pooling size, stride, padding과 intermediate tensor shape가 없어 total parameter 수와 FLOPs는 계산할 수 없다.

## 3.3 경량화 방법

| 기법 | 적용 여부 |
|---|---|
| INT8 quantization | 적용 |
| Post-training 또는 QAT | 미기재 |
| Pruning | 본 모델에 적용했다는 근거 없음 |
| Knowledge distillation | 없음 |
| Hardware-aware NAS | 없음 |
| Layer fusion | 일반 TinyML 설명에만 등장. 본 구현 적용 여부 미기재 |
| Lightweight architecture | 작은 1D CNN을 사용 |

핵심 경량화는 **raw-signal 1D CNN architecture와 INT8 variant 비교**다.

---

## 3.4 모델 variant 비교

### Table 2 원문 수치

| 모델 variant | Latency | Classifier RAM | Total RAM | Flash | Accuracy |
|---|---:|---:|---:|---:|---:|
| 1D CNN unoptimized FP32 | 30 ms | 18.7 KB | 29.3 KB | 43.3 KB | 99.26% |
| 1D CNN quantized INT8 | 265 ms | 61.2 KB | 61.2 KB | 69.7 KB | 99.36% |

### DNN 관련 본문 수치

| 모델 variant | Accuracy | Latency | Flash | RAM |
|---|---:|---:|---:|---:|
| Feature DNN, training result | 85% 또는 98% | 미보고 | 미보고 | 미보고 |
| Quantized DNN | 68.01% | 1212 ms | 25.0 MB | 미보고 |

DNN accuracy는 Section 3.2.1에서 98%, Section 3.3.1에서 85%로 서로 다르다.

---

## 3.5 Table 2와 본문 사이의 중요한 모순

Table 2는 INT8 model이 FP32보다 다음과 같이 더 느리고 더 큰 것으로 적혀 있다.

$$
265\ \mathrm{ms}
>
30\ \mathrm{ms}
$$

$$
61.2\ \mathrm{KB}
>
29.3\ \mathrm{KB}
$$

$$
69.7\ \mathrm{KB}
>
43.3\ \mathrm{KB}
$$

그러나 Abstract와 Section 4는 quantized INT8 model의 결과를 다음처럼 서술한다.

- Accuracy: 99.36%
- Latency: 30 ms
- RAM: 29.3 KB
- Flash: 69.7 KB

이는 Table 2의 서로 다른 두 행에서 값을 섞은 조합이다.

| 항목 | 본문이 INT8에 귀속한 값 | Table 2에서 실제 위치 |
|---|---:|---|
| Accuracy | 99.36% | INT8 row |
| Latency | 30 ms | FP32 row |
| RAM | 29.3 KB | FP32 row |
| Flash | 69.7 KB | INT8 row |

따라서 **INT8의 정확한 latency와 RAM은 원문만으로 신뢰성 있게 확정하기 어렵다.** Table 2를 그대로 따르면 265 ms와 61.2 KB이고, 저자의 narrative를 따르면 30 ms와 29.3 KB다.

---

### 4. 검증 방법

## 4.1 Dataset와 classes

| Class | Condition |
|---|---|
| C0 | Healthy |
| C1 | Lubrication failure |
| C2 | Contamination |
| C3 | Flaking |
| C4 | Electrical erosion |
| C5 | Combined or composite fault |

- Speed: 3000 RPM
- Load: 0%, 25%, 50%, 75%, 100%
- Fault severity가 섞인 multiclass classification
- Training epochs: 30
- Learning rate: 0.001
- Batch size: 32
- Validation split: 20%

## 4.2 $f_s$, $W$, $H$

원문은 segmentation에서 상충되는 값을 제시한다.

- Section 3.1: 각 segment는 10000 data points
- Section 3.2.2와 Figure 6: raw input은 7500 points
- Figure 3 caption과 plot: 10000-sample segment
- Sliding window: minimal overlap
- Exact overlap, stride, hop: 미보고
- Sampling rate: 미보고

따라서 개인연구 변수로는 다음처럼 기록해야 한다.

$$
W=
\begin{cases}
10000 & \text{Section 3.1 기준}\\
7500 & \text{1D CNN input 기준}
\end{cases}
$$

$$
H=\text{미정의}
$$

Sampling rate가 없으므로

$$
T_W=\frac{W}{f_s}
$$

를 계산할 수 없다.

## 4.3 실제 MCU 배포 여부

- ESP-EYE에서 model memory와 latency를 평가했다고 서술
- 실제 MCU benchmark는 수행한 것으로 보임
- Motor-mounted live data acquisition은 수행하지 않음
- Sensor acquisition, buffering, preprocessing, inference를 포함한 end-to-end system latency는 미보고

## 4.4 측정 지표

- Accuracy
- Confusion matrix
- Inference latency
- Classifier RAM
- Total RAM
- Flash

측정하지 않은 항목:

- Energy per inference
- Average power
- Clock cycles
- Memory bandwidth
- Maximum, p95, p99 latency
- Deadline misses

---

## 1.2 Novelty

> **새로운 VLSI architecture나 hardware accelerator보다는 MCU-targeted TinyML deployment study에 가깝다.**

### Model contribution

- Raw triaxial vibration을 직접 입력하는 compact 1D CNN
- Feature-engineered DNN보다 높은 accuracy와 작은 deployment footprint를 주장

### Hardware-efficient deployment contribution

- Edge Impulse를 이용해 FP32와 INT8 variant를 ESP32 계열 board에 배포
- RAM, Flash, latency를 비교
- 25 MB 수준의 DNN이 MCU deployment에 부적합하고 compact 1D CNN이 적합함을 보여줌

### 구현 contribution의 한계

- New accelerator, custom datapath, memory architecture, cycle-level optimization은 없음
- Energy와 cycle 수를 측정하지 않음
- Live motor-mounted implementation은 future work
- Table 2와 본문 수치가 모순됨

**근거:** Section 3–5, pp.3–5.

---

# 2. 핵심 수치

| 지표 | 값 |
|---|---|
| 플랫폼 | Espressif ESP-EYE, ESP32. Clock, board RAM, board Flash 사양은 미보고 |
| 실행 환경 | Edge Impulse. OS, RTOS, bare-metal 여부와 runtime은 미보고 |
| 센서 | ADXL354C triaxial MEMS accelerometer |
| $f_s$ | 미보고 |
| $W$ | 10000 samples라고 서술하지만 1D CNN input은 7500 points로 모순 |
| $T_W$ | 계산 불가 |
| $H$ | `minimal overlap`만 기재. 정확한 hop 미보고 |
| $T_H$ | 계산 불가 |
| 모델 구조 | 3-layer 1D CNN, Dense 32–16, 6-class softmax |
| Quantization | INT8. PTQ인지 QAT인지 미기재 |
| Accuracy | FP32 99.26%, INT8 99.36% according to Table 2 |
| Inference latency | FP32 30 ms, INT8 265 ms according to Table 2. 본문은 INT8 30 ms라고 서술 |
| Energy per cycle | 미보고 |
| Power | 미보고 |
| Clock cycles | 미보고 |
| Model size | Flash FP32 43.3 KB, INT8 69.7 KB according to Table 2 |
| RAM 사용량 | FP32 total 29.3 KB, INT8 total 61.2 KB according to Table 2 |
| Parameter count | 미보고 |
| FLOPs or MACs | 미보고 |

---

# 3. Deadline 판정

## 종합 판정: **X**

| 판정 항목 | 결과 | 원문 근거 |
|---|---|---|
| 명시적 deadline 선언 | X | Deadline $D$를 정의하지 않음 |
| RTOS 또는 PREEMPT_RT | X | OS와 scheduling environment 미보고 |
| Deadline miss, p99, max 측정 | X | 보고하지 않음 |
| 평균 inference latency | O | Table 2에 latency를 제시하지만 측정 통계는 없음 |
| Hop period $H$ 또는 acquisition period | X | Minimal overlap만 언급하고 $f_s$, $H$, period를 보고하지 않음 |
| $W/H/M$ runtime 변경 | X | Fixed model deployment이며 runtime switching 없음 |

### 판정 근거

Input sample count는 존재하지만 sampling rate와 hop이 없어 acquisition duration이나 diagnosis period를 계산할 수 없다. 따라서 30 ms 또는 265 ms가 다음 input arrival 이전에 끝나는지 판단할 기준이 없다.

이 논문의 `real-time`은 low-latency MCU inference라는 의미이며, periodic deadline satisfaction을 뜻하지 않는다.

---

# 4. 한 줄 gap

> Thota et al.은 fixed raw-signal 1D CNN을 ESP32에 배포해 latency와 memory를 비교하지만, $W/H$의 physical timing을 정의하지 않고 machine condition $q$와 system slack $S$에 따른 runtime $M$ selection이나 deadline analysis를 수행하지 않는다.

---

# 5. 세 문장 압축

Thota et al.은 distributed bearing fault 여섯 상태를 raw triaxial vibration으로 분류하는 compact 1D CNN을 제안하고 Edge Impulse를 통해 ESP-EYE에 배포한다. Table 2는 FP32 99.26%, 30 ms, 29.3 KB RAM과 INT8 99.36%, 265 ms, 61.2 KB RAM을 보고하지만, 본문은 INT8에 30 ms와 29.3 KB를 귀속해 수치가 모순된다. 또한 $f_s$, $H$, explicit deadline, tail latency, energy와 $q+S$ 기반 runtime mode adaptation은 제공하지 않는다.

---

# 6. Related Work

> Thota et al. deployed a compact raw-signal 1D CNN for six-class distributed bearing-fault diagnosis on an ESP32-class device, but did not define the sensing period or deadline and reported internally inconsistent latency and memory figures for the quantized model.

---

# 7. 불확실한 점

1. ESP-EYE의 정확한 ESP32 chip revision과 clock
2. Board RAM과 Flash capacity
3. OS, FreeRTOS, bare-metal 여부
4. Edge Impulse 내부 runtime과 TFLite Micro 사용 여부
5. INT8이 post-training quantization인지 quantization-aware training인지
6. $f_s$
7. $W=10000$과 raw 1D CNN input 7500 points의 관계
8. Sliding-window overlap과 $H$
9. FP32 30 ms와 INT8 265 ms가 정확한지 여부
10. Abstract와 Section 4가 INT8 latency 30 ms라고 서술한 이유
11. INT8 RAM이 FP32보다 증가한 이유
12. INT8 Flash가 FP32보다 증가한 이유
13. Latency 측정 횟수와 mean, standard deviation, maximum, p99
14. Feature extraction 또는 data copy가 latency에 포함되는지
15. Energy, average power, mJ per inference
16. Clock cycle과 hardware performance counter
17. 1D CNN parameter 수와 MACs
18. DNN accuracy가 98%, 85%, 68.01%로 다르게 제시된 이유
19. Actual motor-mounted sensing-to-classification deployment 여부
20. Dataset split이 recording 단위인지 overlapping segment 단위인지
