# 주제 구체화 - Codex v1

> 문서 버전: Codex v1<br>
> 작성일: 2026-08-01<br>
> 문서 성격: 학위연구 주제 구체화 및 교수님 논의용 초안<br>
> 현재 근거 범위: 정독 완료 섹션 `elastic scheduling` 19편, `real-time fault diagnosis` 20편<br>
> 미반영 범위: `adaptive input`과 `real-time DNN serving`은 카드 수준의 예비 관찰만 참고하며, 정독 후 본문과 연구 gap을 다시 수정한다.

---

## 가제

### 국문

**제한 자원 Linux 엣지 플랫폼에서 기계 상태와 시스템 슬랙을 고려한 실시간 진동 결함 진단의 탄력적 모드 선택**

### English

**Machine- and Slack-Aware Elastic Mode Selection for Real-Time Vibration Fault Diagnosis on Resource-Constrained Linux Edge Platforms**

### 대안 제목

1. **진동 결함 진단을 위한 Feasibility-First Elastic Scheduling: 입력 윈도우와 진단 주기의 런타임 선택**
2. **Feasibility-First Runtime Selection of Window Size and Diagnosis Period for Vibration Fault Diagnosis**
3. **Deadline-Aware Elastic Diagnosis on Raspberry Pi Zero 2W with PREEMPT_RT**

현재는 첫 번째 가제를 기준으로 한다. `M`을 고정한 `(W,H)` 실험이 초기 범위이므로 제목에 `W/H/M joint adaptation`을 직접 넣지 않는다. PREEMPT_RT는 중요한 평가 환경이지만 방법론이 특정 kernel에 종속되지 않는다면 최종 제목에서는 제외할 수 있다.

## Keywords

`Real-Time Fault Diagnosis`, `Elastic Scheduling`, `Runtime Mode Selection`, `Vibration Analysis`, `System Slack`, `PREEMPT_RT`, `Edge Computing`, `Schedulability`

---

## 국문 요약 초안

제한된 연산 자원을 가진 엣지 디바이스에서 진동 기반 결함 진단을 수행하려면 진단 품질과 시간 예측 가능성을 함께 고려해야 한다. 기존 임베디드 결함 진단 연구는 주로 경량 모델, 양자화, pruning과 입력 압축을 통해 평균 추론시간을 줄이지만, explicit deadline, tail latency, deadline miss와 system-level scheduling을 함께 평가한 사례는 현재 검토 범위에서 제한적이었다. 반면 elastic scheduling 연구는 system load 변화에 따라 task period와 utilization을 조절하는 이론적 기반을 제공하지만, 대체로 execution time을 고정하거나 사전에 정한 mode별 bound를 사용하며 vibration window의 진단적 의미와 machine condition을 다루지 않는다.

본 연구는 진동 결함 진단 mode를 입력 window size `W`, hop size 또는 diagnosis period `H`, model configuration `M`의 tuple로 표현하고, machine condition `q`와 system slack `S`를 함께 사용하는 feasibility-first runtime mode-selection policy를 연구한다. 첫 구현에서는 `M`을 고정하고 discrete `(W,H)` mode bank를 구성한다. 각 mode의 execution-time distribution과 diagnostic utility를 offline에서 profile한 뒤, runtime에는 deadline과 utilization 조건을 만족하는 feasible mode만 남기고 현재 기계 상태에 가장 유용한 mode를 선택한다. 구현과 평가는 Raspberry Pi Zero 2W의 일반 Linux와 PREEMPT_RT에서 수행하며, 부하 조건별 response time, jitter, p99/max latency, deadline miss와 diagnosis utility를 측정한다. 초기 단계의 목표는 hard real-time을 주장하는 것이 아니라 empirical deadline feasibility를 명확히 검증하고, 보수적 execution bound와 transition analysis가 확보될 경우에만 formal guarantee 범위를 확장하는 것이다.

## English Abstract Draft

Vibration-based fault diagnosis on resource-constrained edge devices requires both diagnostic utility and predictable timing behavior. The embedded fault-diagnosis studies reviewed so far primarily reduce average inference time through lightweight models, quantization, pruning, or input compression, while explicit deadlines, tail latency, deadline misses, and system-level scheduling are addressed only to a limited extent. Elastic scheduling provides a foundation for adapting task periods and utilization under changing system load, but commonly assumes fixed execution costs or offline-bounded mode costs and does not capture the diagnostic meaning of vibration windows or machine-condition-driven adaptation.

