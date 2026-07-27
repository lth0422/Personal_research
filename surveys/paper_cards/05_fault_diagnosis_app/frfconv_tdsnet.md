# FRFconv-TDSNet: Lightweight, Noise-Robust Convolutional Neural Network Leveraging Full-Receptive-Field Convolution and Time-Domain Statistics for Intelligent Machine Fault Diagnosis

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S2 (adaptive fidelity 배경·기준선), S4 (edge inference 자원 측정)
- **플랫폼 태그**: `PL-SBC-SOC`
- **실행환경 태그**: `ENV-LINUX` (OS·kernel 원문 미기재, PyTorch Mobile + XNNPACK)
- **출처/연도**: IEEE Transactions on Instrumentation and Measurement, Vol. 73, 2024
- **저자**: Seongjae Lee, Taehyoun Kim (본 연구실 논문)
- **원문 위치**: `papers/05_fault_diagnosis_app/` (파일명 별도 확인)
- **분석 PDF**: `papers/05_fault_diagnosis_app/reviews/FRFconv_TDSNet_M후보_RT_개인연구_정밀분석.pdf`

---

## 두 질문

- **가변 변수**: 없음. W=2048 samples 비중첩 고정; M(FRFconv-TDSNet) 단일 모델 고정; H(runtime 진단 주기) 정의 없음. FRF kernel shape는 layer input length에 종속되므로 W를 바꾸면 model variant가 달라진다.
- **트리거**: 없음. offline model 설계 및 평가 연구. 기계 상태(q)나 scheduling slack(S)에 의한 runtime adaptation 없음.

---

## RT 등급: B (확정)

| 판정 항목 | 결과 | 원문 근거 |
|---|---|---|
| 명시적 deadline 수치 | X | 논문 전체에 없음 |
| RTOS 또는 RT-Linux | X | Raspberry Pi 4B OS·kernel 미기재 |
| Deadline miss 측정 | X | 없음 |
| Tail latency (p99/max) | X | p99 미보고; range만 있음 |
| Schedulability 분석 | X | task model, utilization, RTA 없음 |
| Formal WCET bound | X | empirical max만 사용 |
| 평균 inference latency | O | Figure 6: avg 약 3.40 ms |
| Observed maximum latency | O | Figure 6 range: 약 3.67 ms (100 runs) |
| W/H/M runtime 변경 | X | W=2048 고정, H 미정의, M 단일 고정 |
| Task period | X | 정의 없음 |

**핵심 패턴**: 논문은 safety-critical application에서 WCET가 중요하다고 언급하며 maximum inference time을 평가하지만, static WCET analysis·cache state bound·OS interference model·CPU frequency control이 없다. 정확한 표현은 "100 warm-up 후 100회 측정에서의 empirical maximum latency"이다. Empirical average/max는 측정했지만 local deadline을 정의하거나 miss를 검증하지 않았으므로 E로 상향 불가 → **B**.

---

## 핵심 방법 요약

### 1. 입력 설계 (W)

| 항목 | 원문 값 | 원문 표현/해석 |
|---|---|---|
| W — input window | 2048 samples | 각 train/validation/test set을 2048-point sample로 분할 |
| Sampling rate | 확인 불가 | CWRU·MFPT·UoC의 sampling rate를 논문 본문에 기재하지 않음 |
| T_W 시간 환산 | 확인 불가 | T_W = W/f_s이나 f_s 미기재로 계산 불가 |
| W 선택 근거 | 명시되지 않음 | 베어링 characteristic frequency/회전 주기/FFT resolution/latency budget 어느 것으로도 연결하지 않음 |
| Overlap | 없음 | "2048 data points without overlapping" |
| Stride | 2048 samples | 비중첩 slicing, stride = window |
| H — runtime 진단 주기 | 확인 불가 | Dataset stride는 있지만 배포 시스템의 diagnosis period 정의 없음 |
| Dataset | CWRU, MFPT, UoC | bearing 2종 + gearbox 1종 |

**(W=2048) 선택 근거 판정**: 물리적 timing 또는 회전역학 근거가 제시된 값이 아니라, 세 데이터셋을 동일한 크기로 표준화하기 위한 experimental segmentation choice로 보인다. 이는 해석이며 저자가 직접 명시하지는 않았다.

