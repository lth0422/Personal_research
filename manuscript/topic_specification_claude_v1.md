# 주제 구체화 문서 — Runtime (W, H, M) Mode Selection for Real-Time Vibration Fault Diagnosis

> 작성자: Claude (Claude Code) · 버전: v1 · 작성일: 2026-08-01
> 상태: 초안. 리뷰 완료 섹션은 real-time fault diagnosis와 elastic scheduling 두 개이며, adaptive diagnostic fidelity와 rt-dnn serving은 서베이 보강 후 반영 예정이다.
> 기준 문서: `PROJECT_CONTEXT.md`, `manuscript/problem_formulation.md`, `surveys/realtime_fault_diagnosis_survey_protocol.md`, `surveys/elastic_scheduling_survey.md`
> 작성 규칙: 본문은 한국어, 정착된 전문 용어는 영어를 유지한다. 단정적 표현을 피하고 미검증 내용은 목표로 표시한다.

---

## 제목 (가제)

- **국문 가제**: 엣지 디바이스에서 기계 상태와 시스템 slack을 함께 고려하는 실시간 진동 결함 진단용 (W, H, M) 런타임 모드 선택 elastic scheduling
- **English (working title)**: Machine-Condition and System-Slack Aware Runtime (W, H, M) Mode Selection for Real-Time Vibration Fault Diagnosis on Edge Devices

대안 가제

- Elastic Scheduling of Diagnosis Modes: Joint Window, Period, and Model Selection under Machine-State and Slack Triggers
- Anomaly-Driven Elastic Diagnosis: Feasibility-First Runtime Mode Selection for Vibration Fault Diagnosis on PREEMPT_RT

## Keywords

`real-time systems`, `elastic scheduling`, `vibration fault diagnosis`, `runtime mode selection`, `schedulability`, `anomaly-driven adaptation`, `edge computing`, `PREEMPT_RT`, `adaptive inference`, `window-period-model tuple`

---

## 국문 초록

제한된 엣지 디바이스에서 진동 기반 결함 진단을 실시간으로 수행할 때, 진단 정확도와 스케줄 가능성은 서로 상충한다. 더 큰 입력 window와 무거운 model은 진단 신뢰성을 높이지만 실행시간과 utilization을 함께 키워 deadline을 위협한다. 본 연구는 진단 태스크의 입력 window `W`, 진단 주기를 결정하는 hop `H`, 추론 model `M`을 하나의 mode tuple `a = (W, H, M)`로 묶고, 기계 상태 `q`와 시스템 slack `S`를 동시에 트리거로 사용해 runtime에 mode를 선택하는 elastic scheduling 정책을 제안한다. 정책은 사전 profiling한 feasible mode set 안에서만 진단 utility가 큰 mode를 고르는 feasibility-first 구조를 따른다. 평가 플랫폼은 Raspberry Pi Zero 2W이며 일반 Linux와 PREEMPT_RT를 비교한다. 본 문서는 두 축의 선행 연구, 즉 real-time fault diagnosis와 elastic scheduling을 체계적으로 검토한 결과를 종합하고, 연구 공백과 정식화, 실험 설계, 남은 과제를 정리한다. 검토한 진동 결함 진단 문헌은 대부분 평균 latency나 online 동작만 보고하는 best-effort 수준이었고, elastic scheduling 문헌은 주기와 자원을 조절하되 정확도를 바꾸는 변수나 외부 기계 상태 트리거를 다루지 않았다. 두 축이 만나는 자리, 즉 기계 상태로 트리거되어 정확도를 바꾸는 mode를 deadline 보장 아래 선택하는 문제가 본 연구의 위치다.

## Abstract (English)

