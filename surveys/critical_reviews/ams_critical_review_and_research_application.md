# 심박수 기반 Adaptive Model Selection 논문 비판적 검토 및 개인연구 적용안

> 문서 성격: paper card보다 상세한 비판적 재검토 메모이다. 아래 적용안 중 `(W,H,M)` feasibility-first mode selection은 현재 핵심 방향이며, independent model과 Anytime 구조 비교는 핵심 정책이 정리된 뒤 검토할 후속 ablation 후보로 둔다. PREEMPT_RT 실험에서 formal WCET를 증명하지 않는 한 p99 또는 관측 max를 WCET로 표현하지 않는다.

> 대상 논문
>
> **Y. Li et al., “Adaptive Model Selection for Real-Time Heart Disease Detection on Embedded Systems,” RTCSA 2025.**
>
> 비교 참고 논문
>
> **Y. Hu et al., “On Exploring Image Resizing for Optimizing Criticality-based Machine Perception,” RTCSA 2021.**

---

# 1. 핵심 요약

이 논문은 심박수에 따라 ECG 추론 태스크의 시간 여유가 달라진다는 점에 착안하여, 다음 세 가지 계산 모드를 동적으로 선택한다.

- **High HR**: Lightweight
- **Mid HR**: Moderate
- **Low HR**: Advanced

또한 세 모델을 각각 저장하는 대신, 공통 backbone과 여러 exit를 갖는 **Anytime CNN**으로 통합하여 메모리와 전환 비용을 줄이려 한다.

논문의 핵심 장점은 단순 정확도 비교를 넘어 다음 요소를 하나의 흐름으로 연결했다는 점이다.

1. 생리적 상태 변화
2. 상태 의존적 deadline
3. 모델 복잡도 선택
4. EDF 기반 schedulability 분석
5. 임베디드 플랫폼 실험

다만 비판적으로 보면, **독립 모델보다 Anytime 구조가 실제로 더 필요한지**, **메모리 절감 주장이 평가 플랫폼에서 충분히 설득력 있는지**, **이론적 deadline과 실험 threshold가 일관되는지**에 대해서는 부족한 부분이 있다.

---

# 2. 논문의 실제 제안 범위

이 논문은 단순히 기존 모델 여러 개를 심박수에 따라 바꾸는 논문은 아니다.

## 2.1 ECG 진단 모델 설계

저자들은 다음 요소를 결합한 ECG 분류 모델을 구성했다.

- 1D Convolution
- Residual Block
- Squeeze-and-Excitation
- Period branch
- Global Attention
- Fully connected classification head

입력은 다음 두 종류다.

- **ECG branch**: 각 heartbeat cycle을 256 sample로 리샘플링한 파형
- **Period branch**: 원래 R-R interval의 실제 길이

즉, ECG 파형의 형태적 특징과 실제 박동 주기 정보를 분리하여 처리한 뒤 attention으로 결합한다.

## 2.2 모델 복잡도 세 단계

- **Lightweight**: SE와 Global Attention 제거
- **Moderate**: Residual + SE 유지, Global Attention 제거
- **Advanced**: Residual + SE + Global Attention

## 2.3 Anytime CNN

세 독립 모델을 완전히 별도로 저장하지 않고 다음처럼 공유 구조로 통합한다.

```text
Shared Backbone
  ├─ Early Exit       → Lightweight
  ├─ Intermediate Exit → Moderate
  └─ Deep Exit        → Advanced
```

심박수에 따라 실행 깊이를 미리 정하고 해당 exit까지만 계산한다.

---

# 3. 비판적 검토

## 3.1 메모리 부족을 Anytime 구조의 핵심 동기로 제시한 점은 설득력이 약함

논문은 세 독립 checkpoint를 저장하면 스마트워치 메모리 예산을 소진할 수 있다고 주장한다.

하지만 2-cycle 설정 기준 모델 크기는 다음과 같다.

| 모델 | 모델 크기 |
|---|---:|
| Lightweight | 0.44 MB |
| Moderate | 2.09 MB |
| Advanced | 6.22 MB |
| **합계** | **8.75 MB** |
| AMS+Anytime | 4.12 MB |

