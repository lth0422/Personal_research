# Pubalan et al. (2025) — 1D CNN 기반 Simulated RT-FDD 분석

> **대상 논문**  
> B. Pubalan, M. S. R. M. Saufi, M. S. Leong, and A. Jamali,  
> “Real-Time Bearing Fault Detection and Visualization Using 1D CNN: A Simulated Deployment with the CWRU Dataset,”  
> *IEEE ICSIMA*, 2025.  
> DOI: 10.1109/ICSIMA66552.2025.11233248
>
> **개인연구 기준**
>
> $$
> a=(W,H,M), \quad \text{trigger}=q+S
> $$
>
> **분류**  
> 경량화 대조군 Set B  
> Simulated deployment  
> RT 등급 B

---

# 0. 초록 번역

본 논문은 연속 진동 데이터 처리, 저지연 결함 분류, GUI 기반 시각화를 통합한 bearing fault detection framework를 제안한다. CWRU 데이터를 실시간처럼 순차 재생한 실험에서 1D CNN은 prediction당 0.03 s의 가장 짧은 latency를 보였으며, 다른 부하 조건에서는 few-shot transfer learning으로 정확도를 회복하였다. 다만 실제 산업 장치에 배포한 결과가 아니라 PC 환경에서 수행한 simulated real-time validation이다.

---

# 1. 논문 논리 흐름과 Novelty

## 1.1 논리 흐름

### 1. 문제 제기

기존 bearing fault diagnosis 연구는 classification accuracy나 prediction speed만 강조하는 경우가 많고, 다음 요소를 하나의 시스템으로 통합하지 못한다는 문제를 제기한다.

- Data acquisition
- Low-latency preprocessing
- Fault classification
- Operator-facing visualization
- Cross-load generalization

이에 저자는 1D CNN과 MATLAB GUI를 결합한 RT-FDD framework를 제안하고, CWRU 데이터를 이용해 실시간 동작을 모사한다.

**근거:** Section I, p.1; Section II, p.2.

---

### 2. 시스템 구성

논문은 offline model-development pipeline과 simulated real-time pipeline을 분리한다.

```text
Offline phase
CWRU vibration data
        ↓
Segmentation and preprocessing
        ↓
Model training and validation
        ↓
Selected model

Simulated real-time phase
Segmented CWRU data replay
        ↓
Preprocessing
        ↓
1D CNN prediction
        ↓
GUI signal display
        ↓
Fault class and confidence aggregation
```

실시간 검증에서는 실제 sensor가 새 vibration을 수집한 것이 아니라, 저장된 CWRU segment를 trained model에 순차적으로 입력한다. GUI는 MATLAB App Designer로 구현되며 다음 기능을 제공한다.

- Vibration waveform visualization
- Latest fault prediction
- Data-acquisition setting display
- Monitoring 종료 후 class별 aggregated confidence 표시

예를 들어 130회 prediction 중 90%가 inner-race fault라면 최종 결과를 inner-race fault로 집계한다.

**근거:** Section III-A, p.2; Section III-C, pp.3–4; Figures 1 and 5.

---

### 3. 1D CNN 설계

#### 입력 형태

$$
\text{Input shape}=1\times1602
$$

하나의 input segment는 1797 rpm에서 shaft one revolution에 대응한다.

#### 모델 구조

- Sequence input layer
- Four convolutional blocks
- 각 block에 1D convolution, batch normalization, ReLU
- 일부 block 뒤 max pooling
- Dropout
- Global average pooling
- Fully connected layer 64 neurons
- Softmax output

Figure 4는 32, 64, 128 filter 규모와 64-neuron fully connected layer를 보여준다. 출력 class는 CWRU의 10개 상태로 해석된다.

다만 다음 항목은 보고되지 않는다.

- Convolution kernel size
- 각 block의 정확한 filter 수
- Stride와 padding
- Dropout rate
- Parameter count
- FLOPs
- Model file size

**근거:** Section III-B.2, p.3; Figure 4.

---

### 4. 핵심 분석

