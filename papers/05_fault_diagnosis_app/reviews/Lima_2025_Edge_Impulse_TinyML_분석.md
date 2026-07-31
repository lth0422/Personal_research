# Lima (2025) — Edge Impulse 기반 TinyML 유도전동기 고장 감지 분석

> **대상 논문**  
> J. P. B. Lima,  
> “Real-Time Fault Detection in Induction Motors Using TinyML: An Evaluation of the Edge Impulse Platform,”  
> *IEEE Latin Conference on IoT*, 2025.  
> DOI: 10.1109/LCIoT64881.2025.11118459
>
> **개인연구 기준**
>
> $$
> a=(W,H,M), \quad \text{trigger}=q+S
> $$
>
> **분류**  
> 경량화 대조군 Set B

---

# 0. 초록 번역

본 논문은 유도전동기 회전자 봉 파손을 모터 외함의 진동 신호로 감지하기 위해 Edge Impulse 기반 TinyML 개발 절차를 평가한다. Arduino Nano 33 BLE의 nRF52840 MCU에 모델을 실제 배포하여 4개 봉 파손에서는 98.6%, 1개 봉 파손에서는 95.8%의 test accuracy를 보고한다. INT8 quantization은 4개 봉 파손 모델의 latency를 27 ms에서 1 ms로 줄였지만, 1개 봉 파손에서는 accuracy가 크게 저하되었다.

---

# 1. 논문 논리 흐름과 Novelty

## 1.1 논리 흐름

### 1. 문제 제기

대상 고장은 **유도전동기의 broken rotor bar**다. Bearing fault가 아니다.

논문은 다음 두 binary classification 문제를 별도로 구성한다.

- Normal vs. 1 broken rotor bar
- Normal vs. 4 broken rotor bars

검출 신호는 **모터 외함에서 측정한 tangential vibration**이다. 원 dataset에는 electrical signal과 mechanical signal이 모두 포함되지만, 본 논문은 vibration만 사용한다.

저자는 stator-current analysis가 일반적이지만 vibration signal이 load variation에 더 robust할 수 있다는 선행연구를 근거로 vibration을 선택한다.

**근거:** Section I-A–B, pp.1–2; Section II-C, p.2.

---

### 2. 시스템 구성과 Edge Impulse 활용

전체 개발 흐름은 다음과 같다.

```text
Experimental induction-motor vibration dataset
        ↓
18-second recordings
        ↓
2-second samples로 분할
        ↓
Edge Impulse upload
        ↓
Resampling + FFT 또는 Wavelet feature extraction
        ↓
EON Tuner grid search
        ↓
ANN architecture 및 DSP configuration 선택
        ↓
EON Compiler quantization
        ↓
Arduino Nano 33 BLE에 firmware 배포
        ↓
nRF52840에서 inference, RAM, Flash, latency 측정
```

#### Hardware

- Development board: Arduino Nano 33 BLE
- MCU: Nordic Semiconductor nRF52840
- CPU: ARM Cortex-M4, 64 MHz
- Flash: 1 MB
- RAM: 256 KB

#### Edge Impulse 역할

- Data preprocessing
- Sampling-rate 변경
- FFT 또는 Wavelet feature extraction
- ANN hyperparameter grid search
- Validation 및 test evaluation
- EON Compiler 기반 quantization
- nRF52840용 embedded deployment

**근거:** Section I-B, p.2; Section II, pp.2–3.

---

### 3. Configuration sweep

## 3.1 탐색한 변수

| 변수 | 후보 |
|---|---|
| Sampling window | 1000 ms, 2000 ms |
| Window increment | 1000 ms window에서 250, 500, 1000 ms |
| Window increment | 2000 ms window에서 500, 1000, 2000 ms |
| Sampling rate $f_s$ | 100, 250, 500, 1000 Hz |
| FFT size | 16, 32 points |
| Wavelet | Haar, Biorthogonal 1.3 |
| First hidden-layer neurons | 20, 40 |
| Number of layers | 2, 3 |
| Dropout | 0, 0.25, 0.5 |
| Learning rate | 0.0005, 0.001, 0.002 |
| Training cycles | 30, 50, 100, 200, 300 |

