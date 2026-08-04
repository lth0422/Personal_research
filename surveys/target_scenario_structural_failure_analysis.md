# Target-Scenario Structural Failure Analysis

> 작성일: 2026-08-04
> 목적: 기존 접근의 차이를 나열하는 대신, 본 연구의 target scenario에서 어떤 failure condition을 막지 못하는지와 제안 방법의 proof obligation을 연결한다.

## 0. 해석 원칙

- 이 문서에서 `구조적 한계`는 논문 자체가 실패했다는 뜻이 아님.
- 각 논문은 자신의 application, task model과 timing assumption 안에서 유효할 수 있음.
- 여기서는 해당 접근을 vibration fault diagnosis의 상태별 진단 요구와 runtime resource variation에 적용할 때 필요한 변수·상태·제약을 표현할 수 있는지 평가함.
- 단순히 논문에 `W`, `H`, `M` 또는 `q`라는 기호가 없다는 이유만으로 구조적 실패로 판정하지 않음.
- 기존 framework에 mode semantics만 추가하면 본 문제를 그대로 표현할 수 있는지 확인하는 subsumption test를 함께 수행함.
- 정량 결과와 보장 수준은 paper card에서 확인된 범위만 사용함.

## 1. 먼저 통과해야 하는 연구 성립 조건

### G0. 단일 지배 모드 부재

가장 정밀한 하나의 mode가 모든 상태와 부하에서 다음 조건을 만족하면 runtime adaptation은 필요 없음.

```text
모든 q, system condition에 대해:
  Q(m_best, q) >= Q(m_i, q)
  T_best <= T_max(q)
  R_best^max <= D_best
  U_bg + C_best^max/T_best <= U_bound
```

- 위 조건을 만족하는 `m_best`가 있으면 fixed-precise가 가장 단순한 해법.
- 연구의 첫 실험은 제안 정책의 우수성보다 단일 지배 모드의 존재 여부를 먼저 확인해야 함.
- Pi Zero 2W가 모든 후보를 충분히 빠르게 실행한다면 scheduling challenge와 slack-based adaptation의 필요성이 약해짐.
- 과도한 synthetic stress로 일부러 miss를 만들어 G0를 기각하면 안 됨. Sensor acquisition, preprocessing, logging, communication 등 실제 pipeline workload를 우선 사용함.

### G1. 상태별 요구 차이

- 기계 상태에 따라 최대 허용 진단 주기 `T_max(q)`가 달라지는지 확인.
- 기계 상태에 따라 `(W,M)`의 진단 성능 순위 `Q(W,M,q)`가 달라지는지 확인.
- 모든 상태에서 동일 `(W,M)`이 우세하고 `T_max`도 같으면 `q` 기반 adaptation의 필요성이 약함.

### G2. 시스템 조건별 feasible set 변화

- 현실적인 runtime interference에서 feasible mode set이 실제로 달라지는지 확인.
- 모든 mode가 모든 조건에서 deadline을 만족하면 `S` 기반 filtering이 불필요함.

## 2. Target scenario와 failure condition

### 2.1 Target scenario

- Platform: Raspberry Pi Zero 2W, Linux와 PREEMPT_RT.
- Task: 주기적으로 release되는 vibration fault-diagnosis job.
- Mode: `m_i=(W_i,H_i,M_i)`.
- Period와 초기 operational deadline: `T_i=D_i=H_i/f_s`.
- Application state: vibration anomaly state `q_k`.
- System state: background utilization, interference, scheduling delay를 반영한 runtime feasibility 또는 slack `S_k`.

### 2.2 핵심 충돌

```text
U_i = C(W_i,M_i)/T_i = C(W_i,M_i) f_s/H_i
```

- 더 적합한 `W` 또는 `M`이 `C(W,M)`을 증가시키고, 더 빠른 갱신을 위해 `H`를 줄이면 resource demand가 두 방향에서 증가할 수 있음.
- 반대로 `H`만 늘려 부하를 줄이면 상태 갱신 빈도와 detection timeliness가 악화될 수 있음.
- 위 두 현상은 현재 확인해야 할 연구 가설이며 일반 사실로 전제하지 않음.

### 2.3 Failure condition