## 4.1 $W$ 결정 방식

이 논문의 가장 중요한 특징은 $W$를 고정된 임의 sample 수가 아니라 **shaft one revolution**을 기준으로 정한다는 점이다.

원문 수식은 다음과 같다.

$$
W
=
\frac{f_s}{\mathrm{RPM}/60}
=
\frac{60f_s}{\mathrm{RPM}}
$$

0 HP 조건에서

$$
f_s=48\,000\ \mathrm{Hz}
$$

$$
\mathrm{RPM}=1797
$$

이므로

$$
W
=
\frac{48\,000}{1797/60}
\approx1602.67
$$

논문은 integer segment length로

$$
W=1602\ \mathrm{samples}
$$

를 사용한다.

Window duration은 다음과 같다.

$$
T_W
=
\frac{1602}{48\,000}
\approx0.033375\ \mathrm{s}
=
33.375\ \mathrm{ms}
$$

이는 shaft revolution period와 거의 같다.

$$
T_{\mathrm{rev}}
=
\frac{60}{1797}
\approx33.39\ \mathrm{ms}
$$

즉 이 논문의 $W$는 **현재 회전속도라는 machine condition을 물리적 입력 길이로 변환한 결과**다.

**근거:** Section III-B.1, p.2, Equation 1.

---

## 4.2 RPM이 달라지면 $W$도 달라지는가

수식 자체는 다음 관계를 의미한다.

$$
W(\mathrm{RPM})
=
\frac{60f_s}{\mathrm{RPM}}
$$

따라서 속도가 낮아지면 한 회전에 필요한 sample 수가 증가한다.

논문에 보고된 다른 load의 RPM에 동일한 식을 적용하면 다음과 같다.

| Load | RPM | 수식으로 계산한 one-revolution $W$ |
|---:|---:|---:|
| 0 HP | 1797 | 약 1603 samples |
| 1 HP | 1772 | 약 1625 samples |
| 2 HP | 1750 | 약 1646 samples |
| 3 HP | 1730 | 약 1665 samples |

위 1–3 HP 값은 논문의 RPM과 Equation 1을 이용한 계산이다. 원문은 cross-load 실험에서 실제로 각 RPM에 맞추어 $W$를 재계산했는지 명확히 설명하지 않는다.

따라서 다음과 같이 구분해야 한다.

- **설계 원리:** RPM에 따라 $W$가 달라지는 physics-based rule
- **실제 runtime adaptation:** 확인되지 않음
- **$q$ 기반 online trigger:** 없음
- **Offline preprocessing에서 condition별 $W$ 재설정:** 원문 불명확

---

## 4.3 $H$ 정의 여부

논문은 overlap, stride, hop size를 보고하지 않는다.

$$
H=\text{미정의}
$$

따라서 다음 항목은 계산할 수 없다.

- Diagnosis period
- Segment arrival period
- $T_H$
- Deadline과 prediction latency의 직접 비교
- Overlapping-window 여부

Section III-A는 각 incoming data point를 즉시 처리한다고 표현하지만, Section IV는 segmented CWRU data를 sequentially streaming했다고 설명한다. 실제 model input은 1602-sample segment이므로 sample-by-sample inference라기보다 segment-by-segment replay로 해석하는 편이 타당하다.

---

## 4.4 Sampling frequency

$$
f_s=48\ \mathrm{kHz}
$$

CWRU 0 HP, 1797 rpm condition을 사용한다.

**근거:** Section III-B.1, p.2.

---

### 5. 검증 방법

#### 비교 모델

- 1D CNN
- 2D CNN with CWT
- 2D CNN with STFT
- SVM
- Random Forest

#### 평가 지표

- Five-run mean accuracy
- Accuracy standard deviation
- Aggregated prediction confidence
- Per-prediction latency
- Cross-load zero-shot performance
- Few-shot transfer learning performance
- Precision, recall, F1, accuracy under target loads

#### Load conditions

