# Elastic Scheduling 서베이 정리

> 작성일: 2026-07-25  
> 대상 카드: `surveys/paper_cards/01_elastic_scheduling/` 19편  
> 목적: 이론 발전 계보와 실제 적용 사례를 구분해 본 연구의 연결점과 gap을 한눈에 파악한다.

본 연구 관련 기호 정의: W=입력 윈도우 크기, H=hop/진단 주기, M=모델, C(W,M)=모드별 실행시간, z=기계 상태, S=시스템 슬랙

---

## Section 1: 이론 발전 계보

### 읽는 법

- **C 가정** 열이 핵심이다. 기존 이론은 거의 C 고정을 전제한다. 본 연구의 C(W,M)처럼 모드에 따라 C가 달라지면 기존 feasibility 조건을 그대로 쓸 수 없다.
- **트리거** 열에 "system overload/부하"만 있으면, 기계 상태 z를 쓰는 본 연구와 차별화 지점이 생긴다.

| 논문 | 연도 | venue | 핵심 확장 (이전 대비) | 가변 변수 | C 가정 | feasibility 조건 | 트리거 | 본 연구와의 gap |
|---|---|---|---|---|---|---|---|---|
| Buttazzo, Lipari, Abeni [1] | 1998 | RTSS | **원형 제안** — spring 모델, elastic coefficient, period 압축 | period T | 고정 | EDF·RM utilization bound | rate 변경 요청, overload | W·H·M·z·PREEMPT_RT 없음 |
| Buttazzo, Lipari, Caccamo, Abeni [2] | 2002 | IEEE TC | 1998 확장 — decompression·SRP blocking 분석·period 안전 전환 규칙 | period T | 고정 | utilization bound + SRP blocking | overload, rate 요청 | 동일. 실행시간 추정은 future work |
| Buttazzo, Abeni [3] | 2000 | CDC | 런타임 C 추정 기반 period 피드백 (별도 계보) | period T | 런타임 관측값 (C_mean·C_max 가중합) | empirical estimated load | 커널이 관측한 실행시간 | soft RT (transient miss 허용). C(W,M) 모드 semantics 없음 |
| Chantem, Hu, Lemmon [4] | 2009 | IEEE TC | **일반화** — constrained deadline D≤T, QP optimization으로 확장 | period T, deadline D | 고정 | QP 기반 heuristic + EDF schedulability | system overload | vibration W·M·z 없음. heuristic, optimal 아님 |
| Tian, Gui [5] | 2011 | RTS | QoC feedback을 elastic scheduling과 결합한 control 특화 확장 | period T, utilization | 고정 | QoC 최대화 constrained optimization | QoC measurement, workload | control QoC ≠ vibration diagnosis utility |
| Marinoni, Buttazzo [6] | 2007 | IEEE TII | elastic scheduling + DVS 통합 — discrete freq·voltage mode 공동 조절 | period T, CPU freq/voltage mode | freq에 따라 scaled (WCET table) | elastic utilization + WCET table | processor utilization vs. available speed | CPU mode ≠ inference model M. z·W 없음 |
| Wang, Li, Wonham [7] | 2016 | IEEE TII | TDES supervisory control — multiple-period safe sequence 형식 합성 | period T (범위에서 선택) | 고정 WCET | non-blocking safe language (TDES) | initial model infeasible 시 offline reconfiguration | runtime slack·z·W·M 없음. offline only |
| Baruah [8] | 2023 | RTNS | constrained deadline elastic task에 PDA 직접 적용 — utilization 근사 대신 정확한 demand-bound | period T | 고정 | processor-demand analysis (exact EDF) | offline period assignment | C(W,M) 가변 없음. runtime trigger 없음 |
| Sudvarg, Gill, Baruah [9] | 2021 | RTS | O(n) 온라인 admission control — O(n²) compression 개선 | utilization, period | 고정 | utilization bound (linear time) | new task admission, overload | algorithm 효율성 연구. 도메인 없음 |
| Sudvarg, Gill, Baruah [10] | 2025 | LITES | quasilinear compression·multiprocessor 확장 (partition EDF, global EDF/RM) | utilization, period | 고정 | utilization bound (quasilinear/polynomial) | overload, resource 변화 | algorithm 효율성 연구. 도메인 없음 |
| Sudvarg et al. [11] | 2024 | RTAS | **harmonic task system 확장** — offline lookup table + online binary search | period T (harmonic 제약) | 고정 | harmonic EDF schedulability | available CPU bandwidth 변화 | H harmonic constraint 참고. z·W·M·PREEMPT_RT 없음 |
| Sudvarg et al. [12] | 2024 | RTSS | **subtask-level 확장** — parallel DAG subtask workload compression, core allocation | subtask workload, utilization, core | resource allocation별 profiling | federated scheduling demand-bound | limited resource, overload | multicore·DAG 중심. vibration 단일 태스크와 구조 다름 |
| Sudvarg (dissertation) [13] | 2024 | PhD | 위 Sudvarg 계열 논문 종합 (constrained-deadline·harmonic·subtask·FIMS·ORB-SLAM3) | 전체 | 전체 | 전체 | 전체 | 개별 출판 논문 우선 인용. dissertation은 배경 보조 |