Running vibration-based fault diagnosis in real time on a resource-constrained edge device exposes a direct conflict between diagnostic fidelity and schedulability. A larger input window and a heavier model improve diagnostic reliability but simultaneously increase execution time and utilization, threatening deadlines. This work groups the input window `W`, the hop `H` that determines the diagnosis period, and the inference model `M` into a single mode tuple `a = (W, H, M)`, and proposes an elastic scheduling policy that selects a mode at runtime using both the machine condition `q` and the system slack `S` as triggers. The policy is feasibility-first: it chooses the diagnostically most useful mode only within a set of pre-profiled feasible modes. The evaluation platform is a Raspberry Pi Zero 2W, comparing stock Linux against PREEMPT_RT. This document synthesizes a systematic review of two research axes, real-time fault diagnosis and elastic scheduling, and organizes the resulting research gap, formulation, evaluation design, and remaining tasks. Most reviewed fault-diagnosis studies remain best-effort, reporting only average latency or online operation, while elastic-scheduling studies adjust period or resources without varying an accuracy-changing quantity or using an external machine-state trigger. The intersection of these two axes, selecting an accuracy-changing mode under a machine-state trigger while preserving deadline feasibility, is the position of this research.

---

## 1. Background

### 1.1 연구 동기와 문제 정의

회전 기계의 진동 기반 결함 진단은 엣지 디바이스에서 수행할 때 두 가지 요구가 충돌한다. 첫째는 진단 신뢰성이다. 더 긴 입력 window는 더 많은 회전 주기와 주파수 정보를 담아 약한 결함을 더 잘 드러내고, 더 무거운 model은 표현력이 크다. 둘째는 실시간성이다. 엣지 디바이스의 자원은 제한적이며, 진단 결과는 정해진 deadline 안에 나와야 한다.

선행연구 KCC 2026에서 확인한 핵심 관계가 이 충돌을 정량적으로 보여준다. STM32F407 + Zephyr RTOS 환경에서 depthwise convolution의 복잡도가 window 크기에 대해 `O(W^2)`로 증가하여, window를 줄이면 latency가 superlinear하게 감소했다. 같은 데이터를 비중첩 window 가정으로 utilization을 계산하면 다음과 같다.

| W | C max | T at 8 kHz | U = C / T |
| ---: | ---: | ---: | ---: |
| 512 | 40.3 ms | 64 ms | 0.63 |
| 1024 | 129.8 ms | 128 ms | 1.01 |
| 2048 | 460.3 ms | 256 ms | 1.80 |

정밀 mode로 갈수록 `C`가 증가하고, 주기 `T`가 충분히 커지지 않으면 utilization이 1을 넘어 단일 태스크만으로도 스케줄이 깨질 수 있다. 즉 "정확도를 높이는 선택"이 곧바로 "스케줄 가능성을 위협하는 선택"이 된다.

본 연구의 착안은 이 선택을 고정하지 않는 것이다. 기계가 정상일 때는 가벼운 mode로 slack을 확보하고, 이상 징후가 감지되면 정밀 mode로 전환하되 그 전환이 deadline 안에서 실행 가능한 경우에만 허용한다. 이때 조절 대상은 window `W` 하나가 아니라, 진단 주기를 정하는 hop `H`와 model `M`을 함께 묶은 mode tuple이다. 이 결합이 필요한 이유는 2.2절에서 다룬다.

> 참고: KCC 2026의 model은 fault classification 형태이지만 내부적으로 anomaly detection을 수행하며, 그 anomaly score가 elastic scheduling의 트리거 신호 `q`가 된다.

### 1.2 관련 연구 종합

연구 질문 중심으로 문헌을 여섯 섹션 S1~S6으로 태깅한다. 이 중 현재 체계적으로 검토를 마친 축은 **S1 real-time fault diagnosis**와 **S3 elastic scheduling** 두 개다. **S2 adaptive diagnostic fidelity**와 **S4 deadline-aware AI inference / rt-dnn serving**은 서베이 보강 예정이며 1.2.3절에 현재까지 파악한 범위만 기록한다.

#### 1.2.1 Real-Time Fault Diagnosis (검토 완료)