- Training and initial test: 0 HP, 1797 rpm
- Cross-load: 1 HP, 1772 rpm
- Cross-load: 2 HP, 1750 rpm
- Cross-load: 3 HP, 1730 rpm

Few-shot adaptation은 target load마다 class당 20개 labeled sample을 사용한다.

---

## 1.2 Novelty

> **신규 fault-diagnosis algorithm contribution이라기보다 simulated system integration과 cross-load validation contribution에 가깝다.**

### System implementation contribution

- Data-processing pipeline
- 1D CNN inference
- MATLAB GUI visualization
- Prediction confidence aggregation

을 하나의 RT-FDD framework로 구성한다.

### Simulated deployment contribution

저장된 CWRU segment를 sequentially replay하여 real-time acquisition과 prediction을 모사하고 model별 latency를 비교한다.

### Generalization contribution

0 HP에서 학습한 model을 1–3 HP에서 zero-shot으로 평가하고, class당 20개 sample을 이용한 few-shot transfer learning으로 성능을 회복한다.

새로운 convolution operation, loss function, compression, scheduling algorithm을 제안하지는 않는다.

**근거:** Section I, p.1; Section III, pp.2–4; Section IV, pp.4–6.

---

## 1.3 “Simulated Deployment”의 의미

## 판정

> **실제 MCU, SBC, embedded GPU에 model을 배포한 것이 아니라, PC의 MATLAB GUI에서 CWRU segment를 순차 입력한 software replay다.**

원문은 simulated real-time validation을 다음처럼 설명한다.

> Segmented CWRU data를 trained models에 sequentially streaming하였다.

또한 future work에 다음을 포함한다.

- Live hardware-in-the-loop testing
- Industrial deployment
- Multi-sensor monitoring
- IIoT and cloud integration

이는 현재 실험에서 실제 sensor-to-edge deployment가 이루어지지 않았음을 보여준다.

### 실제 hardware 여부

| 항목 | 판정 |
|---|---|
| MCU deployment | 없음 |
| SBC deployment | 없음 |
| GPU edge board deployment | 없음 |
| Live accelerometer acquisition | 검증 실험에서 없음 |
| Offline CWRU replay | 있음 |
| GUI simulation | 있음 |
| Prediction latency 측정 | 있음 |
| Timing platform 사양 | 미보고 |

Figure 5의 GUI에는 DAQ device와 sampling-rate 설정 항목이 표시되지만, 논문의 성능 검증은 CWRU data replay로 수행된다.

---

# 2. 핵심 수치

| 지표 | 값 |
|---|---|
| 플랫폼 | 구체적인 PC 또는 laptop 사양 미보고. 실제 embedded target 없음 |
| 실행 환경 | MATLAB App Designer. OS, MATLAB version, CPU, GPU 미보고 |
| $W$ | 1602 samples at 1797 rpm |
| $H$ | 미정의 |
| $f_s$ | 48 kHz |
| $T_W$ | 약 33.375 ms |
| $T_H$ | 계산 불가 |
| 1D CNN prediction latency | 0.03 s per prediction, 즉 약 30 ms |
| 2D CNN-STFT latency | 0.13 s per prediction |
| 2D CNN-CWT latency | 2.44 s per prediction |
| SVM latency | 약 0.07 s per prediction |
| Random Forest latency | 약 0.07 s per prediction |
| 1D CNN accuracy at 0 HP | 97.37% mean, standard deviation ±0.56 over five runs |
| 1D CNN aggregated confidence | Class별 82.8–100% |
| F1 | 0 HP의 단일 대표 F1 수치는 미보고. Few-shot target-load Figure에서 macro F1을 제시 |
| Parameter count | 미보고 |
| FLOPs | 미보고 |
| Model size | 미보고 |

## 2.1 0.03 s의 의미

$$
0.03\ \mathrm{s}
=
30\ \mathrm{ms}
$$

이는 **prediction latency**다.

논문은 이를 다음 의미로 사용한다.

> 하나의 pre-segmented input을 model에 전달한 뒤 하나의 prediction을 얻는 데 걸린 시간

