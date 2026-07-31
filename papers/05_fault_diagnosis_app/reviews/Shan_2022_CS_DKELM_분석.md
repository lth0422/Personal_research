# Shan et al. (2022) — CS-DKELM 기반 고속 결함 진단 분석

> **대상 논문**  
> N. Shan, X. Xu, X. Bao, and S. Qiu,  
> “Fast Fault Diagnosis in Industrial Embedded Systems Based on Compressed Sensing and Deep Kernel Extreme Learning Machines,”  
> *Sensors*, Vol. 22, 2022, Art. no. 3997.  
> DOI: 10.3390/s22113997
>
> **개인연구 기준**
>
> $$
> a=(W,H,M), \quad \text{trigger}=q+S
> $$

---

# 0. 초록 번역

본 논문은 자원이 제한된 산업용 임베디드 시스템에서 고주파 monitoring data를 빠르게 진단하기 위해 compressed sensing과 deep kernel extreme learning machine을 결합한 CS-DKELM을 제안한다. 원 신호를 저차원 compressed representation으로 줄인 뒤 이를 복원하지 않고 DKELM에 직접 입력하여 transmission, storage, computation 부담을 줄이면서 높은 진단 정확도를 유지하는 것이 핵심이다.

---

# 1. 논문 흐름과 Novelty

## 1.1 논리 흐름

### 1. 문제 제기

고주파 센서와 다수의 monitoring point는 많은 데이터를 생성한다. 기존 방법은 다음 문제가 있다.

- 원 신호에 중복 정보가 많아 transmission, storage, computation 부담이 큼
- 원 신호 기반 feature extraction은 계산 복잡도와 시간이 큼
- 기존 diagnosis model은 sparse compressed signal에 적합하지 않거나, embedded resource에서 속도와 정확도를 함께 확보하기 어려움

이에 저자는 data sampling부터 fault classification까지 전체 pipeline을 경량화하려 한다.

### 2. Compressed Sensing이 하는 일

원래 vibration window는 다음과 같다.

$$
x\in\mathbb{R}^{N}, \qquad N=4800
$$

CS는 원 신호를 measurement matrix로 저차원 공간에 projection한다.

$$
y=\Phi x=\Phi\Psi s
$$

여기서 $\Phi\in\mathbb{R}^{M\times N}$이고 $M\ll N$이다. 논문은 vibration signal이 원래 transform domain에서 충분히 sparse하지 않다고 보고 Fourier transform을 먼저 적용한 뒤 Gaussian random measurement matrix를 사용한다.

Compression ratio는 다음과 같이 정의한다.

$$
CR=\frac{N-M}{N}\times100\%
$$

주 설정은 다음과 같다.

$$
N=4800,\qquad M=960,\qquad CR=80\%
$$

즉 원 데이터의 80%를 줄이고 20%인 960개 compressed value만 DKELM에 전달한다.

기존 CS 기반 diagnosis가 compressed signal을 원 time-domain signal로 복원한 뒤 분류하는 것과 달리, 본 논문은 **compressed representation을 복원하지 않고 직접 분류**한다.

**근거:** Section 2.1–2.2, pp.4–6, Equations 1–2.

### 3. DKELM이 하는 일

ELM은 hidden-layer weight와 bias를 random하게 설정하고 output weight를 generalized inverse로 한 번에 계산한다. 일반적인 backpropagation DNN처럼 여러 epoch 동안 gradient를 반복 갱신하지 않으므로 training이 빠르다.

DELM은 여러 ELM-AutoEncoder를 쌓아 greedy layer-wise unsupervised training을 수행한다. DKELM은 DELM의 마지막 classification 단계에 RBF kernel을 추가하여, 저차원 sparse feature를 더 높은 차원으로 mapping하고 linearly separable하게 만든다.

$$
K(x,x_i)
=
\exp\left(
-\frac{\lVert x-x_i\rVert^2}{\gamma}
\right)
$$

또한 PSO를 이용해 다음 parameter를 offline으로 최적화한다.

- Hidden-layer node 수
- Regularization coefficient
- Penalty coefficient
- RBF kernel parameter

따라서 DKELM은 일반 DNN보다 단순한 one-step 또는 least-squares 기반 학습을 사용하면서, stacked ELM-AE와 kernel mapping으로 sparse compressed signal의 분류력을 보완한다.

**근거:** Section 2.3–2.4, pp.6–8.

### 4. Zynq MPSoC에서 CS와 DKELM이 실행되는 위치

| Module | FPGA fabric 실행 여부 | ARM CPU 실행 여부 | 원문 판정 |
|---|---|---|---|
| CS | FPGA PL 구현 근거 없음 | ARM에서 실행한다고 명시하지 않음 | 정확한 mapping 미보고 |
| DKELM와 PSO | FPGA PL 구현 근거 없음 | ARM에서 실행한다고 명시하지 않음 | 정확한 mapping 미보고 |

