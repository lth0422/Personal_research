# Problem Formulation

이 문서는 원고의 problem formulation 초안이다.
확인되지 않은 실험 결과나 정량 수치는 넣지 않는다.

## 1. Diagnosis Task Model

We consider a vibration-based fault diagnosis task running on a resource-constrained edge device.
The task repeatedly receives a vibration signal segment, runs inference, and outputs a diagnosis result before its deadline.

Let the raw vibration stream be sampled at frequency:

```text
f_s
```

At diagnosis step `k`, the runtime selects one diagnosis mode:

```text
a_k in A
```

where `A` is a predefined candidate mode set.
Each mode is represented as:

```text
a = (W_a, H_a, M_a)
```

where:

- `W_a`: input window size in samples.
- `H_a`: hop size between consecutive diagnosis windows in samples.
- `M_a`: model or inference configuration.

The diagnosis period induced by hop size is:

```text
T_a = H_a / f_s
```

This arrival period is distinct from the end-to-end diagnosis deadline and the local inference budget:

```text
T_arrival(a) = H_a / f_s
D_e2e(a)     = end-to-end diagnosis deadline
B_infer(a)   = execution budget allocated to inference
```

Their relationship must be stated explicitly for each experiment. A model-selection threshold must not be treated as the task period or the end-to-end deadline unless the system model actually makes them equal.

This definition intentionally keeps `W` and `H` separate.
In vibration diagnosis, the amount of signal context and the frequency of diagnosis are different design choices.

## 2. Timing Variables

For each mode `a`, let:

```text
C_a
```

be the execution cost of the inference path under mode `a`.
In measurement-based evaluation, `C_a` should be reported as a distribution:

```text
C_a_mean, C_a_p95, C_a_p99, C_a_max
```

The observed response time is:

```text
R_a = C_a + I_a + L_os
```

where:

- `I_a`: interference from other workload or shared resources.
- `L_os`: operating-system scheduling latency or runtime delay.

For Linux PREEMPT_RT, this work should not claim a static hard real-time WCET unless it is actually proven.
The initial formulation should use empirical tail response time:

```text
R_a_p99 <= D_a
```

or conservative observed response time:

```text
R_a_max <= D_a
```

where `D_a` is the relative deadline of mode `a`.

## 3. Utilization and Feasibility

The utilization contribution of the diagnosis task under mode `a` is:

```text
U_a = C_a / T_a
```

A conservative tail-based version is:

```text
U_a_p99 = C_a_p99 / T_a
```

Let `U_bg` be the utilization of background workload or other real-time tasks.
The total utilization under mode `a` is:

```text
U_total(a) = U_bg + U_a
```

A mode is timing-feasible at step `k` if it satisfies both utilization and response-time constraints:

```text
U_total(a) <= U_bound
R_a_tail <= D_a
```

where `R_a_tail` can be `R_a_p95`, `R_a_p99`, or `R_a_max` depending on the target strictness.

The feasible mode set is:

```text
A_feasible(k) = { a in A | U_total(a) <= U_bound and R_a_tail <= D_a }
```

If `A_feasible(k)` is empty, the runtime must execute a predefined fallback mode or report overload.
This fallback rule must be specified explicitly in the algorithm section.

If fallback requires aborting or re-executing inference, its feasibility must include already consumed execution and transition cost:

```text
C_spent + C_abort + C_fallback <= B_infer
```

Detecting a deadline miss and then restarting a lighter model is not itself a timing guarantee. The initial implementation should therefore prefer offline-profiled admissible modes; re-execution is optional unless its budget is explicitly reserved.

After the 2026-07-08 meeting, this feasibility condition becomes the first research question rather than a secondary detail:

```text
When the machine condition becomes suspicious and the runtime prefers a more precise mode,
is that mode still schedulable, and how is that guaranteed?
```

The policy should therefore be defined as a feasibility-first policy:

```text
1. Build a mode bank A from profiled modes.
2. Reject modes that do not satisfy utilization and tail-response constraints.
3. Select the diagnostically best mode only inside A_feasible(k).
```

This means that "switching to a precise mode" is allowed only when the precise mode is in the feasible mode set.
If the most precise mode is infeasible, the runtime chooses the best feasible fallback.