| ID | Failure condition | 판정 기준 | Application 영향 |
| --- | --- | --- | --- |
| F0 | 단일 지배 모드 존재 | 하나의 mode가 모든 `q`와 system condition에서 진단·timing 조건 만족 | Adaptation 자체가 불필요. 현재 연구 질문 기각 또는 축소 |
| F1 | Timing infeasibility | `R_i^max > D_i` 또는 `U_total > U_bound` | Deadline miss, pending job과 backlog 누적 |
| F2 | Stale diagnosis | `T_i > T_max(q_k)` | 이상 상태 갱신과 진단 결과 생성이 요구보다 느림 |
| F3 | Diagnostic insufficiency | `Q(m_i,q_k) < Q_min(q_k)` 또는 상태별 대안보다 유의하게 낮음 | 이상 구간 recall·분류 성능 부족 가능 |
| F4 | State-blind degradation | System load만 보고 fidelity 또는 rate를 낮춤 | 정상·이상 상태의 요구 차이를 반영하지 못함 |
| F5 | Resource-blind escalation | `q`만 보고 고비용 mode를 선택 | 현재 system condition에서 F1 발생 가능 |
| F6 | Unsafe mode transition | 이전 mode carry-over job과 새 mode job이 겹쳐 transition demand가 bound 초과 | Steady-state에서 feasible해도 전환 직후 miss 가능 |

## 3. 기존 접근의 구조적 분석

### 3.1 논문별 target-scenario failure test

| Ref. | 접근과 핵심 mechanism | Target scenario에서 직접 표현하는 것 | 직접 표현하지 않는 것 | 예상 failure condition | 판정 |
| --- | --- | --- | --- | --- | --- |
| [1] | Elastic Task Model: 고정 `C`, 가변 period `T`, utilization compression | System load에 따른 `H/T` 조절과 schedulability | State-dependent diagnostic utility, `C(W,M)`, W/M 선택 | F2, F4. 부하를 줄이기 위해 period를 늘릴 때 진단 적시성 요구를 위반할 수 있음 | 부분 적용 가능. `T_max(q)`와 `C(W,M)` 확장 필요 |
| [2] | ATER: message drop·processing rate를 관측해 sensor sampling rate 조절 | Runtime bottleneck과 production/consumption rate mismatch | Deadline guarantee, diagnosis utility, anomaly state, W/M | F2, F4. Rate 감소가 sensor information과 perception utility에 미치는 영향은 평가 범위 밖 | Empirical H baseline으로 적합 |
| [3] | ADW: anomaly deviation으로 window size 선택, `H=beta W` | Signal pattern에 따른 W utility | Runtime slack·deadline, W/H 독립 선택 | F1. 선택 W가 현재 platform에서 infeasible할 수 있음. F2는 H가 W에 종속돼 독립 대응 불가 | Signal-side W baseline |
| [4,5] | AIL·AILWTLN: bearing physics·speed로 input length 결정, lightweight model 결합 | Bearing-domain input length 근거와 W/M 설계 | Runtime system state, explicit deadline, independent H | F1, F2. Signal에 적합한 input이 timing-feasible한지 판정하지 않음 | Offline W/M baseline |
| [6] | Industrial Internet FD: 저비용 anomaly stage가 vibration fault를 지목하면 CNN 실행 | Machine evidence `q`가 expensive diagnosis를 gate | Execution-time/deadline model, system slack, graded mode choice | F5. CNN이 필요한 시점의 resource feasibility를 확인하지 않음 | q-trigger baseline |
| [7] | AMS: Heart rate에 따라 deadline과 model depth 선택 | Physiological condition에서 M과 deadline 연결 | Runtime system slack, vibration W/H, tail-latency guarantee | F5 가능. HR에 맞는 model이 independent resource interference에서 infeasible할 수 있음 | Condition-aware M의 강한 선례 |
| [8] | DNN-SAM: physical ToC로 mandatory RoI를 정하고 slack으로 optional input scale 선택 | External physical context + runtime slack + fidelity selection + conditional schedulability | Temporal W, diagnosis period H, model M, machine-health utility | F2·F3은 target mode semantics를 추가하지 않으면 표현 불가 | 가장 강한 novelty 위협. 단순 mode 확장으로 본 문제를 흡수할 수 있는지 검토 필요 |
| [9] | Imprecise DL: deadline-feasible stage depth 중 input confidence reward 최대화 | Feasibility-first quality maximization | External machine state, temporal W/H, model bank | F2·F3은 현재 stage-depth action으로 표현 불가 | 최적화 구조가 본 연구와 거의 동일. Action set 확장 시 흡수 가능성 큼 |
| [10] | Physical-State-Aware Slack: physical state별 execution budget과 safe slack reclamation | External physical state + system-wide schedulability-aware slack | Diagnostic utility, W/H/M, state별 진단 주기 | F2·F3. State가 execution demand만 정하고 diagnostic requirement를 정하지 않음 | q+S 결합 자체의 novelty를 반증 |
| [11] | Decntr: mode별 controller·period·resource allocation과 transition DBF 검증 | State/mode change, period, resource allocation, carry-over transition | Vibration W와 diagnosis utility의 domain semantics | 본 framework에 diagnosis mode와 utility를 넣으면 F1·F2·F6을 다룰 가능성 | 가장 중요한 subsumption threat. 새 scheduling framework 주장에 주의 |
| [12] | Safety-Aware: plant safety를 보존하는 common period와 weakly-hard pattern offline 합성 | Application safety와 period/deadline miss pattern 연결 | Runtime anomaly/slack, `C(W,M)`, online mode selection | F3·F5. Diagnosis utility와 runtime resource variation 미포함 | `T_max(q)`에 물리적 근거가 필요하다는 반례 |

