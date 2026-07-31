# Arciniegas et al. (2025) — XIAO ESP32S3 TinyML 이상 진동 감지 분석

> **대상 논문**  
> S. Arciniegas, D. Rivero, J. Piñan, E. Diaz, and F. Rivas,  
> “IoT Device for Detecting Abnormal Vibrations in Motors Using TinyML,”  
> *Discover Internet of Things*, Vol. 5, 2025, Art. no. 41.  
> DOI: 10.1007/s43926-025-00142-4
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

본 논문은 XIAO ESP32S3와 MPU6050을 이용해 모터 진동을 edge에서 분석하고, TinyML 기반 이상 감지 결과를 MQTT, Node-RED, Telegram으로 전달하는 IoT 시스템을 제안한다. 실험실 환경에서 96.5% accuracy와 약 300 ms의 sensing-to-alert latency를 보고하며, 저전력 MCU에서도 spectral feature와 neural-network inference를 결합한 상태 감시가 가능하다고 주장한다.

---

# 1. 논문 흐름과 Novelty

## 1.1 논리 흐름

### 1. 문제 제기

Cloud 중심의 예지보전은 network latency, bandwidth, privacy, 지속적인 연결 의존 문제가 있다. 저자는 vibration sensing, FFT 기반 feature extraction, TinyML inference, alert generation을 edge와 IoT 계층에 통합해 low-latency 상태 감시를 구현하려 한다.

### 2. 시스템 구성

```text
Motor bearing
    ↓
MPU6050
X/Y/Z vibration, 100 Hz
    ↓
XIAO ESP32S3
Filtering + FFT + TinyML inference
    ↓
MQTT broker
    ↓
Node-RED
Alert rule and dashboard
    ↓
Telegram notification
    ↓
InfluxDB storage
```

- Sensor: MPU6050 triaxial accelerometer
- Edge device: Seeed XIAO ESP32S3 Sense
- Communication: Wi-Fi and MQTT
- IoT processing: Node-RED
- Alert: Telegram bot
- Long-term storage: InfluxDB

**근거:** Section 4, pp.4–5; Section 6, pp.6, 10–12; Figures 2 and 7.

### 3. TinyML model 설계

#### 분류 형태

이 논문은 하나의 단일 multi-class fault classifier가 아니다.

1. **DNN classifier**
   - Stopped
   - Average speed
   - High speed

2. **K-means anomaly detector**
   - Normal operating cluster에서 멀어진 data point를 anomaly로 판정

따라서 구조는 다음과 같다.

```text
Operating-state classification
        +
Cluster-distance anomaly score
        ↓
Final normal / anomaly decision
```

즉 DNN은 세 가지 운전 상태를 분류하고, K-means가 별도로 abnormal vibration을 탐지한다. 논문은 bearing inner-race, outer-race, imbalance 같은 구체적인 fault type을 multi-class로 분류하지 않는다.

Section 5.1은 output layer가 3 neurons라고 쓰면서 `Stopped, Average Speed, High Speed, and Anomaly`를 함께 나열해 서술상 모순이 있다. Section 6.6과 Figure 4의 설명을 기준으로 보면 DNN output은 세 운전 상태이고 anomaly는 K-means가 담당한다고 해석하는 것이 가장 일관적이다.

#### Edge Impulse에서의 생성과 배포

1. MPU6050 data를 Edge Impulse에 upload하고 label 부여
2. Low-pass filtering과 FFT 기반 spectral feature extraction
3. Dense neural network 학습
4. 32-bit weight를 INT8로 quantization
5. Matrix factorization 기반 pruning과 layer 단순화
6. Edge Impulse가 생성한 firmware를 XIAO ESP32S3에 배포
7. MCU에서 feature extraction과 inference 실행
8. 결과를 MQTT로 publish

모델 구조:

- Input: X, Y, Z에 대응하는 3 neurons
- Dense layer: 20 neurons, ReLU
- Dense layer: 10 neurons, ReLU
- Output: 3 neurons, Softmax
- Anomaly detector: K-means, 32 clusters

### 4. 검증 방법

- Laboratory classification and anomaly-detection evaluation
- Accuracy, precision, recall, F1
- False-positive rate와 false-negative rate
- On-device average inference time
- Sensing-to-alert end-to-end latency
- Random Forest와 SVM baseline 비교
- 실제 fan motor에서 loose bearing과 external vibration 사례 확인
- 2개월 industrial operation에서 overall detection accuracy 98%를 추가 보고

---

## 1.2 Novelty

> **신규 학습 알고리즘보다는 시스템 구현 contribution에 가깝다.**

- XIAO ESP32S3에서 FFT, TinyML classification, K-means anomaly detection을 함께 실행
- Edge inference 결과를 MQTT, Node-RED, Telegram alert로 연결한 end-to-end IoT pipeline 구현
- TinyML neural network와 K-means를 병렬적으로 활용해 operating-state classification과 anomaly detection을 결합
- MCU inference latency뿐 아니라 sensing-to-alert end-to-end latency를 함께 보고

---

# 2. 핵심 수치

| 지표 | 값 |
|---|---|
| 플랫폼 | Seeed XIAO ESP32S3 Sense, Xtensa LX7 dual-core, MPU6050 |
| 실행 환경 | OS 미기재. Edge Impulse가 생성한 firmware와 inference code 사용. TFLite Micro 여부는 원문에서 명시하지 않음 |
| $W$ | FFT analysis window 기준 16 samples |
| $H$ | 50% overlap이므로 8 samples로 해석 가능 |
| $W$와 $H$의 선정 근거 | `충분한 frequency resolution`과 transient continuity 확보를 위해 16 samples와 50% overlap을 사용했다고 설명. 정량 ablation이나 물리 기반 유도는 없음 |
| Sampling rate | 100 Hz |
| Window duration | $16/100=160$ ms |
| Hop duration | $8/100=80$ ms |
| 모델 종류와 양자화 | Dense DNN 3-class classifier와 K-means anomaly detector. 32-bit weight를 INT8로 quantization. Matrix factorization 기반 pruning과 Huffman coding 언급 |
| Inference latency | 평균 25 ms, standard deviation 3 ms |
| End-to-end sensing-to-alert latency | 약 300 ms |
| Inference와 E2E 사이 구간 | Data collection 80 ms, model inference 25 ms, data transmission and alert generation 195 ms |
| Maximum / p99 latency | 미보고 |
| Accuracy / detection rate | Laboratory accuracy 96.5%, precision 96.19%, recall 97.11%, F1 96.64%. 2개월 industrial operation overall detection accuracy 98% 추가 보고 |
| Model size | Flash와 RAM 수치 미보고 |

## 2.1 Inference 25 ms와 E2E 300 ms의 차이

논문은 end-to-end latency를 다음과 같이 분해한다.

$$
T_{\mathrm{E2E}}
=
T_{\mathrm{collection}}
+
T_{\mathrm{inference}}
+
T_{\mathrm{network+alert}}
$$

$$
300
=
80+25+195\ \mathrm{ms}
$$

| 구간 | 시간 | 포함되는 작업 |
|---|---:|---|
| Data collection | 80 ms | MPU6050에서 vibration sample 확보 |
| Model inference | 25 ms | Edge device의 TinyML inference |
| Data transmission and alert generation | 195 ms | Wi-Fi, MQTT publish, broker 전달, Node-RED rule processing, Telegram alert |
| Total | 약 300 ms | Sensing 시작부터 alert 생성까지 |

중요한 점은 **FFT, filtering, segmentation 시간이 별도로 분리되어 있지 않다**는 것이다. 이 preprocessing cost가 25 ms inference에 포함되는지, 80 ms data-collection 구간에 포함되는지 원문은 명확히 설명하지 않는다.

