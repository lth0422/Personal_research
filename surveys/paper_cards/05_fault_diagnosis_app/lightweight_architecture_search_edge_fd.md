# A Real-Time Mechanical Fault Diagnosis Approach Based on Lightweight Architecture Search Considering Industrial Edge Deployments

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S3 (경량화 대조군), S4 (hardware-aware objective 비교)
- **플랫폼 태그**: `PL-DESKTOP`
- **실행환경 태그**: `ENV-OTHER` (OS, framework, thread 수 미기재; AMD Ryzen 5 4600H CPU)
- **출처/연도**: Engineering Applications of Artificial Intelligence, Vol. 123, 2023, Art. 106433
- **저자**: Sihan Ma, Hongchun Sun, Sheng Gao, Guixing Zhou
- **분석 MD**: `papers/05_fault_diagnosis_app/reviews/Ma_2023_Lightweight_Architecture_Search_FD_분석 3aadc25ad4e88096b649e5ed19f6078b.md`

---

## 두 질문

- **가변 변수**: 없음. W=1024 고정, H 미보고, M은 differentiable NAS로 offline 탐색 후 배포 시 고정. Runtime adaptation 없음.
- **트리거**: 없음. Target CPU에서 candidate operation의 measured time을 NAS objective에 포함하지만, 이는 offline search 단계의 기준이다. Runtime에 machine condition이나 system slack에 반응하지 않는다.

---

## 초록 번역

딥러닝 기반 기계 지능형 진단 모델은 진단 정확도를 향상시켰다. 그러나 딥러닝 모델이 요구하는 추가 메모리와 증가하는 계산 부담은 edge deployment를 제한하고 real-time performance를 저하시켜 산업 적용을 어렵게 한다.

이에 본 논문은 variable-layer search, efficient search space, real-time search strategy를 결합한 multi-objective automatic optimisation architecture search 기반 기계 고장 진단 전략을 제안한다. 제안 방식은 edge deployment의 계산 요구사항, real-time testing, 진단 정확도를 함께 고려하는 lightweight diagnostic network를 자동으로 구성한다.

또한 engineering application에서 나타나는 rotating machinery의 compound fault와 strong noise의 영향을 고려한다. 두 종류의 회전기계 고장 데이터에 대한 실험 결과, 제안 모델은 기존 advanced baseline보다 더 경량이면서도 더 높은 정확도를 보였다.

---

## 논문 흐름 + Novelty

### 논리 흐름

1. 기존의 수작업 lightweight network는 설계자 경험에 의존하고, 일반적인 NAS도 accuracy 위주로 구조를 탐색해 실제 edge device에서의 execution time을 충분히 반영하지 못한다고 문제를 제기한다.
2. 진동 신호용 network를 Feature extraction cell, Normal cell, Reduce cell, Classifier로 나누고, cell 내부 operation과 Normal cell의 유지 여부를 differentiable NAS로 탐색한다.
3. Candidate operation에는 여러 kernel size의 convolution, group convolution, dilated convolution, pooling을 포함해 작은 parameter 수와 넓은 receptive field를 동시에 노린다.
4. 각 candidate operation을 target CPU에서 실제 실행해 measured time을 accuracy loss와 결합하여, 빠르면서 정확한 architecture를 탐색한다.
5. Mixed bearing–gear–rotor dataset과 Northeastern University bearing–rotor dataset에서 accuracy, test time, FLOPs, model volume, noise robustness를 비교하고 ablation으로 각 구성요소의 효과를 검증한다.

### 저자가 주장하는 Novelty

| # | 내용 | 근거 |
|---|---|---|
| 1 | 진동 진단용 efficient cell search space (Feature/Normal/Reduce cell 분리, 넓은 kernel 후보 포함) | Section 3.1, pp.4–5; Figure 7 |
| 2 | Group + dilated convolution (GD-Conv)을 search space에 추가해 channel 연결과 계산량을 동시에 줄임. g=3, dilation rate는 Table 1의 사전 정의값 | Section 3.1, p.5; Table 1 |
| 3 | Variable-layer differentiable NAS: Normal cell마다 module path weight (γ_m)와 residual path weight (γ_r)를 두고, γ_m < γ_r이면 해당 cell 제거 → network depth도 search 대상 | Section 3.2, p.5; Figure 8, p.6 |
| 4 | 실제 device execution time 기반 objective: FLOPs 대신 candidate operation을 target device에서 실행한 measured time을 architecture weight로 연속 완화한 뒤 accuracy loss와 결합 | Section 3.3, pp.5–6; Equations (8)–(11) |