This study investigates a feasibility-first runtime mode-selection policy for vibration fault diagnosis. A diagnosis mode is represented by window size `W`, hop size or diagnosis period `H`, and model configuration `M`. The runtime uses both machine condition `q` and system slack `S`; however, the initial implementation fixes `M` and evaluates a discrete `(W,H)` mode bank. Mode-dependent execution-time distributions and diagnostic utility are profiled offline. At runtime, infeasible modes are filtered using deadline and utilization constraints, and the most useful feasible mode is selected for the current machine condition. The system is implemented on a Raspberry Pi Zero 2W and evaluated under vanilla Linux and PREEMPT_RT using response time, jitter, tail latency, deadline misses, and diagnostic utility. The initial target is empirical deadline feasibility rather than an unsupported hard real-time guarantee.

---

## 1. Background

### 1.1 연구 배경

진동 기반 fault diagnosis는 일정 길이의 신호 window를 수집한 뒤 feature extraction 또는 neural inference를 수행한다. 이때 `W`는 연산량만 결정하는 parameter가 아니다. Window가 포함하는 회전 주기, fault characteristic component와 transient information이 달라지므로 diagnosis quality에도 영향을 준다. `H`는 consecutive window 사이의 hop size이며 sampling frequency `f_s`가 고정되면 diagnosis task의 arrival period를 결정한다.

```text
T_a = H_a / f_s
```

큰 `W`와 복잡한 model은 더 많은 진단 정보를 제공할 가능성이 있지만 execution cost와 memory demand를 증가시킨다. 반대로 작은 `W`와 긴 `H`는 system load를 낮출 수 있지만 fault evidence가 부족해지거나 diagnosis update가 늦어질 수 있다. 따라서 설정 선택은 단순한 latency minimization이 아니라 diagnostic utility와 timing feasibility의 공동 문제다.

### 1.2 선행연구에서 확보한 출발점

STM32F407과 Zephyr RTOS를 사용한 KCC 2026 선행 결과에서는 동일한 fault-diagnosis model에서도 `W`에 따라 execution cost가 크게 달라졌다. Non-overlapping window와 `f_s=8 kHz`를 가정한 max-latency 기반 utilization은 다음과 같다.

| `W` | `C_max` | `T=W/f_s` | `U=C/T` |
| ---: | ---: | ---: | ---: |
| 512 | 40.3 ms | 64 ms | 0.63 |
| 1024 | 129.8 ms | 128 ms | 1.01 |
| 2048 | 460.3 ms | 256 ms | 1.80 |

이 결과는 특정 MCU와 model implementation에서 얻은 motivation이며 Pi Zero 2W의 비용으로 직접 사용할 수 없다. 다만 mode에 따라 `C`가 달라지고 정밀 mode가 자동으로 feasible하지 않다는 문제를 보여준다. Pi Zero 2W에서는 runtime, kernel과 interference가 다르므로 모든 mode를 다시 profile해야 한다.

### 1.3 Real-Time Fault Diagnosis 서베이에서 확인한 점

현재 20편의 direct 또는 adjacent real-time fault-diagnosis 문헌을 동일 기준으로 비교했다. 현재 표의 예비 판정에서는 외부 문헌 20편이 모두 `B`, 즉 average latency, throughput 또는 acquisition interval 대비 처리시간 중심의 best-effort 범주에 놓였다. 다수 연구는 architecture search, quantization, pruning, compressed sensing 또는 lightweight network를 사용해 deployment cost를 줄였다 [7]--[12]. 일부 연구는 period 또는 allowable latency를 제시하지만 이를 explicit deadline으로 정의하고 tail/miss와 schedulability를 함께 분석하지 않았다.

이 관찰은 다음과 같이 제한해서 사용한다.

- `real-time`이라는 표현과 real-time guarantee를 구분한다.
- RTOS 사용이나 짧은 average latency만으로 hard real-time을 판정하지 않는다.
- 현재 검색식과 확보 문헌 안에서의 관찰이며 전체 분야의 부재 증명이 아니다.
- 현재 연구의 직접 비교축은 model 경량화 여부보다 deadline 정의, tail/miss 측정, scheduling과 runtime adaptation 여부다.

### 1.4 Elastic Scheduling 서베이에서 확인한 점

Classic elastic task model은 periodic task의 period를 elastic variable로 두고 overload나 rate-change request가 발생하면 utilization bound 안에서 period를 재분배한다 [1], [2]. 이 계열은 `H`를 elastic variable로 해석할 수 있는 이론적 기반을 제공한다. 그러나 주된 가정은 fixed execution cost `C_i`다. Runtime execution-time estimate를 feedback으로 사용하는 연구도 있지만 transient 또는 sporadic deadline miss를 허용하는 soft real-time 접근이다 [3].