Anytime 모델은 약 4.63 MB를 절약하므로 상대적인 감소는 분명하다. 그러나 절대 크기로 보면 다음 플랫폼에서는 매우 작은 편이다.

- Raspberry Pi 4
- Raspberry Pi Zero 2 W, RAM 512 MB
- 일반적인 Linux 기반 스마트워치 SoC

Raspberry Pi Zero 2 W의 512 MB RAM을 기준으로 8.75 MB는 약 1.7%에 불과하다.

\[
\frac{8.75}{512}\times 100 \approx 1.71\%
\]

따라서 다음 두 문장은 구분해야 한다.

- **타당한 주장**: Anytime 모델은 메모리를 절약한다.
- **과도한 주장**: 독립 모델 세 개는 메모리 때문에 사용할 수 없다.

논문이 실제로 사용한 Raspberry Pi 4 환경에서는 후자의 주장이 충분히 입증되지 않았다.

---

## 3.2 저장 용량과 runtime memory가 구분되지 않음

모델 파일이 SD 카드나 flash에 저장되는 것과 추론 중 RAM을 점유하는 것은 다른 문제다.

실제 메모리 요구량은 다음과 같다.

\[
M_{\mathrm{runtime}}
=
M_{\mathrm{weights}}
+
M_{\mathrm{activations}}
+
M_{\mathrm{buffers}}
+
M_{\mathrm{framework}}
\]

그러나 논문은 주로 `Model Size`만 보고한다.

필요한데 빠진 항목은 다음과 같다.

- Peak resident memory
- Peak activation memory
- Interpreter/runtime overhead
- 세 모델 동시 상주 시 RSS
- 모델 load/unload latency
- 모델 선택 시 cache effect
- 모델 switching jitter

따라서 이 논문만으로는 독립 모델과 Anytime 모델의 **실제 runtime memory 비교**를 판단하기 어렵다.

---

## 3.3 독립 모델 AMS와 Anytime AMS의 직접 비교가 없음

논문은 세 독립 모델의 성능과 AMS+Anytime의 성능을 표에 제시한다. 그러나 다음 두 시스템을 정면으로 비교하지 않는다.

### A. Independent-model AMS

```text
HR → Lightweight / Moderate / Advanced 중 하나 선택
```

### B. Anytime-model AMS

```text
HR → Early / Intermediate / Deep exit 선택
```

공정한 비교를 위해서는 다음 항목이 필요하다.

- 동일한 HR sequence
- 동일한 input cycle 수
- 동일한 deadline
- 전체 평균 정확도
- deadline miss
- peak RAM
- 모델 전환 비용
- cold-cache/warm-cache 지연
- 에너지

논문은 이 비교 없이 Anytime 구조가 실용적이라고 결론 내린다.

따라서 정확한 해석은 다음과 같다.

> Anytime 모델이 독립 모델보다 우수함을 증명한 것이 아니라, 단일 checkpoint로도 높은 정확도와 낮은 지연을 달성할 수 있음을 보인 것이다.

---

## 3.4 Early exit가 각 계산 예산에 최적인지 불분명함

비교 논문인 RTCSA 2021의 image resizing 연구는 다음 주장을 한다.

> 같은 실행시간이라면 큰 모델을 중간까지만 실행하는 것보다, 해당 계산량에 맞게 따로 학습한 작은 모델이 더 높은 정확도를 낼 수 있다.

그 이유는 multi-exit 모델의 shared backbone이 여러 exit의 loss를 동시에 만족해야 하기 때문이다.

\[
L
=
\lambda_1L_{\mathrm{early}}
+
\lambda_2L_{\mathrm{middle}}
+
\lambda_3L_{\mathrm{deep}}
\]

이 경우 backbone은 각 exit에 개별적으로 최적화되지 않고 타협된 표현을 학습할 수 있다.

반면 독립 모델은 각 모드별 목적에 맞춰 따로 최적화된다.

\[
M_k^*
=
\arg\min_{M_k}L_k
\]

따라서 심박수 논문은 다음 trade-off를 명시적으로 다뤘어야 한다.

| 구조 | 장점 | 단점 |
|---|---|---|
| 독립 모델 | 모드별 최적 정확도 | 메모리 증가, 관리 복잡성 |
| Anytime | parameter sharing, 단일 checkpoint | exit별 정확도 타협 가능 |
| 부분 공유 모델 | 중간 수준의 메모리와 정확도 | 구조 및 학습 복잡성 증가 |

