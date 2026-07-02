# Dual-Track Research Plan: RTAS 2027 Stretch Goal / RTCSA 2027 Main Target

> Codex note: 이 문서는 내부 연구 전략 문서로 사용한다. 공식 CFP, 실험 결과, 교수님 피드백이 확정되기 전까지 원고 본문에는 venue 일정이나 수용 가능성을 단정적으로 쓰지 않는다.
> Codex는 이 문서를 연구 방향을 좁히는 참고자료로 쓰되, 아래 `Codex Critical Review` 기준으로 비판적으로 반영한다.

## Codex Critical Review

### 받아들일 부분

- 핵심 방향인 `W/H/M coupling + machine condition + system slack`은 현재 `PROJECT_CONTEXT.md`, `surveys/claim_bank.md`, `manuscript/draft.md`와 일관된다.
- “작은 window가 항상 schedulability를 개선하지 않는다”는 주장은 강한 연구 포인트가 될 수 있다. `U = C/T`와 `T = H/f_s`를 함께 보여주면 단순 latency 최적화와 차별화된다.
- baselines는 적절하다: `Static-Light`, `Static-Heavy`, `Condition-Only`, `Slack-Only`, `Proposed`.
- slack은 mean이 아니라 `p95/p99/max response time` 기반으로 정의해야 한다는 지적은 타당하다.
- hysteresis 또는 switch penalty를 넣어 mode oscillation을 막는 방향도 systems paper 관점에서 중요하다.
- RTAS/RTCSA를 분리된 두 이야기가 아니라 같은 technical core의 strictness 차이로 보는 전략은 유지할 만하다.

### 경계할 부분

- RTAS 2027, RTCSA 2027 일정은 공식 CFP 확인 전까지 내부 가정이다. 원고에는 날짜를 넣지 않는다.
- RTAS를 목표로 하려면 “경험적 policy”만으로는 약할 수 있다. 최소한 formal mode model, feasible mode filtering, response-time/tail-latency 근거, baseline 대비 명확한 trade-off가 필요하다.
- Pi Zero 2W 단일 플랫폼만으로 top conference 주장을 하기에는 약할 수 있다. 단, core story가 충분히 강하면 RTCSA에는 가능성이 있다. 추가 플랫폼은 core 결과가 안정된 뒤 결정한다.
- PREEMPT_RT는 hard real-time guarantee처럼 표현하면 안 된다. “empirical deadline feasibility”, “tail response-time characterization”처럼 제한적으로 써야 한다.
- diagnostic utility `Q(a,z)`는 가장 취약한 부분이다. dataset, label, anomaly score, health index 중 무엇을 쓸지 빨리 정해야 한다.
- `M`이 서로 다른 model인지, quantization/runtime configuration인지, early-exit/variant인지 명확히 정의해야 한다. 애매하면 논문 기여가 흐려진다.
- `machine condition`이 실제로 runtime trigger로 계산 가능한지 검증해야 한다. condition estimation이 heavy하면 policy 자체가 무너진다.

### Codex가 다음 원고 작업에 반영할 기준

- 원고 초안은 “새 neural network”가 아니라 “schedulability-aware runtime mode selection” 중심으로 쓴다.
- `W/H/M`은 독립 변수가 아니라 미리 정의된 safe mode tuple set으로 시작한다.
- 실험 설계는 먼저 `mode feasibility table`과 `W/H coupling table`을 만든 뒤 policy 비교로 간다.
- claims는 `확인한 문헌 범위에서는` 또는 `we study` 수준에서 시작하고, 정량 결과가 나온 뒤 강화한다.

> Working direction: **Machine- and Slack-Aware Runtime Mode Selection for Deadline-Aware Vibration Fault Diagnosis on Resource-Constrained Edge Devices**  
> Purpose of this document: 정리된 연구 아이디어를 Codex/Claude/논문 초안 작업에 바로 넣기 위한 내부 기획 문서.  
> Status: **Very early draft / idea consolidation**. 확인되지 않은 수치, 실험 결과, venue 표현은 `TBD`로 유지한다.  
> Current planning date: **2026-07-02**  
> Venue strategy: **RTAS 2027 = stretch goal**, **RTCSA 2027 = realistic main target**.


---

# 0. Venue Strategy and Schedule Assumptions

This section should be treated as a planning guide, not as a final venue claim. As of 2026-07-02, official RTAS 2027 and RTCSA 2027 schedules are not yet fully confirmed in this draft. The plan below uses the most recent visible schedule patterns from RTAS 2026 and RTCSA 2026.

## 0.1 Public Schedule Anchors

Known recent schedule anchors:

- **RTAS 2026**
  - Submission deadline: **2025-11-13**
  - Author response: **2026-01-14 to 2026-01-18**
  - Notification: **2026-01-29**
  - Conference: **2026-05-12 to 2026-05-14**
  - Source to verify later: `https://2026.rtas.org/cfp/`, `https://2026.rtas.org/submission/`

- **RTCSA 2026**
  - Abstract/full paper deadline after extension: **2026-03-25**
  - Notification: **2026-05-04**
  - Camera-ready: **2026-06-12**
  - Conference: **2026-08-11 to 2026-08-13**
  - Source to verify later: `https://rtcsa2026.github.io/`

Working assumptions for 2027 planning:

```text
RTAS 2027 expected regular-paper deadline: around Nov 2026
RTCSA 2027 expected regular-paper deadline: around Mar-Apr 2027
```

Important rule:

```text
Do not write fixed RTAS 2027 or RTCSA 2027 dates in the manuscript until official CFPs are confirmed.
Use "expected", "working assumption", or keep the dates only in internal planning notes.
```

## 0.2 Two-Track Targeting Strategy

This project should be developed under two simultaneous tracks.

| Track | Role | Expected deadline window | Paper style | Risk | Purpose |
|---|---|---:|---|---|---|
| **RTAS 2027** | Stretch goal | Nov 2026, expected | Narrow, formal, timing-heavy systems paper | High | Force the work to become a real-time systems contribution |
| **RTCSA 2027** | Main target | Mar-Apr 2027, expected | Embedded/edge real-time ML application + runtime policy paper | Medium | Realistic full-paper target with stronger experiments |

Interpretation:

```text
RTAS 2027 is not the "safe" target.
It is a pressure target to sharpen the research into schedulability-aware adaptive inference.

RTCSA 2027 is the realistic main venue.
It gives enough time to improve experiments, writing, platform evaluation, and related work.
```

## 0.3 Venue-Specific Framing Difference

### RTAS 2027 framing

RTAS framing should emphasize:

```text
- formal mode/task model
- schedulability-aware mode selection
- W/H/M coupling analysis
- response-time and tail-latency feasibility
- workload interference
- fallback behavior under insufficient slack
- why the work is a real-time systems contribution
```

RTAS paper question:

```text
Can learning-enabled vibration diagnosis be formulated and managed as a schedulability-aware adaptive inference task?
```

RTAS contribution should not sound like:

```text
We made a fault diagnosis neural network faster.
```

It should sound like:

```text
We formulate and evaluate a runtime mechanism that selects diagnosis modes under real-time feasibility constraints.
```

### RTCSA 2027 framing

RTCSA framing can be slightly broader and more application/system oriented:

```text
- real-time vibration fault diagnosis on resource-constrained edge devices
- PREEMPT_RT timing behavior
- mode-level latency/accuracy trade-off
- adaptive runtime policy
- controlled workload interference
- practical edge implementation
```

RTCSA paper question:

```text
Can a resource-constrained edge platform maintain useful vibration diagnosis quality while controlling deadline misses through runtime mode selection?
```

## 0.4 Decision Gates

Use these gates to decide whether the RTAS submission attempt remains realistic.

| Gate | Date target | Required state | Decision |
|---|---:|---|---|
| **G1: Formulation freeze** | 2026-07-31 | Mode tuple `a=(W,H,M)`, candidate modes, timing measurement design, initial related-work map | If not done, RTAS becomes unlikely |
| **G2: Mode profiling** | 2026-08-15 | Per-mode `C_mean/p95/p99/max`, `T`, `U=C/T`, basic feasibility map | If not done, stop adding features and focus on RTCSA |
| **G3: Policy result** | 2026-08-31 | Static-Light, Static-Heavy, Condition-Only, Slack-Only, Proposed all runnable | If proposed does not show a clear timing/diagnosis trade-off, RTAS full is weak |
| **G4: Paper skeleton** | 2026-09-15 | Introduction, problem formulation, algorithm, evaluation plan, related work 70% draft | If not done, RTAS becomes a practice submission only |
| **G5: Result freeze** | 2026-10-15 | Main figures/tables fixed; no new core experiment design | If experiments are still changing, switch to RTCSA-first |
| **G6: RTAS submission decision** | 2026-10-25 | Professor review + internal stress test | Submit to RTAS only if story is narrow and defensible |

RTAS go/no-go rule:

```text
Submit to RTAS only if the paper has:
1. a clear W/H/M coupling result,
2. a clear schedulability-aware policy,
3. a clear proposed-vs-baseline trade-off result,
4. a manuscript that reads as a real-time systems paper.
```

If any of these is missing, keep developing for RTCSA 2027.

## 0.5 Timeline A: RTAS 2027 Stretch Goal

### July 2026: problem definition and profiling infrastructure

```text
Goal:
  Make the research executable, not just conceptual.

Must finish:
  - Freeze the one-sentence claim.
  - Define mode tuple a=(W,H,M).
  - Decide initial W/H/M candidate modes.
  - Set up Raspberry Pi Zero 2W + Linux/PREEMPT_RT environment.
  - Implement timing profiler.
  - Start per-mode response-time measurement.
  - Draft problem formulation and algorithm sections.

Do not do:
  - Add many platforms.
  - Invent a new fault diagnosis model.
  - Chase too many diagnostic metrics.
```

### August 2026: policy and baselines

```text
Goal:
  Produce the first result that can become a figure.

Must finish:
  - Mode feasibility map.
  - W/H coupling experiment.
  - Static-Light baseline.
  - Static-Heavy baseline.
  - Condition-Only baseline.
  - Slack-Only baseline.
  - Proposed condition+slack policy.
  - At least 2-3 workload interference levels.

Critical figure:
  Proposed should reduce deadline misses compared with Static-Heavy,
  while preserving more diagnostic utility than Static-Light.
```

### September 2026: paper assembly

```text
Goal:
  Turn results into a defensible RTAS-style manuscript.

Must finish:
  - Introduction with sharp gap.
  - Formal problem formulation.
  - Policy algorithm.
  - Evaluation section with main figures.
  - Related work table and positioning.
  - Limitations/threats to validity.
```

### October 2026: polish and decision

```text
Goal:
  Decide whether this is an RTAS submission or should wait for RTCSA.

Must finish:
  - Freeze experiments by mid-October.
  - Improve figures/tables.
  - Remove weak or overclaiming statements.
  - Stress-test against reviewer questions.
  - Prepare anonymous version.
```

### November 2026: expected RTAS submission window

```text
Submit only if:
  - the contribution is clearly real-time systems,
  - the main result is not merely "faster inference",
  - the paper can defend why machine+slack awareness is necessary.
```

## 0.6 Timeline B: RTCSA 2027 Main Target

If RTAS is not ready, the work should continue toward RTCSA 2027 without treating the RTAS attempt as failure.

### November-December 2026: consolidation after RTAS decision

```text
Goal:
  Convert the RTAS-pressure draft into a stronger RTCSA-ready paper.

Tasks:
  - Clean up all profiling data.
  - Add repeated experiments.
  - Improve workload interference design.
  - Strengthen PREEMPT_RT timing characterization.
  - Improve diagnostic utility evaluation.
  - Prepare a stronger system overview figure.
```

### January 2027: stronger evaluation

```text
Goal:
  Make the paper more complete and less fragile.

Potential additions:
  - More stable cyclictest/scheduler-latency characterization.
  - More complete load scenarios.
  - Better detection-delay or HI-quality metric.
  - Better ablation: no hysteresis, mean-slack vs p99-slack, condition-only, slack-only.
  - Optional second platform only if the first platform results are already solid.
```

### February 2027: manuscript maturation

```text
Goal:
  Move from internal draft to submission-quality manuscript.

Tasks:
  - Complete related work with actual citation keys.
  - Replace all TBD values that have experimental support.
  - Convert internal notes into polished claims.
  - Prepare tables and figures in final style.
  - Get professor and lab feedback.
```

