# Zhan et al. (2026) — APTL-net 분석

> **대상 논문**  
> Z. Zhan, S. Zhang, J. Xu, and D. Ma,  
> “Edge-Oriented Bearing Fault Diagnosis via Triple-Lightweight Network With Adaptive Pruning,”  
> *IEEE Transactions on Instrumentation and Measurement*, Vol. 75, 2026.  
> DOI: 10.1109/TIM.2026.3699722
>
> **개인연구 기준**
>
> $$
> a=(W,H,M), \quad \text{trigger}=q+S
> $$

---

# 0. 초록 번역

본 논문은 클라우드 전송 지연과 edge device의 제한된 계산·저장 자원을 해결하기 위해 adaptive pruning triple-lightweight network인 APTL-net을 제안한다. APTL-net은 경량 sequence model, FDD 기반 weight-sharing multiscale feature extraction, dependency-aware pruning을 결합하며, Jetson Xavier NX에서 99.54% accuracy를 유지하면서 parameter, FLOPs, inference latency를 각각 47.82%, 49.98%, 20.59% 줄였다고 보고한다.

---

# 1. 논문 흐름 요약

## 1.1 문제 제기

기존 bearing fault diagnosis는 cloud server나 고성능 local server에 의존하므로 raw vibration transmission에 따른 latency와 보안 문제가 발생한다. 기존 lightweight model은 계산량을 줄이는 과정에서 representation capacity가 감소하기 쉽고, multiscale feature extraction은 여러 branch와 kernel을 추가해 다시 모델을 무겁게 만들 수 있다. 기존 pruning도 반복적인 pretraining, pruning, fine-tuning이 필요하며 layer 간 dependency를 충분히 고려하지 못한다.

## 1.2 Triple-Lightweight의 세 요소

| 경량화 단계 | 제안 요소 | 담당하는 경량화 |
|---|---|---|
| Model construction | Parallel training과 recursive inference를 지원하는 multiscale retentive network | Training에서는 병렬 계산을 사용하고 inference에서는 recurrent state update를 사용해 constant memory와 linear complexity를 지향 |
| Feature extraction | FDD 기반 weight-sharing multiscale convolution | FFT로 주요 period를 찾고 동일한 convolution kernel을 여러 scale에서 공유해 multiscale representation의 추가 parameter와 연산 부담을 억제 |
| Structural pruning | Dependency-aware adaptive pruning | Layer 간 연결 관계를 보존하면서 중요도가 낮은 parameter group을 제거해 Params, FLOPs, latency를 감소 |

첫 번째 요소는 attention 기반 global computation 대신 recursive state update를 사용해 online inference 비용을 줄인다. 두 번째 요소는 dominant frequency로 1-D signal을 여러 2-D periodic representation으로 변환하고 shared convolution을 적용한다. 세 번째 요소는 dependency graph를 이용해 서로 연결된 parameter를 일관되게 pruning한다.

## 1.3 Adaptive Pruning의 정체

### 판정

> **Offline training-time structured pruning이다. Online runtime adaptive pruning이 아니다.**

### 판정 근거

- Section III-C는 group sparse regularization이 training 중 중요도가 낮은 parameter group을 억제한다고 설명한다.
- Section III-D와 Algorithm 1은 sparse regularization으로 model을 pretrain한 뒤 dependency graph를 구성하고, target pruning rate에 따라 중요도가 낮은 group을 제거한 후 fine-tuning한다고 명시한다.
- 배포 단계에서는 pruning이 완료된 고정 APTL-net을 Jetson Xavier NX에 올려 inference한다.
- 입력 상태나 system load에 따라 runtime에 pruning rate 또는 topology를 변경하는 절차는 없다.

따라서 논문에서 말하는 `adaptive`는 **training 과정에서 model dependency와 importance distribution에 맞추어 pruning group을 자동 결정한다는 뜻**이다. Runtime condition에 따라 model이 가변적으로 작아지는 의미는 아니다.