최근 practical extension은 reservation bandwidth [4], mode별 controller와 resource allocation [5], runtime sensor rate regulation [6]을 다룬다. 특히 offline에서 feasible mode와 transition을 검증한 뒤 runtime event에 따라 mode를 적용하는 Decntr 구조는 본 연구와 가깝다 [5]. 그러나 이 계열의 application utility는 control safety 또는 QoC이며 vibration window의 signal semantics, machine condition과 fault-diagnosis utility는 포함하지 않는다.

### 1.5 현재 연구 gap

현재 정독한 두 섹션을 기준으로 확인된 분리는 다음과 같다.

```text
Real-Time Fault Diagnosis
  model/input optimization과 fixed deployment는 존재
  explicit deadline + tail/miss + schedulability + runtime mode selection은 제한적

Elastic Scheduling
  period/resource adaptation과 feasibility analysis는 존재
  vibration-specific W, machine condition q, diagnostic utility는 없음
```

따라서 현재 연구 질문은 “elastic scheduling을 fault diagnosis에 적용한다”에서 끝나지 않는다. 핵심은 mode-dependent cost `C(W,M)`와 vibration-specific utility를 정의하고, machine condition이 요구하는 fidelity를 system feasibility 안에서 선택하는 것이다. 다만 adaptive input과 RT-DNN 문헌 정독 전에는 이 결합의 novelty를 확정하지 않는다.

### 1.6 연구 범위

**포함 범위**

- Raspberry Pi Zero 2W와 Linux/PREEMPT_RT
- vibration fault diagnosis inference pipeline
- initial discrete `(W,H)` mode bank와 fixed `M`
- machine condition과 system slack 기반 runtime selection
- empirical tail latency, deadline miss와 diagnostic utility 평가

**현재 제외 범위**

- MCU + RTOS 추가 실험. 기존 KCC 결과는 motivation으로만 사용
- 새로운 neural network architecture 제안
- OTTA 또는 online training과 inference의 동시 scheduling
- application-level 근거 없이 weakly-hard `(m,K)` constraint를 도입하는 것
- PREEMPT_RT 실험만으로 hard real-time guarantee를 주장하는 것
- 초기 단계에서 여러 model을 동시에 관리하는 full `W/H/M` adaptation

---

## 2. Research Questions and Hypotheses

### RQ1. Application semantics

진동 결함 진단에서 `W`와 `H`는 diagnostic utility와 diagnosis delay에 각각 어떤 영향을 주는가?

### RQ2. Mode feasibility

Mode-dependent execution cost `C(W,M)`와 interference를 고려할 때 각 `(W,H)` mode의 deadline feasibility를 어떻게 판정할 것인가?

### RQ3. Runtime policy

Machine condition `q`와 system slack `S`를 함께 사용한 feasibility-first policy가 static mode, condition-only policy와 slack-only policy보다 diagnostic utility와 deadline behavior의 균형을 개선하는가?

### RQ4. Runtime platform

일반 Linux와 PREEMPT_RT에서 kernel과 interference 조건이 mode별 tail response time, feasible mode set과 policy decision에 어떤 차이를 만드는가?

### 검증 가설

- **H1**: 동일 model에서도 `W`와 platform/load condition에 따라 execution-time distribution이 달라지므로 mode별 profiling이 필요하다.
- **H2**: `W`만 줄이는 것과 `H`를 함께 줄이는 것은 utilization에 다른 결과를 만들며, 단일 변수 선택보다 tuple 기반 선택이 필요하다.
- **H3**: Condition-only policy는 low-slack 상태에서 infeasible high-fidelity mode를 선택할 수 있고, feasibility filtering은 이러한 선택을 줄인다.
- **H4**: Static-light mode보다 condition-aware feasible selection이 suspicious/fault condition에서 더 높은 diagnostic utility를 제공할 가능성이 있다.
- **H5**: PREEMPT_RT의 효과는 mean inference time보다 interference 아래 tail response time과 deadline miss에서 더 분명하게 나타날 가능성이 있다.

H1--H5는 검증할 가설이며 현재 결과로 쓰지 않는다.

---

## 3. Methodology

### 3.1 Diagnosis task model

Sampling frequency `f_s`의 vibration stream에서 runtime이 선택하는 mode를 다음과 같이 정의한다.

```text
a = (W_a, H_a, M_a)
T_a = H_a / f_s
```

- `W_a`: input window size in samples
- `H_a`: consecutive windows 사이의 hop size in samples
- `T_a`: diagnosis task arrival period
- `M_a`: model 또는 inference configuration