### 이론 계보 흐름 요약

```
Buttazzo 1998 (원형: spring, period compression, EDF/RM bound)
    │
    ├── Buttazzo 2002 (SRP blocking, decompression 공식화)
    │
    ├── Buttazzo & Abeni 2000 (런타임 C 추정 → soft RT 별도 계보)
    │
    ├── Chantem 2009 (D≤T 일반화, QP optimization)
    │       │
    │       └── Baruah 2023 (PDA 정확한 demand-bound)
    │
    ├── Tian 2011 (QoC feedback 결합)
    │
    ├── Marinoni 2007 (DVS discrete mode 결합)
    │
    ├── Wang 2016 (TDES formal safe sequence 합성)
    │
    └── Sudvarg 계열 (2021→RTAS 2024→RTSS 2024→LITES 2025→dissertation)
             │
             admission control O(n) → harmonic → subtask·DAG → quasilinear
```

### 본 연구 관련 핵심 관찰

- **모든 이론 논문은 C 고정을 전제**한다. 본 연구의 C(W,M) — 즉 모드마다 실행시간이 달라지는 구조 — 는 기존 이론의 직접 적용 범위를 벗어난다.
- **트리거가 전부 시스템 부하나 utilization 변화**다. 기계 상태 z(anomaly score)를 트리거로 쓰는 사례는 없다.
- Buttazzo & Abeni 2000이 런타임 C 추정을 쓰는 가장 가까운 사례지만 soft RT이며 진단 utility 개념이 없다.
- Baruah 2023은 D < T 구조를 다루므로 본 연구 diagnosis task deadline model 선택 시 참고할 feasibility 분석 배경이다.

---

## Section 2: 실제 적용 사례

### 읽는 법

- **트리거** 열이 핵심이다. 기계 상태 z(anomaly score) 기반이 있으면 즉시 novelty 재점검 필요.
- **보장 수준** 열에서 hard, soft, empirical을 구분한다.