### 3.2 접근 계열별 구조적 failure

| 계열 | 대표 문헌 | Target scenario에서 남는 문제 |
| --- | --- | --- |
| Fixed or gated fault diagnosis | [6] | Machine event는 반영하지만 timing feasibility와 graded fidelity가 없음 |
| Signal-only input adaptation | [3--5] | W utility는 반영하지만 runtime timing과 independent H를 반영하지 않음 |
| Load-only rate adaptation | [1,2] | Feasibility는 개선할 수 있으나 진단 요구와 상태 인지 속도를 보존하지 않음 |
| Condition-only model selection | [7] | Application state는 반영하지만 독립적인 system interference를 제한하지 않음 |
| Deadline-aware DNN quality scheduling | [8,9] | Feasibility-first 구조는 이미 존재. Vibration temporal mode와 state-dependent diagnosis requirement가 없음 |
| Physical-state-aware scheduling | [10--12] | Physical state와 timing 보장은 이미 결합됨. Diagnostic utility semantics가 없거나 다른 application model에 묶임 |

## 4. Subsumption test: 기존 framework로 충분한가

구조적 novelty를 주장하려면 다음 질문에 `아니오`라고 답할 근거가 필요함.

### ST1. DNN-SAM action set만 바꾸면 되는가

- DNN-SAM의 optional scale 후보를 `(W,H,M)` 후보로 바꾸고 ToC를 vibration anomaly `q`로 바꾸면 본 정책과 유사해질 수 있음.
- 그러나 H가 바뀌면 future job release pattern과 utilization이 달라져, 한 job의 optional slack 안에서 scale을 고르는 문제와 동일하지 않을 수 있음.
- 필요한 차이 증명: period-changing mode가 만드는 future demand와 carry-over transition을 DNN-SAM의 per-job slack selection으로 처리할 수 없는 조건.

### ST2. Imprecise DL의 action을 mode bank로 바꾸면 되는가

- `feasible set -> quality argmax` 구조는 본 연구와 거의 동일.
- Stage depth 대신 `(W,H,M)` action을 넣는 것만으로 해결된다면 optimization structure는 신규하지 않음.
- 필요한 차이 증명: H 변경, acquisition semantics, state-dependent `T_max(q)`와 transition demand가 기존 fixed-period stage scheduling에 추가하는 새 분석 문제.

### ST3. Decntr에 diagnosis mode를 넣으면 되는가

- Decntr는 application mode, period, resource allocation과 transition schedulability를 이미 공동 설계함.
- Diagnosis utility와 `(W,H,M)` WCET table을 제공하면 상당 부분 흡수할 가능성이 있음.
- 이 경우 가능한 기여는 새 generic scheduler가 아니라 다음으로 좁혀짐.
  - Vibration diagnosis에서 `W/H/M`의 state-dependent utility와 timing profile을 구축하는 방법.
  - Linux/PREEMPT_RT의 measurement-based feasibility에서 online interference를 반영하는 방법.
  - 정상→이상 전환에서 diagnosis timeliness와 mode-transition demand를 함께 검증한 system study.