### Pruning 대상

Pruning은 individual scalar weight를 독립적으로 0으로 만드는 unstructured pruning보다 **dependency-aware structured group pruning**에 가깝다.

- Parametric layer와 nonparametric operation의 input-output dependency를 graph로 구성
- Interlayer dependency와 intralayer dependency를 함께 고려
- 연결된 convolution, normalization, skip path의 parameter dimension을 group으로 묶음
- Group 또는 channel/filter dimension 단위로 일관되게 제거
- Whole layer를 runtime에 선택적으로 제거하는 방식은 아님

### Criterion

Group importance는 group 안의 weight norm으로 계산한다.

$$
I(g)=\sum_{w\in g}\lVert w\rVert_2
$$

Training 중에는 group sparse regularization을 적용한다.

$$
R(g,k)=\sum_{k=1}^{K}\sum_{w\in g}\gamma_k\lVert w[k]\rVert_2^2
$$

Importance가 작은 dimension에 더 강한 regularization을 부여하고, sparse training 이후 normalized importance를 계산한다.

$$
\hat{I}_{g,k}
=
\frac{N\cdot I_{g,k}}
{\sum \operatorname{TOPN}(I_g)}
$$

마지막으로 importance가 가장 낮은 group부터 target pruning rate $P$에 맞추어 제거하고 fine-tuning한다.

**근거:** Section III-C–D, p.5, Equations 22–27, Algorithm 1.

## 1.4 검증 방법

### 데이터셋과 운전 조건

- CWRU bearing dataset
- Sampling frequency: 12 kHz
- Speed: 1730, 1750, 1772, 1797 r/min
- Ball, inner-race, outer-race faults와 normal class
- Train 70%, validation 15%, test 15%
- Run-level split 이후 각 subset에서 sliding window 생성
- 세 speed로 학습하고 남은 한 speed에서 평가하는 cross-domain task C1–C4

추가로 rotor test bench, laser vibrometer, NI USB DAQ, Jetson Xavier NX를 이용한 10분 online physical validation을 수행한다.

### 비교 baseline

- Autoformer
- MICN
- Transformer
- LightTS
- GhostNet

### 측정 지표

- Accuracy, precision, recall, F1-score, macro-F1
- FLOPs, parameter count
- Inference time와 standard deviation
- Memory, average power, energy per inference
- Pruning rate별 accuracy-compression trade-off
- Variable-speed cross-domain performance

---

# 2. 핵심 수치

| 지표 | 값 |
|---|---|
| 플랫폼 | NVIDIA Jetson Xavier NX |
| 실행 환경 | Ubuntu 20.04, JetPack 5.1.2, TensorRT 8.5.1.7, PyTorch, CUDA, cuDNN |
| $W$ | 원문에서 sample 수를 확인하지 못함. 입력은 길이 $T$의 sliding window로만 정의 |
| $H$ | 미정의. Sliding window 사용은 명시하지만 stride와 overlap은 미보고 |
| Preprocessing 포함 여부 | Table V forward-pass latency는 preprocessing 제외. 배포 pipeline에서는 preprocessing 1.42 ms를 별도 추가 |
| Average latency | 50% pruning forward pass 14.782 ms. Preprocessing 포함 total latency는 본문 기준 16.36 ms. TensorRT edge deployment는 Table VIII에서 16.588 ms |
| Maximum / p99 latency | 미보고 |
| Standard deviation | TensorRT edge deployment 9.227 ms. 50% pruned edge model 42.179 ms |
| FLOPs | 50% pruning에서 10.81 G. Baseline 21.61 G |
| Model size | 50% pruning에서 0.96 M parameters. Baseline 1.84 M parameters. File size는 미보고 |
| Accuracy | 50% pruning에서 99.54%. Unpruned full model의 comparison accuracy는 99.48% |
| Memory | TensorRT edge deployment 365 MiB |
| Power | TensorRT edge deployment 평균 5.21 W |
| Energy | TensorRT edge deployment 86.4 mJ/inference |
| 측정 횟수 | Edge deployment configuration별 50 independent runs |