논문은 1D CNN, LSTM, MLP를 별도 model family로 비교하지 않는다. 탐색 대상은 **dense artificial neural network의 depth와 width**, DSP 방식, sampling configuration이다.

## 3.2 Quantization 후보

- FP32
- INT8

INT8은 EON Compiler에서 32-bit variable을 8-bit로 줄이는 방식이다. 다른 bit-width는 평가하지 않는다.

**근거:** Section II-E, p.3, Table I; Section III, pp.3–4.

---

## 3.3 주요 configuration 결과

논문은 전체 grid의 모든 조합 결과를 공개하지 않고, 최종 선택된 두 configuration만 상세히 제시한다.

| 설정 | Accuracy | Latency | RAM | Flash |
|---|---:|---:|---:|---:|
| 4 bars, $f_s=250$ Hz, $W=1000$ ms, $H=500$ ms, Biorthogonal 1.3, 2-layer ANN, FP32 | Test 98.6% | 27 ms | 1.4 KB | 14.5 KB |
| 4 bars, same configuration, INT8 | 98.1% | 1 ms | 미보고 | 미보고 |
| 1 bar, $f_s=1000$ Hz, $W=1000$ ms, $H=250$ ms, Haar, 2-layer ANN, FP32 | Test 95.8% | 39 ms | 1.6 KB | 21.4 KB |
| 1 bar, quantized INT8 | 68.3% | 미보고 | 미보고 | 미보고 |

### 4 broken bars 최적 구성

$$
f_s=250\ \mathrm{Hz}
$$

$$
T_W=1000\ \mathrm{ms}
$$

$$
T_H=500\ \mathrm{ms}
$$

따라서 sample 수로 환산하면

$$
W=250\ \mathrm{samples}
$$

$$
H=125\ \mathrm{samples}
$$

Model configuration:

- Wavelet: Biorthogonal 1.3
- First layer: 20 neurons
- Layers: 2
- Dropout: 0.5
- Learning rate: 0.0005
- Training cycles: 300

### 1 broken bar 최적 구성

$$
f_s=1000\ \mathrm{Hz}
$$

$$
T_W=1000\ \mathrm{ms}
$$

$$
T_H=250\ \mathrm{ms}
$$

따라서

$$
W=1000\ \mathrm{samples}
$$

$$
H=250\ \mathrm{samples}
$$

Model configuration:

- Wavelet: Haar
- First layer: 40 neurons
- Layers: 2
- Dropout: 0
- Learning rate: 0.0005
- Training cycles: 100

**근거:** Section III, pp.3–4; Tables II–III.

---

### 4. 검증 방법

## 4.1 Training data

원 dataset:

- 1 hp, 4-pole, 60 Hz three-phase induction motor
- Nominal speed: 1715 rpm
- Load: 12.5%–100%
- Sampling rate: 7600 Hz
- Class당 원 recording 10개
- Recording duration: 약 18 s
- Fault progression: Normal, 1, 2, 3, 4 broken bars

본 논문은 다음 load만 사용한다.

- 87.5% nominal load
- 100% nominal load

그리고 다음 binary dataset 두 개를 별도로 구성한다.

- Normal vs. 1 broken bar
- Normal vs. 4 broken bars

18-second recording을 2-second sample로 나누어 dataset 수를 늘린다.

## 4.2 실제 장치 배포 여부

> **실제 nRF52840 MCU에 model을 배포했다.**

Section III는 accuracy, RAM, Flash, latency가 model embedding 이후 microcontroller에서 직접 평가되었다고 명시한다.

다만 다음은 구분해야 한다.

- Actual MCU inference: 있음
- Live accelerometer-to-MCU sensing pipeline: 확인되지 않음
- 저장된 vibration dataset을 board에 입력해 inference: 가능성이 높음
- EON Tuner의 on-PC estimate만 사용: 아님

즉 deployment latency는 simulation-only 수치보다 신뢰도가 높지만, sensor acquisition부터 decision까지의 end-to-end latency는 아니다.

## 4.3 평가 지표

- Validation accuracy
- Test accuracy
- Inference latency
- RAM usage
- Flash usage
- Quantization 전후 accuracy와 latency
- Confidence threshold
- Majority voting