### ST4. 기존 방법의 단순 조합이면 충분한가

- ADW의 W 선택 + ATER의 H regulation + AMS의 M selection을 순차 적용할 수 있음.
- 각 controller가 독립적으로 action을 바꾸면 `C(W,M)/T(H)` coupling과 transition demand를 공동으로 보지 못할 수 있음.
- 필요한 차이 증명: 독립 controller 조합이 infeasible mode 또는 oscillation을 만드는 조건과 joint mode admission이 이를 방지하는 결과.

## 5. 제안 방법과 failure 제거 mechanism

### 5.1 Mechanism

| Mechanism | 입력 | 결정 또는 제약 | 대상으로 하는 failure |
| --- | --- | --- | --- |
| M0. Dominance gate | 모든 mode의 Q·C·R profile | 단일 지배 mode가 있으면 adaptation 중단 | F0을 숨기지 않고 연구 필요성 판정 |
| M1. State requirement model | anomaly state `q_k` | `T_i <= T_max(q_k)`, `Q(m_i,q_k)` 또는 `Q_min(q_k)` | F2, F3, F4 |
| M2. Timing-feasible mode filter | `C_i^max`, recent interference, `D_i`, `U_bg` | `R_i^est <= D_i`, `U_total <= U_bound` | F1, F5 |
| M3. Joint discrete mode bank | `(W_i,H_i,M_i)` profile | Coupled `C(W,M)/T(H)`를 하나의 admission 단위로 평가 | 독립 controller 조합의 coupling 누락 |
| M4. Transition admission | carry-over demand, next mode period·cost | 전환 직후 demand까지 feasible한 mode만 허용 | F6 |
| M5. Feasible-set utility selection | M1과 M2를 통과한 후보 | `argmax Q(m_i,q_k)` | Feasibility를 지키면서 diagnostic loss 최소화 |

### 5.2 제안 정식화 초안

```text
F(k) = {
  m_i |
  T_i <= T_max(q_k),
  R_i^est(k) <= D_i,
  U_bg(k) + C_i^max/T_i <= U_bound,
  TransitionFeasible(m_prev, m_i)
}

m_k* = argmax_{m_i in F(k)} Q(m_i, q_k)
```

- `F(k)`가 비면 fallback 또는 요구 완화 규칙이 필요함.
- 위 식은 설계 초안이며 formal guarantee가 아님.
- PREEMPT_RT에서 측정 최대를 사용하면 measurement-based conditional guarantee로 표현해야 함.

## 6. Proof obligation

| ID | 증명 또는 실험 질문 | 필요한 비교 | 성공 기준 | 실패 시 조치 |
| --- | --- | --- | --- | --- |
| PO0 | 단일 지배 mode가 없는가 | 모든 `(W,H,M)` × q × realistic load | 항상 우세한 fixed mode 없음 | 있으면 adaptation 연구 축소 또는 종료 |
| PO1 | 상태별 진단 요구가 실제로 다른가 | q별 W/M 성능과 H별 detection timeliness | Mode ranking 또는 `T_max`가 상태별로 다름 | q-based adaptation 제거 |
| PO2 | System condition이 feasible set을 바꾸는가 | Linux/PREEMPT_RT × realistic load | 일부 mode의 feasible/infeasible 판정이 조건별로 바뀜 | S-based selection 제거 |
| PO3 | 기존 단일 축 접근이 target failure를 보이는가 | fixed, period-only, W-only, M-only, q-only, S-only | F1--F6 중 사전 지정 failure 관측 | 해당 failure claim 제거 |
| PO4 | Joint admission이 failure를 방지하는가 | 독립 조절 조합 vs joint mode bank | 동일 timing constraint에서 F1/F2/F3 감소 | 제안 mechanism 재설계 |
| PO5 | Transition에서도 timing이 유지되는가 | steady-state admission vs transition admission | carry-over 포함 miss·backlog bound 만족 | Steady-state claim으로 제한 |
| PO6 | 여러 모델에서 결과가 유지되는가 | 대표 M 3--5개 | 효과 방향이 복수 구조에서 재현 | 특정 모델 결과로 제한 |