### March-April 2027: expected RTCSA submission window

```text
Goal:
  Submit a mature embedded/real-time systems application paper.

RTCSA version should emphasize:
  - practical edge implementation,
  - timing characterization,
  - adaptive runtime policy,
  - vibration diagnosis application relevance,
  - deadline miss and tail-latency evaluation.
```

## 0.7 How to Use the Two Tracks in Writing

Use the same technical core, but adjust emphasis.

| Section | RTAS emphasis | RTCSA emphasis |
|---|---|---|
| Introduction | schedulability-aware adaptive inference | real-time edge diagnosis system |
| Motivation | W/H/M coupling and non-trivial feasibility | edge resource constraints and diagnosis quality/timing trade-off |
| Model | formal mode/task definitions | clear definitions plus practical explanation |
| Algorithm | feasibility filtering, fallback, hysteresis | runtime policy behavior and implementation |
| Evaluation | p99/max, miss ratio, interference, baselines | timing, diagnosis, platform practicality, load sensitivity |
| Discussion | guarantee limitations, empirical feasibility | deployment lessons, limitations, generalizability |

Do not maintain two separate technical stories. Maintain one story with two levels of strictness.

## 0.8 Bottom-Line Strategy

```text
Aim high with RTAS 2027 to force a strong real-time systems formulation.
Plan seriously for RTCSA 2027 as the realistic main target.
Keep the core contribution stable: W/H/M coupling + schedulability-aware machine/slack runtime mode selection.
```


---

# 1. One-Line Summary

본 연구는 진동 기반 결함 진단을 단순한 모델 경량화 문제가 아니라, **입력 윈도우 크기 `W`, hop/diagnosis period `H/T`, 모델 구성 `M`, 실행시간 `C`, deadline `D`, system slack `S`, machine condition `z`가 결합된 real-time adaptive inference problem**으로 정의한다.

핵심 아이디어는 다음과 같다.

> 현재 기계 상태에서 진단적으로 필요한 mode들 중, 현재 시스템 slack과 schedulability 조건을 만족하는 mode만 선택한다.

즉, 목표는 새로운 fault diagnosis neural network를 제안하는 것이 아니라, **diagnostic fidelity와 real-time feasibility를 함께 고려하는 runtime mode-selection policy**를 제안하는 것이다.

---

# 2. Why This Is Not Just a KCC Extension

KCC 수준의 기존 결과는 다음에 가깝다.

- STM32F407 + Zephyr RTOS 환경에서 neural fault diagnosis inference를 실제 MCU에 올림.
- CMSIS-NN과 window size 축소를 통해 deadline 내 추론 가능성을 보임.
- 평균 latency, deadline 만족 가능성, edge deployment feasibility를 확인함.

그러나 RTAS/RTCSA급 논문으로 확장하려면 단순히 다음을 주장하면 부족하다.

```text
We made inference faster on an embedded board.
```

대신 다음처럼 문제를 재정의해야 한다.

```text
We formulate vibration fault diagnosis as a real-time adaptive inference task,
where the runtime must jointly select input window size, diagnosis period, and model configuration
under machine-condition changes and system-slack constraints.
```

즉, 논문의 중심은 **model acceleration**이 아니라 **schedulability-aware runtime adaptation**이다.

---

# 3. Target Venue Perspective

This section describes the intellectual framing of each venue. The schedule-driven strategy is defined earlier in Section 0.

## 3.1 RTCSA-Level Framing

RTCSA 관점에서는 다음 키워드가 잘 맞는다.

- embedded and real-time systems
- edge AI / resource-constrained edge devices
- real-time machine learning
- deadline-aware inference
- Linux PREEMPT_RT / RTOS timing behavior
- application-driven real-time system evaluation

RTCSA용으로는 실제 platform evaluation과 timing metrics가 충분히 탄탄하면 가능성이 있다.

## 3.2 RTAS-Level Framing

RTAS를 목표로 한다면 더 강한 systems contribution이 필요하다.

RTAS급으로 가려면 연구가 다음 중 여러 요소를 포함해야 한다.

1. formal task/mode model
2. schedulability-aware mode-selection algorithm
3. response-time / tail-latency / interference-aware feasibility analysis
4. deadline miss를 줄이는 강한 실험 결과
5. 기존 elastic scheduling, imprecise computation, adaptive DNN serving과의 명확한 차이
6. static policy, condition-only policy, slack-only policy와의 비교
7. PREEMPT_RT 또는 RTOS-level timing behavior 분석

핵심은 다음이다.

```text
Bad RTAS framing:
We accelerate AI inference for fault diagnosis.

Good RTAS framing:
We design a schedulability-aware adaptive inference runtime for learning-enabled vibration diagnosis tasks.
```


## 3.3 Minimum Viable Paper by Venue

### RTAS minimum viable version

The RTAS version should be intentionally narrow. It can survive with one platform if the real-time systems contribution is strong.

Required:

```text
- formal mode model: a=(W,H,M)
- explicit W/H/M coupling analysis
- empirical or analytical feasibility filtering
- response-time and deadline-miss evaluation under interference
- baseline comparison proving that condition+slack is better than condition-only or slack-only
```

Optional but helpful:

```text
- stronger response-time model
- fallback/admission-control argument
- artifact/reproducibility package
- additional platform only if it does not distract from the core claim
```

### RTCSA minimum viable version

The RTCSA version can be broader and more implementation/application oriented.

Required:

```text
- working edge implementation
- PREEMPT_RT timing characterization
- clear mode-level latency/diagnosis trade-off
- adaptive policy evaluation
- practical lessons for real-time vibration diagnosis on constrained edge devices
```

Optional but helpful:

```text
- second platform
- more complete diagnostic metrics
- stronger comparison with RTOS/Zephyr motivation
- deeper manufacturing/fault-diagnosis discussion
```

---

# 4. Core Research Question

## 4.1 Main Question

```text
How can a resource-constrained edge device select vibration fault-diagnosis modes at runtime
so that diagnostic fidelity is improved when machine conditions become suspicious,
while deadline misses are avoided under varying system slack and workload interference?
```

## 4.2 More Technical Form

Given a set of candidate diagnosis modes:

```text
A = {a_1, a_2, ..., a_n}
```

where each mode is defined as:

```text
a = (W_a, H_a, M_a)
```

select a mode at each diagnosis step `k`:

```text
a*_k ∈ A
```

that maximizes diagnostic utility while satisfying real-time feasibility.

```text
maximize    Q(a, z_k)
subject to  R_a <= D_a
            U_total(a) <= U_bound
            a ∈ A
```

where:

- `W_a`: input window size of mode `a`
- `H_a`: hop size of mode `a`
- `T_a = H_a / f_s`: diagnosis period derived from hop size and sampling frequency
- `M_a`: model or inference configuration
- `C_a`: execution cost of mode `a`
- `R_a`: response time including inference, OS delay, and interference
- `D_a`: relative deadline
- `Q(a, z_k)`: diagnostic utility of mode `a` under machine condition `z_k`
- `z_k`: current machine condition score, anomaly score, health index, or confidence state
- `S_k`: measured system slack at step `k`
- `U_total(a)`: total system utilization if mode `a` is selected

---

# 5. Key Insight: Smaller Window Is Not Always Better

A central point of the paper should be:

> Reducing the input window size lowers the per-inference execution cost, but it does not necessarily improve schedulability when the hop size or diagnosis period is reduced accordingly.

This is important because vibration fault diagnosis has coupled variables:

- `W`: how much signal context one inference observes
- `H`: how far the window advances each diagnosis step
- `T`: how often the diagnosis task runs
- `C`: how long each inference takes
- `D`: deadline of each diagnosis instance
- `Q`: diagnostic utility

A naive view is:

```text
W decreases
→ C decreases
→ deadline satisfaction improves
```

But the actual real-time load depends more directly on:

```text
U = C / T
```

Therefore, if reducing `W` also reduces `H` and `T`, the system may run a smaller inference much more frequently.

Example conceptual cases:

## Case A: W decreases, T fixed

```text
W decreases
C decreases
T fixed
U = C/T decreases
```

This usually improves schedulability.

## Case B: W decreases, H/T also decreases

```text
W decreases
C decreases
T decreases
U = C/T may increase
```

This may degrade schedulability even though each individual inference is faster.

## Case C: W large, H small

```text
W large
H small
T small
C large
```

This can improve temporal context and detection delay, but may be heavy for the system.

## Contribution Candidate

```text
We show that input adaptation in vibration fault diagnosis is not a one-dimensional latency optimization problem.
Since input window size, hop size, diagnosis period, and model execution cost are coupled,
reducing the window size can either improve or degrade schedulability depending on the resulting mode utilization.
```

Korean explanation:

> 진동 결함 진단에서 입력 적응은 단순히 윈도우를 줄여 실행시간을 줄이는 문제가 아니다. 윈도우 크기, hop size, 진단 주기, 모델 실행시간이 결합되어 있기 때문에 작은 윈도우가 오히려 높은 진단 빈도와 결합되면 schedulability를 악화시킬 수 있다.

---

# 6. Mode Definition

## 6.1 Basic Mode Tuple

The current draft uses:

```text
mode a = (W, H, M)
```

Recommended detailed definition:

```text
mode a = (W_a, H_a, M_a)
```

where:

```text
W_a: input window size
H_a: hop size between consecutive diagnosis windows
T_a = H_a / f_s: diagnosis period
M_a: model or inference configuration
C_a: execution cost
D_a: deadline
Q_a: diagnostic utility
```

## 6.2 Candidate Mode Set

Initial candidate mode set could look like:

```text
A = {
  (W512,  H512,  M_small),
  (W512,  H256,  M_small),
  (W512,  H128,  M_small),
  (W1024, H512,  M_medium),
  (W1024, H256,  M_medium),
  (W2048, H1024, M_large),
  (W2048, H512,  M_large)
}
```

The exact modes are `TBD`.

Important design choice:

- Include modes where `W` is small but `H/T` is also small.
- Include modes where `W` is large but `H/T` is moderate.
- This allows the paper to show that the schedulability impact is not determined by `W` alone.

---

# 7. Timing and Schedulability Model

## 7.1 Per-Mode Cost

For each mode `a`, measure or estimate:

```text
C_a_mean
C_a_p95
C_a_p99
C_a_max
```

Possible response-time definition:

```text
R_a = C_a + I_a + L_os
```

where:

- `C_a`: model execution / inference cost
- `I_a`: workload interference from other tasks
- `L_os`: OS scheduling latency or kernel-level delay

On Linux PREEMPT_RT, a fully static WCET may be difficult. Initial paper can use empirical real-time feasibility:

```text
R_a_p99 <= D_a
```

or conservative observed maximum:

```text
R_a_max_observed <= D_a
```

## 7.2 Utilization

For each diagnosis mode:

```text
U_a = C_a / T_a
```

More conservative version:

```text
U_a_p99 = C_a_p99 / T_a
```

For a task set:

```text
U_total = U_bg + U_a
```

where:

- `U_bg`: background or system workload utilization
- `U_a`: diagnosis task utilization under selected mode

A mode may be considered feasible if:

```text
U_total <= U_bound
R_a_p99 <= D_a
```

## 7.3 Slack Definition

Avoid defining slack using only mean latency:

```text
Weak:
S = D - C_mean
```

Better:

```text
S_k = D - p99(R_recent)
```

or:

```text
S_k = D - R_recent_max
```

Possible definitions:

```text
S_k_mean = D - mean(R_recent)
S_k_p95  = D - p95(R_recent)
S_k_p99  = D - p99(R_recent)
S_k_max  = D - max(R_recent)
```

For RTAS-style framing, `S_k_p99` or `S_k_max` is more defensible than `S_k_mean`.

---

# 8. Machine Condition Model

Machine condition must be quantified, not just described verbally.

Candidate variables:

```text
z_k: anomaly score
h_k: health index
r_k: RPM variation or regime-change indicator
conf_k: model confidence
q_k: signal quality score
```

Initial simple condition states:

```text
Normal:  z_k < θ1
Watch:   θ1 <= z_k < θ2
Warning: z_k >= θ2
```

Runtime intuition:

```text
Normal:
  prefer lightweight mode to preserve slack

Watch:
  prefer balanced mode if feasible

Warning:
  prefer high-fidelity mode if slack allows;
  otherwise fallback to balanced or lightweight feasible mode
```

Important point:

> Machine condition changes the utility of each mode.

For example:

- In normal state, a lightweight mode may be enough.
- In suspicious state, a larger window or stronger model may have higher utility.
- In high-risk state, lower detection delay may become more important.

---

# 9. Diagnostic Utility

The policy needs a notion of diagnostic utility.

Possible utility metrics:

```text
classification accuracy
macro F1
fault recall
anomaly detection delay
health-index monotonicity
health-index trendability
confidence / uncertainty
feature quality
RPM-robustness
```

For early experiments, start with simple metrics:

- classification accuracy or macro F1 if labeled fault data is available
- detection delay if degradation sequence data is available
- HI quality if RUL/health-index data is used

A possible utility function:

```text
Q(a, z_k) = diagnostic value of mode a under condition z_k
```

More concrete scoring form:

```text
Score(a, k) = Q(a, z_k) - λ * U_a - μ * SwitchCost(a_prev, a)
```

where:

- `Q(a, z_k)`: condition-dependent diagnostic utility
- `λ * U_a`: penalty for system utilization
- `μ * SwitchCost`: penalty for frequent mode switching

But for a first version, it may be cleaner to use constrained optimization:

```text
Select the highest-utility mode among feasible modes.
```

That is:

```text
A_feasible(k) = {a ∈ A | R_a_p99 <= D_a and U_total(a) <= U_bound}

a*_k = argmax_{a ∈ A_feasible(k)} Q(a, z_k)
```

---

# 10. Proposed Runtime Policy

## 10.1 Core Policy Sentence

```text
The runtime first filters out modes that are infeasible under the current timing condition,
and then selects the diagnostically most useful mode for the current machine condition.
```

Korean:

> 현재 timing 조건에서 불가능한 mode를 먼저 제거하고, 남은 mode 중 현재 기계 상태에 가장 진단적으로 유용한 mode를 선택한다.

## 10.2 Algorithm Draft

```text
Algorithm: Machine- and Slack-Aware Mode Selection

Input:
  A: candidate mode set
  z_k: current machine condition score
  R_recent: recent response-time history
  a_prev: previously selected mode
  D: deadline
  U_bound: utilization bound

Output:
  a*_k: selected diagnosis mode

1. Estimate current timing slack:
     S_k = D - p99(R_recent)

2. Build feasible mode set:
     A_feasible = {a in A | p99(R_a under current load) <= D_a
                            and U_total(a) <= U_bound}

3. For each feasible mode a:
     estimate diagnostic utility Q(a, z_k)

4. Select candidate:
     a_candidate = argmax Q(a, z_k), a ∈ A_feasible

5. Apply hysteresis / switching rule:
     if condition or slack change is persistent:
         a*_k = a_candidate
     else:
         a*_k = a_prev

6. Execute diagnosis using a*_k
```

## 10.3 Hysteresis

Adaptive policy can switch too frequently. Add hysteresis:

```text
A mode switch is allowed only if the new condition/slack state persists for N consecutive diagnosis steps.
```

or:

```text
Switch only if Score(new_mode) - Score(current_mode) > δ
```

Potential switch penalty:

```text
Score(a) = Q(a, z_k) - λU(a) - μSwitchCost(a_prev, a)
```

This makes the policy more systems-oriented and avoids unstable mode oscillations.

---

# 11. Baselines

The proposed method must be compared against clear baselines.

| Baseline | Description | Expected weakness |
|---|---|---|
| Static-Light | Always uses lightweight mode | Low deadline miss, but lower diagnostic utility |
| Static-Heavy | Always uses high-fidelity mode | High diagnostic utility, but possible deadline miss under load |
| Condition-Only | Selects mode from machine condition only | Can overload system when slack is low |
| Slack-Only | Selects mode from timing slack only | Can miss diagnostic needs when fault condition becomes suspicious |
| Proposed | Uses both machine condition and slack | Should balance diagnosis quality and deadline feasibility |

The expected story:

```text
Proposed vs Static-Heavy:
  fewer deadline misses and lower tail latency

Proposed vs Static-Light:
  better diagnostic utility / lower detection delay

Proposed vs Condition-Only:
  more robust under workload interference

Proposed vs Slack-Only:
  better response to suspicious machine conditions
```

---

# 12. Evaluation Metrics

## 12.1 Timing Metrics

Must include more than mean latency.

```text
mean response time
median response time
p95 response time
p99 response time
max observed response time
jitter
deadline miss ratio
mode-switching overhead
mode-switch count
```

Important:

- RT-style evaluation should emphasize p95/p99/max and deadline miss ratio.
- Mean latency alone is insufficient.

## 12.2 System Metrics

```text
CPU utilization
memory usage
background load level
scheduler latency from cyclictest
thermal throttling indicator if relevant
```

## 12.3 Diagnostic Metrics

```text
accuracy
macro F1
fault recall
anomaly detection delay
HI monotonicity
HI trendability
false alarm rate
```

## 12.4 Adaptation Metrics

```text
time spent in each mode
mode transition count
unnecessary switch count
fallback count
percentage of time high-fidelity mode was rejected due to infeasibility
```

---

# 13. Experimental Design

## 13.1 Platforms

Planned platforms:

```text
Raspberry Pi Zero 2W + Linux
Raspberry Pi Zero 2W + Linux PREEMPT_RT
TBD additional board: Raspberry Pi 4/5, STM32F407, or other ARM edge platform
```

KCC STM32F407 + Zephyr results can be used as motivation or background, but should not be presented as new results for this paper unless carefully integrated.

## 13.2 Workload Interference

Need controlled load conditions:

```text
No background load
CPU load low / medium / high
Memory pressure
I/O or logging load
Competing periodic task
Sensor acquisition + inference + output pipeline
```

Possible tools:

```text
stress-ng
cyclictest
custom periodic background tasks
Linux perf / ps / top / ftrace if needed
```

## 13.3 Mode Feasibility Map

For each mode:

```text
W, H, T, M
C_mean, C_p95, C_p99, C_max
U_mean, U_p99
R_mean, R_p95, R_p99, R_max
D
deadline miss ratio
diagnostic utility
```

Expected table:

| Mode | W | H | T | M | C_p99 | U_p99 | Miss ratio | Diagnostic utility |
|---|---:|---:|---:|---|---:|---:|---:|---:|
| Light | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| Fast-hop | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| Balanced | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| Heavy | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

## 13.4 Key Experiment: W/H Coupling

Purpose:

> Show that smaller `W` does not always imply better schedulability when `H/T` also changes.

Experiment design:

- Compare modes with different `W` and `H` combinations.
- Plot or tabulate `C`, `T`, `U=C/T`, deadline miss ratio.
- Highlight cases where lower `C` still results in higher utilization or more deadline pressure due to smaller `T`.

Possible figure:

```text
x-axis: mode
left y-axis: C_p99
right y-axis: U_p99 or miss ratio
```

or heatmap:

```text
rows: W
columns: H
cell: U_p99 or miss ratio
```

## 13.5 Key Experiment: Adaptive Policy Comparison

Compare:

```text
Static-Light
Static-Heavy
Condition-Only
Slack-Only
Proposed
```

under:

```text
normal condition
watch condition
warning condition
changing machine condition
varying workload interference
```

Show:

- deadline miss ratio
- p99 response time
- diagnostic score
- detection delay
- mode transitions

---

# 14. Related Work Structure

Current related work outline is good. Keep the following 5-part structure.

## 14.1 Elastic Scheduling

Key point:

- Elastic scheduling adapts task periods/utilizations under overload.
- It supports the idea of treating diagnosis period `H/T` as elastic.
- But classical elastic scheduling does not handle vibration-specific window size `W`, model `M`, or machine-condition-driven utility.

Gap sentence:

```text
These studies provide a scheduling foundation for adapting diagnosis periods,
but they do not jointly model vibration window size, diagnosis model configuration,
and machine-condition-dependent diagnostic utility.
```

## 14.2 Input-Adaptive Perception and Fault Diagnosis

Key point:

- Input size affects accuracy and execution time.
- In fault diagnosis, window size affects noise robustness, frequency resolution, fault-pattern capture, and detection delay.
- Existing work often selects window size offline or based on signal characteristics only.

Gap sentence:

```text
Most input-adaptive fault diagnosis methods treat window size primarily as a signal-processing or accuracy parameter,
without considering deadline misses, system slack, or OS-level timing behavior.
```

## 14.3 Deadline-Aware DNN Serving

Key point:

- DNN serving systems select model exits, batch sizes, offloading targets, or model variants to meet SLO/deadline constraints.
- Useful comparison because they perform runtime quality-latency trade-offs.
- But they often target vision, GPU/edge-cloud serving, or request-level inference.

Gap sentence:

```text
Unlike DNN serving workloads, vibration fault diagnosis couples input window size,
diagnosis period, and model configuration, which jointly affect both diagnostic utility and real-time schedulability.
```

## 14.4 PREEMPT_RT and Edge Platform Studies

Key point:

- PREEMPT_RT studies show scheduling latency, jitter, and interference matter on Linux edge platforms.
- Raspberry Pi / ARM SBC studies motivate measuring p99/max latency and deadline misses.

Gap sentence:

```text
Platform studies characterize timing behavior, but they typically do not connect measured slack to adaptive diagnosis-mode selection.
```

## 14.5 Positioning

Core positioning:

```text
In contrast, this study treats vibration fault diagnosis as a real-time adaptive inference problem.
The runtime jointly selects input window size, diagnosis period, and model configuration using both machine condition and system slack.
```

---

# 15. Abstract Direction

## 15.1 Current Abstract Purpose

At the early stage, the abstract should not include unverified numbers.

Do not write:

```text
We reduce deadline misses by X%.
```

until verified.

Use `TBD` for all numbers.

## 15.2 Abstract Draft Candidate

```text
Vibration-based fault diagnosis on resource-constrained edge devices must balance diagnostic fidelity with timing predictability. While prior work has studied elastic scheduling for adapting task periods, input-adaptive perception for trading sensing fidelity against execution time, and deadline-aware DNN serving for selecting models or offloading targets, these directions typically treat machine condition, input window size, diagnosis period, model configuration, and operating-system timing behavior as separate concerns.

This paper presents a runtime mode-selection approach for real-time vibration fault diagnosis on embedded edge platforms. We model each diagnosis configuration as a mode consisting of an input window size, a diagnosis hop or period, and an inference model. The proposed policy selects modes using both machine condition and measured system slack. Under normal conditions, the runtime favors lightweight modes to preserve timing slack; under suspicious conditions, it switches to more informative modes when the measured timing budget allows. In this way, the policy connects diagnostic utility with real-time feasibility rather than optimizing inference latency or diagnostic accuracy in isolation.

The proposed design targets Linux PREEMPT_RT-based edge platforms such as Raspberry Pi Zero 2W and can be extended to RTOS-based microcontroller deployments. The evaluation compares static and adaptive diagnosis modes under controlled workload interference using response time, jitter, tail latency, deadline miss ratio, and diagnostic performance. The goal is not to introduce a new fault diagnosis neural network, but to provide a system-level runtime mechanism that coordinates diagnosis fidelity and real-time schedulability for vibration-based fault diagnosis on resource-constrained edge devices.
```

Later, replace final paragraph with result-focused claims:

```text
Compared with static high-fidelity and static lightweight baselines, the proposed policy reduces deadline misses by TBD while maintaining diagnostic performance within TBD of the high-fidelity configuration.
```

---

# 16. Contribution Draft

Potential contribution list:

```text
This paper makes the following contributions.

1. We formulate vibration fault diagnosis as a real-time adaptive inference task whose runtime mode is defined by input window size, diagnosis hop/period, and model configuration.

2. We analyze the coupling between input window size, hop size, execution cost, and diagnosis period, showing that smaller input windows do not necessarily improve schedulability when they require more frequent diagnosis.

3. We propose a machine- and slack-aware mode-selection policy that jointly considers diagnostic condition and measured timing slack when selecting the diagnosis mode.

4. We implement the proposed runtime on a resource-constrained Linux PREEMPT_RT edge platform and characterize response time, jitter, tail latency, and deadline miss behavior under workload interference.

5. We evaluate the trade-off between diagnostic performance and real-time feasibility against static lightweight, static high-fidelity, condition-only, and slack-only baselines.
```