| 논문 | 연도 | venue | 응용 도메인 | 가변 변수 | 트리거 | 플랫폼·환경 | 보장 수준 | 본 연구와의 gap |
|---|---|---|---|---|---|---|---|---|
| Burgio et al. [15] | 2010 | ICCD | MPSoC 실시간 제어 (shared TDMA bus) | TDMA slot·bandwidth, period T | core workload 변화로 bandwidth 요청 발생 | STBus MPSoC, ERIKA RTOS, EDF | TDMA isolation + WCET table + elastic bound (hard 지향) | 중앙 master + offline WCET table 필요. z·W·M 없음 |
| Salman et al. [16] | 2021 | ETFA | 분산 CPS — compositional/hierarchical 실시간 | period T, reservation bandwidth | bandwidth 초과, period 변경 요청 | uniprocessor compositional evaluation | two-level (application period → system bandwidth) | vibration W·M·z·PREEMPT_RT 없음. reservation ↔ slack S mapping 별도 필요 |
| Gifford et al. (Decntr) [17] | 2024 | RTAS | 멀티모드 CPS 제어 (automotive) — controller + scheduling + resource co-design | controller, period T, core mapping, cache·bandwidth allocation | runtime mode-change event (ex. 장애물 감지) | Intel Xeon 16-core + CAT·MemGuard profiling / RPi 3 B+ WCET | DBF schedulability (mode별·transition별), linear plant safety invariant | **구조적으로 가장 가까운 비교군.** vibration window W, diagnosis utility, anomaly score, PREEMPT_RT measurement 없음 |
| Xu et al. (Safety-Aware) [18] | 2023 | RTCSA | Automotive safety-critical feedback control | common period T (boosting·compressing) | offline only — WCET·plant model·safety margin 입력 | Julia 구현, control model 평가 | weakly-hard constraint + automata schedule synthesis (offline) | runtime slack·z·W·M 없음. offline synthesis only. safety margin ≠ diagnosis utility |
| Li et al. (ATER) [19] | 2025 | RTCSA | ROS 2 자율 시스템 publish-subscribe task chain | sensor sampling rate R_tmr (timer period 역수) | runtime observer: message drop indicator, 처리율 vs. backlog | Intel Core i7 desktop, Ubuntu 22.04, ROS 2 Humble | empirical feedback regulation (hard deadline·admission 없음) | **diagnosis period H와 가장 직접 대응.** 그러나 vibration W·M, anomaly z, feasible-mode admission, PREEMPT_RT 없음 |

### 실제 적용 계열 관찰

- **Decntr** — 사전 profiling한 feasible mode set 안에서 runtime event로 mode를 선택하는 구조가 본 연구와 가장 가깝다. 차이: 제어 안전 invariant vs. 진단 utility, controller/resource co-design vs. W·H·M 선택.
- **ATER** — runtime rate regulation이 diagnosis period H 조절과 직접 대응된다. 차이: empirical soft RT vs. feasible-mode admission. 기계 상태 트리거 없음.
- **Safety-Aware** — weakly-hard miss와 application-level utility를 연결한다. 본 연구에서 일부 deadline miss를 허용할 경우의 비교군.
- **Burgio, Salman** — elastic scheduling을 시스템 자원(bus·reservation)과 결합한 사례. 본 연구는 단일 SBC에서 C(W,M)과 H를 함께 조절하므로 구조가 다름.

---

## 전체 Summary

### 본 연구가 채우는 자리

| 항목 | 기존 이론·적용 최선 사례 | 본 연구 |
|---|---|---|
| C 가정 | 고정 (이론), offline profiling table (Decntr) | 측정 기반 C(W,M) — 모드마다 달라짐 |
| 트리거 | 시스템 부하·utilization·bandwidth 변화 | 기계 상태 z (anomaly score) + 시스템 슬랙 S |
| 가변 변수 | period T (대부분), subtask workload (Sudvarg RTSS) | W, H, M 동시 |
| 플랫폼 | 이론 (uniprocessor), MPSoC, ROS 2 desktop | Pi Zero 2W + Linux/PREEMPT_RT |
| 도메인 | general RT, control, autonomous driving | 진동 기반 결함 진단 |
| 진단 utility 정의 | QoC (Tian), control safety (Decntr, Safety-Aware) | 미정 — anomaly score 기반 후보 |

### 인용 우선순위 (본 연구 원고 기준)

- **이론 배경**: Buttazzo 1998·2002 (원형), Chantem 2009 (일반화), Baruah 2023 (D<T)
- **runtime C 피드백 근거**: Buttazzo & Abeni 2000 (단, soft RT 한계 명시)
- **구조적 비교군**: Decntr 2024 (mode set offline synthesis + runtime selection)
- **H 조절 비교군**: ATER 2025 (rate regulation, empirical)
- **application safety 비교군**: Safety-Aware 2023 (weakly-hard miss 허용 논거)
- **알고리즘 overhead**: Sudvarg 2021, LITES 2025 (runtime mode switch 비용 배경)