## 7. 최소 선행 실험 순서

1. Dataset gate
   - 정상→이상 전환 continuous waveform과 fault onset timestamp 존재 여부 확인.
   - 정적 segment만 있으면 detection delay claim을 제거하거나 별도 데이터 확보.
2. Diagnostic profile
   - `q × W × M`별 accuracy, recall, confusion matrix와 calibration 측정.
3. Timing profile
   - `(W,M) × OS × realistic load`별 mean, p99, observed max, memory 측정.
4. Dominance test
   - 가장 정밀한 mode가 가장 작은 필요한 H에서도 모든 조건을 만족하는지 확인.
5. Structural baseline test
   - fixed-light, fixed-precise, period-only, W-only, M-only, q-only, S-only 비교.
6. Joint policy test
   - F1--F6과 진단 지표를 동시에 비교.
7. Transition test
   - 정상→의심→경고 mode sequence에서 carry-over, backlog와 miss 측정.

## 8. 결과별 가능한 claim

| 관측 결과 | 허용되는 claim |
| --- | --- |
| 단일 지배 mode 존재 | Runtime adaptation 불필요. 현재 핵심 가설 기각 |
| q별 utility만 다름, 모든 mode timing-feasible | Machine-condition-aware selection. Slack claim 제외 |
| Feasible set만 load별로 다름, q별 utility 동일 | Runtime feasibility selection. Machine-condition claim 제외 |
| W/H만 trade-off, M 효과 없음 | `(W,H)` mode selection으로 축소 |
| q별 utility와 load별 feasible set 모두 다름 | q+S 역할 분리의 필요성 지지 |
| 독립 조절보다 joint mode bank가 F1--F6을 줄임 | Coupling-aware joint admission 기여 가능 |
| Transition admission이 steady-state 방식의 miss를 제거 | Mode-transition schedulability 기여 가능 |

## 9. Paper card 재검토 규칙

기존 paper card를 다시 볼 때 다음 항목을 추가로 추출함.

1. 논문이 보장하려는 failure는 무엇인가?
2. 어떤 상태를 관측하는가: application state, system state, 둘 다, 없음.
3. 어떤 action을 조절하는가: W, H/T, M, depth, scale, resource, budget.
4. Application requirement를 어떤 식으로 표현하는가: utility, safety, accuracy, deadline, 없음.
5. Feasibility를 어떤 식으로 표현하는가: utilization, RTA/DBF, slack, empirical latency, 없음.
6. Action 변경이 future release pattern 또는 transition demand를 바꾸는가?
7. Target scenario의 F0--F6 중 무엇을 막을 수 있는가?
8. Action 이름만 `(W,H,M)`으로 바꾸면 본 문제를 흡수할 수 있는가?
9. 흡수할 수 없다면 깨지는 가정은 무엇인가?
10. 그 차이를 증명하기 위해 필요한 실험 또는 theorem은 무엇인가?

## 10. 우선 재검토 순서

1. DNN-SAM [8]: q-like physical context + slack + fidelity가 이미 결합된 가장 강한 직접 비교군.
2. Imprecise DL [9]: `feasible set -> quality maximization` 구조가 본 정책과 거의 동일.
3. Decntr [11]: period/resource/transition을 포함해 generic framework가 본 문제를 흡수할 가능성이 가장 큼.
4. AMS [7]: condition-dependent deadline과 M 선택의 직접 비교군.
5. Physical-State-Aware Slack [10]: external state + formal slack 결합의 직접 비교군.
6. Elastic Task Model·ATER [1,2]: H-only adaptation의 failure baseline 설계에 필요.
7. ADW·AIL·AILWTLN [3--5]: W utility와 runtime timing의 분리 근거.
8. Industrial Internet FD [6]: q-only gated diagnosis baseline.

## 참고문헌