---

## NAS 탐색 공간

### 탐색하는 변수

| 변수 | 탐색 내용 |
|---|---|
| Operation type | Standard conv / GD-Conv / Average pooling / Max pooling |
| Kernel size | k ∈ {3, 5, 7, 11, 31, 63}; cell별 후보 범위 다름 |
| Network depth | Normal cell 유지·제거 (γ_m < γ_r이면 제거) |

초기 hyper-network 구조: `F-R-N-N-R-N-N-R-N-N-C` (Feature-Reduce-Normal×3 반복)

### 탐색하지 않는 변수

| 변수 | 이유 |
|---|---|
| Input window (W) | 모든 실험에서 1024로 고정 |
| Hop / period (H) | segmentation stride/overlap 미기재 |
| Channel 수 | candidate별 channel-width 범위 제시 안 됨 |
| Group 수 g | 3으로 고정 |
| Quantisation | search space 외부 |
| Memory | 결과 지표로만 보고 |

### W는 왜 1024인가

Case 1에서는 서로 다른 sampling rate의 dataset을 하나의 model에 넣기 위해 W=1024로 통일한다. Case 2에서는 Northeastern Univ. dataset이 10 kHz로 수집되므로 W=1024 그대로 사용한다. W의 물리적·신호처리적 선정 근거는 원문에 없다.

---

## Hardware-Aware Objective

candidate operation k의 target device 실행 시간 t_{op_k}를 미리 측정하고, architecture weight α_k를 이용해 mixed time을 구성한다:

```
t̄ = Σ softmax(α_k) · t_{op_k}
t_b = min{t_{op_1}, ..., t_{op_m}}
L_time = log(t̄ / t_b)
L_loss = (1-λ)·L_acc + λ·L_time    λ=0.8
```

- t̄/t_b가 1에 가까울수록 가장 빠른 operation에 수렴
- λ=0.8은 실험적 선택이며 저자도 subjectivity를 한계로 인정
- FLOPs와 memory는 search objective에 직접 포함되지 않고 결과 비교 지표로만 사용
- Deadline constraint (C(M) ≤ D) 형태의 hard constraint가 아니라 weighted soft optimisation

---

## RT 등급: B (확정)

| 판정 항목 | 결과 | 원문 근거 |
|---|---|---|
| 명시적 deadline | X | 없음 |
| RTOS 또는 RT-Linux | X | 미기재 |
| Deadline miss 측정 | X | 없음 |
| Tail latency (p99/max) | X | 미보고 |
| Schedulability 분석 | X | 없음 |
| Average latency (proxy) | △ | batch test-set 처리 시간을 sample당 평균으로 환산 (0.780 ms/sample) |
| Acquisition period (implicit) | △ | T_W=51.2 ms (f_s=20kHz, W=1024)를 implicit 기준으로 사용하지만 deadline으로 선언하지 않음 |
| W/H/M runtime 변경 | X | 전부 고정 |

---

## 실행 수치

### 측정 환경

| 항목 | 내용 |
|---|---|
| Processor | AMD Ryzen 5 4600H with Radeon Graphics |
| 목적 | Resource-constrained edge deployment simulation |
| Training epoch | 200 |
| Architecture search epoch | 100 |
| Search 횟수 | 3회; searched network별 반복 10회; model comparison 반복 30회 |
| 통계 | 95% confidence interval |
| OS / Framework / Thread 수 | 미기재 |
| Batch size (test) | 미기재 (training batch=128) |

실제 embedded edge board가 아닌 desktop/laptop-class CPU로 edge deployment를 모사한다.

### Case 1 — Mixed fault dataset

| 지표 | 값 |
|---|---|
| Dataset | Mixed bearing, gear, rotor (20 classes) |
| Samples | Training 3100, Test 820 |
| W | 1024 samples |
| f_s (최고) | 20,000 Hz → T_W = 51.2 ms |
| 전체 test time | 0.64 ± 0.02 s |
| 환산 평균 | 0.780 ms/sample |
| FLOPs | 6.08 M |
| Model volume | 82 K params |

