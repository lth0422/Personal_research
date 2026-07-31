# Ma_2023_Lightweight_Architecture_Search_FD_분석

# Ma et al. (2023) — Lightweight Architecture Search 기반 실시간 기계 결함 진단 분석

> **대상 논문**
> 
> 
> S. Ma, H. Sun, S. Gao, and G. Zhou,
> 
> “A Real-Time Mechanical Fault Diagnosis Approach Based on Lightweight Architecture Search Considering Industrial Edge Deployments,”
> 
> *Engineering Applications of Artificial Intelligence*, Vol. 123, 2023, 106433.
> 
> **평가 플랫폼**
> 
> AMD Ryzen 5 4600H CPU with Radeon Graphics
> 
> **개인연구 기준**
> 
> $$
> a=(W,H,M),\qquad \text{trigger}=q+S
> $$
> 
> **핵심 질문**
> 
> 1. NAS가 정확히 무엇을 탐색하는가?
> 2. 입력 window (W)도 탐색 대상인가?
> 3. Hardware latency를 search objective에 어떻게 반영하는가?
> 
> **페이지 표기**
> 
> `p.n`은 첨부 PDF의 n번째 페이지를 의미한다.
> 

---

# 0. 초록 번역

딥러닝 기반의 기계 지능형 진단 모델은 진단 정확도를 향상시켰다. 그러나 딥러닝 모델이 요구하는 추가 메모리와 증가하는 계산 부담은 각각 edge deployment를 제한하고 real-time performance를 저하시켜 산업 적용을 어렵게 한다.

이에 본 논문은 **variable-layer search**, **efficient search space**, **real-time search strategy**를 결합한 multi-objective automatic optimisation architecture search 기반 기계 고장 진단 전략을 제안한다. 제안 방식은 edge deployment의 계산 요구사항, real-time testing, 진단 정확도를 함께 고려하는 lightweight diagnostic network를 자동으로 구성한다.

또한 engineering application에서 나타나는 rotating machinery의 compound fault와 strong noise의 영향을 고려한다. 두 종류의 회전기계 고장 데이터에 대한 실험 결과, 제안 모델은 기존 advanced baseline보다 더 경량이면서도 더 높은 정확도를 보였다.

---

# 1. 논문 흐름과 Novelty

## 1.1 문제 → 방법 → 검증 흐름