- [1] G. C. Buttazzo, G. Lipari, L. Abeni, "Elastic Task Model for Adaptive Rate Control," IEEE RTSS, 1998; G. C. Buttazzo, G. Lipari, M. Caccamo, L. Abeni, "Elastic Scheduling for Flexible Workload Management," IEEE Transactions on Computers, 2002.
- [2] R. Li, Z. Song, M. Lv, J.-M. Wu, C. J. Xue, J. Wang, N. Guan, "ATER: Adaptive Task Execution Rate Regulation for Enhanced Real-Time Performance in ROS 2," IEEE RTCSA, 2025.
- [3] M. Kim, S. Lee, D. Oh, B. Park, J. Jo, C. Lee, "Anomaly Deviation-Based Window Size Selection of Sensor Data for Enhanced Fault Diagnosis Efficiency in Autonomous Manufacturing Systems," Mathematics, 2026.
- [4] G. Tang, C. Yi, L. Liu, Z. Xing, Q. Zhou, J. Lin, "Integrating Adaptive Input Length Selection Strategy and Unsupervised Transfer Learning for Bearing Fault Diagnosis under Noisy Conditions," Applied Soft Computing, 2023.
- [5] G. Tang, C. Yi, L. Liu, X. Yang, D. Xu, Q. Zhou, J. Lin, "A Novel Transfer Learning Network with Adaptive Input Length Selection and Lightweight Structure for Bearing Fault Diagnosis," Engineering Applications of Artificial Intelligence, 2023.
- [6] S. Langarica, C. Rüffelmacher, F. Núñez, "An Industrial Internet Application for Real-Time Fault Diagnosis in Industrial Motors," IEEE Transactions on Automation Science and Engineering, 2020.
- [7] Y. Li, Z. Li, A. A. Arafat, D. Johnson, N. Sui, A. Gehi, Z. Guo, "Adaptive Model Selection for Real-Time Heart Disease Detection on Embedded Systems," IEEE RTCSA, 2025.
- [8] W. Kang, S. Chung, J. Y. Kim, Y. Lee, K. Lee, J. Lee, K. G. Shin, H. S. Chwa, "DNN-SAM: Split-and-Merge DNN Execution for Real-Time Object Detection," IEEE RTAS, 2022.
- [9] S. Yao, Y. Hao, Y. Zhao, H. Shao, D. Liu, S. Liu, T. Wang, J. Li, T. Abdelzaher, "Scheduling Real-Time Deep Learning Services as Imprecise Computations," IEEE RTCSA, 2020.
- [10] H. S. Chwa, K. G. Shin, H. Baek, J. Lee, "Physical-State-Aware Dynamic Slack Management for Mixed-Criticality Systems," IEEE RTAS, 2018.
- [11] R. Gifford, F. Galarza-Jiménez, L. T. X. Phan, M. Zamani, "Decntr: Optimizing Safety and Schedulability with Multi-Mode Control and Resource Allocation Co-Design," IEEE RTAS, 2024.
- [12] S. Xu, B. Ghosh, C. Hobbs, P. S. Thiagarajan, P. Joshi, S. Chakraborty, "Safety-Aware Implementation of Control Tasks via Scheduling with Period Boosting and Compressing," IEEE RTCSA, 2023.

## 근거 paper card

- `surveys/paper_cards/01_elastic_scheduling/elastic_scheduling_flexible_workload.md`
- `surveys/paper_cards/01_elastic_scheduling/ater_ros2_rate_regulation.md`
- `surveys/paper_cards/01_elastic_scheduling/decntr_multimode_codesign.md`
- `surveys/paper_cards/01_elastic_scheduling/safety_aware_period_boosting_compressing.md`
- `surveys/paper_cards/02_input_adaptive/anomaly_deviation_window_size.md`
- `surveys/paper_cards/02_input_adaptive/integrating_adaptive_input_length_noisy_tl.md`
- `surveys/paper_cards/02_input_adaptive/novel_tl_adaptive_input_lightweight.md`
- `surveys/paper_cards/03_rt_dnn_serving/adaptive_model_selection_heart_disease.md`
- `surveys/paper_cards/03_rt_dnn_serving/dnn_sam.md`
- `surveys/paper_cards/03_rt_dnn_serving/imprecise_deep_learning_services.md`
- `surveys/paper_cards/05_fault_diagnosis_app/industrial_internet_motor_fault_diagnosis.md`
- `surveys/paper_cards/08_misc_realtime_scheduling/physical_state_aware_slack.md`