---

### 2. FRFconv 구조 — Full-Receptive-Field의 정확한 의미

#### 2.1 FRF kernel은 W=2048인가?

아니다. 첫 FRF convolution의 실제 kernel은 255이며, 후반 FRF convolution의 kernel은 31이다.

개념적 정의:
- FRF convolution의 kernel은 해당 layer에 입력되는 feature map의 전체 길이(L)를 덮는다.
- 입력 길이가 짝수이므로 same-size output을 만들기 위해 실제 구현은 K = L-1, P = L/2 - 1을 사용한다.

W=2048 흐름:
```
2048 → (stride-8 downsampling) → 256 → FRF kernel K=255
     → (stride-8 downsampling) → 32  → FRF kernel K=31
```

근거: Section III-B, pp.4-5; Table I, p.5.

#### 2.2 일반 convolution과의 차이

| 방식 | 한 output이 보는 범위 |
|---|---|
| (K=3) convolution | 인접한 작은 local patch |
| FRF convolution | padding을 포함해 입력 전체 길이에 해당하는 receptive field |

FRF convolution은 각 output position을 계산할 때 전 구간 정보를 반영하므로, 일부 구간에 noise가 들어와도 특정 local pattern에만 의존하지 않고 global pattern을 활용할 수 있다는 것이 저자의 핵심 주장이다.

#### 2.3 FRFconv는 입력 길이 (W)에 종속되는가?

**종속된다.** FRF kernel tensor의 길이가 해당 layer input length에 의해 결정된다.

| W 값 | feature-map 흐름 | FRF kernels |
|---|---|---|
| W=2048 | 2048 → 256 → 32 | K=255, K=31 |
| W=1024 | 1024 → 128 → 16 | K=127, K=15 |
| W=512 | 512 → 64 → 8 | K=63, K=7 |

기존 K=255 weight tensor를 K=127 또는 K=63 convolution에 그대로 사용할 수 없다. 따라서 같은 FRFconv-TDSNet이라는 model family는 사용할 수 있지만, 동일한 trained model instance를 여러 (W)에 그대로 공유할 수는 없다.

보다 정확한 mode 표기: `a_i = (W_i, H_i, M_FRF^(W_i))`

#### 2.4 Pooling/stride 구조

- 첫 downsampling block: kernel 64, stride 8
- 두 번째 downsampling block: kernel 24, stride 8
- 마지막: Global Average Pooling (Max pooling 사용 안 함)
- FRF convolution block의 stride: 1
- Downsampling의 역할: (1) 작은 kernel로 local detail 추출, (2) 다음 FRF convolution의 입력 길이를 1/8로 줄여 계산량 감소

#### 2.5 FRF convolution block 내부

```
Input
├── (residual 경로)
└── Zero padding
    → Depthwise Conv (K=L-1)
    → BatchNorm → ReLU
    → Pointwise Conv (1×1)
    → BatchNorm
    → element-wise sum (+ residual)
    → ReLU
```

모든 convolution channel 수: 8로 제한

#### 2.6 Depthwise separable convolution의 경량화 효과

표준 convolution 대비 parameter·computation 비율: 1/C_out + 1/K

예: (K=255), (C_out=8)이면 표준 convolution의 약 **13.9%** parameter와 computation만 사용한다. (근거: Section III-B, p.4)

---

### 3. 전체 레이어 구조 (Table I 재현)

| Layer | Type | Kernel | Channel | Stride | Padding | Output |
|---|---|---|---|---|---|---|
| Input | Raw vibration | — | 1 | — | — | (2048) |
| 1 | Downsampling Conv | 64 | 8 | 8 | 28 | (256) |
| 2 | FRF convolution | 255 | 8 | 1 | 127 | (256) |
| 3 | FRF convolution | 255 | 8 | 1 | 127 | (256) |
| 4 | FRF convolution | 255 | 8 | 1 | 127 | (256) |
| 5 | Downsampling Conv | 24 | 8 | 8 | 8 | (32) |
| 6 | FRF convolution | 31 | 8 | 1 | 15 | (32) |
| 7 | FRF convolution | 31 | 8 | 1 | 15 | (32) |
| 8 | FRF convolution | 31 | 8 | 1 | 15 | (32) |
| 9 | Conv + BN + ReLU | 9 | 8 | 1 | 4 | (32) |
| 10 | Global Average Pooling | — | — | — | — | 8 |
| TDS | Mean, Peak, RMS, CF | — | — | — | — | 4 |
| Fusion | Concatenation | — | — | — | — | 12 |
| Classifier | FC + Softmax | — | (N_c) | — | — | (N_c) |