---

## Section 3: 실제 적용 5편 심층 분석

> 각 논문의 주된 가정과 접근 방법을 단계별로 정리한다.  
> 표(Section 2)의 한 줄 gap과 함께 읽으면 본 연구 차별화 지점이 명확해진다.

---

### [15] Burgio et al. — Adaptive TDMA Bus Allocation and Elastic Scheduling (ICCD 2010)

#### 주된 가정

- 플랫폼: 다수의 core가 STBus TDMA 공유 버스로 통신하는 MPSoC. 각 core는 ERIKA RTOS + EDF 스케줄러.
- bus allocation(TDMA slot 수)에 따라 각 task의 C가 달라진다. 그러나 이 C 값들은 offline profiling으로 미리 측정해 **lookup table**로 저장한다. runtime에 C를 새로 측정하지 않는다.
- 각 task는 elastic task model: `(C_i, T_min,i, T_max,i, E_i)`. C_i는 bus allocation별 table에서 선택.
- 중앙 master node가 존재하며 모든 core의 bandwidth 요청을 집중해 조정한다.
- QoS 목표는 가중 합으로 정의되며, master는 이 목표를 기준으로 TDMA wheel을 재배분한다.

#### 접근 방법

1. 각 core의 periodic task가 sampling period를 바꾸려 할 때, bus bandwidth 수요가 달라지면 bandwidth 변경 요청을 master에게 보낸다.
2. 중앙 master가 모든 core의 요청을 수집하고 QoS-aware 알고리즘으로 TDMA slot을 재배분한다.
3. 각 core는 새로 배정받은 bus allocation을 lookup table에서 찾아 해당 C_i를 가져온다.
4. 각 core는 lookup한 C_i로 elastic scheduling 알고리즘을 로컬 실행해 period를 재계산한다.
5. coordination overhead는 실험에서 task computation time의 5% 미만으로 보고한다.

#### 보장 방식

- TDMA wheel → bus predictability (slot별 격리)
- offline WCET table → 각 core의 C 상한 보장
- elastic utilization bound → EDF schedulability

#### 본 연구와의 거리

C가 bus allocation에 따라 달라진다는 점은 본 연구의 C(W,M)와 구조적으로 유사하다. 그러나 C 결정이 offline table + 중앙 master 방식이고, vibration window W, 기계 상태 z, PREEMPT_RT single-SBC 구조와는 전혀 다르다.

---

### [16] Salman et al. — Scheduling Elastic Applications in Compositional Real-Time Systems (ETFA 2021)

#### 주된 가정

- 시스템 구조: 상위 system level + 하위 application level의 two-level 계층.
- application은 elastic task model (period 조절 가능).
- system은 Periodic Resource Model(PRM): 각 application에 bandwidth Θ와 period Π로 정의된 reservation 할당.
- uniprocessor 전제. 분산 CPS이지만 schedulability 분석은 compositional 방식으로 uniprocessor 단위로 처리.
- 기본 전략: application level에서 먼저 대응하고, 실패할 때만 system level 조정 요청.
- C는 고정 WCET. 가변 변수는 period T와 reservation bandwidth뿐.

#### 접근 방법

1. task execution time이 증가하거나 period 변경 요청이 발생하면, application elastic scheduler가 먼저 period T를 늘려 utilization bound를 만족하려 시도한다.
2. application level 조절로 해결되면 system level은 변경하지 않는다. 다른 application에 영향 없음.
3. application level 조절 실패 시(T_max에 도달해도 schedulable하지 않으면): system scheduler에 reservation bandwidth 증가 요청.
4. system scheduler가 PRM 조건(supply utilization bound) 안에서 해당 application의 Θ를 늘리고, 필요하면 다른 application의 Θ를 줄인다.
5. 재조정 후 각 application이 elastic scheduling을 재수행해 period를 다시 설정한다.

#### 보장 방식

- application level: elastic utilization bound 만족
- system level: PRM supply utilization 조건 만족
- 두 조건이 모두 충족될 때 schedulability 보장

#### 본 연구와의 거리