비교 baseline (Table 3): MobileNet 3.85 s / ShuffleNet 1.94 s / GhostNet 7.78 s / LEFENet 2.40 s / DARTS 17.11 s

### Case 2 — Northeastern University dataset

| 지표 | 값 |
|---|---|
| Dataset | Bearing, rotor (11 classes) |
| Samples | Training 1760, Test 440 |
| W | 1024 samples |
| f_s | 10,000 Hz → T_W = 102.4 ms |
| 전체 test time | 0.38 ± 0.02 s |
| 환산 평균 | 0.864 ms/sample |
| Accuracy | 99.09 ± 0.45% |
| FLOPs | 3.13 M |
| Model volume | 70 K params |

### 실시간성 주장과 해석 주의사항

논문은 C_avg ≪ T_W를 근거로 real-time 동작을 주장한다. 그러나 Table의 test time은 batch test-set 전체 처리 시간이므로 다음이 불명확하다:

- DataLoader 시간 포함 여부
- Batch-1 single-window online latency와의 동일성
- 첫 inference warm-up 포함 여부
- Per-window maximum 또는 p99 latency

추가로, 원문의 processed-data throughput 계산(약 130k data/s)이 표의 수치로 계산한 값(약 1.31×10^6 points/s)과 약 10배 불일치한다.

---

## 개인연구와의 연결

### 이 논문에서 가져올 수 있는 것

Hardware-aware NAS에서는 FLOPs proxy 대신 target device에서 candidate operation의 measured time을 search objective에 직접 포함할 수 있다. 이 아이디어를 개인연구의 mode profiling에 적용하면:

```
P = {A_i, C_i^{p99}, Mem_i}   각 (W/H/M) mode를 Pi Zero 2W에서 profile한 timing table
```

### 결정적 차이

| 관점 | Ma et al. | 개인연구 |
|---|---|---|
| W | 1024 고정 | runtime mode 변수 |
| H | 미정 | diagnosis period 변수 |
| M | offline NAS로 하나만 탐색 | runtime 선택 후보 집합 |
| Trigger | 없음 | q + S |
| Platform | Ryzen 5 desktop CPU | Pi Zero 2W + PREEMPT_RT |
| Timing | test-set total time | per-job tail latency |
| W-latency curve | 없음 | 핵심 분석 대상 |

---

## 세 문장 압축

Ma et al.은 vibration diagnosis network의 convolution, GD-Conv, pooling operation과 Normal cell 유지 여부를 differentiable NAS로 탐색하고, target CPU에서 측정한 candidate operation time을 accuracy loss와 결합한다. 그러나 입력 window는 모든 dataset에서 W=1024로 고정되며, NAS는 W나 H가 아니라 model architecture M만 offline으로 탐색한다. Ryzen 5 CPU에서 820개 sample을 0.64 s에 처리하지만 이는 batch test-set throughput이며, W별 latency, batch-1 p99, deadline miss, runtime q+S mode selection은 평가하지 않는다.

## Related Work 영어 한 줄

> Ma et al. co-optimised diagnostic accuracy and measured operator latency in a variable-depth differentiable NAS, but fixed the input length to 1024 samples and searched only a single offline architecture without runtime W/H/M adaptation.

---

## 불확실한 점

1. Channel width가 architecture search parameter인지 명확히 제시되지 않는다.
2. Dataset별 segmentation overlap과 hop H가 보고되지 않는다.
3. W=1024의 물리적·신호처리적 선정 근거가 없다.
4. CPU timing 시 framework, OS, thread 수, affinity가 미기재다.
5. Test time이 batch inference인지 sample-wise inference인지 명확하지 않다.
6. Table의 test-set total time을 online single-window response time으로 직접 해석하기 어렵다.
7. p95, p99, maximum latency와 deadline miss가 없다.
8. Search objective에는 FLOPs와 memory capacity가 직접 들어가지 않는다.
9. λ=0.8 선택은 실험적 관찰에 의존하며 저자도 subjectivity를 한계로 인정한다.
10. 원문의 processed-data throughput 계산이 표의 sample 수·길이·시간과 약 10배 불일치한다.
11. 실제 embedded edge device가 아니라 Ryzen 5 CPU에서 평가한다.
12. Target device가 변경될 때 실제로 다른 architecture가 선택되는지 cross-device search 결과를 제시하지 않는다.