근거: Figure 1 p.3; Table I p.5.

---

### 4. TDS — Time-Domain Statistics

| 통계량 | 의미 | 결합 위치 |
|---|---|---|
| Mean | 진동의 중심축·DC 성분 | GAP 이후 8-D FRF output과 concat |
| Peak | 최대 진동 크기 | 동일 |
| RMS | 전체 진동 energy/magnitude | 동일 |
| Crest Factor (CF) | impulse의 극단성 | 동일 |
| Skewness/Kurtosis | 사용하지 않음 | — |

**TDS 합쳐지는 위치**: GAP으로 얻은 FRF CNN의 8차원 vector와 TDS 4차원 vector를 concatenate하여 12차원 classifier input을 만드는 **late feature fusion**이다. Feature-map level fusion, convolution 중간 layer fusion, element-wise addition이 아니다.

수식:

y = σ(W · [FRF(Pre(x)); TDS(x)] + b)

FRF(Pre(x)) ∈ R^8, TDS(x) ∈ R^4, W ∈ R^(N_c × 12)

FRF CNN input은 L_∞ normalization([-1,1] 범위)으로 정규화한다. 이 과정은 signal scale을 통일하지만 결함을 구분하는 절대 진동 크기 정보를 약화시킨다. TDS는 raw signal에서 직접 계산되므로 peak와 RMS 같은 magnitude 정보를 보존한다 — 이것이 TDS가 noise에 강한 핵심 이유이다.

---

### 5. 전체 모델 요약

| 항목 | 값 | 근거 |
|---|---|---|
| Input | (2048) | Fig. 1, Table I |
| FRF blocks | 6 | Section III-B |
| Downsampling blocks | 2 | Section III-B |
| Conv channels | 모두 8 | Section III-B |
| FRF output | 8-D | GAP output |
| TDS output | 4-D | Mean, Peak, RMS, CF |
| Classifier input | 12-D | Concatenation |
| Parameters | **9K** | Table VI, p.7 |
| Computation | **1.80 MAdds** | Table VI, p.7 |
| FP32 model size | 약 36 KB | 9K × 4 byte 이론 환산; 원문 미보고 |
| Class count | CWRU 10, MFPT 3, UoC 9 | Dataset별 상이 |
| Training epochs | 100 | Section IV-B |
| Training batch | 128 | Section IV-B |
| Optimizer | Adam, LR=0.01 | Section IV-B |
| Training repetitions | 16 (평균 및 95% CI) | |
| Input dropout | p=0.5 | Section III-A |

비교 대상 10개 모델:
- 2D CNN: ResNet-18, EfficientNet-B0
- 1D CNN: WDCNN, TICNN, WKCNN, SECN, MBSDCN, MSDCNN
- Transformer: CLFormer, S-Transformer

---

## Noise Robustness

### 실험 조건

- SNR: -4, 0, 4 dB + noise-free
- AWGN을 원본 test signal에 추가
- **Clean data로 학습하고 unseen AWGN noise에서 시험**, training 과정에서는 input dropout(p=0.5)으로 random masking robustness를 학습

### TDS ablation (-4 dB, 16회 평균)

| Dataset | FRF without TDS | FRF + TDS | 평균 향상 |
|---|---|---|---|
| CWRU | 79.31% | 88.03% | +8.72%p |
| MFPT | 78.16% | 85.38% | +7.22%p |
| UoC | 84.41% | 88.78% | +4.37%p |

### FRF kernel ablation (-4 dB)

| Dataset | K=3 | K=7 | K=L/4-1 | K=L/2-1 | K=L-1 (FRF) |
|---|---|---|---|---|---|
| CWRU | 81.25 | 81.35 | 85.92 | 83.47 | **88.03** |
| MFPT | 79.49 | 80.83 | 83.47 | 84.57 | **85.38** |
| UoC | 52.92 | 60.73 | 76.28 | 84.51 | **88.78** |