local adaptation → system-level adaptation 순서는 본 연구의 feasible mode set 필터링 구조와 개념이 유사하다. 그러나 reservation bandwidth ↔ system slack S의 mapping은 별도 정의가 필요하고, W/M/z는 전혀 없다.

---

### [17] Gifford et al. (Decntr) — Optimizing Safety and Schedulability with Multi-Mode Control and Resource Allocation Co-Design (RTAS 2024)

#### 주된 가정

- plant는 **선형 시스템**. mode가 바뀌면 controller도 교체되며 controlled invariant set으로 safety를 정의한다.
- mode graph가 사전에 완전히 알려져 있음. runtime에 새 mode가 생기지 않는다.
- task WCET: cache/bandwidth allocation에 따라 달라지는 함수 `e_i(c, w)`. 각 (c, w) 조합은 offline profiling으로 측정해 table화.
- multicore (16-core Intel Xeon): Intel CAT + MemGuard로 cache·bandwidth 격리.
- carry-over job의 worst-case demand를 분석 시점에 알 수 있다고 가정.
- transition마다 safe deadline relaxation 범위가 linear invariant set 조건으로 제한됨.

#### 접근 방법

**Offline co-design phase:**

1. 각 mode에서 controlled invariant set 조건을 만족하는 controller 후보와 safe sampling period 범위를 계산한다.
2. task의 resource sensitivity를 profiling하고 resource-sensitive task는 전용 core에 배치한다. 나머지는 공유 core에 배치.
3. 각 core의 cache partition과 memory bandwidth를 CAT·MemGuard로 배분한다.
4. 각 mode에서 EDF demand-bound test(DBF)를 수행해 schedulability 검증.
5. schedulable하지 않으면: task split/migrate, safe 범위 안에서 period 늘림, carry-over job deadline relaxation을 순서대로 시도.
6. 각 transition에서 carry-over demand + new-mode demand를 합산한 DBF test 수행.
7. 실패하면 new-mode period를 safe 범위 안에서 조정하거나 추가 deadline relaxation 적용.

**Runtime phase:**

1. mode-change event 발생 (예: 장애물 감지 신호).
2. 사전에 합성한 해당 mode의 resource allocation을 즉시 적용.
3. carry-over job의 deadline을 offline에서 계산한 safe 범위 안에서 조정.
4. 이후 new-mode의 normal EDF schedule로 전환.

#### 보장 방식

- 각 mode: EDF DBF schedulability (per-mode isolated analysis)
- 각 transition: carry-over + new-mode 복합 DBF
- control safety: linear plant invariant set에 대한 증명 (가정: linear plant, known mode graph)

#### 본 연구와의 거리

**구조적으로 가장 가까운 비교군.** feasible set을 offline에서 합성하고 runtime event로 적용하는 방식이 A_feasible(k) + runtime policy와 같은 결을 가진다. 차이는 세 가지다: control invariant set 대신 diagnosis utility Q(a,z), linear plant 대신 vibration fault-detection 문제, multicore resource co-design 대신 단일 SBC에서 W/H/M 선택.

---

### [18] Xu et al. (Safety-Aware) — Safety-Aware Implementation of Control Tasks via Scheduling with Period Boosting and Compressing (RTCSA 2023)

#### 주된 가정

- 여러 control task의 sampling period가 서로 다르며, 일부 조합은 utilization이 1을 초과한다.
- task별 WCET C_i, 기존 period P_i, plant safety margin `d_i^safe`가 모두 사전에 알려져 있다.
- plant는 finite horizon trajectory deviation으로 안전성을 판단할 수 있는 선형 시스템.
- common period를 채택하는 time-triggered schedule(LET model)을 사용한다.
- **runtime trigger 없음**: 전 과정이 offline synthesis.
- deadline miss를 일부 허용하되 physical safety property로 허용 범위를 제한한다(weakly-hard).

#### 접근 방법