논문은 ALINX FPGA development board와 Zynq UltraScale+ MPSoC XCZU9EG를 사용했다고 설명한다. 해당 SoC는 processing system과 programmable logic을 함께 포함하지만, 논문은 CS와 DKELM을 PS와 PL 중 어디에 배치했는지 설명하지 않는다.

다음 FPGA 구현 근거도 제시되지 않는다.

- RTL 또는 HLS design
- FPGA resource utilization
- ARM–FPGA data-transfer 구조
- DPU mapping
- Kernel별 hardware acceleration 결과

실험은 Linux, Python 3.8, PyTorch 1.7.0 기반으로 구현되었다고 서술한다. 따라서 **이 논문을 CS는 FPGA, DKELM은 ARM에서 실행한 hardware-software co-design으로 분류해서는 안 된다.** Software execution으로 보이지만 정확한 processing target은 원문만으로 확정할 수 없다.

또한 원문은 CUDA 10.2와 cuDNN 7.0을 사용했다고 적지만, XCZU9EG 자체에는 NVIDIA CUDA GPU가 없다. 외부 GPU 또는 별도 accelerator 사용 여부가 설명되지 않아 실행환경 기술에 내부 불명확성이 있다.

**근거:** Section 3.1, p.9.

### 5. 검증 방법

#### CWRU dataset

- Sampling frequency: 48 kHz
- Window: 4800 samples
- Classes: Normal과 3개 fault type의 세 severity를 포함한 10 classes
- Class별 100 samples, 총 1000 samples
- Train 70%, test 30%
- Main compression ratio: 80%
- Compressed input: 960 dimensions
- 20회 반복 평균

#### Compression-ratio analysis

$$
CR\in\{50,60,70,80,85,90,95\}\%
$$

Compression ratio에 따른 accuracy와 diagnosis time을 비교한다.

#### Baselines

- DELM
- DKELM
- CS-DELM
- SVM
- DBN
- SPBO-SDAE
- PSO-DNN
- CS-IMSNs

#### Physical platform validation

- PT006 rotating machinery test bench
- Sampling frequency: 48 kHz
- Speed: 1450 r/min
- 10 health conditions
- Window: 4800 samples
- Non-overlapping segmentation
- Class별 200 samples
- 20 trials

---

## 1.2 Novelty

### Contribution 1 — Sampling부터 classification까지 통합 경량화

Model compression만 수행하는 기존 경량화와 달리, compressed sampling, adaptive feature extraction, fast classification을 하나의 pipeline으로 통합한다.

### Contribution 2 — Reconstruction 없는 compressed-domain diagnosis

Compressed signal을 다시 원 신호로 복원하지 않고 DKELM이 직접 분류한다. 이를 통해 reconstruction과 원신호 feature extraction 비용을 제거한다.

### Contribution 3 — Sparse signal용 DKELM

DELM에 RBF kernel을 추가해 compressed sparse signal의 nonlinear separability와 classification stability를 개선한다.

### Contribution 4 — Compression ratio의 accuracy–time trade-off 분석

Compression ratio를 50%에서 95%까지 바꾸며 더 높은 compression이 diagnosis time을 줄이는 대신 accuracy를 저하시킨다는 관계를 실험한다.

### Contribution 5 — Real-time data flow용 incremental calculation

Sliding window가 이동할 때 이전 window와 중복되는 compressed calculation을 재사용한다. 저자는 이를 통해 fault-detection time을 최대 약 20% 줄일 수 있다고 보고한다.

---

# 2. 핵심 수치

| 지표 | 값 |
|---|---|
| 플랫폼 | ALINX FPGA development board, Xilinx Zynq UltraScale+ MPSoC XCZU9EG, quad Cortex-A53 1.5 GHz |
| 실행 환경 | Linux, Python 3.8, PyTorch 1.7.0, CUDA 10.2, cuDNN 7.0 |
| 원래 입력 크기 $W$ | 4800 samples |
| Sampling rate | 48 kHz |
| Window acquisition duration | $4800/48000=100$ ms |
| CS 적용 후 압축 크기 | 960 dimensions |
| Compression ratio | 80% reduction, 20% retention |
| $H$ | CWRU preprocessing에서는 stride 미보고. Physical validation은 non-overlapping이므로 $H=4800$ samples |
| 논문이 주장하는 diagnosis time | Table 2의 CS-DKELM testing time 0.0607 s, 즉 60.7 ms를 근거로 100 ms requirement 충족을 주장 |
| 실제 측정된 average diagnosis time | Physical test-bench validation에서 0.17 s, 즉 170 ms |
| 추가 timing 결과 | Table 6에서 CS-DKELM average time $0.16\pm0.23$ s |
| 불일치 | 있음. 60.7 ms는 100 ms보다 작지만 160–170 ms는 100 ms보다 큼 |
| Accuracy 최고 결과 | 단일 classification result 100%. CWRU 20회 평균 99.97% ± 0.44. Physical platform 99.67% ± 0.47 |
| Model size | 미보고 |
| Platform memory | DDR4 8 GB, eMMC 32 GB |