UoC에서 FRF가 K=3 convolution보다 평균 35.86%p 높다. (근거: Table VIII, p.9)

### 왜 TDS가 noise에 강한가 (논문 3단계 설명)

1. L_∞ normalization에서 사라지는 magnitude 정보를 TDS가 raw signal에서 직접 복구
2. Noise 아래에서도 class 간 TDS 관계(특히 Peak·RMS)가 상당 부분 유지됨 (Figure 10)
3. Final FC output을 직접 보정 — FC decomposition에서 TDS contribution을 더했을 때 CWRU OR3와 MFPT IR fault의 잘못된 분류가 수정됨 (Figure 11)

---

## Raspberry Pi 4B Latency 분석

### 측정 환경

| 항목 | 원문 내용 |
|---|---|
| Device | Raspberry Pi 4B |
| Framework | PyTorch Mobile |
| Backend | XNNPACK |
| Architecture target | ARM |
| Warm-up | 1000회 |
| Timed runs | 100회 |
| Reported statistic | Average + observed min/max range (Figure 6) |
| Inference batch size | 확인 불가 |
| Thread count | 확인 불가 |
| OS / kernel | 확인 불가 |
| CPU governor/frequency | 확인 불가 |
| Quantization | 언급 없음 (FP32 추정) |

### FRFconv-TDSNet 수치 (Figure 6 bar chart 근사값)

| 지표 | 수치 |
|---|---|
| Average inference | 약 3.40 ms |
| Observed minimum | 약 3.30 ms |
| Observed maximum | 약 3.67 ms |
| p99 | 미보고 |
| Jitter statistic | 미보고 |
| Formal WCET bound | 없음 |

Conclusion의 "less than 5 ms"는 평균만이 아니라 Figure 6에서 관측된 maximum도 5 ms보다 작다는 의미로 해석 가능. 그러나 이 maximum은 100회 측정의 sample maximum일 뿐, formal WCET가 아니다.

### 비교 모델 latency (Figure 6 bar chart 근사값)

| Model | Average (ms) | Observed min (ms) | Observed max (ms) |
|---|---|---|---|
| FRFconv-TDSNet | **3.40** | 3.30 | **3.67** |
| WDCNN | 2.96 | 2.76 | 4.43 |
| TICNN | 3.86 | 3.70 | 5.63 |
| WKCNN | 3.04 | 2.76 | 6.42 |
| CLFormer | 15.23 | 14.99 | 20.60 |
| SECN | 18.44 | 18.08 | 22.15 |
| S-Transformer | 23.44 | 22.94 | 27.74 |
| MBSDCN | 8.54 | 8.29 | 13.81 |
| MSDCNN | 6.96 | 6.70 | 11.52 |

**상대적 위치**: 평균만 보면 WDCNN·WKCNN이 약간 빠르지만, FRFconv-TDSNet은 100회 범위에서 **가장 짧은 observed maximum**을 기록한다. 1.80 MAdds로 계산량은 더 많지만 XNNPACK이 depthwise separable convolution을 효율적으로 최적화하여 실제 latency가 안정적이다.

---

## 내 연구 관점

### 본 연구와의 gap 비교표

| 관점 | FRFconv-TDSNet | 개인연구 |
|---|---|---|
| Platform | Raspberry Pi 4B | Raspberry Pi Zero 2W |
| OS | 확인 불가 | Linux + PREEMPT_RT |
| Runtime | PyTorch Mobile + XNNPACK | 선정 예정 |
| W | 2048 고정 | Runtime mode 변수 |
| H | 정의 없음 | 진단 period/hop 변수 |
| M | 고정 FRFconv-TDSNet | Runtime 선택 후보 |
| Trigger | 없음 | Machine condition (q) + slack (S) |
| Scheduling | 없음 | PREEMPT_RT task analysis |
| Deadline | 없음 | 명시적 D |
| Tail | 100-run observed max | p99/max/miss |
| Noise robustness | FRF + TDS | Model quality dimension |
| System interference | 고려 안 함 | 핵심 평가 대상 |