첫 구현에서는 `M_a=M_0`로 고정하고 다음 mode bank를 사용한다.

```text
A_0 = { (W_a, H_a, M_0) }
```

현재 확보한 model input을 고려하면 `W` 후보는 512, 1024, 2048에서 시작할 수 있다. `H` 후보는 non-overlap과 overlap 조건을 포함하되, exact set은 diagnosis utility와 acquisition semantics를 확인한 뒤 확정한다. 단순히 가능한 조합을 모두 넣지 않고 physical admissibility와 memory constraint를 통과한 mode만 포함한다.

### 3.2 Offline mode-bank construction

각 mode에 대해 다음 profile을 만든다.

```text
P_a = {
  C_mean, C_p95, C_p99, C_max,
  R_mean, R_p95, R_p99, R_max,
  memory,
  diagnostic utility by condition
}
```

Mode bank 생성 절차는 다음과 같다.

1. Signal semantics를 기준으로 허용 가능한 `W/H` 후보를 정한다.
2. Kernel과 load condition별 execution/response-time distribution을 측정한다.
3. Deadline과 utilization 조건을 만족하지 못하는 mode를 표시한다.
4. Machine condition별 accuracy, F1, confidence calibration 또는 detection-delay 관련 utility를 평가한다.
5. Runtime이 사용할 compact lookup table을 생성한다.

### 3.3 Timing feasibility

Mode `a`의 diagnosis utilization은 다음과 같다.

```text
U_a = C_a / T_a
U_total(a) = U_bg + U_a
```

Observed response time은 execution cost 외에 interference와 OS/runtime delay를 포함한다.

```text
R_a = C_a + I_a + L_os
```

초기 empirical feasibility set은 다음과 같이 정의한다.

```text
A_feasible(k) = {
  a in A_0 |
  U_bg(k) + C_a,tail / T_a <= U_bound
  and R_a,tail <= D_a
}
```

`tail`은 p99 또는 observed max 후보이며 실험 결과에 따라 하나를 선택한다. Linux/PREEMPT_RT에서 관찰한 p99 또는 max는 formal WCET가 아니다. 따라서 초기 결과는 `empirical deadline feasibility`로 표현한다. Hard guarantee를 주장하려면 conservative execution bound, interference model, scheduler assumption과 mode-transition demand를 별도로 증명해야 한다.

### 3.4 Machine condition and utility

Runtime machine condition은 다음 기호로 둔다.

```text
q_k = machine-condition indicator at step k
```

후보는 anomaly score, calibrated fault probability, health index와 model confidence다. 이 값들은 서로 같은 의미가 아니므로 첫 구현 전에 하나를 확정한다. 특히 confidence를 machine degradation으로 직접 해석하려면 calibration과 false-negative behavior를 검증해야 한다.

Mode utility는 다음과 같이 둔다.

```text
Q(a, q_k)
```

`Q`는 단순 classification accuracy 하나로 고정하지 않는다. Normal, suspicious와 fault condition에서 필요한 context와 update rate가 다를 수 있으므로 accuracy/F1, detection delay, result age와 update frequency를 포함할 수 있다. 최종 utility 구성은 adaptive-input 정독과 dataset 실험 후 확정한다.

### 3.5 System slack

Mean latency 기반 slack은 tail behavior를 숨길 수 있으므로 최근 response-time history에서 계산한다.

```text
S_k,p99 = D - p99(R_recent)
S_k,max = D - max(R_recent)
```

`S`는 policy trigger이고 `A_feasible`은 safety filter다. Slack threshold만으로 mode를 선택하는 heuristic과 feasibility test를 구분한다.

### 3.6 Feasibility-first policy

정책은 다음 두 단계를 따른다.

```text
1. Timing constraint를 위반하는 mode를 제거한다.
2. 남은 mode 중 현재 q에서 utility가 가장 높은 mode를 선택한다.

a*_k = argmax Q(a, q_k),  a in A_feasible(k)
```

`A_feasible(k)`가 비어 있으면 사전 정의된 fallback mode를 사용하거나 overload를 보고한다. Deadline miss를 감지한 뒤 lighter model을 다시 실행하는 방식은 이미 소비한 비용까지 예약하지 않으면 timing guarantee가 아니다. 초기 구현은 miss 후 재실행보다 사전 profile에 기반한 admission을 우선한다.

### 3.7 Transition control

Mode endpoint가 각각 feasible하더라도 transition이 자동으로 feasible한 것은 아니다. 다음 요소를 측정하거나 bound해야 한다.