다음 의미는 아니다.

- $H$
- Diagnosis period
- Acquisition period
- Explicit deadline
- End-to-end sensor-to-alert latency

흥미롭게도

$$
30\ \mathrm{ms}
<
T_W\approx33.375\ \mathrm{ms}
$$

이지만, 이는 보고된 수치를 이용한 사후 계산이다. $H$가 없고 replay pacing도 명시되지 않아 논문이 one-revolution period 내 completion을 검증했다고 볼 수는 없다.

---

# 3. Deadline 판정

## 종합 판정: **△**

| 판정 항목 | 결과 | 원문 근거 |
|---|---|---|
| 명시적 deadline 선언 | X | Deadline 값을 정의하지 않음 |
| RTOS 또는 PREEMPT_RT | X | PC 기반 MATLAB simulation이며 RT execution environment 미보고 |
| Deadline miss, p99, max 측정 | X | 0.03 s per prediction만 보고 |
| 평균 추론 latency | △ | 1D CNN 0.03 s per prediction을 보고하지만 통계 방법과 hardware 사양 미보고 |
| 주기적 trigger 또는 acquisition period | △ | One-revolution window duration은 33.4 ms로 계산 가능하지만 $H$는 미정의 |
| $W/H/M$ runtime 변화 | X | Offline model과 preprocessing 설정을 사용하며 runtime mode selection 없음 |

### 판정 근거

- Equation 1로 one-revolution window와 physical time scale은 정의된다.
- 그러나 논문은 이를 deadline으로 선언하지 않는다.
- $H$와 segment-arrival cadence가 없다.
- Deadline miss, maximum, p99를 측정하지 않는다.
- 실제 embedded device나 real-time OS에서 검증하지 않는다.

따라서 deadline처럼 해석 가능한 physical window duration은 존재하지만 explicit real-time deadline evaluation은 아니다.

---

# 4. 한 줄 gap

> Pubalan et al.은 RPM 기반 one-revolution rule로 $W$를 설계하지만, runtime machine condition $q$와 system slack $S$에 따라 $W/H/M$을 선택하지 않으며 실제 edge hardware에서 deadline와 tail latency를 검증하지 않는다.

---

# 5. 세 문장 압축

Pubalan et al.은 one-revolution vibration segment와 1D CNN을 이용하고 MATLAB GUI에서 CWRU 데이터를 순차 재생하는 simulated RT-FDD framework를 제안한다. 0 HP에서 1D CNN은 97.37% mean accuracy와 0.03 s per-prediction latency를 보였으며, unseen load 성능 저하는 class당 20개 sample의 few-shot transfer learning으로 회복하였다. 그러나 실제 embedded deployment, $H$, explicit deadline, p99, deadline miss, $q+S$ 기반 runtime mode selection은 다루지 않는다.

---

# 6. Related Work

> Pubalan et al. derived a one-revolution input length from shaft speed and demonstrated a 30-ms 1D-CNN prediction pipeline through sequential CWRU replay, but did not validate deadline-aware operation on real edge hardware or adapt $W/H/M$ according to machine condition and system slack.

---

# 7. 불확실한 점

1. Simulated replay를 수행한 PC 또는 laptop의 CPU, GPU, RAM
2. OS와 MATLAB version
3. CNN training framework와 inference backend
4. Latency 측정 횟수와 평균, minimum, maximum, standard deviation
5. $H$, stride, overlap, segment arrival cadence
6. Cross-load 조건에서 RPM별로 $W$를 다시 계산했는지 여부
7. Parameter count, FLOPs, model file size, memory usage
8. Kernel size, stride, padding, dropout rate 등 CNN 세부 구조
9. GUI의 DAQ 설정과 실제 simulated experiment 사이의 연결 방식
10. 0.03 s에 preprocessing과 GUI update가 포함되는지 여부
11. “Each incoming data point immediately”라는 설명과 1602-sample segment inference 사이의 관계
12. Confidence aggregation의 monitoring duration과 prediction count가 실험마다 동일한지 여부