4-bar model은 2-second sample 안에서 1000 ms window와 500 ms increment를 사용해 3개 subsample을 만들고, 각 prediction의 majority vote로 최종 class를 결정한다. Confidence가 60% 미만이면 `Uncertain`으로 판정한다.

---

## 1.2 Novelty

> **신규 fault-diagnosis algorithm보다는 Edge Impulse platform의 체계적 평가 contribution이다.**

주요 contribution:

1. Vibration-based broken-rotor-bar detection을 Edge Impulse workflow로 구현
2. Sampling rate, window, DSP, ANN architecture를 EON Tuner로 탐색
3. nRF52840에서 accuracy, latency, RAM, Flash를 실제 측정
4. Simple fault와 subtle fault에서 INT8 quantization 효과가 다름을 비교
5. Edge Impulse의 usability와 hardware limitation을 실증

즉 새로운 ANN 구조나 학습 알고리즘을 제안한 것이 아니라, **configuration search와 MCU deployment를 통한 platform evaluation**에 가깝다.

**근거:** Section I-B, p.2; Section II-E, p.3; Section III–IV, pp.3–4.

---

# 2. 핵심 수치

| 지표 | 값 |
|---|---|
| 플랫폼 | Arduino Nano 33 BLE, Nordic nRF52840, Cortex-M4 64 MHz |
| 실행 환경 | Edge Impulse firmware와 EON Compiler. OS, SDK version, TFLite Micro 사용 여부는 미보고 |
| 센서 종류 | Motor casing tangential vibration accelerometer. Sensor model 미보고 |
| 원 dataset sampling rate | 7600 Hz |
| $f_s$ 후보 | 100, 250, 500, 1000 Hz |
| $W$ 후보 | 1000 ms 또는 2000 ms. Sample 수는 $W=f_sT_W$로 설정별 상이 |
| $T_W$ | 1000 ms 또는 2000 ms |
| $H$ 후보 | 250, 500, 1000, 2000 ms. Window configuration에 따라 다름 |
| Model 후보 | Dense ANN. First-layer 20 또는 40 neurons, 2 또는 3 layers |
| DSP 후보 | FFT 16/32 points, Haar wavelet, Biorthogonal 1.3 wavelet |
| Quantization 후보 | FP32, INT8 |
| 4-bar 최적 accuracy | 98.6% FP32, 98.1% INT8 |
| 4-bar latency | 27 ms FP32, 1 ms INT8 |
| 4-bar memory | RAM 1.4 KB, Flash 14.5 KB. INT8 memory는 미보고 |
| 1-bar 최적 accuracy | 95.8% FP32 |
| 1-bar latency | 39 ms FP32 |
| 1-bar memory | RAM 1.6 KB, Flash 21.4 KB |
| 1-bar INT8 result | Accuracy 68.3%. Latency와 memory 미보고 |

---

## 2.1 $W$, $H$, $f_s$ 관계

Window와 hop은 시간 단위로 search되며, sample 수는 다음 식으로 계산된다.

$$
W_{\mathrm{samples}}
=
f_sT_W
$$

$$
H_{\mathrm{samples}}
=
f_sT_H
$$

단, $T_W$와 $T_H$는 초 단위다.

### 4-bar model

$$
W=250\times1=250\ \mathrm{samples}
$$

$$
H=250\times0.5=125\ \mathrm{samples}
$$

### 1-bar model

$$
W=1000\times1=1000\ \mathrm{samples}
$$

$$
H=1000\times0.25=250\ \mathrm{samples}
$$

미세한 1-bar fault는 4-bar fault보다 높은 sampling rate와 더 짧은 hop을 필요로 했다는 결과다. 이는 machine condition에 따라 적절한 sensing/model configuration이 달라질 수 있음을 보여준다. 다만 이 차이는 **서로 다른 binary model을 offline에서 별도로 최적화한 결과**이며 runtime adaptation은 아니다.

---

## 2.2 Latency 해석

27 ms, 39 ms, 1 ms는 **MCU의 model inference latency**다.

이는 다음과 다르다.

- Window acquisition duration
- Hop period
- 2-second sample 전체의 final decision latency
- Majority-voting latency
- Sensor-to-alert end-to-end latency