결정적 차이: FRFconv-TDSNet은 노이즈에 강하고 경량인 (M)의 설계를 다루지만, 기계 상태와 scheduling slack에 따라 (W/H/M)을 runtime에 선택하는 문제는 다루지 않는다.

### (M) 후보 적합성 평가

**강점**:
- 9K parameter로 매우 작음
- Pi 4B observed maximum 약 3.67 ms — 비교 모델 중 가장 안정적
- (-4) dB 강한 noise에서 세 dataset 모두 최고 수준 accuracy
- TDS branch가 설명 가능성과 magnitude 정보 제공
- Depthwise separable convolution이 ARM XNNPACK에서 효율적으로 최적화됨
- CWRU, MFPT, UoC 세 종류 bearing/gearbox dataset에서 검증

**약점**:
- (W)와 FRF kernel shape가 구조적으로 결합 — 동일 model instance를 여러 (W)에 공유 불가
- H (runtime diagnosis period) 미정의
- Deadline/RT scheduling 없음
- Pi 4B OS/thread/frequency 조건 미보고
- PyTorch Mobile FP32로 평가 — Pi Zero 2W + PREEMPT_RT 환경과 직접 비교 불가
- Synthetic AWGN만 평가; actual factory noise에서의 성능 미검증

### (W) 변경 시 구현 전략

**전략 A — (W)별 별도 모델 학습** (권장):
```
W=512  → FRFconv-TDSNet-512
W=1024 → FRFconv-TDSNet-1024
W=2048 → FRFconv-TDSNet-2048
```
장점: Window 감소에 따라 연산량·parameter도 실제로 감소; 9K 이하로 매우 작아 복수 저장 부담이 비교적 작음
단점: (M)이 사실상 (W)에 종속; mode별로 학습·검증·calibration 필요; runtime model switching 또는 model residency 관리 필요

**전략 B — 모든 입력을 2048로 resampling/padding**:
장점: 동일 model weight 공유 가능
단점: W 감소의 latency 이점 약해짐; padding/resampling으로 신호의 주파수 특성이 변할 수 있음; 논문에서 검증하지 않음

**전략 C — FRF 구조 수정** (Adaptive conv, Dilated conv, Early-exit 등):
원 논문의 방법이 아닌 연구 확장안이다.

### 가장 적합한 활용 방식

**권고안 A — Mode별 FRF model family**:

A = {(W_512, H_1, M_FRF512), (W_1024, H_2, M_FRF1024), (W_2048, H_3, M_FRF2048)}

원 구조를 유지하면서 mode-selection 연구와 결합하기 가장 자연스럽다.

**권고안 B — Baseline과 candidate 역할 분리**:
- Baseline (M_1): 일반 small-kernel 1D CNN
- Noise-robust (M_2): FRFconv-TDSNet
- Fast (M_3): 더 작은 lightweight CNN

Runtime policy가 (q), noise estimate, (S)를 보고 model을 선택할 수 있다:
```
Noise high + slack sufficient → FRFconv-TDSNet
Slack low                    → Fast CNN
Machine critical + slack sufficient → Large-window FRF model
```

### Pi Zero 2W 이식성 추정

"Pi Zero 2W가 Pi 4B보다 약 3-5배 느리다"는 가정 아래 단순 비례 추정:

| 지표 | Pi Zero 2W 예상 |
|---|---|
| Average inference | 약 10~17 ms |
| Observed max 대응 | 약 11~18 ms |

이 추정은 Cortex-A53과 A72의 microarchitecture 차이, XNNPACK kernel 지원·최적화 차이, CPU clock/governor, memory bandwidth, thermal throttling, PREEMPT_RT overhead, task interference, thread count를 반영하지 않은 거친 비례 추정이다. 실제 연구에서는 반드시 Pi Zero 2W에서 직접 profiling해야 한다.

512 MB RAM에서의 실행 가능성: 9K parameter, FP32 약 36 KB → model tensor 자체는 매우 여유롭게 들어감. 다만 PyTorch Mobile framework/runtime memory overhead가 model weight보다 훨씬 클 수 있으므로 Pi Zero 2W에서는 PyTorch Mobile 외에 ONNX Runtime Mobile, TFLite, C++ 직접 구현 등의 후보를 비교하는 것이 좋다.