## 2.1 Compression-ratio별 accuracy와 diagnosis time

Figure 10의 값을 정리하면 다음과 같다.

| $CR$ | Retained dimension | Accuracy | Diagnosis time |
|---:|---:|---:|---:|
| 50% | 2400 | 100% | 0.4014 s |
| 60% | 1920 | 100% | 0.2568 s |
| 70% | 1440 | 99.92% | 0.1649 s |
| 80% | 960 | 99.86% | 0.0637 s |
| 85% | 720 | 97.69% | 0.0605 s |
| 90% | 480 | 90.71% | 0.0571 s |
| 95% | 240 | 83.28% | 0.0489 s |

논문은 80%에서 accuracy 감소가 작고 time reduction이 크다고 보고 이를 기본 설정으로 선택한다.

## 2.2 100 ms 주장과 실제 결과의 불일치

Section 3.3은 다음 취지로 주장한다.

> 대부분 산업 시스템의 real-time requirement는 100 ms 이내이며, CS-DKELM은 이를 만족한다.

이 주장의 직접 근거는 Table 2의 60.7 ms이다. 그러나 다른 결과는 다음과 같다.

- Table 6: $0.16\pm0.23$ s
- Table 8 physical platform: 0.17 s
- 두 수치 모두 100 ms를 초과

불일치의 가능한 원인은 다음과 같다.

1. **Test sample 수 차이**  
   CWRU test set은 300 samples이고 physical dataset test set은 약 600 samples다.

2. **Timing 단위가 per-window인지 dataset-total인지 불명확**  
   Section 3.3은 300 test samples를 입력했다고 한 뒤 하나의 `Testing Time`을 보고한다. 따라서 60.7 ms가 단일 diagnosis job latency인지 300-sample batch total인지 명확하지 않다.

3. **측정 경계가 통일되지 않음**  
   CS projection, DKELM inference, PSO optimisation, data loading, training 중 무엇이 포함되는지 표마다 명확하지 않다.

4. **Table 6은 training cost가 섞였을 가능성**  
   비교 설명에서 PSO-DNN과 CS-IMSNs의 긴 시간을 training time과 연결해 설명하므로, Table 6을 online inference latency로 직접 해석하기 어렵다.

따라서 **논문은 100 ms criterion을 제시하지만, end-to-end per-window latency가 100 ms 이내임을 일관된 조건에서 입증했다고 보기는 어렵다.**

---

# 3. CS 압축과 개인연구의 $W$ 축소 비교

## 3.1 유사점

두 접근 모두 model에 전달되는 input data와 후속 computation을 줄여 diagnosis cost를 감소시킨다.

```text
CS
4800-sample observation
        ↓
960-dimensional compressed representation
        ↓
DKELM cost 감소
```

```text
개인연구
W=2048
   ↓
W=1024 또는 512
   ↓
Acquisition과 inference cost 감소
```

또한 두 접근 모두 accuracy–time trade-off를 가진다.

- Compression ratio 증가 → 적은 input과 짧은 diagnosis time, 정보 손실 증가
- $W$ 감소 → 짧은 acquisition과 inference time, vibration context 감소

## 3.2 결정적 차이

| 관점 | Shan et al. CS | 개인연구의 $W$ 축소 |
|---|---|---|
| Observation duration | 기본적으로 4800 samples의 temporal interval을 유지 | Window 자체가 짧아짐 |
| Model input | 동일 window를 960차원으로 projection | 실제 sample 수가 감소 |
| Acquisition time | 실제 dataset 실험에서는 전체 4800 samples를 먼저 수집한 뒤 압축하므로 감소가 입증되지 않음 | $W/f_s$가 직접 감소 |
| Physical information | 같은 observation interval의 sparse information을 보존하려 함 | 포함되는 회전 수와 fault impulse 수가 달라질 수 있음 |
| Runtime adaptation | 없음 | $q+S$ 기반 선택 예정 |

저자는 CS를 sampling과 compression의 통합으로 설명하므로 전용 compressive acquisition hardware가 있다면 measurement 수를 줄일 수 있다. 그러나 본 실험은 이미 Nyquist rate로 취득된 4800-sample dataset을 software로 projection한다. 따라서 실험적으로 입증된 것은 **acquisition-time 감소보다 representation, storage, processing cost 감소**에 가깝다.