## 3.1 KCC Utilization Motivation

Using the KCC measurements with non-overlapping windows:

```text
f_s = 8 kHz
T = W / f_s
```

and max observed latency:

| W | C max | T | U=C/T |
| ---: | ---: | ---: | ---: |
| 512 | 40.3 ms | 64 ms | 0.63 |
| 1024 | 129.8 ms | 128 ms | 1.01 |
| 2048 | 460.3 ms | 256 ms | 1.80 |

This shows the conflict directly.
Larger windows may provide more diagnostic context, but the execution cost grows faster than the period in this measurement.
Therefore, a precise mode can become infeasible unless the hop size or period is also adjusted.

The same table should be recomputed using average, p95, p99, and max execution times when the measurement logs are finalized.

## 4. Machine Condition and Diagnostic Utility

Let:

```text
z_k
```

be the machine condition at diagnosis step `k`.
Possible definitions include anomaly score, health index, model confidence, or fault probability.
The first implementation must choose one concrete definition.

Each mode has condition-dependent diagnostic utility:

```text
Q(a, z_k)
```

The utility should represent the diagnostic value of mode `a` under current machine condition.
For example:

- under normal condition, a lightweight mode may be sufficient;
- under suspicious condition, a larger window or stronger model may be more useful;
- under warning condition, lower detection delay may become more important.

The policy objective is:

```text
a*_k = argmax Q(a, z_k)
       subject to a in A_feasible(k)
```

This formulation separates diagnostic preference from timing feasibility.
The runtime first removes infeasible modes, then selects the diagnostically most useful feasible mode.

## 5. Slack Definition

The system slack at step `k` should be based on recent response-time history, not only mean latency.

Weak definition:

```text
S_k = D - mean(R_recent)
```

Preferred definitions:

```text
S_k_p95 = D - p95(R_recent)
S_k_p99 = D - p99(R_recent)
S_k_max = D - max(R_recent)
```

For a real-time systems paper, `S_k_p99` or `S_k_max` is more defensible than mean slack.
The exact choice should match the evaluation strictness and platform variability.

## 6. W/H/M Coupling Insight

The central modeling point is that input adaptation is not one-dimensional.
Reducing the window size `W` can reduce execution cost `C`, but it may also be paired with a smaller hop size `H`, which reduces the diagnosis period `T`.

Since:

```text
U_a = C_a / T_a
T_a = H_a / f_s
```

a smaller `W` does not necessarily reduce utilization or deadline pressure.

Case 1:

```text
W decreases
C decreases
H and T fixed
U = C/T decreases
```

This usually improves schedulability.

Case 2:

```text
W decreases
C decreases
H and T also decrease
U = C/T may increase
```

This can worsen schedulability even though each inference is faster.

Therefore, the runtime should select from mode tuples:

```text
(W, H, M)
```

rather than choosing window size alone.

## 7. Initial Problem Statement

Given:

- candidate mode set `A`;
- current machine condition `z_k`;
- recent response-time history `R_recent`;
- background workload estimate `U_bg`;
- deadline `D`;
- utilization bound `U_bound`;

select a diagnosis mode:

```text
a*_k = (W*, H*, M*)
```

that maximizes diagnostic utility while satisfying empirical real-time feasibility:

```text
maximize    Q(a, z_k)
subject to  a in A
            U_bg + C_a_tail / T_a <= U_bound
            R_a_tail <= D_a
```

where:

```text
T_a = H_a / f_s
```

The intended contribution is a runtime mode-selection formulation and policy for vibration fault diagnosis, not a new neural network architecture alone.

## 8. Open Design Choices

- What exact `W` values should be included in `A`?
- What exact `H` values should be included in `A`?
- What does `M` represent in the first implementation: distinct models, quantization options, early-exit variants, or runtime configurations?
- Is `z_k` an anomaly score, health index, confidence value, or thresholded fault probability?
- Which tail metric is used for feasibility: `p95`, `p99`, or observed max?
- What fallback mode is used when `A_feasible(k)` is empty?
- How much hysteresis is needed to avoid excessive mode switching?

These choices should be resolved before writing final algorithm and evaluation sections.