1. 기존의 수작업 lightweight network는 설계자의 경험과 반복 실험에 크게 의존하며, 일반적인 NAS도 **accuracy 위주로 구조를 탐색해 실제 edge device에서의 execution time을 충분히 반영하지 못한**다고 문제를 제기한다.
2. 이를 해결하기 위해 vibration signal용 network를 Feature extraction cell, Normal cell, Reduce cell, Classifier로 나누고, 각 cell 내부의 operation과 전체 network의 cell 유지 여부를 differentiable NAS로 탐색한다.
3. Candidate operation에는 여러 kernel size의 convolution, group convolution, dilated convolution, pooling을 포함해 작은 parameter 수와 넓은 receptive field를 동시에 노린다.
4. 각 candidate operation을 target CPU에서 실제로 실행한 measured time을 accuracy loss와 결합하여, 빠르면서 정확한 architecture를 탐색한다.
5. Mixed bearing–gear–rotor dataset과 자체 bearing–rotor dataset에서 accuracy, test time, FLOPs, model volume, noise robustness를 비교하고 ablation으로 각 구성요소의 효과를 검증한다.
    
    [NAS 란](https://app.notion.com/p/NAS-3aadc25ad4e8802ab6a8fd128e5117a2?pvs=21)
    

---

[논문에서 제안하는 나스 시스템의 흐름](https://app.notion.com/p/3aadc25ad4e880c8a6f5f0332685d68b?pvs=21)

## 1.2 저자가 주장하는 Novelty

### Novelty 1 — 진동 진단용 efficient cell search space

Network를 다음 네 부분으로 나눈다.

```
Feature extraction cell
        ↓
Normal cell
        ↓
Reduce cell
        ↓
Classifier
```

Classifier는 단일 fully connected layer와 softmax로 고정하고, 나머지 세 cell을 architecture search 대상으로 둔다.

Feature extraction cell은 **넓은 범위의 convolution kernel을 포함해 고주파 detail과 저주파·denoising feature를 함께 추출**하도록 구성한다.

![image.png](image.png)

**근거:** Section 3.1, pp.4–5; Figure 7.

### Novelty 2 — Group + dilated convolution을 search space에 추가

저자는 **group convolution**으로 **channel 연결과 계산량을 줄이고**, dilated convolution으로 작은 실제 kernel을 사용하면서도 넓은 receptive field를 유지하는 **GD-Conv**를 candidate operation으로 추가한다.

Group 수는 탐색하지 않고 다음 값으로 고정한다.

$$
g=3
$$

Dilation rate도 Table 1의 사전 정의값으로 고정된다.

![image.png](image%201.png)

**근거:** Section 3.1, p.5; Table 1.

### Novelty 3 — Variable-layer differentiable architecture search

기존 cell-based NAS는 hyper-network의 cell 수와 순서를 사람이 미리 정한다. 본 논문은 Normal cell마다

- cell path weight (_m)
- residual path weight (_r)

를 두고, search 종료 후

$$
\gamma_m < \gamma_r
$$

이면 해당 Normal cell을 제거한다.

즉 cell 내부 operation뿐 아니라 **network depth**, 더 정확히는 Normal cell의 유지·제거도 자동으로 결정한다.

**근거:** Section 3.2, p.5; Figure 8, p.6.

### Novelty 4 — 실제 device execution time 기반 objective

FLOPs(Floating Potint Operations: 모델이 한 번 추론할 때 수행해야 하는 "실수 연산의 개수”) 같은 간접 지표만 사용하는 대신, **candidate operation을 target device에서 실제로 실행하여 시간을 측정**한다. -⇒ 간접 지표를 활용하지 않고, 실제 실행시간을 측정해서 반영한다.

각 operation의 measured time을 architecture weight로 연속 완화한 뒤 accuracy loss와 결합한다.

$$
L_{\mathrm{loss}}
=
(1-\lambda)L_{\mathrm{acc}}
+
\lambda L_{\mathrm{time}}
$$

실험에서는

$$
\lambda=0.8
$$

을 사용한다.

**근거:** Section 3.3, pp.5–6; Equations (8)–(11).

---

# 2. NAS 탐색 공간 — (W)가 포함되는가?

## 2.1 핵심 결론

> **이 논문의 NAS는 입력 window (W)를 탐색하지 않는다.**
> 

모든 실험에서 input sample length는 다음과 같이 고정된다.

$$
W=1024\ \mathrm{samples}
$$

NAS가 탐색하는 것은 (W)가 아니라 **고정된 길이 1024 입력을 처리할 model architecture (M)** 이다.

개인연구 관점으로 표현하면 다음에 가깝다.

$$
a=(W=1024,\ H=\text{미정},\ M_{\mathrm{NAS}})
$$

즉 (M)만 offline search하고, runtime에는 고정된 searched model을 사용한다.

---

## 2.2 NAS가 실제로 탐색하는 변수

### A. Cell 내부의 operation type

Node 사이 연결에서 다음 candidate operation 중 하나를 선택한다.

#### Feature extraction cell

Figure 7 기준 후보는 다음과 같다.

- (1) convolution
- (1) convolution
- (1) convolution
- (1) convolution
- (1) convolution
- (1) convolution
- 각 kernel에 대응하는 GD-Conv
- (1) average pooling
- (1) max pooling

#### Normal / Reduce cell

- (1) convolution
- (1) convolution
- (1) convolution
- (1) GD-Conv
- (1) GD-Conv
- (1) GD-Conv
- (1) average pooling
- (1) max pooling

Reduce cell은 stride 2 operation을 사용해 feature-map length를 줄인다.

**근거:** Section 3.1, p.5; Figure 7.

---

### B. Kernel size

Kernel size는 search space에 포함된다.

주요 후보:

$$
k\in\{3,5,7,11,31,63\}
$$

다만 모든 cell에서 전체 후보를 사용하지는 않는다.

- Feature extraction cell: 큰 kernel까지 포함
- Normal/Reduce cell: 주로 (3,5,7)

큰 kernel은 low-frequency feature와 denoising에 유리하고, 작은 kernel은 high-frequency detail을 추출한다는 논리를 사용한다.

---

### C. Convolution 방식

다음 operation type을 선택한다.

- Standard convolution
- Group and dilated convolution, GD-Conv
- Average pooling
- Max pooling

즉 convolution operation의 종류도 search 대상이다.

---

### D. Network depth / Normal cell 수

Hyper-network 초기 구조는 다음처럼 설정된다.

```
F-R-N-N-R-N-N-R-N-N-C
```

논문의 표기:

```
FRNNRNNRNNC
```

각 Normal cell에서 module path와 residual path의 weight를 비교해 cell을 유지하거나 제거한다.

따라서 **Normal cell의 개수와 전체 network depth가 search 결과에 따라 달라진다.**

단, 다음 요소는 고정이다.

- Feature extraction cell
- Reduce cell 위치
- Classifier
- Hyper-network의 기본 큰 틀

---

## 2.3 탐색하지 않는 변수

| 변수 | 탐색 여부 | 설명 |
| --- | --- | --- |
| Input window (W) | **아니오** | 모든 sample length를 1024로 통일 |
| Hop (H) | **아니오** | Segmentation stride/overlap 미기재 |
| Runtime model switching | **아니오** | Search 후 하나의 고정 architecture 사용 |
| Channel 수 | 원문상 명시적 search 없음 | Candidate별 channel-width 범위가 제시되지 않음 |
| Group 수 (g) | 아니오 | (g=3) 고정 |
| Dilation rate | 아니오 | Table 1의 값으로 사전 설정 |
| Reduce-cell 위치 | 아니오 | Hyper-network에 사전 배치 |
| Classifier 구조 | 아니오 | FC + softmax로 고정 |
| Quantisation bit-width | 아니오 | Search space에 없음 |
| Pruning ratio | 아니오 | 별도 pruning search 없음 |
| Memory footprint | objective에 직접 포함되지 않음 | 결과 평가 지표로만 보고 |
| FLOPs | objective에 직접 포함되지 않음 | 결과 평가 지표로만 보고 |

---

## 2.4 (W=1024)는 어떻게 사용되는가?

### Case 1 — Mixed bearing, gear, rotor dataset

서로 sampling rate와 출처가 다른 데이터를 하나의 integrated diagnosis model에 넣기 위해 sample length를 1024로 통일한다.

Gear dataset에 대해서는 원문이 다음과 같이 설명한다.

> Dataset sample size를 통일하기 위해 각 gear-data segment를 1024 sampling points로 downsample한다.
> 

전체 Case 1 구성:

- Training samples: 3100
- Test samples: 820
- Sample length: 1024
- Fault classes: 20

**근거:** Section 4.1, pp.7–8.

### Case 2 — Northeastern University dataset

- Training samples: 1760
- Test samples: 440
- Sample length: 1024
- Sampling rate: 10 kHz
- Fault classes: 11

**근거:** Section 4.1 Case 2, p.9.

---

## 2.5 (W)는 물리적으로 설계되었는가?

### **아니다.**

원문은 (W=1024)를 다음 물리량으로 유도하지 않는다.

- Shaft revolution
- RPM
- Bearing characteristic frequency
- BPFO/BPFI/BSF/FTF
- Speed-change time scale
- Minimum number of fault impulses
- Acquisition deadline

Case 1에서는 서로 다른 dataset의 input shape를 맞추기 위한 **data-format unification** 성격이 강하다.

따라서 이 논문에서 (W)는 search variable이 아니라 **search 전에 고정되는 dataset preprocessing parameter**다.

---

# 3. Hardware constraint를 NAS objective에 반영하는 방법

## 3.1 실제 operation time 측정

Node (x^{(i)})와 (x^{(j)}) 사이에 (m)개의 candidate operation이 있다고 하자.

각 operation을 target device에서 실행해 다음 time set을 만든다.

$$
T=
\left\{
t_{op_1},
t_{op_2},
\ldots,
t_{op_m}
\right\}
$$

Architecture weight (_k)를 이용한 mixed time은 다음과 같다.

$$
\bar{t}
=
\sum_{k=1}^{m}
\operatorname{softmax}(\alpha_k)
t_{op_k}
$$

그리고 candidate 중 가장 빠른 measured time을 benchmark로 둔다.

$$
t_b
=
\min
\left\{
t_{op_1},t_{op_2},\ldots,t_{op_m}
\right\}
$$

Time loss:

$$
L_{\mathrm{time}}
=
\log
\frac{\bar{t}}{t_b}
$$

최종 objective:

$$
L_{\mathrm{loss}}
=
(1-\lambda)L_{\mathrm{acc}}
+
\lambda L_{\mathrm{time}}
$$

실험값:

$$
\lambda=0.8
$$

---

## 3.2 의미

- ({t}/t_b)가 1에 가까울수록 candidate mixture가 가장 빠른 operation에 가까움
- (L_{})가 작아지는 방향으로 architecture weight를 update
- 동시에 (L_{})도 고려하므로, 무조건 가장 빠른 operation만 선택하지는 않음
- Device마다 실제 operation time이 다르므로 target device가 바뀌면 다른 architecture가 선택될 수 있음

즉 이 논문의 중요한 장점은 다음이다.

> **FLOPs를 latency proxy로만 사용하지 않고, target CPU에서 candidate operation의 실제 measured time을 architecture-search objective에 직접 넣는다.**
> 

---

## 3.3 FLOPs와 memory는 어떻게 반영되는가?

### FLOPs

FLOPs는 final comparison table과 ablation에서 보고하지만, Equation (11)의 search objective에는 직접 들어가지 않는다.

### Model volume / memory

Model volume도 최종 결과 지표로 보고할 뿐, explicit memory constraint나 memory loss로 objective에 포함하지 않는다.

### Deadline

특정 deadline (D) 또는 latency upper bound를 constraint로 두지 않는다.

즉 이 방법은

$$
C(M)\le D
$$

를 만족하는 architecture를 찾는 hard-constrained search가 아니다.

대신

$$
\min \left[(1-\lambda)L_{\mathrm{acc}}+\lambda L_{\mathrm{time}}\right]
$$

형태의 weighted soft optimisation이다.

---

# 4. Edge deployment 수치

## 4.1 평가 플랫폼과 조건

| 항목 | 내용 |
| --- | --- |
| Processor | AMD Ryzen 5 4600H with Radeon Graphics |
| Timing device | CPU |
| 사용 목적 | Resource-constrained edge deployment의 simulation |
| Batch size | 128 |
| Training epoch | 200 |
| Architecture-search epoch | 100 |
| Search 횟수 | 3회 |
| Searched network별 반복 | 10회 |
| Model comparison 반복 | 30회 |
| 통계 | 95% confidence interval |
| OS | 미기재 |
| Framework/version | 미기재 |
| CPU thread 수 | 미기재 |
| Core affinity/governor | 미기재 |
| Batch-1 latency | 미기재 |

중요한 점은 실제 embedded edge board에서 측정한 것이 아니라 **desktop/laptop-class CPU로 edge deployment를 모사**했다는 것이다.

---

## 4.2 Case 1 — Mixed fault dataset

Test set:

- 820 samples
- (W=1024)

Proposed model:

$$
0.64\pm0.02\ \mathrm{s}
$$

820개 전체 test-set 처리 시간이다.

Sample당 평균으로 환산하면

$$
\frac{0.64}{820}
\approx0.000780\ \mathrm{s}
=0.780\ \mathrm{ms/sample}
$$

Table 3:

| Model | Test time | FLOPs | Model volume |
| --- | --- | --- | --- |
| MobileNet | 3.85 ± 0.33 s | 326.43 M | 12637 K |
| ShuffleNet | 1.94 ± 0.02 s | 117.06 M | 6540 K |
| GhostNet | 7.78 ± 0.06 s | 107.55 M | 11838 K |
| LEFENet | 2.40 ± 0.05 s | 8.45 M | 329 K |
| DARTS | 17.11 ± 0.06 s | 2034.27 M | 11464 K |
| **Proposed** | **0.64 ± 0.02 s** | **6.08 M** | **82 K** |

**근거:** Table 3, p.8.

---

## 4.3 Case 2 — Northeastern University dataset

Test set:

- 440 samples
- (W=1024)

Proposed model:

$$
0.38\pm0.02\ \mathrm{s}
$$

Sample당 평균:

$$
\frac{0.38}{440}
\approx0.000864\ \mathrm{s}
=0.864\ \mathrm{ms/sample}
$$

Accuracy:

$$
99.09\pm0.45\%
$$

FLOPs:

$$
3.13\ \mathrm{M}
$$

Model volume:

$$
70\ \mathrm{K}
$$

**근거:** Table 4, p.9.

---

## 4.4 논문의 real-time 주장

### Case 1

가장 높은 sampling frequency:

$$
f_s=20\ \mathrm{kHz}
$$

Window:

$$
W=1024
$$

한 window acquisition duration:

$$
T_W
=
\frac{1024}{20000}
=
51.2\ \mathrm{ms}
$$

환산된 **평균 per-sample processing**:

$$
C_{\mathrm{avg}}
\approx0.780\ \mathrm{ms}
$$

따라서 batch-test 평균을 그대로+ online single-window latency로 간주하면

$$
C_{\mathrm{avg}}\ll T_W
$$

이다.

### Case 2

Sampling frequency:

$$
f_s=10\ \mathrm{kHz}
$$

Window duration:

$$
T_W
=
\frac{1024}{10000}
=
102.4\ \mathrm{ms}
$$

평균 per-sample processing:

$$
C_{\mathrm{avg}}
\approx0.864\ \mathrm{ms}
$$

논문은 이러한 처리 throughput을 근거로 여러 장치를 동시에 real-time 진단할 수 있다고 주장한다.

---

## 4.5 하지만 latency 해석에 주의해야 한다

Table 3과 Table 4의 `Test time`은 **한 window의 batch-1 latency**가 아니라 test set 전체 처리 시간이다.

![image.png](image%202.png)

![image.png](image%203.png)

따라서 다음이 명확하지 않다.

- DataLoader 시간 포함 여부
- Test batch size 128 적용 여부
- Batch inference인지 sample-by-sample inference인지
- 첫 inference warm-up 포함 여부
- Online acquisition pipeline과 동일한 조건인지
- Per-window maximum 또는 p99 latency

따라서

$$
0.64/820=0.780\ \mathrm{ms}
$$

는 test-set throughput에서 환산한 평균이며, strict real-time response-time 측정값으로 보기는 어렵다.

[Worst case에 대한 분석 부족 정리](https://app.notion.com/p/Worst-case-3aadc25ad4e88029b805e3c9023f4b92?pvs=21)

---

## 4.6 논문 내부 throughput 계산의 불일치

Case 1:

$$
\frac{820\times1024}{0.64}
\approx1.31\times10^6
\ \mathrm{points/s}
$$

그러나 원문은 이를 약 **130k data/s**라고 표현한다.

Case 2:

$$
\frac{440\times1024}{0.38}
\approx1.19\times10^6
\ \mathrm{points/s}
$$

그러나 원문은 약 **118k data/s**라고 표현한다.

두 경우 모두 계산상 약 10배 차이가 난다.

가능성:

1. 원문에서 소수점 또는 단위를 잘못 표기
2. Sample point가 아닌 다른 처리 단위를 사용했으나 설명 누락
3. Test time이 실제로는 다른 단위·조건을 포함하지만 표 설명이 불충분

따라서 “여러 장치를 동시에 처리할 수 있다”는 정량 주장은 주의해서 해석해야 한다.

---

# 5. (W)와 inference time 관계

## 핵심 결론

> **(W)별 latency 관계는 평가하지 않는다.**
> 

모든 주요 실험이

$$
W=1024
$$

에서 수행된다.

평가하지 않은 것:

- (W=256)
- (W=512)
- (W=2048)
- (W=4096)
- (C(W)) scaling
- (A(W)) accuracy trade-off
- (W)에 따른 searched architecture 변화

따라서 이 논문만으로는

$$
W\downarrow \Rightarrow C\downarrow
$$

또는

$$
W\uparrow \Rightarrow M_{\mathrm{NAS}}\text{ 구조 변화}
$$

를 분석할 수 없다.

---

# 6. 개인연구와의 관계

## 6.1 같은 점

- Edge deployment를 고려한 lightweight model 설계(근데 실기기에 배포한 것은 아니니..;)
- 실제 measured execution time을 optimisation에 반영
- Accuracy와 latency의 multi-objective trade-off
- Raw 1D vibration 기반 fault diagnosis
- Compound fault와 noise를 실험에 포함

## 6.2 결정적 차이

> Ma et al.은 (W=1024)를 고정한 상태에서 target CPU에 빠른 하나의 model architecture (M)을 offline search한다.
> 

> 개인연구는 runtime에 machine condition (q)와 system slack (S)를 관찰하여 (W/H/M) mode를 선택한다.
> 

---

## 6.3 비교표

| 관점 | Ma et al. | 개인연구 |
| --- | --- | --- |
| (W) | 1024 고정 | Runtime mode 변수 |
| (H) | 미정 | Diagnosis period 변수 |
| (M) | NAS로 offline 탐색 | Runtime 선택 후보 |
| Trigger | 없음 | (q+S) |
| Hardware metric | Candidate operation의 measured CPU time | Mode별 p99/WCET와 slack |
| Objective | Accuracy + average operation time | Quality + deadline feasibility |
| Constraint | Soft weighted objective | Deadline/schedulability 가능 |
| Runtime adaptation | 없음 | 있음 |
| Platform | Ryzen 5 desktop CPU | Raspberry Pi Zero 2W + PREEMPT_RT |
| Timing | Test-set total time | Per-job tail latency와 miss |
| (W)-latency curve | 없음 | 핵심 분석 대상 |

---

# 7. 세 문장 압축

> Ma et al.은 vibration diagnosis network의 convolution·GD-Conv·pooling operation과 Normal-cell 유지 여부를 differentiable NAS로 탐색하고, target CPU에서 측정한 candidate-operation time을 accuracy loss와 결합한다.
> 
> 
> 그러나 입력 window는 모든 dataset에서 (W=1024)로 고정되며, NAS는 (W)나 (H)가 아니라 model architecture (M)만 탐색한다.
> 
> Ryzen 5 CPU에서 820개 sample을 (0.64) s에 처리하지만 이는 batch test-set throughput이며, (W)별 latency, batch-1 p99, deadline miss, runtime (q+S) mode selection은 평가하지 않는다.
> 

---

# 8. Related Work 영어 한 줄

> Ma et al. co-optimised diagnostic accuracy and measured operator latency in a variable-depth differentiable NAS, but fixed the input length to 1024 samples and searched only a single offline architecture without runtime (W/H/M) adaptation.
> 

---

# 9. 불확실한 점

1. Channel width가 architecture search parameter인지 명확히 제시되지 않는다.
2. Dataset별 segmentation overlap과 hop (H)가 보고되지 않는다.
3. (W=1024)의 물리적·신호처리적 선정 근거가 없다.
4. CPU timing 시 framework, OS, thread 수, affinity가 미기재다.
5. Test time이 batch inference인지 sample-wise inference인지 명확하지 않다.
6. Table의 test-set total time을 online single-window response time으로 직접 해석하기 어렵다.
7. p95, p99, maximum latency와 deadline miss가 없다.
8. Search objective에는 FLOPs와 memory capacity가 직접 들어가지 않는다.
9. () 선택은 실험적 관찰에 의존하며 저자도 subjectivity를 한계로 인정한다.
10. 원문의 processed-data throughput 계산이 표의 sample 수·길이·시간과 약 10배 불일치한다.
11. 실제 embedded edge device가 아니라 Ryzen 5 CPU에서 평가한다.
12. Target device가 변경될 때 실제로 다른 architecture가 선택되는지 cross-device search 결과를 제시하지 않는다.

---

# 10. 최종 핵심 해석

## 이 논문에서 우리가 가져올 수 있는 부분

> **Hardware-aware NAS에서는 FLOPs를 proxy로만 사용하지 않고, 실제 target device에서 candidate operation의 execution time을 측정해 search objective에 포함할 수 있다.**
> 

개인연구의 mode profiling에도 다음 방식으로 활용할 수 있다.

$$
\mathcal{P}
=
\left\{
A_i,\ C_i^{p99},\ \mathrm{Mem}_i
\right\}
$$

즉 각 (W/H/M) mode를 target platform에서 실제 profile하여 runtime policy가 사용할 timing table을 구축할 수 있다.

## 이 논문이 하지 않은 부분

> **Input length (W)와 period (H)는 search space에 없고, machine condition이나 system slack에 따라 runtime architecture를 전환하지 않는다.**
> 

따라서 개인연구의 차별점은 다음과 같이 정리할 수 있다.

```
Ma et al.
고정 W=1024
    ↓
Target CPU에서 빠른 M 하나를 offline NAS
    ↓
Deployment 후 M 고정

개인연구
q + S 관찰
    ↓
W/H/M mode의 quality·timing profile 비교
    ↓
Deadline-aware runtime mode selection
```

뭐 나스 쓸일은 없을듯 솔직히