---

## 3.5 Table II의 threshold는 deadline이지만 설정 근거가 약함

Table II의 threshold는 실험적으로 다음과 같이 사용된다.

| HR 구간 | Threshold |
|---|---:|
| High HR | 1.5 ms |
| Mid HR | 1.75 ms |
| Low HR | 2.0 ms |

실험에서는 실제 inference latency가 이 값을 넘으면 deadline miss로 계산한다.

따라서 threshold는 사실상 **inference-level deadline budget**이다.

문제는 이 값이 다음 중 무엇에서 유도되었는지가 충분히 명확하지 않다는 점이다.

- R-R interval 자체
- ECG sampling period
- 다른 시스템 태스크를 제외하고 inference에 할당한 CPU budget
- 임상적으로 허용되는 response time
- 임의의 평가용 threshold

예를 들어 HR 90 bpm이면 R-R interval은 약 667 ms이다.

\[
RR = \frac{60}{90}\approx0.667\text{ s}
\]

그런데 inference deadline은 1.5 ms다. 따라서 1.5 ms는 생리적 beat interval 자체가 아니라, 전체 시스템 중 inference에 배정한 작은 budget으로 해석해야 한다.

논문은 이를 충분히 설명하거나 system-level workload에서 유도하지 않는다.

---

## 3.6 이론의 \(D(HR)\)와 실험 threshold의 관계가 완전히 정리되지 않음

이론에서는 ECG task를 다음처럼 모델링한다.

\[
E=(C(HR),D(HR),HR)
\]

또한 \(D(HR)\)를 relative deadline이자 sampling period라고 둔다.

그러나 실험에서 Table II의 threshold는 inference에 허용한 1.5–2.0 ms budget이다.

즉 다음 두 개가 혼재한다.

1. ECG task의 inter-arrival time 또는 sampling period
2. 모델 inference의 local execution deadline

이 둘이 같으려면 명확한 system assumption이 필요하다. 하지만 논문에서는 그 연결이 충분히 설명되지 않는다.

더 엄밀한 모델은 다음과 같이 구분하는 편이 낫다.

\[
T_{\mathrm{arrival}}(HR)
\]

\[
D_{\mathrm{e2e}}(HR)
\]

\[
B_{\mathrm{infer}}(HR)
\]

- \(T_{\mathrm{arrival}}\): 입력 또는 beat 기반 task 도착 간격
- \(D_{\mathrm{e2e}}\): end-to-end diagnosis deadline
- \(B_{\mathrm{infer}}\): inference에 배정된 실행 budget

---

## 3.7 schedulability 분석이 단순함

논문은 EDF에서 다음 조건을 사용한다.

\[
\sum_i \frac{C_i}{T_i}
+
\max_j\frac{C^j(HR)}{D^j(HR)}
\leq 1
\]

하지만 실제 시스템에는 다음 오버헤드가 존재한다.

- ECG acquisition
- R-peak detection
- segmentation
- resampling
- preprocessing
- model selection
- inference
- postprocessing
- user alert
- interrupt
- context switch
- cache interference
- OS scheduler overhead

따라서 실제 실행시간은 다음처럼 모델링하는 것이 더 타당하다.

\[
C_{\mathrm{e2e}}^{(m)}
=
C_{\mathrm{acq}}
+
C_{\mathrm{seg}}
+
C_{\mathrm{prep}}^{(m)}
+
C_{\mathrm{infer}}^{(m)}
+
C_{\mathrm{post}}
+
C_{\mathrm{sched}}
\]

논문은 추론시간 중심의 평가를 수행했으며, 실제 end-to-end schedulability를 충분히 검증하지 않는다.

---

## 3.8 평균 inference latency를 사용하며 WCET 보장이 약함

논문은 평균 inference time을 주요 지표로 제시한다.

그러나 hard 또는 firm real-time 관점에서는 다음이 더 중요하다.

- Maximum latency
- p99 latency
- p99.9 latency
- WCET upper bound
- jitter
- deadline miss under interference