진동/회전 기계 결함 진단 문헌을 재현 가능한 판정 규칙으로 검토했다. 핵심 판정 축은 두 가지다. 하나는 Deadline 판정으로, 명시적 deadline을 정의하고 miss를 측정하면 O, period나 window 같은 시간 기준은 있으나 deadline으로 선언하지 않으면 △, 시간 기준 자체가 없으면 X로 구분한다. 다른 하나는 real-time 등급으로, formal hard/firm 보장은 H, weakly-hard는 W, deadline과 tail/miss를 측정하되 formal 보장이 없으면 E, 평균 latency나 throughput 중심이면 B로 구분한다.

검토 결과는 다음과 같다.

- 검토한 직접 비교군 대부분이 **RT 등급 B**였다. Deadline을 명시적으로 정의하고 평가한 O 사례는 확인되지 않았다. 다수 논문의 "real-time"은 online monitoring 또는 낮은 평균 latency를 뜻하며 주기적 deadline 충족을 뜻하지 않았다.
- 대표적 반례로 He et al.은 개선된 cyclostationary 분석을 STM32F407에 구현했으나 전체 pipeline이 약 10.294 s로 1 s acquisition window를 10배 이상 초과했다. 논문은 이를 deadline miss로 다루지 않고 online 실행 자체를 real-time으로 표현한다. 이는 "엣지에서 online 실행"과 "deadline 충족"이 별개임을 보여주는 근거다.
- "adaptive"라는 표현은 대개 runtime 적응이 아니라 training-time pruning이거나 초록에만 등장하는 미구현 주장이었다. Zhan et al.의 adaptive pruning은 학습 시점 구조 pruning이고, Gupta and Shivhare의 adaptive sampling은 실험에서 window와 sampling이 고정되어 있었다.
- runtime에 `W`, `H`, `M`을 함께 바꾸며 그 트리거로 기계 상태 `q`와 시스템 slack `S`를 동시에 사용하는 문헌은 확인되지 않았다.

한편 본 연구의 구성요소를 부분적으로 예고하는 선례는 존재한다.

- **q 트리거의 구조적 선례**: Langarica et al.은 1 Hz DIPCA+SPE anomaly detection이 vibration 관련 결함을 지목했을 때에만 무거운 CNN을 실행한다. 즉 machine evidence가 값비싼 추론을 gate하는 구조로, 본 연구 `q` 트리거의 직접 선례다. 다만 시스템 slack `S`를 보지 않아 `a = (W, H, M)` 선택은 없다.
- **q가 최적 설정을 바꾼다는 간접 근거**: Lima의 Edge Impulse 평가에서 미세 결함은 명확한 결함보다 더 높은 sampling rate와 더 짧은 hop을 최적으로 요구했다. 이는 기계 상태에 따라 적절한 `W`, `H`가 달라진다는 간접 근거지만, Lima는 이를 offline blind grid search로 고장 유형별 단일 구성으로 고정할 뿐 runtime 규칙으로 정식화하지 않는다.
- **물리 기반 window 결정**: Pubalan et al.은 `W = 60 f_s / RPM`으로 shaft 한 회전에 맞춰 window를 정한다. 회전속도라는 machine condition을 입력 길이로 변환한 선례이나 runtime 적응은 아니다.
- **timing 인지 트리거의 가장 가까운 FD 사례**: Yang et al.은 confidence와 allowable latency로 edge 개입을 결정하는 end-edge 협업을 제시한다. machine evidence와 timing constraint를 함께 트리거로 쓰는 가장 가까운 진단 비교군이나 schedulability 분석은 없다.

정리하면, 진동 결함 진단 축에서 scheduling을 정면으로 다룬 직접 비교군은 검토 범위에서 드물었고, 정확도-스케줄 결합과 기계 상태 트리거를 동시에 다룬 사례는 확인되지 않았다.

#### 1.2.2 Elastic Scheduling (검토 완료)

elastic scheduling 축은 이론 계보와 응용 사례를 함께 검토했다. 각 논문을 가변 변수와 트리거, 보장 수준으로 정리한 결과는 다음과 같다.