- window buffer 재구성 비용
- mode lookup과 policy decision overhead
- unfinished/carry-over inference 처리
- model 변경 시 loading 또는 cache warm-up 비용
- transition 직후 activation jitter

초기 `(W,H)` implementation에서는 model loading을 제거할 수 있다. Minimum residence time과 hysteresis를 사용해 oscillation을 제한하고, transition cost를 response-time measurement에 포함한다.

---

## 4. Experiment

### 4.1 Evaluation stages

실험은 KSC용 platform characterization과 학위연구 mode-selection evaluation을 구분한다.

| 단계 | 목적 | 핵심 산출물 |
| --- | --- | --- |
| E0. Kernel validation | PREEMPT_RT 적용과 kernel scheduling latency 확인 | cyclictest p99/p999/max |
| E1. Fixed-mode pipeline | Vanilla와 PREEMPT_RT의 fixed `W=512` timing 비교 | response-time distribution, miss |
| E2. Mode profiling | `(W,H,M_0)`별 execution cost와 utility profile 구축 | mode profile table |
| E3. Static feasibility | 각 mode endpoint의 empirical feasibility 판정 | feasible-mode map |
| E4. Runtime policy | static/condition/slack/joint policy 비교 | utility-timing trade-off |
| E5. Transition evaluation | mode switch overhead와 transient behavior 측정 | transition matrix/overhead |

E0과 E1은 KSC 2026 단기 트랙의 중심이며 E2--E5를 위한 platform evidence를 제공한다. 장기 contribution은 E2--E5에서 검증한다.

### 4.2 Platform and workload

| 항목 | 설정 |
| --- | --- |
| Board | Raspberry Pi Zero 2W, Cortex-A53 quad-core, 512 MB RAM |
| OS | Raspberry Pi OS Lite 64-bit |
| Kernel | vanilla Linux, PREEMPT_RT |
| Runtime | TFLite/LiteRT, XNNPACK 또는 실제 사용 backend 기록 |
| Initial model | FRFconv-TDSNet INT8 |
| Dataset | UOS shaft-fault dataset, 8 kHz condition부터 시작 |
| Load | idle, CPU, memory, I/O, combined |
| Repetition | 조건당 최소 3회, tail 안정성에 따라 확대 |

실제 kernel version, runtime version, thread 수, affinity, priority, governor와 thermal condition을 모두 기록한다.

### 4.3 Experimental factors

```text
Kernel      = {vanilla, PREEMPT_RT}
Load        = {idle, cpu, memory, io, combined}
Mode        = candidate (W,H,M0) set
Policy      = {Static-Light, Static-Heavy, Condition-Only,
               Slack-Only, Proposed-q+S}
Condition   = {normal, suspicious, fault} or dataset-supported equivalent
```

`suspicious` condition이 dataset과 detector에서 독립적으로 정의되지 않으면 임의로 만들지 않는다. 이 경우 normal/fault 또는 score quantile 기반 sensitivity analysis로 범위를 제한하고 그 사실을 명시한다.

### 4.4 Baselines

- **Static-Light**: 항상 가장 낮은 cost mode 사용
- **Static-Heavy**: 항상 가장 높은 fidelity mode 사용
- **Condition-Only**: machine condition만으로 mode 선택
- **Slack-Only**: system slack만으로 mode 선택
- **Proposed-q+S**: feasibility filtering 후 condition-dependent utility 최대화
- **Offline Oracle**: 각 condition/run을 사후에 알고 선택하는 upper-bound 참고선. 실제 runtime baseline으로 해석하지 않는다.

### 4.5 Metrics

**Timing metrics**

- activation jitter
- inference latency와 end-to-end response time
- p50, p95, p99, p999와 max
- deadline miss ratio
- consecutive miss와 maximum update gap
- mode-switch overhead와 transition jitter

**Diagnostic metrics**

- accuracy, macro F1과 class-wise recall
- false negative 또는 missed-fault behavior
- detection delay 또는 time-to-detection, 정의 가능한 경우
- condition별 mode utility
- result age와 effective diagnosis update rate

**System metrics**

- CPU utilization과 per-core load
- memory usage
- temperature와 throttling
- I/O activity
- policy decision overhead와 switch frequency

### 4.6 Analysis

1. Kernel/load/mode별 latency distribution과 CDF를 비교한다.
2. Mean 차이와 tail 차이를 분리한다.
3. Mode별 `C/T`, p99/max feasibility와 deadline miss를 표로 만든다.
4. Policy별 diagnostic utility, deadline miss와 update gap을 함께 비교한다.
5. 반복 run과 seed/run order를 block으로 취급하고 confidence interval을 제시한다.
6. R1에서 관찰된 extreme outlier는 원인을 확정하지 않고 R2/R3 재현 여부와 logging boundary를 먼저 확인한다.