평균이 1.33 ms여도 간헐적으로 2 ms를 넘으면 deadline miss가 발생할 수 있다.

특히 Linux 기반 Raspberry Pi 4에서는 다음 요인이 tail latency를 만든다.

- scheduler interference
- DVFS
- background daemon
- page fault
- cache miss
- memory contention
- thermal throttling

따라서 RTCSA 논문으로는 평균뿐 아니라 tail latency와 system load 하의 반복 측정이 필요하다.

---

## 3.9 fallback 재실행은 deadline 관점에서 위험함

Algorithm 1은 선택한 모델이 deadline을 넘으면 더 얕은 모델로 다시 실행하거나 timing anomaly를 표시한다고 한다.

```text
Advanced 실행
↓
deadline 초과 감지
↓
Moderate 또는 Lightweight로 재실행
```

하지만 이미 deadline을 초과한 뒤 다시 실행하면 해당 job의 deadline을 만족할 수 없다.

watchdog가 \(kD(HR)\), 예를 들어 0.8D에서 미리 중단하더라도 다음 비용이 필요하다.

\[
C_{\mathrm{spent}}
+
C_{\mathrm{abort}}
+
C_{\mathrm{fallback}}
\leq D
\]

논문은 이 조건을 명시적으로 보장하지 않는다.

더 안전한 방식은 다음 중 하나다.

- offline WCET profile로 처음부터 안전한 모델만 선택
- conservative admission test
- prefix reuse가 가능한 cascade
- fallback 전용 reserved slack 확보

---

## 3.10 심박수 하나만으로 모델을 선택함

AMS 정책은 사실상 두 threshold 비교다.

```text
HR ≥ 90        → Lightweight
70 ≤ HR < 90   → Moderate
HR < 70        → Advanced
```

하지만 실제 시스템 부하는 심박수만으로 결정되지 않는다.

- UI task load
- communication load
- sensor fusion
- logging
- temperature
- CPU frequency
- battery mode
- concurrent inference
- cache state

즉, 같은 HR이라도 available slack이 다를 수 있다.

이 논문의 정책은 **condition-aware**이지만 **system-state-aware**하지 않다.

---

## 3.11 threshold 주변 thrashing 방지가 충분히 구체적이지 않음

70 또는 90 bpm 주변에서 HR이 흔들리면 모델이 반복 전환될 수 있다.

예:

```text
89 → 91 → 89 → 92 → 88 bpm
```

이 경우 모델 또는 exit가 자주 바뀐다.

논문은 peak-anchored window로 HR을 smoothing한다고 설명하지만 다음 요소는 명확하지 않다.

- hysteresis 폭
- minimum residence time
- transition cost
- state persistence
- 급격한 HR 변화 탐지

보다 안정적인 정책은 다음과 같다.

```text
Advanced → Moderate: HR > 72
Moderate → Advanced: HR < 68
```

처럼 서로 다른 진입·이탈 threshold를 사용한다.

---

## 3.12 cycle 수와 task arrival 설명이 일부 혼재함

논문은 한편으로 높은 HR에서 같은 시간 안에 cycle 수가 증가하여 계산량이 증가한다고 설명한다.

다른 한편으로 모델 입력은 \(\beta=1,2,3,4\)개의 cycle을 하나의 segment로 묶어 한 번의 inference에 넣는다.

따라서 다음 세 개를 명확히 구분해야 한다.

- HR: heartbeat 발생 빈도
- \(\beta\): 한 inference 입력에 포함하는 cycle 수
- task arrival rate: inference job이 도착하는 빈도

논문의 설명에서는 이 세 요소가 일부 혼재되어 있다.

---

## 3.13 실제 wearable이 아니라 Raspberry Pi 4에서 평가함

Raspberry Pi 4는 임베디드 Linux 플랫폼으로는 적절하지만 실제 스마트워치와 다음 측면에서 차이가 있다.

- 전력 예산
- 메모리 계층
- OS
- CPU architecture
- thermal limit
- sensor I/O
- battery
- real-time scheduling support

논문도 이를 한계로 인정하지만, 메모리와 실시간성에 대한 강한 주장에 비해 실제 평가 플랫폼은 상당히 여유롭다.

---

## 3.14 모델 크기 증가 추세가 구조적으로 이상해 보이는 부분