## 3.3 Compression ratio는 offline 고정인가?

주 실험과 배포 설정에서는 다음 값으로 고정된다.

$$
CR=80\%
$$

50%에서 95%까지의 sweep은 offline ablation이다. Runtime에 condition이나 load에 따라 compression ratio를 전환하는 algorithm은 없다.

Section 3.6은 real-time stream에서 이전 window의 계산을 재사용하지만, 이는 compression ratio adaptation이 아니라 incremental computation optimisation이다.

## 3.4 Accuracy 영향을 평가하는가?

평가한다. Figure 10은 compression ratio가 80%를 넘으면 accuracy가 크게 하락할 수 있음을 보여준다.

- 80%: 99.86%
- 85%: 97.69%
- 90%: 90.71%
- 95%: 83.28%

따라서 이 논문은 compression–accuracy–time trade-off를 명시적으로 보여준다는 점에서 개인연구의 mode profiling과 연결할 수 있다.

## 3.5 $q$ 또는 $S$에 따라 compression ratio를 조절하는가?

조절하지 않는다.

- Machine condition $q$를 compression trigger로 사용하지 않음
- System slack $S$를 측정하지 않음
- Deadline miss에 따라 compression ratio를 바꾸지 않음
- Runtime에는 하나의 고정 CS-DKELM configuration을 사용

---

# 4. Deadline 판정

## 판정: **O — 단, 약한 empirical deadline**

### 판정 근거

Section 3.3, p.11에서 저자는 산업 시스템의 real-time requirement를 100 ms 이내로 명시하고, Table 2의 60.7 ms와 비교해 requirement를 만족한다고 평가한다.

또한 다음 관계가 성립한다.

$$
T_W=\frac{4800}{48000}=100\ \mathrm{ms}
$$

Physical validation에서는 non-overlapping window를 사용하므로 다음처럼 해석할 수 있다.

$$
T=H/f_s=100\ \mathrm{ms}
$$

다만 원문은 100 ms requirement와 window acquisition duration을 직접 연결하지 않는다.

### 한계

- Physical platform average time 170 ms는 100 ms를 초과
- Maximum, p99, deadline miss 미보고
- Per-window response time인지 batch testing time인지 불명확
- Task scheduling과 interference 분석 없음

따라서 deadline criterion은 명시되었지만, strict real-time guarantee로 보기는 어렵다.

---

# 5. 한 줄 gap

> Shan et al.은 offline에서 선택한 고정 compression ratio로 input representation을 줄이지만, machine condition $q$와 system slack $S$에 따라 compression ratio 또는 $W/H/M$을 runtime에 조절하지 않으며 100 ms deadline 만족도 일관된 per-job timing으로 검증하지 않는다.

---

# 6. 세 문장 압축

Shan et al.은 4800-sample vibration window를 compressed sensing으로 960차원까지 줄인 뒤 복원 없이 DKELM에 직접 입력하는 CS-DKELM을 제안한다. Compression ratio를 높일수록 diagnosis time은 감소하지만 accuracy도 하락하며, 80% compression에서 약 99.9% accuracy와 약 60 ms testing time을 근거로 100 ms real-time requirement를 만족한다고 주장한다. 그러나 physical test-bench의 average time은 170 ms이며, FPGA와 ARM 사이의 실행 mapping, per-window timing boundary, p99와 deadline miss는 보고되지 않는다.

---

# 7. Related Work 영어 한 줄

> Shan et al. reduced fault-diagnosis cost by directly classifying compressed vibration measurements with a kernelised extreme learning machine, but used a fixed offline compression ratio and did not adapt the acquisition or model configuration according to machine condition or system slack.

---

# 8. 불확실한 점

- CS와 DKELM이 Zynq processing system, programmable logic, 또는 별도 accelerator 중 어디에서 실행되는지
- CUDA와 cuDNN이 XCZU9EG platform에서 어떻게 사용되었는지
- 60.7 ms가 단일 window latency인지 300-sample test-set total time인지
- Table 2, Table 6, Table 8에서 포함하는 processing stage가 동일한지
- CWRU segmentation의 stride와 overlap
- Maximum, p95, p99 latency와 deadline-miss ratio
- CS-DKELM parameter 수, model file size, runtime memory
- CS projection 자체의 execution time
- 실제 compressive acquisition hardware를 사용했는지, Nyquist data에 software compression만 적용했는지
- Table 5의 `Compressed rate: 0.2`가 Equation 2의 $CR=80\%$와 반대로 retention ratio를 의미하는지
- Table 6의 $0.16\pm0.23$ s에서 standard deviation이 mean보다 큰 이유와 통계 단위