| 논문 | 가변 변수 | 트리거 | 보장 수준 | 본 연구에 주는 것 |
| --- | --- | --- | --- | --- |
| Buttazzo et al. (RTSS 1998, IEEE TC 2002) | period `T` | 시스템 부하, admission | 제한된 모델 내 formal hard | elastic task model 원형, `e_i/E_v` 재분배, period transition 규칙 |
| Burgio et al. TDMA+Elastic (ICCD 2010) | bus bandwidth, period | runtime 부하 이벤트 | soft, 실험적 QoC | 설정 이산화 + WCET LUT 메커니즘 |
| Salman et al. Compositional (ETFA 2021) | period `T`, reservation | runtime 이벤트 | hard, PRM utilization bound | 2계층 국소성, `T_min` 불변성 논증 |
| Gifford et al. Decntr (RTAS 2024) | controller, period, resource allocation | offline + mode-change event | hard, invariant set | mode transition 분석의 이론 골격 |
| Xu et al. Safety-Aware (RTCSA 2023) | 공통 period, miss 패턴 | offline | soft-but-formal, `d_safe`/`⟨m,k⟩` | 정확도-스케줄 결합의 정식화 도구 |
| Li et al. ATER (RTCSA 2025) | sensor sampling rate | runtime 관측 | empirical only | 관측-조절 피드백 루프, overhead 실측 방법 |

두 가지 축으로 이 문헌들을 배치하면 공통된 빈자리가 드러난다.

- **트리거 축**: 검토한 elastic 문헌은 전부 시스템 내부 신호로 트리거된다. 부하, 자원 경합, 메시지 드롭, 또는 offline 합성이다. 외부 물리 세계의 기계 상태로 트리거하는 사례는 없다.
- **가변 변수 축**: 검토한 문헌은 주기, rate, 대역폭을 조절한다. 이들은 semantics를 보존하는 변수로, 조절해도 계산 결과의 의미가 바뀌지 않는다. 설정이 정확도 자체를 바꾸는 사례는 없다. Xu et al.이 정확도와 가장 가깝지만 그것도 주기 변경이며 대상은 제어 안전이다.

즉 트리거 축의 "외부 기계 상태"와 가변 변수 축의 "정확도를 바꾸는 변수"가 교차하는 사분면이 비어 있고, 이 자리가 본 연구의 위치다.

각 논문의 역할은 다음과 같이 나눈다. Decntr은 mode transition 분석의 이론 템플릿을 제공한다. Salman의 compositional 논문은 국소성과 `T_min` 불변성, 즉 범위 안의 조정은 상위 재검증 없이 안전하다는 논증 형태를 제공한다. Xu의 Safety-Aware는 `d_safe`와 `⟨m,k⟩`로 정확도-스케줄 결합을 정식화하는 도구를 제공하며, 이는 본 연구의 진단 utility `Q` 정의의 유력 후보다. TDMA+Elastic은 설정을 몇 개 이산 값으로 두고 각 실행시간을 LUT로 관리하는 메커니즘을 제공한다. ATER는 저오버헤드 관측-조절 루프와 그 overhead 실측 방법을 제공한다. Buttazzo 원저는 "늘리는 건 즉시, 줄이는 건 다음 release"라는 완성된 elastic 도구를 제공한다.

#### 1.2.3 Adaptive Diagnostic Fidelity 및 RT-DNN Serving (검토 예정)

두 축은 아직 체계적 검토를 마치지 않았다. 현재까지 파악한 범위만 기록하며, 서베이 보강 후 확정한다.

- **S2 Adaptive Diagnostic Fidelity**: 입력 크기나 model fidelity를 조절해 정확도-비용을 절충하는 계열이다. AIL, ADW 같은 adaptive window 연구는 window를 정확도 축에서 조절하지만 대체로 offline 설계이거나 트리거가 없다. 본 연구는 이 정확도 축을 elastic scheduling의 시스템 축과 결합한다는 점에서 갈린다. image resizing 계열은 vision 도메인의 입력 크기 조절 사례로, 시간축 진동 window `W`와의 차이를 명확히 해야 한다.
- **S4 Deadline-Aware AI Inference / RT-DNN Serving**: deadline이나 slack 안에서 model, early-exit, batch, input resolution을 고르는 계열이다. DNN-SAM은 system slack으로 input fidelity를 고르는 강한 직접 비교군이고, AMS는 condition에 따라 model complexity를 고르는 condition-기반 선택의 비교군이다. 다만 이들은 vision/GPU 중심이며 진동의 시간축 `W`, `H`, anomaly 트리거, PREEMPT_RT 실측은 다루지 않는다. 검토 완료 후 본 연구의 mode-selection 정책과의 정밀 대비를 1.3절 공백에 반영한다.