현재 E1 R1에서는 vanilla Linux의 I/O load 조건에서 큰 latency outlier와 deadline miss 1회가 관찰되었다. 이는 preliminary observation이며, PREEMPT_RT의 인과적 효과나 정확한 I/O blocking mechanism을 주장하려면 반복 실험과 tracing이 필요하다.

### 4.7 Success criteria

최소 성공 조건은 다음과 같다.

- Mode별 execution/response-time distribution이 재현 가능하게 측정된다.
- `W`와 `H` 조합에 따라 feasible/infeasible region이 구분된다.
- Proposed policy가 condition-only 대비 deadline behavior를 악화시키지 않으면서 static-light보다 condition-dependent utility를 개선한다.
- Kernel 효과를 mean뿐 아니라 p99/max와 miss로 설명할 수 있다.
- Transition overhead를 무시하지 않고 전체 response time에 포함한다.

위 조건이 충족되지 않으면 `q+S` policy의 복잡성을 늘리기보다 mode bank, deadline과 utility 정의를 먼저 수정한다.

---

## 5. Expected Contributions

아래는 검증 전 contribution candidate다.

1. **Mode-dependent diagnosis task model**<br>
   Fixed `C`와 variable `T` 중심의 elastic task model을 vibration diagnosis mode별 `C(W,M)`와 `T=H/f_s` 구조로 확장한다.

2. **Feasibility-first machine- and slack-aware policy**<br>
   Machine condition은 desired fidelity를 결정하고 system slack은 feasible mode를 제한하도록 역할을 분리한다.

3. **Application-aware mode bank**<br>
   Window를 단순 input-size knob으로 보지 않고 signal semantics와 diagnostic utility를 반영한 discrete mode로 구성한다.

4. **Linux/PREEMPT_RT empirical evaluation**<br>
   Pi Zero 2W에서 kernel과 interference가 mode별 tail response time, feasible set과 runtime policy에 미치는 영향을 평가한다.

5. **Evidence-based separation of real-time claims**<br>
   Embedded fault diagnosis의 model-level best-effort와 deadline/tail/scheduling evidence를 분리하여 제안 방법의 보장 범위를 명확히 한다.

Contribution 1은 fixed `C`를 dynamic measured feedback으로 바꾸는 것만으로는 부족하다. 기존 연구에도 runtime execution-time feedback과 allocation-dependent offline WCET table이 존재한다 [3]--[5]. 차별성은 vibration mode semantics, application utility, feasibility filtering과 transition을 함께 검증할 때 성립한다.

---

## 6. Limitations and Claim Boundaries

- 현재 literature gap은 77개 paper card와 정독 완료한 두 섹션의 범위에서 도출했다.
- Adaptive input과 RT-DNN 정독 결과에 따라 novelty와 baseline 구성이 바뀔 수 있다.
- Measured p99/max는 WCET가 아니므로 초기 연구를 hard real-time system으로 부르지 않는다.
- 현재 연구는 weakly-hard real-time을 target으로 하지 않는다.
- Initial `M`은 fixed다. 따라서 초기 결과를 full joint `W/H/M` adaptation으로 표현하지 않는다.
- KCC의 STM32 latency와 Pi Zero 2W latency를 직접 비교하지 않는다.
- R1 outlier 하나로 PREEMPT_RT의 일반적 우위를 확정하지 않는다.
- Diagnostic utility와 machine condition indicator의 정의가 불충분하면 policy contribution도 약해진다.

---

## 7. Survey and Research To-Do

### 7.1 Adaptive Input and Diagnostic Fidelity

- [ ] `02_input_adaptive` 8편을 원문 기준으로 재검토한다.
- [ ] 각 논문의 input/window 선택이 offline design인지 runtime adaptation인지 재판정한다.
- [ ] `W`를 결정하는 physics rule, anomaly deviation, speed와 fault frequency 근거를 비교한다.
- [ ] `W_min`, operating-condition-dependent admissibility와 utility 정의에 사용할 수 있는 근거를 추린다.
- [ ] Vision image resizing의 spatial input과 vibration temporal window를 동일시하지 않고 차이를 정리한다.
- [ ] Machine condition이 실제 runtime trigger인 논문이 있는지 재검색한다.
- [ ] 결과를 `claim_bank`, `comparison_table`, 본 문서 1.3--1.5와 3.4에 반영한다.