---

## KCC 2026 구현과 반드시 구분할 점

| 항목 | IEEE TIM 2024 (이 논문) | KCC 2026 구현 (본 선행연구) |
|---|---|---|
| Platform | Raspberry Pi 4B | STM32F407 |
| Runtime | PyTorch Mobile | TensorFlow Lite Micro |
| Backend | XNNPACK | CMSIS-NN |
| Precision | 양자화 언급 없음 (FP32 추정) | INT8 |
| Input | (W=2048) | (W=2048/1024/512) variants |
| Latency | avg 약 3.40 ms, max 약 3.67 ms | MCU에서 별도 실측값 |
| 목적 | 모델 noise robustness + edge efficiency | MCU 실시간 추론 최적화 |

두 논문의 latency를 직접 비교하면 안 된다. Hardware, runtime, precision, backend가 전부 다르다.

---

## 서베이 표 항목

| 항목 | 내용 |
|---|---|
| 가변 변수 | 없음 — W=2048/H/M 전부 offline 고정 |
| 트리거 | 없음 — offline model 설계 및 평가 |
| 플랫폼·환경 | Raspberry Pi 4B; PyTorch Mobile + XNNPACK; OS·kernel 미기재 |
| 경량화·배포 기법 | 경량 아키텍처 수동 설계 (FRFconv depthwise separable + TDS late fusion); 9K parameter, 1.80 MAdds |
| 보장 수준 | B — avg 3.40 ms, observed max 3.67 ms (100회), deadline/tail/p99 없음 |
| 본 연구와의 gap | W/H 고정, H 미정의, q+S trigger 없음, PREEMPT_RT/scheduling 없음 |

---

## 세 문장 압축

이 논문은 입력 전 구간을 보는 FRF depthwise separable convolution과 raw vibration의 mean·peak·RMS·crest factor를 결합해 경량·노이즈 강건 결함진단 모델을 제안하며, Raspberry Pi 4B에서 PyTorch Mobile + XNNPACK으로 평균 약 3.40 ms·observed maximum 약 3.67 ms의 추론 성능을 보고한다. W=2048은 비중첩 고정 입력이며 H는 정의하지 않고, FRF kernel이 layer input length에 종속되므로 W를 바꾸려면 별도 model variant가 필요해 동일 trained model instance를 여러 W에 공유할 수 없다. 기계 상태 q와 scheduling slack S에 따라 (W/H/M) mode를 runtime에 선택하는 것, PREEMPT_RT 환경의 task interference 분석, 명시적 deadline 정의는 다루지 않는다.

---

## Related Work용 영어 문장

> Lee and Kim proposed a lightweight 1-D CNN that combines full-receptive-field depthwise separable convolution with raw-signal time-domain statistics, achieving strong robustness under unseen AWGN and sub-5-ms empirical inference on a Raspberry Pi 4B. However, the model uses a fixed 2048-point input and does not define a diagnosis period, deadline, or runtime mode-selection policy.

---

## 불확실한 점

1. CWRU·MFPT·UoC의 실제 sampling rate — 논문 본문에 기재 없음
2. 2048-point window의 물리적 선택 근거 (characteristic frequency·회전 주기 등과 연결 없음)
3. Runtime diagnosis period (H) — 정의 없음
4. Raspberry Pi 4B OS·kernel 버전 및 RT 설정 여부
5. Raspberry Pi 4B RAM 용량
6. CPU clock/governor 및 frequency fixed 여부
7. Thread 수와 core affinity
8. Inference batch size
9. p95/p99 latency — 100회 min/max만 보고
10. 100회 이후 장시간 tail behavior
11. Actual factory noise에서의 성능 (synthetic AWGN만 평가)
12. (W) 변경 시 model accuracy·latency 변화 (variable-W 실험 수행하지 않음)
13. 동일 weight의 variable-length input 지원 여부 (논문에서 미검증)
14. PyTorch Mobile model file size (.ptl 형식)
15. Pi Zero 2W에서의 실제 PyTorch Mobile 실행 가능성 (runtime memory 미측정)