> 이 두 절의 내용은 잠정적이며, 서베이 보강 후 검증된 판정으로 대체한다.

### 1.3 연구 공백

검토를 종합하면 세 층위의 공백이 드러난다.

1. **진단 축의 공백**: 진동 결함 진단 문헌은 대부분 best-effort이며 deadline과 tail/miss, schedulability를 결합한 사례가 드물다. runtime에 `W`, `H`, `M`을 함께 조절하는 사례는 확인되지 않았다.
2. **스케줄링 축의 공백**: elastic scheduling 문헌은 정확도를 바꾸는 변수를 다루지 않고, 트리거가 시스템 내부 또는 offline에 한정된다. 외부 기계 상태로 트리거하는 사례는 없다.
3. **결합의 공백**: 두 축을 잇는 문헌, 즉 기계 상태 `q`와 시스템 slack `S`를 분리된 역할로 사용해 정확도를 바꾸는 feasible mode `(W, H, M)`를 선택하고 그 스케줄 가능성을 제시하는 문헌은 확인되지 않았다.

본 연구는 세 번째 공백을 목표로 한다.

---

## 2. Methodology

정식화의 상세는 `manuscript/problem_formulation.md`를 기준으로 하며, 본 절은 그 핵심을 요약한다.

### 2.1 시스템 및 진단 태스크 모델

Raspberry Pi Zero 2W에서 일반 Linux 또는 PREEMPT_RT 위에 진동 결함 진단 태스크가 주기적으로 실행된다. 태스크는 진동 신호 segment를 받아 추론하고 deadline 안에 진단 결과를 출력한다. 원신호는 sampling frequency `f_s`로 취득된다.

진단 step `k`에서 runtime은 사전 정의된 후보 집합 `A`에서 하나의 mode를 선택한다.

```text
a = (W_a, H_a, M_a),   a in A
```

- `W_a`: 입력 window 크기, sample 수.
- `H_a`: 연속 진단 window 사이의 hop, sample 수.
- `M_a`: model 또는 추론 구성.

hop이 유도하는 진단 주기는 `T_a = H_a / f_s`이며, 이 arrival 주기는 end-to-end 진단 deadline이나 로컬 추론 budget과 구분한다. model-selection threshold를 태스크 주기나 deadline으로 혼동하지 않는다. `W`와 `H`를 의도적으로 분리하는 이유는 진동 진단에서 "얼마나 많은 신호 맥락을 볼 것인가"와 "얼마나 자주 진단할 것인가"가 서로 다른 설계 선택이기 때문이다.

### 2.2 Mode Tuple과 런타임 정책: 왜 W, H, M을 함께 묶는가

입력 적응은 1차원이 아니다. window `W`를 줄이면 실행시간 `C`가 줄지만, 더 짧은 hop `H`와 짝지어지면 진단 주기 `T`도 줄어든다. utilization은 `U_a = C_a / T_a`, `T_a = H_a / f_s`이므로 다음 두 경우가 갈린다.

- **경우 1**: `W` 감소로 `C` 감소, `H`와 `T`는 고정 → `U = C/T` 감소 → 스케줄 가능성 개선.
- **경우 2**: `W` 감소로 `C` 감소, 그러나 `H`와 `T`도 감소 → `U = C/T`가 오히려 증가할 수 있음 → 각 추론은 빨라져도 스케줄 가능성은 악화.

따라서 runtime은 window 하나가 아니라 mode tuple `(W, H, M)`에서 선택해야 한다. 이 관찰이 mode tuple을 묶는 근거다.