Table III에서는 cycle 수가 증가할 때 모델 크기가 크게 증가한다.

예를 들어 Advanced는 다음과 같다.

| Cycles | Size |
|---:|---:|
| 1 | 2.1 MB |
| 2 | 6.22 MB |
| 3 | 19.5 MB |
| 4 | 44.6 MB |

일반적인 fully convolutional 구조에서는 입력 길이가 증가해도 weight parameter 수 자체는 동일할 수 있다.

이 논문에서는 \(\beta\)에 따라 채널 수가 \(8\beta,16\beta,32\beta,64\beta\)로 증가하고 FC 차원도 커지기 때문에 모델 크기 자체가 증가한다.

따라서 cycle 수 비교는 단순히 입력 길이만 바꾼 실험이 아니라 **네트워크 width와 parameter count도 함께 바뀐 실험**이다.

이 때문에 다음 효과가 분리되지 않는다.

- 더 긴 temporal context
- 더 많은 parameter
- 더 넓은 channel
- 더 큰 FC layer
- 더 긴 inference

보다 엄밀한 ablation이라면 다음 두 실험을 분리해야 한다.

1. 동일 모델 parameter에서 input cycle 수만 변경
2. cycle 수에 따라 width를 확장하는 구조

---

# 4. 내 개인연구에 적용할 수 있는 핵심

## 4.1 논문의 가장 중요한 아이디어는 Anytime이 아니라 상태 의존적 mode selection

이 논문에서 가장 직접적으로 가져올 부분은 다음 문제 정의다.

> 변화하는 입력·운전 상태에서, deadline을 만족하는 모드 중 가장 높은 진단 품질을 제공하는 모드를 선택한다.

내 연구에서는 ECG의 HR을 다음으로 치환할 수 있다.

| ECG 논문 | 내 연구 |
|---|---|
| HR | RPM, load, operating condition |
| ECG cycle | 회전 주기 또는 진동 window |
| CVD severity | fault type 또는 severity |
| Lightweight/Moderate/Advanced | W512/W1024/W2048 및 모델 복잡도 |
| \(D(HR)\) | 상태 의존적 diagnosis deadline |
| Anytime exit | 독립 모델 또는 multi-exit mode |
| Period branch | RPM/load/운전조건 branch |

---

## 4.2 내 연구는 condition-aware를 넘어 slack-aware로 확장 가능

심박수 논문은 HR만 본다.

내 연구에서는 다음 상태를 함께 사용할 수 있다.

\[
z_i=
(\text{RPM}_i,\text{load}_i,\text{machine state}_i)
\]

\[
s_i=
\text{available system slack}
\]

\[
u_i=
\text{model uncertainty}
\]

정책은 다음처럼 정의할 수 있다.

\[
m_i
=
\pi(z_i,s_i,u_i)
\]

즉 다음을 동시에 고려한다.

- 기계 상태
- 현재 CPU 여유
- 모델 예측 불확실성

이 방향은 심박수 기반 논문보다 더 일반적이고 시스템적인 기여가 될 수 있다.

---

## 4.3 mode를 window 크기만으로 정의하지 말고 tuple로 정의

현재 연구에서는 다음과 같은 window 후보가 있다.

- W512
- W1024
- W2048

하지만 mode를 window 하나로만 정의하면 model architecture와 period를 충분히 표현하기 어렵다.

모드를 다음처럼 정의하는 편이 좋다.

\[
m_k=(W_k,M_k,T_k,D_k)
\]

여기서:

- \(W_k\): input window size
- \(M_k\): model 또는 exit
- \(T_k\): task period
- \(D_k\): relative deadline

추가로 sampling rate와 preprocessing도 포함할 수 있다.

\[
m_k=(W_k,M_k,f_{s,k},T_k,D_k)
\]

이렇게 하면 runtime mode selection이 진짜 real-time system problem이 된다.

---

## 4.4 초기 baseline은 독립 모델 방식이 더 적절함

심박수 논문의 Anytime 구조를 바로 따라가기보다 먼저 독립 모델을 baseline으로 구축하는 것이 좋다.

```text
Mode 1: W512 전용 모델
Mode 2: W1024 전용 모델
Mode 3: W2048 전용 모델
```