또한 설정 간 내부 불일치가 있다.

- Sampling rate 100 Hz
- FFT window 16 samples
- 따라서 전체 window 수집에는 160 ms 필요
- 그러나 reported data-collection latency는 80 ms

80 ms는 8 samples, 즉 50% overlap에 따른 hop duration과 일치한다. 따라서 80 ms는 최초 window acquisition time보다 **steady-state window update interval**로 해석할 가능성이 높지만, 원문은 이를 명시적으로 설명하지 않는다.

## 2.2 개인연구식 mode 표현

보고된 설정을 steady-state 기준으로 표현하면 다음과 같다.

$$
a=
(W=16,\ H=8,\ M=\mathrm{DNN+K\mbox{-}means})
$$

그러나 이 mode는 runtime에 바뀌지 않는다.

---

# 3. Deadline 판정

## 판정: **△**

### 근거

- Section 5.2.1과 6.4.2에서 $W=16$ samples와 50% overlap을 제시한다.
- Sampling rate가 100 Hz이므로 steady-state hop은 다음과 같이 계산할 수 있다.

$$
T_H=\frac{8}{100}=80\ \mathrm{ms}
$$

- Section 7.1.1은 average inference time 25 ms와 end-to-end latency 300 ms를 보고한다.
- 그러나 논문은 $D=80$ ms 또는 $D=300$ ms라고 explicit deadline을 선언하지 않는다.
- Inference time을 hop period와 비교하지 않으며 deadline miss, maximum, p99를 측정하지 않는다.

따라서 period-like timing reference는 존재하지만 explicit deadline evaluation은 아니다.

---

# 4. 한 줄 gap

> Arciniegas et al.은 고정 $W/H/M$으로 edge inference와 IoT alert pipeline을 구현하지만, machine condition $q$와 system slack $S$에 따라 mode를 변경하거나 p99와 deadline miss를 분석하지 않는다.

---

# 5. 세 문장 압축

Arciniegas et al.은 MPU6050, XIAO ESP32S3, Edge Impulse, MQTT, Node-RED, Telegram을 연결한 TinyML 기반 motor-vibration monitoring system을 구현한다. DNN은 stopped, average-speed, high-speed 상태를 분류하고 K-means가 abnormal vibration을 별도로 탐지하며, average inference latency 25 ms와 sensing-to-alert latency 약 300 ms를 보고한다. 그러나 $W=16$과 50% overlap은 고정되어 있고 explicit deadline, p99, deadline miss, runtime $q+S$ mode selection은 다루지 않는다.

---

# 6. Related Work 영어 한 줄

> Arciniegas et al. integrated FFT-based TinyML inference and K-means anomaly detection with an MQTT–Node-RED alert pipeline on a XIAO ESP32S3, but used a fixed sensing and model configuration without runtime $W/H/M$ adaptation or tail-latency analysis.

---

# 7. 불확실한 점

- Edge Impulse firmware 내부 runtime이 TensorFlow Lite Micro인지 여부
- Exact model Flash, RAM, arena size와 parameter 수
- FFT와 filtering latency가 25 ms inference에 포함되는지
- 80 ms data-collection latency와 16-sample window의 관계
- Initial full-window acquisition latency와 steady-state hop latency의 구분
- Inference-time 측정 횟수
- Maximum, p95, p99 latency와 deadline-miss ratio
- 300 ms end-to-end latency의 반복 횟수와 standard deviation
- Wi-Fi, MQTT broker, Node-RED, Telegram 각 구간의 세부 latency
- Quantization이 full-integer INT8인지 weight-only INT8인지
- Pruning ratio와 Huffman compression 이후 actual model size
- Laboratory accuracy 96.5%와 2개월 industrial accuracy 98%의 dataset size와 평가 절차 차이
- DNN output class 설명에서 3 neurons와 four labels를 함께 언급한 원문 서술 모순