정책은 기계 상태 `q`와 시스템 slack `S`를 분리된 역할로 사용한다. `q`는 mode의 진단 utility 순위를 정하고, `S`는 deadline-feasible mode를 제한한다.

```text
π : (q = machine condition, S = system slack) → a = (W, H, M)
정상 → 가벼운 mode로 slack 확보 / 이상 → 정밀 mode 전환
```

`q`의 구체 정의는 anomaly score, health index, model confidence, thresholded fault probability 중 하나로 확정해야 하며, 첫 구현은 KCC model 내부의 anomaly score를 우선 후보로 둔다.

### 2.3 Feasibility와 Schedulability: feasibility-first 정책

0708 면담 이후 첫 번째 연구 질문은 "이상 징후 시 정밀 mode로 전환해도 static하게 schedulable한가, 그리고 그 보장을 어떻게 제시할 것인가"이다. 따라서 정책은 단순히 정밀 mode를 고르는 것이 아니라 feasibility-first 구조를 따른다.

```text
1. 사전 profiling한 mode로 mode bank A를 만든다.
2. utilization과 tail-response 제약을 어기는 mode를 제거한다.
3. A_feasible(k) 안에서만 진단 utility가 가장 큰 mode를 고른다.
```

feasibility 조건은 다음과 같다. 각 mode `a`의 실행시간은 분포 `C_a_mean, C_a_p95, C_a_p99, C_a_max`로 보고하고, 관측 응답시간은 `R_a = C_a + I_a + L_os`로 둔다. PREEMPT_RT에서 static hard WCET를 증명 없이 주장하지 않으며, 초기 정식화는 경험적 tail 기준을 쓴다.

```text
A_feasible(k) = { a in A | U_bg + C_a_tail / T_a <= U_bound  and  R_a_tail <= D_a }
```

정책 목적은 다음과 같이 진단 선호와 timing feasibility를 분리한다.

```text
a*_k = argmax Q(a, z_k)   subject to  a in A_feasible(k)
```

`A_feasible(k)`가 비면 사전 정의된 fallback mode를 실행하거나 overload를 보고한다. deadline miss를 감지한 뒤 가벼운 model을 재실행하는 것은 그 자체로 timing 보장이 아니므로, 초기 구현은 offline-profiled admissible mode를 우선하고 재실행은 budget을 명시적으로 예약한 경우에만 둔다.

slack은 평균이 아니라 최근 응답시간 이력의 tail로 정의하는 편이 real-time 논문에서 방어 가능하다.

```text
S_k_p99 = D - p99(R_recent)   또는   S_k_max = D - max(R_recent)
```

### 2.4 이론적 근거의 역할 분담

정식화의 각 부분은 검토한 elastic scheduling 문헌에서 다음을 빌린다. mode transition의 스케줄 가능성 증명은 Decntr의 carry-over 분석 골격을 참조한다. "범위 안의 조정은 상위 재검증 없이 안전"이라는 논증은 Salman의 `T_min` 불변성 형태를 빌린다. 진단 utility `Q`는 Xu의 `d_safe` 이탈 거리 또는 weakly-hard `⟨m,k⟩` 중 하나로 정식화하는 것을 우선 검토한다. mode bank의 이산화와 실행시간 관리는 TDMA+Elastic의 LUT 메커니즘을 따른다. runtime 관측-조절 루프와 그 overhead 실측은 ATER의 방법을 참조한다.

다만 본 연구의 `C = C(W, M)`는 설정에 따라 실행시간이 바뀌므로, 실행시간을 고정으로 두는 elastic 이론의 utilization 논증을 그대로 쓸 수 없다. 국소성 논증의 형태만 빌리고 실제 bound는 `U ∝` window-model 구조로 다시 유도해야 한다.

---

## 3. Experiment

### 3.1 플랫폼과 baseline