이유는 다음과 같다.

- 각 window에 맞춰 독립 최적화 가능
- 정확도 비교가 명확함
- mode별 timing profile을 분리하기 쉬움
- 모드별 memory를 분리 측정 가능
- RTCSA 2021 논문의 dedicated-model 우위 주장과 비교 가능
- 향후 Anytime 모델의 정확도 손실을 정량화 가능

---

## 4.5 독립 모델과 Anytime 모델의 직접 비교는 후속 ablation 후보

내 연구에서는 다음 세 구조를 비교할 수 있다.

### A. Independent models

```text
W512 model
W1024 model
W2048 model
```

### B. Fully shared Anytime model

```text
Shared Backbone
  ├─ Early Exit
  ├─ Middle Exit
  └─ Deep Exit
```

### C. Partially shared multi-branch model

```text
Shared Stem
  ├─ Fast branch
  ├─ Balanced branch
  └─ Accurate branch
```

비교 항목은 다음과 같다.

| 지표 | 목적 |
|---|---|
| Accuracy/F1 | 진단 성능 |
| Average latency | 일반 성능 |
| p99/p99.9 | tail latency |
| p99/관측 max 또는 formal WCET | timing feasibility. 측정 상한과 formal WCET는 구분 |
| Peak RAM | 실제 runtime memory |
| Flash/storage | 저장 크기 |
| Mode transition time | 전환 비용 |
| Energy | 배터리 또는 전력 |
| Deadline miss | 실시간성 |
| Scheduler overhead | 정책 비용 |

이 비교는 심박수 논문이 충분히 하지 못한 부분을 보완할 수 있다. 다만 현재 핵심은 `(W,H,M)` feasibility-first 정책이므로, 구조 비교가 정책 검증을 지연시키면 후속 실험으로 둔다.

---

# 5. 내 기존 STM32 결과와의 연결

현재 확보된 결과는 다음과 같다.

| 설정 | 추론시간 |
|---|---:|
| W2048 + CMSIS-NN | 약 460.3 ms |
| W1024 + CMSIS-NN | 약 129.8 ms |
| W512 + CMSIS-NN | 약 40.3 ms |

W512는 64 ms deadline을 만족했고 정확도는 약 99.3%였다.

이 결과는 이미 다음 trade-off를 보여준다.

\[
W\downarrow
\Rightarrow
C_{\mathrm{infer}}\downarrow
\]

하지만 앞으로는 다음도 함께 분석해야 한다.

\[
W\downarrow
\Rightarrow
\text{temporal context}\downarrow
\]

\[
T(W)\downarrow
\Rightarrow
\text{job arrival rate}\uparrow
\]

즉, window를 줄이면 한 번의 inference는 빨라지지만 더 자주 inference를 실행해야 할 수 있다.

전체 utilization은 다음처럼 봐야 한다.

\[
U(W)=\frac{C(W)}{T(W)}
\]

따라서 단순히 \(C(W)\)가 감소한다고 schedulability가 반드시 개선되는 것은 아니다.

이 점이 내 후속 연구의 중요한 출발점이다.

---

# 6. 제안하는 문제 정의

## 6.1 기본 문제

시점 \(i\)에서 실행 가능한 mode 집합을 다음과 같이 둔다.

\[
\mathcal{M}
=
\{m_1,m_2,\ldots,m_K\}
\]

각 mode는 다음 tuple이다.

\[
m_k=(W_k,M_k,T_k,D_k)
\]

목표는 deadline을 만족하면서 진단 utility를 최대화하는 것이다.

\[
m_i^*
=
\arg\max_{m\in\mathcal M}
Q(m,z_i)
\]

subject to

\[
C_{\mathrm{e2e}}(m,z_i)
\leq
D(m,z_i)
\]

그리고 전체 task set이 schedulable해야 한다.

\[
U_{\mathrm{other}}
+
U_{\mathrm{diag}}(m_i)
\leq 1
\]

---

## 6.2 slack-aware 선택

현재 slack을 \(S_i\)라 하면 안전한 mode는 다음을 만족해야 한다.

\[
C_{\mathrm{remain}}(m_i)
+
C_{\mathrm{switch}}(m_{i-1},m_i)
\leq
S_i
\]