## 2.1 Latency 수치 해석 주의

논문에는 서로 다른 실행 경로의 latency가 함께 제시된다.

| 조건 | Inference time |
|---|---:|
| Table V baseline forward pass | 18.615 ms |
| Table V 50% pruned forward pass | 14.782 ms |
| 50% pruned model + preprocessing | 본문 기준 16.36 ms |
| Table VIII original edge deployment | 324.052 ms |
| Table VIII 50% pruned edge deployment | 234.958 ms |
| Table VIII TensorRT optimized edge deployment | 16.588 ms |

Table V는 neural-network forward pass만 측정한다. Table VIII는 edge deployment configuration 전체를 비교하지만 각 경로의 batch size와 정확한 pipeline boundary가 충분히 설명되지 않는다. 따라서 14.782 ms와 16.588 ms를 동일 조건의 latency로 직접 비교하면 안 된다.

또한 본문은 preprocessing이 1.42 ms라고 보고하지만,

$$
14.782+1.42=16.202\ \text{ms}
$$

로 계산되어 본문에 제시된 total latency 16.36 ms와 약 0.16 ms 차이가 있다.

---

# 3. 개인연구와의 연결

## 3.1 가변 변수와 트리거

| 관점 | Zhan et al. | 개인연구 |
|---|---|---|
| $W$ | 고정 input length로 사용되나 구체적 sample 수 미보고 | Runtime mode 변수 |
| $H$ | 미정의 | Runtime diagnosis period |
| $M$ | Offline pruning으로 하나의 고정 model 생성 | 여러 model 또는 mode 중 runtime 선택 |
| Adaptive 대상 | Training-time topology와 pruning group | Runtime $a=(W,H,M)$ |
| Trigger | Weight importance와 dependency graph | Machine condition $q$와 system slack $S$ |
| Timing 평가 | Average latency와 standard deviation | p99, max, deadline miss, schedulability |

## 3.2 한 줄 gap

> Zhan et al.은 training 단계에서 dependency-aware pruning으로 edge용 고정 model을 생성하지만, runtime machine condition과 system slack에 따라 $W/H/M$을 전환하지 않으며 explicit deadline과 p99 분석도 제공하지 않는다.

---

# 4. 세 문장 압축

Zhan et al.은 recursive inference framework, FDD 기반 weight-sharing multiscale feature extraction, dependency-aware structured pruning을 결합한 APTL-net을 제안한다. Adaptive pruning은 runtime adaptation이 아니라 sparse training 이후 importance가 낮은 dependent parameter group을 제거하고 fine-tuning하는 offline training-time pruning이다. Jetson Xavier NX에서 50% pruning model은 99.54% accuracy와 14.782 ms forward-pass latency를 보였지만, $W/H$와 explicit deadline, maximum, p99 latency는 보고하지 않는다.

---

# 5. Related Work 영어 한 줄

> Zhan et al. combined recursive inference, weight-shared multiscale feature extraction, and dependency-aware training-time pruning for efficient bearing diagnosis on a Jetson Xavier NX, but their deployed topology remained fixed and did not adapt $W/H/M$ according to machine condition or system slack.

---

# 6. 불확실한 점

- Input window $W$의 구체적인 sample 수
- Sliding-window stride, overlap, diagnosis period $H$
- Table V와 Table VIII 사이의 정확한 execution-path 차이
- Table VIII timing의 batch size
- Preprocessing, data transfer, feature extraction, TensorRT inference 각각의 세부 latency
- Maximum, p95, p99 latency와 deadline-miss ratio
- Explicit deadline 또는 acquisition period와 latency의 관계
- Parameter file size와 storage footprint
- Jetson power mode, clock setting, CPU/GPU affinity
- Online physical validation에서의 exact sample rate와 input cadence