- 평가 플랫폼: Raspberry Pi Zero 2W, Cortex-A53, Raspberry Pi OS Lite. 일반 Linux 커널과 PREEMPT_RT 커널을 비교한다.
- 추론 backend: CMSIS-NN은 Cortex-M 전용이므로 Cortex-A에서는 XNNPACK 또는 reference 구현을 사용한다.
- 비교 baseline: static light mode, static precise mode, `q`-only 정책, `S`-only 정책, 제안 `q + S` 정책.
- PREEMPT_RT 패치의 실효성은 cyclictest 분포 비교로 별도 검증한다. 적용이 지나치게 쉬웠던 정황이 있어 검증 없이 hard real-time을 주장하지 않는다.

### 3.2 측정과 프로파일링

- mode bank `A`의 각 `(W, H, M)`에 대해 실행시간 분포 `C_a_mean, C_a_p95, C_a_p99, C_a_max`를 측정해 timing profile을 만든다.
- KCC의 utilization motivation 표를 평균, p95, p99, max 실행시간 기준으로 각각 재계산한다.
- 부하 조건은 idle, CPU, memory, IO, combined 5종을 stress-ng로 구성하고, 각 부하에서 activation jitter, inference latency, end-to-end latency, deadline miss, p95/p99, 표준편차를 측정한다.

### 3.3 정책 평가 설계

- mode feasibility table을 만들어 각 부하와 mode 조합의 timing-feasibility를 기록한다.
- 기계 상태 `q` 시나리오를 정상, 의심, 경고로 나누어 anomaly score 궤적을 재생하고, 각 궤적에서 정책이 선택하는 mode 열과 그에 따른 진단 utility, deadline miss를 baseline과 비교한다.
- runtime mode-selection의 overhead를 ATER 방식으로 실측하여 실행시간 `C`에 포함해야 하는지 판단한다.

### 3.4 지표

- 실시간성: deadline miss ratio, p99/max response time, activation jitter, utilization.
- 진단: 정확도 또는 detection delay 등 진단 utility 지표. `Q` 정의 확정 후 구체화한다.
- 정책 효과: 제안 `q + S` 정책이 static baseline과 single-trigger baseline 대비 deadline miss를 늘리지 않으면서 진단 utility를 개선하는지 검증한다.

> 위 실험 값과 결과는 아직 측정되지 않았으며, 본 문서에서는 설계로만 제시한다.

---

## 4. To-Do 및 향후 계획

### 4.1 서베이 보강 (본 문서 반영 대상)

- [ ] **S2 Adaptive Diagnostic Fidelity 서베이 정리**: AIL, ADW, image resizing 계열의 가변 변수와 트리거를 재현 가능한 규칙으로 판정하고 1.2.3절과 1.3절 공백에 반영.
- [ ] **S4 Deadline-Aware AI Inference / RT-DNN Serving 서베이 정리**: DNN-SAM, AMS, EdgeServing, Pantheon, FLEX 등을 slack/condition 트리거와 가변 변수로 판정하고 본 연구 정책과의 정밀 대비를 1.3절에 반영.
- [ ] 두 축 반영 후 1.2.3절의 잠정 서술을 검증된 판정으로 대체.

### 4.2 정식화 및 방법 확정

- [ ] 진단 utility `Q(a, z_k)` 정의를 `d_safe` 이탈 거리 또는 weakly-hard `⟨m,k⟩` 중 하나로 확정.
- [ ] mode transition 스케줄 가능성 증명을 Decntr 골격으로 구성. `C(W, M)` 가변 실행시간에 맞게 utilization bound 재유도.
- [ ] mode bank `A`의 구체 `W`, `H`, `M` 값 확정. 첫 구현은 `M` 고정, discrete `(W, H)` mode bank의 feasibility와 runtime selection부터 검증.
- [ ] fallback 규칙과 mode-switching hysteresis 확정.

### 4.3 실험 및 마일스톤

- [ ] G1 (2026-07-31 기준 이미 도래): 후보 mode set `A`, timing profiler, mode feasibility table, problem formulation, algorithm pseudocode 초안 정리. 지연 항목 점검 필요.
- [ ] KSC 2026 (9월 제출 목표): Pi Zero 2W 일반 Linux vs PREEMPT_RT 실시간성 비교. 방향 2를 위한 기초 환경과 원인 분석.
- [ ] 학위논문 (중기): `(W, H, M)` elastic scheduling 코어. 투고 전략은 RTAS 2027 stretch, RTCSA 2027 main.
- [ ] 장기: 추론 + OTTA 학습을 동일 RT 스케줄링에 통합.