이때 가능한 mode 중 가장 높은 진단 품질을 선택한다.

\[
m_i^*
=
\arg\max_m Q(m,z_i)
\]

subject to

\[
C_m+C_{\mathrm{switch}}\leq S_i
\]

---

## 6.3 uncertainty-aware escalation

가벼운 모델의 confidence가 충분하면 종료하고, 불확실하면 slack이 허용하는 범위에서 더 강한 mode로 escalation할 수 있다.

```text
Fast mode inference
↓
confidence 충분
 └─ 결과 확정

confidence 부족
↓
slack 확인
├─ 충분 → deeper/larger mode
└─ 부족 → fast 결과 사용 또는 safe fallback
```

다만 재실행을 허용하려면 다음을 보장해야 한다.

\[
C_{\mathrm{fast}}
+
C_{\mathrm{escalation}}
\leq D
\]

따라서 단순 재실행보다 shared prefix를 재사용하는 cascade가 유리할 수 있다.

---

# 7. 제안하는 시스템 모델

전체 workload를 다음처럼 구성할 수 있다.

\[
\Gamma
=
\{\tau_{\mathrm{acq}},
\tau_{\mathrm{prep}},
\tau_{\mathrm{diag}},
\tau_{\mathrm{comm}},
\tau_{\mathrm{log}},
\tau_1,\ldots,\tau_n\}
\]

진단 태스크의 mode별 end-to-end 실행시간은 다음과 같다.

\[
C_{\mathrm{diag}}^{(m)}
=
C_{\mathrm{window}}^{(m)}
+
C_{\mathrm{feature}}^{(m)}
+
C_{\mathrm{infer}}^{(m)}
+
C_{\mathrm{decision}}^{(m)}
+
C_{\mathrm{transition}}^{(m)}
\]

EDF라면 기본 utilization 분석은 다음과 같이 시작할 수 있다.

\[
\sum_{\tau_j\neq\tau_{\mathrm{diag}}}
\frac{C_j}{T_j}
+
\frac{C_{\mathrm{diag}}^{(m)}}{T_{\mathrm{diag}}^{(m)}}
\leq1
\]

하지만 mode transition과 transient overload까지 고려하려면 demand bound function 또는 mode-change analysis가 필요할 수 있다.

---

# 8. Raspberry Pi Zero 2 W에서의 실험 방향

## 8.1 플랫폼

- Raspberry Pi Zero 2 W
- Linux baseline
- PREEMPT_RT
- CPU frequency 고정
- thermal condition 통제
- 불필요 daemon 최소화

## 8.2 모델 구성

- W512 전용 모델
- W1024 전용 모델
- W2048 전용 모델
- optional: shared early-exit model

## 8.3 workload

- Fault diagnosis task
- Sensor acquisition 또는 stream replay
- Communication task
- Logging task
- Synthetic background CPU workload
- Optional I/O interference

## 8.4 상태 변수

- RPM
- load
- fault severity
- system slack
- background utilization

## 8.5 측정 지표

- Accuracy/F1
- 평균 latency
- maximum latency
- p99/p99.9 latency
- jitter
- peak RAM
- model storage
- mode switching overhead
- deadline miss ratio
- CPU utilization
- energy 또는 power
- policy overhead

---

# 9. 필수 ablation

## 9.1 상태 입력 ablation

| 정책 | 입력 |
|---|---|
| Fixed | 고정 mode |
| Condition-only | RPM/load |
| Slack-only | system slack |
| Condition + Slack | RPM/load + slack |
| Condition + Slack + Uncertainty | 전체 |

## 9.2 모델 구조 ablation

| 구조 | 설명 |
|---|---|
| Independent | 모드별 독립 모델 |
| Anytime | 완전 공유 early-exit |
| Partial Share | stem 공유 + branch 분리 |

## 9.3 timing ablation

- Average-based selection
- p99-based selection
- p99/관측 max 기반 selection. formal WCET가 확보된 경우에만 WCET 기반으로 표현

## 9.4 transition ablation

- 모델 세 개 모두 RAM 상주
- 하나만 상주하고 load
- parameter-shared model
- hysteresis 적용/미적용

---

# 10. 논문 포지셔닝