Potentially shorten to 4 contributions if needed.

---

# 17. Suggested Paper Structure

```text
1. Introduction
   - Edge vibration fault diagnosis needs both diagnostic quality and timing predictability.
   - Window/model adaptation is promising, but not enough.
   - W/H/M coupling makes schedulability non-trivial.
   - We propose machine- and slack-aware runtime mode selection.

2. Background and Motivation
   - Vibration fault diagnosis and windowed inference
   - Real-time diagnosis task model
   - Why smaller windows are not always better
   - Motivating example from STM32/Zephyr or preliminary Pi measurements

3. System and Task Model
   - Mode tuple a=(W,H,M)
   - Period T=H/fs
   - Execution cost C, response time R, deadline D
   - Machine condition z
   - Slack S
   - Feasibility and utility definitions

4. Runtime Mode Selection Policy
   - Feasible mode filtering
   - Machine-condition-aware utility
   - Slack-aware fallback
   - Hysteresis / switching control
   - Algorithm pseudocode

5. Implementation
   - Raspberry Pi Zero 2W
   - Linux vs PREEMPT_RT
   - Inference runtime
   - Sensor/input pipeline or trace replay
   - Background workload generation

6. Evaluation
   - Experimental setup
   - Mode profiling
   - W/H schedulability coupling
   - Static vs adaptive baselines
   - Load sensitivity
   - Diagnostic performance
   - Overhead and switching behavior

7. Related Work
   - Elastic scheduling
   - Input-adaptive perception/fault diagnosis
   - Deadline-aware DNN serving
   - PREEMPT_RT/edge timing studies
   - Positioning

8. Discussion and Limitations
   - Empirical vs analytical guarantees
   - Dependence on machine-condition score
   - Generalization to other edge platforms
   - Hard real-time limitations of Linux PREEMPT_RT

9. Conclusion
```

---

# 18. Codex Work Plan

Use this section to guide Codex tasks.

## 18.1 Repository Organization

Recommended folders:

```text
manuscript/
  draft.md
  abstract.md
  intro.md
  related_work.md
  problem_formulation.md
  algorithm.md
  experiments.md
  tables/
    table1_related_work.md
    table2_modes.md
    table3_metrics.md
  figures/
    fig1_system_overview.md
    fig2_mode_feasibility_map.md
    fig3_policy_flow.md

notes/
  rtas_positioning.md
  schedulability_notes.md
  mode_definition.md
  related_work_claims.md

experiments/
  platform_setup.md
  mode_profiling_plan.md
  workload_interference_plan.md
  metrics_definition.md

scripts/
  TBD
```

## 18.2 Immediate Codex Tasks

### Task 1: Extract Core Claims

Ask Codex:

```text
Read manuscript/draft.md and notes/rtas_positioning.md.
Extract the main research claims into manuscript/intro.md.
Do not invent experimental numbers. Use TBD where necessary.
Emphasize that the contribution is a schedulability-aware runtime policy, not a new neural network.
```

### Task 2: Create Formal Problem Formulation

Ask Codex:

```text
Create manuscript/problem_formulation.md.
Define mode a=(W,H,M), period T=H/fs, execution cost C, response time R, deadline D, slack S, machine condition z, diagnostic utility Q, and feasible mode set A_feasible.
Include the key insight that smaller W can reduce C but may increase utilization if H/T also decreases.
Use equations in Markdown/LaTeX style.
Do not add unverified results.
```

### Task 3: Create Algorithm Section

Ask Codex:

```text
Create manuscript/algorithm.md.
Write pseudocode for machine- and slack-aware runtime mode selection.
The algorithm should:
1. estimate slack from recent response-time history,
2. filter infeasible modes,
3. estimate condition-dependent diagnostic utility,
4. select the highest-utility feasible mode,
5. apply hysteresis to avoid excessive switching.
Use clear variable definitions and no unverified performance claims.
```

### Task 4: Create Evaluation Plan

Ask Codex:

```text
Create experiments/mode_profiling_plan.md and manuscript/experiments.md.
Define baselines: Static-Light, Static-Heavy, Condition-Only, Slack-Only, Proposed.
Define timing metrics: mean, p95, p99, max response time, jitter, deadline miss ratio.
Define diagnostic metrics: accuracy, macro F1, detection delay, HI quality if applicable.
Define system metrics: CPU utilization, memory, cyclictest latency, background workload.
Use TBD for platform-specific values.
```

### Task 5: Related Work Table

Ask Codex:

```text
Update manuscript/tables/table1_related_work.md.
Use columns: Category, Representative direction, What it handles, What it misses, Relevance to our work.
Include Elastic Scheduling, Input-Adaptive Perception/Fault Diagnosis, Deadline-Aware DNN Serving, PREEMPT_RT/Edge Platform Studies.
Do not fabricate citations; use placeholder citation keys like [elastic-scheduling-TBD].
```

---

# 19. Important Writing Rules

## 19.1 Avoid Overclaiming

Do not write:

```text
This paper guarantees hard real-time execution.
```

unless a formal guarantee is actually developed.

Safer alternatives:

```text
This paper studies empirical deadline feasibility on Linux PREEMPT_RT.
```

```text
The proposed policy filters modes using measured tail response time and utilization constraints.
```

```text
The evaluation characterizes deadline miss behavior under controlled workload interference.
```

## 19.2 Use RTAS-Friendly Language

Prefer:

```text
response time
tail latency
jitter
deadline miss ratio
schedulability
feasible mode set
runtime adaptation
workload interference
mode-level utilization
fallback policy
```

Avoid making it sound like only a model paper:

```text
accuracy improvement only
model compression only
neural network architecture only
faster inference only
```

## 19.3 Keep KCC Results as Motivation

KCC STM32F407 + Zephyr results can be used as:

- motivation
- preliminary observation
- proof that window size strongly changes latency
- background for why runtime mode selection matters

But do not present KCC results as if they already prove the new RTAS-level contribution.

---

# 20. Open Questions

## 20.1 Mode Design

- What exact `W` values should be used?
- What exact `H` values should be used?
- Should `M` represent different models, different quantization modes, or different inference configurations?
- Should the policy choose `W` and `H` independently, or only from predefined safe mode tuples?