### 4.4 미결 설계 질문

`manuscript/problem_formulation.md` 8절의 open design choices와 `decisions/open_questions.md`를 단일 기준으로 유지한다. 핵심은 다음과 같다.

- `q`를 anomaly score, health index, confidence, thresholded fault probability 중 무엇으로 둘 것인가.
- feasibility의 tail 지표를 p95, p99, observed max 중 무엇으로 둘 것인가.
- mode 전환이 잦아지지 않도록 hysteresis를 얼마나 둘 것인가.

---

## 부록 A. 관련연구 요약표 (검토 완료 두 축)

### A.1 Real-Time Fault Diagnosis

| 논문 | 가변 변수 | 트리거 | Deadline | RT 등급 | 본 연구와의 관계 |
| --- | --- | --- | :---: | :---: | --- |
| Langarica et al. | 없음 (cascade) | anomaly detection이 CNN을 gate | X | B | `q` 트리거의 구조적 선례. `S` 없음 |
| Lima (Edge Impulse) | 없음 (offline grid search) | 없음 | △ | B | 미세 결함이 더 짧은 hop을 요구 → `q`가 최적 `W/H`를 바꾼다는 간접 근거 |
| Pubalan et al. | 없음 (고정) | 없음 | △ | B | `W = 60 f_s / RPM` 물리 기반 window 결정 선례 |
| Yang et al. | offloading 위치 | confidence + allowable latency | △ | B | machine evidence + timing을 함께 트리거로 쓰는 가장 가까운 FD 사례. schedulability 없음 |
| He et al. | 없음 (고정) | 없음 | △ | B | pipeline 10.294 s가 1 s window 초과. "online ≠ deadline 충족" 반례 |
| 다수 TinyML/경량화 계열 | 없음 (고정) | 없음 (offline) | X 또는 △ | B | 경량화 대조군. runtime 적응·deadline 보장 없음 |
| **본 연구** | **W + H + M 동시** | **q + S** | **목표 O 또는 E** | **목표 E, 조건부 H** | — |

### A.2 Elastic Scheduling

| 논문 | 가변 변수 | 트리거 | 보장 수준 | 본 연구에 주는 것 |
| --- | --- | --- | --- | --- |
| Buttazzo et al. 1998/2002 | period `T` | 부하, admission | 제한 모델 내 formal hard | elastic 원형, 재분배·transition 규칙 |
| Burgio et al. TDMA+Elastic | bus bandwidth, period | runtime 부하 | soft, 실험적 QoC | 설정 이산화 + LUT |
| Salman et al. Compositional | period, reservation | runtime 이벤트 | hard, PRM bound | 2계층 국소성, `T_min` 불변성 |
| Gifford et al. Decntr | controller, period, resource | offline + event | hard, invariant set | mode transition 이론 골격 |
| Xu et al. Safety-Aware | 공통 period, miss 패턴 | offline | soft-but-formal, `d_safe`/`⟨m,k⟩` | 정확도-스케줄 결합 정식화 |
| Li et al. ATER | sampling rate | runtime 관측 | empirical | 관측-조절 루프, overhead 실측 |
| **본 연구** | **W + H + M** | **q + S** | **목표 E, 조건부 H** | — |

### A.3 novelty 위치 요약

- 트리거 축: 검토한 문헌은 시스템 내부 신호 또는 offline. 외부 기계 상태 트리거는 비어 있음.
- 가변 변수 축: 검토한 문헌은 주기/rate/대역폭 등 semantics 보존 변수. 정확도를 바꾸는 변수는 비어 있음.
- 두 빈자리의 교차점이 본 연구의 자리다.

---

> 다음 버전 (v2) 예정 변경: S2 adaptive와 S4 rt-dnn 서베이 반영, `Q` 정의 확정 반영, KCC utilization 표의 p95/p99/max 재계산 반영.