## 10.1 심박수 논문과의 차별점

심박수 논문:

- physiological condition만 사용
- fixed threshold
- 평균 inference 중심
- 독립 모델 대 Anytime 직접 비교 부족
- peak RAM 측정 부족
- 단순 EDF utilization test

내 연구:

- machine condition + system slack 결합
- window/model/period를 하나의 mode로 정의
- 실제 multi-task 환경
- tail latency 및 보수적 관측 max 기반 선택. formal WCET가 확보된 경우에만 WCET로 표현
- 독립 모델과 Anytime 구조 직접 비교
- peak RAM 및 transition overhead 측정
- Linux와 PREEMPT_RT 비교
- end-to-end pipeline 포함

## 10.2 예상 핵심 기여 문장

> We present a machine-condition- and slack-aware runtime mode selection framework for real-time vibration fault diagnosis on resource-constrained edge devices. Unlike prior condition-only approaches, the proposed system jointly selects the input window, inference model, and diagnosis period while accounting for end-to-end execution time and concurrent system workload.

한국어:

> 본 연구는 자원 제약 엣지 장치에서 실시간 진동 고장진단을 수행하기 위해 기계 운전 상태와 시스템 slack을 동시에 고려하는 런타임 mode selection 프레임워크를 제안한다. 기존의 상태 단독 기반 접근과 달리 입력 윈도우, 추론 모델, 진단 주기를 하나의 mode로 통합하고, end-to-end 실행시간과 동시 태스크 부하를 함께 고려한다.

---

# 11. 당장 수행할 다음 단계

## Step 1. 독립 모델 profile 구축

각 mode에 대해 다음 값을 수집한다.

```text
mode_id
window_size
model_size
accuracy
average_latency
p99_latency
max_latency
peak_ram
period
deadline
```

## Step 2. 동일 입력에서 구조 비교. 후속 ablation

- Independent W512/W1024/W2048
- Shared early-exit
- 가능하면 partial-sharing

## Step 3. background load 실험

CPU utilization을 단계적으로 증가시킨다.

```text
0%
20%
40%
60%
80%
```

각 조건에서 다음을 측정한다.

- deadline miss
- tail latency
- 선택된 mode 비율
- accuracy

## Step 4. fixed policy와 adaptive policy 비교

```text
Always W512
Always W1024
Always W2048
Condition-only
Slack-only
Condition + Slack
```

## Step 5. 실제 schedulability 모델과 실험 결과 연결

이론상 schedulable인 영역과 실제 deadline miss가 발생하지 않는 영역을 비교한다.

---

# 12. 최종 판단

심박수 기반 AMS 논문은 내 연구에 매우 유용한 선행연구다. 특히 다음 세 요소를 직접 활용할 수 있다.

1. 상태 의존적 deadline
2. runtime model selection
3. 실시간 schedulability formulation

그러나 Anytime 구조 자체를 그대로 채택할 필요는 없다.

오히려 내 연구에서는 다음 순서가 더 타당하다.

```text
1. 독립 모델 기반 mode pool 구축
2. 각 mode의 accuracy-latency-memory profile 확보
3. condition + slack 기반 선택 정책 구현
4. 독립 모델과 Anytime 모델 직접 비교
5. 실제 multi-task 및 PREEMPT_RT 환경에서 검증
```

부차적 구조 선택 질문은 다음과 같이 정리할 수 있다.

> 메모리 절약을 위해 parameter sharing을 사용하는 것이 실제로 이득인가, 아니면 각 window와 계산 예산에 맞춘 독립 모델을 상주시켜 선택하는 것이 더 높은 accuracy–timeliness 효율을 제공하는가?

현재 핵심 연구 질문은 다음이다.

> 변화하는 기계 상태와 시스템 slack 아래에서, 어떤 window–model–period mode를 선택해야 진단 성능을 유지하면서 deadline miss를 최소화할 수 있는가?

---

# 참고문헌

[1] Y. Li et al., “Adaptive Model Selection for Real-Time Heart Disease Detection on Embedded Systems,” IEEE RTCSA, 2025.

[2] Y. Hu et al., “On Exploring Image Resizing for Optimizing Criticality-based Machine Perception,” IEEE RTCSA, 2021.