4-bar configuration에서 한 prediction은 27 ms지만 2-second sample의 최종 class는 3개 subsample prediction을 majority voting한 결과다. 따라서 final decision을 얻으려면 data acquisition과 여러 inference가 필요하지만, 논문은 end-to-end decision latency를 보고하지 않는다.

---

# 3. Deadline 판정

## 종합 판정: **△**

| 판정 항목 | 결과 | 원문 근거 |
|---|---|---|
| 명시적 deadline 선언 | X | 특정 deadline $D$를 정의하지 않음 |
| RTOS 또는 PREEMPT_RT | X | OS와 scheduler 미보고 |
| Deadline miss, p99, max 측정 | X | Average 또는 대표 inference latency만 제시 |
| 평균 inference latency | O | MCU에서 27 ms, 39 ms, quantized 1 ms 보고 |
| Hop period $H$ 또는 acquisition period | O | Window increment 250 또는 500 ms가 명시됨 |
| $W/H/M$ runtime 변경 | X | EON Tuner가 offline에서 configuration을 선택한 뒤 고정 model 배포 |

### 판정 근거

Window increment가 명시되어 있으므로 periodic inference cadence로 해석할 수 있다.

4-bar:

$$
T_H=500\ \mathrm{ms}
$$

1-bar:

$$
T_H=250\ \mathrm{ms}
$$

Reported inference latency는 각각 hop보다 작다.

$$
27<500\ \mathrm{ms}
$$

$$
39<250\ \mathrm{ms}
$$

그러나 논문은 이를 deadline으로 선언하지 않으며, deadline miss, p99, maximum, concurrent workload를 평가하지 않는다. 따라서 explicit deadline evaluation은 아니며 판정은 △가 적절하다.

---

# 4. 한 줄 gap

> Lima는 EON Tuner로 $W/H/M$ configuration을 offline 탐색하고 nRF52840에 고정 배포하지만, runtime machine condition $q$와 system slack $S$에 따라 configuration을 전환하거나 tail latency와 deadline miss를 평가하지 않는다.

---

# 5. 세 문장 압축

Lima는 motor-casing vibration을 이용해 broken rotor bar를 탐지하는 TinyML pipeline을 Edge Impulse에서 탐색하고 Arduino Nano 33 BLE에 실제 배포한다. 4-bar model은 98.6% accuracy와 27 ms latency를 보였으며 INT8에서 98.1%와 1 ms를 달성한 반면, 1-bar model은 95.8%와 39 ms를 기록하고 quantization 시 accuracy가 68.3%로 저하되었다. 그러나 configuration search는 offline이며, runtime $q+S$ 기반 $W/H/M$ 선택과 explicit deadline, p99, miss 분석은 다루지 않는다.

---

# 6. Related Work

> Lima evaluated Edge Impulse for jointly profiling sensing windows, DSP front ends, neural-network configurations, and quantization on an nRF52840, but selected a fixed configuration offline without runtime adaptation to machine condition or system slack.

---

# 7. 불확실한 점

1. Edge Impulse firmware 내부 inference runtime이 TensorFlow Lite Micro인지 여부
2. Arduino core, compiler, Edge Impulse SDK와 EON Compiler version
3. RTOS 또는 bare-metal execution 여부
4. Accelerometer model과 live sensing hardware 구성
5. MCU latency 측정 횟수, mean, standard deviation, maximum, p99
6. Quantized 4-bar model의 RAM과 Flash
7. Quantized 1-bar model의 latency, RAM, Flash
8. 1-bar quantization 직전 accuracy가 본문 앞부분의 95.8%가 아니라 97.4%로 기재된 이유
9. 2-second sample의 final majority-vote decision latency
10. Feature-extraction latency가 reported inference latency에 포함되는지
11. Data loading과 resampling latency 포함 여부
12. 전체 EON Tuner grid 결과와 configuration별 latency/accuracy table
13. ANN 각 layer의 정확한 neuron 수와 output architecture
14. 87.5%와 100% load data가 training, validation, test에 어떻게 분배되었는지
15. Confidence threshold 60%와 majority voting이 accuracy 결과에 포함되었는지