## 20.2 Machine Condition

- What is the first version of `z_k`?
  - anomaly score?
  - HI?
  - model confidence?
  - thresholded fault probability?
- Is condition computed from the same lightweight model or separate signal features?
- How to avoid condition estimation itself becoming expensive?

## 20.3 Slack Estimation

- Should slack use p95, p99, or max observed response time?
- How large should the recent history window be?
- Should OS scheduling latency from cyclictest be added as a safety margin?
- How should background load be estimated?

## 20.4 Diagnostic Utility

- Is the first evaluation classification-based or degradation/RUL-based?
- Should utility prioritize accuracy, fault recall, detection delay, or HI quality?
- How to define utility under normal vs suspicious condition?

## 20.5 Platform

- Is Raspberry Pi Zero 2W enough for the full evaluation?
- Should a stronger board like Raspberry Pi 4/5 be added for comparison?
- Should STM32F407 + Zephyr remain only motivation, or become a second platform?

---

# 21. Near-Term Action Items


## 21.0 Two-Track Immediate Priorities

The first month should not try to satisfy both venues with separate work. Instead, complete the shared core that both venues need.

Shared core by end of July 2026:

```text
- define candidate mode set A
- implement per-mode timing profiler
- produce first mode feasibility table
- draft problem formulation
- draft algorithm pseudocode
- update related-work table without inventing citations
```

RTAS-specific priority:

```text
Make W/H/M coupling and schedulability analysis central.
Do not add extra platforms before the core timing story is strong.
```

RTCSA-specific priority:

```text
Keep implementation notes, PREEMPT_RT setup details, and diagnostic application context organized,
because these will become valuable if the paper matures toward RTCSA 2027.
```

## Step 1: Clean Manuscript Skeleton

- [ ] Create `manuscript/problem_formulation.md`
- [ ] Create `manuscript/algorithm.md`
- [ ] Create `manuscript/experiments.md`
- [ ] Update `manuscript/related_work.md`
- [ ] Update `manuscript/tables/table1_related_work.md`

## Step 2: Define Candidate Modes

- [ ] Choose initial `W` values
- [ ] Choose initial `H` values
- [ ] Choose initial model/configuration set `M`
- [ ] Create `table2_modes.md`

## Step 3: Build Timing Measurement Script

- [ ] Measure per-mode inference time
- [ ] Measure response time including scheduling/interference
- [ ] Save mean/p95/p99/max
- [ ] Save deadline miss ratio

## Step 4: Build Workload Interference Setup

- [ ] No-load baseline
- [ ] CPU-load condition
- [ ] Memory/I/O-load condition if needed
- [ ] Competing periodic task condition

## Step 5: Implement Baseline Policies

- [ ] Static-Light
- [ ] Static-Heavy
- [ ] Condition-Only
- [ ] Slack-Only
- [ ] Proposed

## Step 6: Prepare First Internal Figure/Table Set

- [ ] Mode feasibility table
- [ ] W/H coupling heatmap or table
- [ ] Policy flow diagram
- [ ] Static vs adaptive comparison table

---

# 22. Strongest Paper Narrative

The strongest narrative is:

```text
Vibration fault diagnosis on edge devices is not only an accuracy problem and not only a latency problem.
The runtime must select how much signal to inspect, how often to inspect it, and which model to run.
These choices are coupled: a smaller window may reduce per-inference cost but increase diagnosis frequency and utilization.
Therefore, diagnosis mode selection must be both machine-aware and slack-aware.
```

Korean version:

```text
엣지 진동 결함 진단은 단순히 정확도를 높이는 문제도 아니고, 단순히 추론을 빠르게 하는 문제도 아니다.
런타임은 얼마나 긴 신호를 볼지, 얼마나 자주 진단할지, 어떤 모델을 실행할지를 함께 선택해야 한다.
이 선택들은 서로 결합되어 있다. 작은 윈도우는 한 번의 실행시간을 줄일 수 있지만, 더 짧은 hop/period와 결합되면 오히려 utilization과 deadline pressure를 증가시킬 수 있다.
따라서 진단 mode 선택은 machine condition과 system slack을 함께 고려해야 한다.
```

This should guide the entire manuscript.

---

# 23. Possible Titles

## Current Working Title

```text
Machine- and Slack-Aware Runtime Mode Selection for Deadline-Aware Vibration Fault Diagnosis on Resource-Constrained Edge Devices
```

## Shorter RTAS-Style Candidates

```text
Machine- and Slack-Aware Runtime Mode Selection for Real-Time Vibration Fault Diagnosis
```

```text
Slack-Aware Adaptive Inference for Real-Time Vibration Fault Diagnosis on Edge Devices
```

```text
Deadline-Aware Runtime Mode Selection for Edge-Based Vibration Fault Diagnosis
```

```text
Schedulability-Aware Adaptive Inference for Vibration Fault Diagnosis on Edge Devices
```

## Korean Candidates

```text
기계 상태와 시스템 Slack을 고려한 실시간 진동 결함 진단 런타임 모드 선택
```

```text
제한된 엣지 디바이스에서 실시간 진동 결함 진단을 위한 Schedulability-Aware 적응형 추론
```

```text
PREEMPT_RT 기반 엣지 환경에서 Deadline-Aware 진동 결함 진단을 위한 적응형 윈도우 및 모델 선택
```

---

# 24. Bottom Line

The current recommended strategy is dual-track:

```text
RTAS 2027:
Stretch goal. Use it to force a narrow, strong, schedulability-aware systems contribution.

RTCSA 2027:
Main realistic target. Use the additional time to build a mature embedded/edge real-time ML paper.
```

This research can be developed in three levels:

```text
Level 1: KCC/KSC-style
MCU/edge deployment and latency reduction for real-time inference.

Level 2: RTCSA-style
Runtime mode selection for real-time vibration fault diagnosis with platform evaluation.

Level 3: RTAS-style
Schedulability-aware adaptive inference runtime with formal mode model,
W/H/M coupling analysis, interference-aware feasibility filtering,
and strong timing evaluation.
```

Current goal if targeting RTAS:

> Develop the paper around **W/H/M coupling and schedulability-aware runtime mode selection**, not around fault diagnosis accuracy or model acceleration alone.