1. WCET C_i를 내림차순으로 정렬한다.
2. 상위 k개의 WCET 합을 common period 후보로 생성한다: `P_k^C = Σ_{i≤k} C_i`.
3. 각 period 후보에서 plant를 re-discretize한다.
4. 원래 controller gain을 사용할 때 finite horizon 동안 trajectory deviation이 safety margin 이내인지 over-approximation으로 확인한다.
5. 실패 시: 새 period에 맞게 controller gain을 재계산하고 다시 확인한다.
6. 안전하다고 판정된 period에서 weakly-hard hit/miss constraint를 구한다 (어느 miss 패턴까지 허용 가능한지).
7. 모든 task의 constraint를 만족하는 time-triggered schedule을 automata-based synthesizer로 합성한다.
8. 평가 예시: 5개 task, 모든 deadline 요구 시 utilization > 1인 상황에서 28 ms common period에 safe schedule 발견, 40 ms에서는 controller gain 재계산 필요.

#### 보장 방식

- finite horizon trajectory deviation ≤ `d_i^safe` → safe 판정 (over-approximation이므로 safe 판정은 보장, 실패는 unsafe를 의미하지 않음)
- automata로 합성된 weakly-hard schedule → deadline miss 패턴이 safety 범위 내
- 하드웨어 실험 없음. Julia 구현, automotive control model 시뮬레이션.

#### 본 연구와의 거리

weakly-hard miss와 application-level safety를 연결하는 방법론은 본 연구에서 일부 deadline miss를 허용할 경우의 이론적 근거가 된다. 그러나 본 연구의 diagnosis utility Q(a,z), runtime slack S, W/H/M 선택은 없고, 전 과정이 offline이어서 runtime 조건 변화에 대응하지 못한다.

---

### [19] Li et al. (ATER) — Adaptive Task Execution Rate Regulation for Enhanced Real-Time Performance in ROS 2 (RTCSA 2025)

#### 주된 가정

- 플랫폼: ROS 2 publish-subscribe task chain. timer task가 선두에서 sensor sampling rate를 결정하고 downstream subscription callback들이 연쇄 활성화된다.
- execution time은 runtime에 **정규분포 (mean/std)** 로 모델링 가능하다고 가정한다.
- message drop이 bottleneck의 주요 지표다.
- source code를 수정하지 않고 외부 monitoring만으로 rate를 조절할 수 있다.
- rate의 상한은 사전에 설정된다. hard deadline, formal schedulability 보장은 요구하지 않는다.
- ROS 2 executor의 내부 scheduling 자체는 변경하지 않는다.

#### 접근 방법

**Runtime observer (LTTng live trace)**:
- observation period마다 각 executor에서 task/message event를 수집한다.
- 각 subscription의 publication rate, message drop 수, buffer 상태, execution time 분포를 측정한다.

**Rate 조절 판단 (2가지 지표)**:

1. MDI (Message Drop Indicator):
   - `drop 수 / 처리 가능한 message 수 > threshold θ_i` → bottleneck 존재, sampling rate를 낮춤.

2. ISRI (Increasing Sampling Rate Indicator):
   - 평균 execution time이 과거 분포보다 충분히 작아졌고
   - 현재 publication rate < 처리 능력이면 → rate를 사전 설정 상한까지 높임.

**Rate 계산 및 적용**:
- 예상 처리율과 buffer backlog를 기반으로 새 sampling rate `R_tmr`를 계산한다.
- timer task의 period를 `1/R_tmr`로 reset한다. downstream callback chain 전체 activation rate가 간접 조절된다.
- timer-reset overhead: ~80 μs.

#### 보장 방식

- empirical feedback regulation. hard deadline, utilization bound, WCET 기반 admission 없음.
- message drop 감소, CPU 낭비 감소, end-to-end average/max latency 개선을 실측으로 확인.
- rate가 사전 설정 상한을 초과하지 않음은 보장하지만 application utility 보장은 없음.

#### 본 연구와의 거리

**diagnosis period H 조절의 가장 직접적인 비교군.** runtime 관측 실행시간과 backlog로 rate를 조절하는 방식은 본 연구의 시스템 슬랙 S 기반 모드 전환과 같은 축에 있다. 차이: ATER는 empirical soft RT이고 anomaly-driven utility가 없으며 feasible-mode admission이 없다. 또한 sampling rate 감소에 따른 정보 손실(진단 품질 저하)을 평가하지 않는다.