### 7.2 Real-Time DNN Serving and Mode Selection

- [ ] `03_rt_dnn_serving` 13편을 원문 기준으로 재검토한다.
- [ ] DNN-SAM의 slack reclaim과 input-scale selection 조건을 확인한다.
- [ ] SCENIC의 capability function, offline co-design과 runtime limitation을 확인한다.
- [ ] Deadline-aware model/exit/batch/offloading 연구의 feasibility guarantee 수준을 분리한다.
- [ ] Condition-aware selection과 slack-aware selection을 함께 사용하는 선행연구를 추가 검색한다.
- [ ] Model switch, early exit, batching과 local vibration `(W,H)` selection의 차이를 정리한다.
- [ ] 결과에 따라 `M`을 initial scope에 넣을지 후속 확장으로 유지할지 결정한다.
- [ ] 결과를 `claim_bank`, `table1_related_work`, 본 문서 RQ3와 contribution 2에 반영한다.

### 7.3 Real-Time Theory

- [ ] Imprecise computation, mode-change protocol과 carry-over job을 통합 정리한다.
- [ ] `D=T`와 `D<T` 중 initial diagnosis deadline model을 확정한다.
- [ ] Empirical admission과 formal schedulability claim의 경계를 정한다.
- [ ] Transition feasibility를 utilization test로 충분히 설명할 수 있는지 검토한다.
- [ ] Weakly-hard는 application-level allowable miss 근거가 생기기 전까지 related-work 비교축으로만 유지한다.

### 7.4 Experiment

- [ ] Fixed `W=512` kernel comparison의 R2/R3를 완료한다.
- [ ] Cyclictest R2/R3와 pipeline result를 동일 load condition으로 맞춘다.
- [ ] `W=512/1024/2048`의 Pi Zero 2W profile을 수집한다.
- [ ] `H` candidate와 deadline definition을 확정한다.
- [ ] Data loading, preprocessing, inference와 logging boundary를 분리 측정한다.
- [ ] Extreme outlier 발생 시 ftrace/perf 또는 적절한 tracing으로 원인을 확인한다.
- [ ] Machine-condition indicator `q`를 선택하고 calibration을 검증한다.
- [ ] Static/condition/slack/joint baseline을 구현한다.
- [ ] Mode transition overhead와 hysteresis를 측정한다.

### 7.5 Writing

- [ ] Adaptive input과 RT-DNN 정독 후 제목과 abstract를 v2로 수정한다.
- [ ] 확정된 RQ와 contribution만 `manuscript/draft.md`에 반영한다.
- [ ] KSC platform 결과와 학위논문 method 결과를 별도 section으로 유지한다.
- [ ] Quantitative claim은 R2/R3와 analysis 완료 후 작성한다.
- [ ] 본인 KCC 2026 선행논문의 정식 citation metadata를 추가한다.

---

## 8. Decision Gates

| Gate | 결정 질문 | 통과 조건 | 실패 시 조치 |
| --- | --- | --- | --- |
| G1. Utility | `W/H`에 따라 condition별 utility 차이가 있는가 | 재현 가능한 accuracy/F1/delay 차이 | `W` adaptation 축소, `H` 중심 재정의 |
| G2. Feasibility | Mode별 feasible region이 구분되는가 | load/kernel에 따라 p99/max 또는 miss 차이 | deadline/load/mode set 재설계 |
| G3. Joint trigger | `q+S`가 single-trigger baseline보다 유리한가 | utility와 timing 중 최소 한 축 개선, 다른 축 비열화 | policy 단순화 또는 trigger 재정의 |
| G4. Transition | Switch cost를 포함해도 이점이 남는가 | residence interval 안에서 overhead 상쇄 | mode 수 축소, hysteresis 강화 |
| G5. Claim level | Formal guarantee가 가능한가 | conservative bound와 schedulability/transition analysis 확보 | empirical deadline-aware claim으로 제한 |
| G6. Scope | `M`을 넣을 실익이 있는가 | distinct model이 Pareto frontier를 확장 | `M` fixed 유지, 후속 연구로 이동 |

---

## 9. Paper Structure Draft

1. **Introduction**
   - Fixed diagnosis configuration의 문제
   - RT-FD와 elastic scheduling 사이의 gap
   - 연구 질문과 contribution
2. **Background and Related Work**
   - Embedded real-time fault diagnosis
   - Adaptive diagnostic fidelity
   - Elastic scheduling and mode transition
   - Deadline-aware DNN inference
3. **System Model and Problem Formulation**
   - `(W,H,M)` mode, arrival period, deadline와 execution cost
   - Machine condition, system slack와 utility
   - Feasible mode set