---

### 이론 발전 계보

[1] G.C. Buttazzo, G. Lipari, L. Abeni, "Elastic Task Model For Adaptive Rate Control," Proc. 19th IEEE Real-Time Systems Symposium (RTSS), 1998

[2] G.C. Buttazzo, G. Lipari, M. Caccamo, L. Abeni, "Elastic Scheduling for Flexible Workload Management," IEEE Transactions on Computers, Vol. 51, No. 3, 2002

[3] G. Buttazzo, L. Abeni, "Adaptive Rate Control through Elastic Scheduling," Proc. 39th IEEE Conference on Decision and Control (CDC), 2000

[4] T. Chantem, X.S. Hu, M.D. Lemmon, "Generalized Elastic Scheduling for Real-Time Tasks," IEEE Transactions on Computers, 2009

[5] Y.-C. Tian, L. Gui, "QoC Elastic Scheduling for Real-Time Control Systems," Real-Time Systems, 2011

[6] M. Marinoni, G. Buttazzo, "Elastic DVS Management in Processors With Discrete Voltage/Frequency Modes," IEEE Transactions on Industrial Informatics, 2007

[7] X. Wang, Z. Li, W.M. Wonham, "Dynamic Multiple-Period Reconfiguration of Real-Time Scheduling Based on Timed DES Supervisory Control," IEEE Transactions on Industrial Informatics, 2016

[8] S. Baruah, "Improved Uniprocessor Scheduling of Systems of Sporadic Constrained-Deadline Elastic Tasks," RTNS 2023

[9] M. Sudvarg, C. Gill, S. Baruah, "Linear-Time Admission Control for Elastic Scheduling," Real-Time Systems, 2021

[10] M. Sudvarg, C. Gill, S. Baruah, "Improved Elastic Scheduling Algorithms for Implicit-Deadline Tasks," Leibniz Transactions on Embedded Systems (LITES), 2025

[11] M. Sudvarg, A. Li, D. Wang, S. Baruah, J. Buhler, C. Gill, N. Zhang, P. Ekberg, "Elastic Scheduling for Harmonic Task Systems," RTAS 2024

[12] M. Sudvarg, D. Wang, J. Buhler, C. Gill, "Subtask-Level Elastic Scheduling," RTSS 2024

[13] M.B. Sudvarg, "Improved Models of Elastic Scheduling," PhD Dissertation, 2024

[14] J. Orr, J. Condori Uribe, C. Gill, S. Baruah, K. Agrawal, S. Dyke, A. Prakash, I. Bate, C. Wong, S. Adhikari, "Elastic Scheduling of Parallel Real-Time Tasks with Discrete Utilizations," RTNS 2020

### 실제 적용 사례

[15] P. Burgio, M. Ruggiero, F. Esposito, M. Marinoni, G. Buttazzo, L. Benini, "Adaptive TDMA Bus Allocation and Elastic Scheduling," IEEE International Conference on Computer Design (ICCD), 2010

[16] S.M. Salman, S. Mubeen, F. Markovic, A.V. Papadopoulos, T. Nolte, "Scheduling Elastic Applications in Compositional Real-Time Systems," ETFA 2021

[17] R. Gifford, F. Galarza-Jimenez, L.T.X. Phan, M. Zamani, "Decntr: Optimizing Safety and Schedulability with Multi-Mode Control and Resource Allocation Co-Design," RTAS 2024

[18] S. Xu, B. Ghosh, C. Hobbs, P.S. Thiagarajan, P. Joshi, S. Chakraborty, "Safety-Aware Implementation of Control Tasks via Scheduling with Period Boosting and Compressing," RTCSA 2023

[19] R. Li, Z. Song, M. Lv, J.-M. Wu, C.J. Xue, J. Wang, N. Guan, "ATER: Adaptive Task Execution Rate Regulation for Enhanced Real-Time Performance in ROS 2," RTCSA 2025