4. **Feasibility-First Runtime Mode Selection**
   - Offline mode bank
   - Runtime policy, fallback와 hysteresis
   - Transition handling
5. **Implementation**
   - Pi Zero 2W, Linux/PREEMPT_RT와 inference pipeline
6. **Evaluation**
   - Mode profiling
   - Kernel/load characterization
   - Policy와 baseline 비교
   - Transition overhead와 ablation
7. **Discussion**
   - Guarantee boundary, generality와 limitations
8. **Conclusion**

---

## 참고문헌

[1] G. C. Buttazzo, G. Lipari, and L. Abeni, "Elastic Task Model for Adaptive Rate Control," *IEEE RTSS*, 1998.

[2] G. C. Buttazzo, G. Lipari, M. Caccamo, and L. Abeni, "Elastic Scheduling for Flexible Workload Management," *IEEE Transactions on Computers*, vol. 51, no. 3, 2002.

[3] G. Buttazzo and L. Abeni, "Adaptive Rate Control through Elastic Scheduling," *IEEE CDC*, 2000.

[4] S. M. Salman, S. Mubeen, F. Markovic, A. V. Papadopoulos, and T. Nolte, "Scheduling Elastic Applications in Compositional Real-Time Systems," *IEEE ETFA*, 2021, doi: 10.1109/ETFA45728.2021.9613375.

[5] R. Gifford, F. Galarza-Jimenez, L. T. X. Phan, and M. Zamani, "Decntr: Optimizing Safety and Schedulability with Multi-Mode Control and Resource Allocation Co-Design," *IEEE RTAS*, 2024, doi: 10.1109/RTAS61025.2024.00032.

[6] R. Li et al., "ATER: Adaptive Task Execution Rate Regulation for Enhanced Real-Time Performance in ROS 2," *IEEE RTCSA*, 2025, doi: 10.1109/RTCSA66114.2025.00019.

[7] S. Ma, H. Sun, S. Gao, and G. Zhou, "A Real-Time Mechanical Fault Diagnosis Approach Based on Lightweight Architecture Search Considering Industrial Edge Deployments," *Engineering Applications of Artificial Intelligence*, 2023.

[8] S. Lee and T. Kim, "FRFconv-TDSNet: Lightweight, Noise-Robust Convolutional Neural Network Leveraging Full-Receptive-Field Convolution and Time-Domain Statistics for Intelligent Machine Fault Diagnosis," *IEEE Transactions on Instrumentation and Measurement*, 2024.

[9] T. Jalonen, M. Al-Sa'd, S. Kiranyaz, and M. Gabbouj, "Real-Time Vibration-Based Bearing Fault Diagnosis Under Time-Varying Speed Conditions," *IEEE ICIT*, 2024, doi: 10.1109/ICIT58233.2024.10540813.

[10] C. Yang, Z. Lai, Y. Wang, S. Lan, L. Wang, and L. Zhu, "A Novel Bearing Fault Diagnosis Method Based on Stacked Autoencoder and End-Edge Collaboration," *IEEE CSCWD*, 2023, doi: 10.1109/CSCWD57460.2023.10152598.

[11] A. Sayghe, "A Physics-Aware Lightweight Transformer Network for Intelligent Bearing Fault Diagnosis Under Variable Operating Conditions," *Artificial Intelligence for Engineering*, 2026, doi: 10.1049/aie2.70014.

[12] Z. Zhan, S. Zhang, J. Xu, and D. Ma, "Edge-Oriented Bearing Fault Diagnosis via Triple-Lightweight Network With Adaptive Pruning," *IEEE Transactions on Instrumentation and Measurement*, 2026, doi: 10.1109/TIM.2026.3699722.

---

## 근거 문서

- `PROJECT_CONTEXT.md`
- `decisions/personal_research_summary_0708.md`
- `decisions/professor_report_0729.md`
- `surveys/elastic_scheduling_survey.md`
- `manuscript/realtime_fault_diagnosis_related_work_table.md`
- `surveys/claim_bank.md`
- `manuscript/problem_formulation.md`
- `experiments/experiment_design.md`

---

## v2 업데이트 조건

다음 조건을 충족하면 `Codex v2`를 작성한다.

1. Adaptive input 8편 정독 완료
2. RT-DNN serving 13편 정독 완료
3. Pi Zero 2W fixed-mode R2/R3 완료
4. Initial `H` set, deadline와 machine-condition indicator 확정
5. Contribution과 guarantee level에 대한 교수님 피드백 반영
