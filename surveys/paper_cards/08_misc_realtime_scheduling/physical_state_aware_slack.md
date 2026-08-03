# Physical-State-Aware Dynamic Slack Management for Mixed-Criticality Systems

- **그룹**: 8 misc_realtime_scheduling
- **연구 섹션**: S5 schedulability·slack management, 인접 mixed-criticality 비교군 (우리 문서의 [24])
- **출처/연도**: IEEE RTAS 2018, DOI 10.1109/RTAS.2018.00023
- **저자**: Hoon Sung Chwa, Kang G. Shin, Hyeongboo Baek, Jinkyu Lee
- **분석 자료**: `papers/08_misc_realtime_scheduling/reviews/physical_state_aware_slack.pdf`

## 위치 — 이 논문이 중요한 이유
- 우리 novelty를 지지·반증할 수 있는 단 하나의 논문. "외부 physical state + runtime slack 결합"을 이미 정형으로 다루므로, **결합 자체는 신규가 아님**을 보여준다.
- 분석의 핵심 검증 결과: **physical state는 state-conditioned execution budget/WCET만 정하고, output quality·diagnostic fidelity·model utility는 정하지 않는다.** 따라서 "우리는 anomaly state가 진단 fidelity를 정하고 W·H를 분리한다"는 차별점이 원문으로 방어된다.

## 두 질문
- **가변 변수**: task의 state-conditioned LC/HC execution budget `C_i = {C_i^L(s_i), C_i^H(s_i)}`. physical state에 따라 이번 job에 허용할 CPU 실행시간 상한을 바꾼다. window·period·model·output 품질은 바꾸지 않는다.
- **트리거**: job release 시 관측한 physical state `s_{i,j}` (외부 physical plant 상태) + actual execution time. state로 budget을 배정하고, 예약분과의 차이를 slack으로 reclaim한다.

## Abstract 3줄 요약
- 자율주행차 같은 safety-critical CPS는 assurance level이 다를 뿐 아니라 execution time이 physical environment에 따라 동적으로 변한다.
- physical-state-aware MC task model + LC/HC-mode slack 개념을 제안해, state-dependent WCET budget을 runtime에 배정하고 slack을 reclaim한다.
- EDF-VD 대비 MC-schedulability를 훼손하지 않으면서 LC job drop을 약 20배 줄였다.

## 논리 흐름 + Novelty
- 문제: Classic Vestal MC는 WCET를 physical state와 무관한 고정값으로 본다. 실제 CPS에서는 state에 따라 execution demand가 크게 달라진다(ACC MPC: steady 1 iteration, transient 최대 약 20배). state 무시 시 자원이 예약만 되고 불필요한 mode-switch·LC drop 발생.
- Physical-state-aware: LC/HC WCET를 상수가 아니라 physical state의 함수로 확장. future job은 state를 모르므로 max state budget 예약, release 시 state 관측 → 작은 budget 배정 → 차이를 slack으로 reclaim (2단계: release 시 `C^max − C(s)`, completion 시 `C(s) − AC`).
- Novelty: 새 control algorithm이나 quality-aware computation mode가 아니라, **physical-state-dependent execution demand를 formal MC scheduling model + slack reclamation에 통합한 scheduling contribution**이다.

## 핵심 검증 결과 (우리 novelty 방어)
| 검증 항목 | 결과 |
|---|---|
| physical state가 무엇인가 | 외부 physical plant 상태(ACC 앞차 거리·MPC active constraint·steady/transient, AVS steering, engine crankshaft speed, camera object 수, controller mode). 시스템 내부 부하 아님 |
| state가 무엇을 바꾸나 | **state-conditioned LC/HC WCET·per-job execution budget만.** output accuracy·diagnostic fidelity·result quality·model utility·window·sampling period·model selection objective는 안 바꿈 |
| accuracy/quality/utility 개념 | **없음.** `argmax Q(a,q)` 구조 없음. 최적화 대상은 LC drop 감소·mode-switch 감소·MC-schedulability 보존 |
| slack 용도 | quality 향상이 아니라 service preservation. LC mode에서 mode-switch 지연, HC mode에서 LC job 추가 실행 |

## 스케줄링 모델
- Task: `τ_i = (T_i, C_i, D_i, L_i)`, `C_i = {C_i^L(s_i), C_i^H(s_i)}`, `D_i = T_i` (implicit), `L_i ∈ {LC, HC}`, uniprocessor. HC task: `C_i^L(s_i) ≤ C_i^H(s_i)`.
- Max budget: `C_i^{L,max} = max_s C_i^L(s)`, `C_i^{H,max} = max_s C_i^H(s)`.
- EDF-VD feasibility (Eq. 4), virtual deadline `VD_i = x·T_i`:

$$\frac{U^L_{\tau^H}}{1 - U^L_{\tau^L}} \le x \le \frac{1 - U^H_{\tau^H}}{U^L_{\tau^L}}$$

- Slack: LC-mode slack `S_LC`, HC-mode slack `S_HC`를 구분. Job release·completion·mode-switch마다 갱신. Safe slack lower bound `S*_M = d_1(t_cur) − t_cur − p_M`, `p_M = Σ q_i`, `q_i = max(0, RC_i − (1−U)(d_i − d_1))` (reverse EDF, Algorithm 2).
- Theorem 1: Eq.4 만족 시 Algorithm 1 + EDF-VD가 no job deadline miss 보장 (Lemmas 5, 6). Slack은 priority ordering을 바꾸지 않고 실행 허용량만 조정.

## Deadline·RT 판정
| 판정 항목 | 결과 | 근거 |
|---|---|---|
| 명시적 deadline | O | `D_i = T_i` implicit-deadline |
| Schedulability 분석 | O | EDF-VD test, Lemmas 4-6, Theorem 1 |
| WCET 근거 | Formal + 혼합 | HC = code-flow analysis + instruction-cycle counting; LC = measurement worst-case |
| Mixed-criticality 보장 | O | LC behavior 시 전 task, HC behavior 시 HC task deadline 보장 |
| Deadline miss proof | O | Eq.4 전제 no-deadline-miss theorem |
| Hardware timing eval | X | MATLAB·synthetic simulation |
| tail/miss ratio 실험 | X | 이론 보장, empirical tail 미보고 |

- **RT 등급: H** (formal MC guarantee: explicit deadline + state-conditioned WCET model + EDF-VD schedulability + slack safety proof + no-deadline-miss theorem). 단 job release 시 physical state가 정확히 식별되고 `C_i^L(s)·C_i^H(s)`가 실제 execution upper bound라는 가정에 조건부.

## 평가 결과
- ADAS case (ACC+AVS HC + LC 4개, period 100 ms, states steady/transient, 80 s): LC drop 13.7% → 0.6% (**~21×**), mode-switch 201 → 12 (~16×), LC-mode interval 388 → 6637 (~17×), slack used 0 → 1753.
- Synthetic: 평균 LC drop Base 5.9%, **Base-PHY 9.6%**(state-aware budget만 쓰고 slack 관리 안 하면 오히려 나빠짐), Base-PHY-DSM 0.3% (~20×). → **state-aware budget과 slack reclamation을 함께 설계해야 함**이 핵심 결과.

## 개인연구 관점 — novelty 차원 ①~⑥
| 차원 | [24] | 근거 |
|---|:---:|---|
| ① 정확도 바꿈 | X | state가 execution budget·WCET만 바꿈. accuracy·fidelity·utility 개념 없음 |
| ② 외부 기계상태 트리거 | O | ACC distance·motion·steering·engine speed 등 external physical state |
| ③ slack을 별도 제약으로 | O | LC/HC-mode slack을 명시적으로 계산하고 안전한 추가 execution 제공 |
| ④ W·H·M 공동 (W/H 분리) | X | window·period·model을 runtime quality mode로 공동 선택하지 않음 |
| ⑤ 진동 FD | X | ADAS·generic CPS mixed-criticality |
| ⑥ 스케줄 가능성 검증 | O | EDF-VD condition + no-deadline-miss theorem |

→ **`[24] = (X, O, O, X, X, O)`. v1_4 문서 novelty 표와 원문이 정확히 일치함(검증 완료).**

## 개인연구와의 정확한 대응
| Chwa et al. | 개인연구 |
|---|---|
| External physical state `s` | Machine anomaly state `q` |
| `s → C^L(s), C^H(s)` (execution budget) | `q → Q(a, q)` (diagnostic utility) |
| State가 execution demand를 설명 | State가 mode별 diagnostic utility를 설명 |
| Slack을 추가 execution에 사용 | Slack이 feasible mode set 구성 제약 |
| LC/HC task service preservation | Diagnostic fidelity selection |
| Fixed task period | `H`를 mode 변수로 분리 |
| Quality ranking 없음 | `a ∈ F(k)` 중 utility 최대화 |

## 내 연구 관점
- 한 줄 gap:
  > Chwa et al.은 external physical state를 state-conditioned LC/HC execution budget에 매핑하고 slack으로 task service를 보존하지만, 본 연구처럼 anomaly state `q`가 `W/H/M` mode의 diagnostic fidelity `Q(a,q)`를 결정하도록 하지는 않는다.
- 내 연구에 쓸 곳: (1) novelty 방어의 결정적 근거 — "외부 상태+slack 결합은 이미 있으나 fidelity 선택·W/H 분리는 없다". (2) 2단계 slack reclaim(release·completion)과 safe slack lower bound(Algorithm 2)는 To-Do 10.2(이용률 bound 재유도) 참고. 단 우리 `S_k = D − max(R_recent)`는 empirical runtime margin이고, Chwa의 slack은 EDF-VD 기반 system-wide future demand를 반영한 schedulability-aware capacity라 성격이 다르다.
- Related Work 영어 한 줄:
  > Chwa et al. mapped external physical states to state-dependent LC and HC execution budgets and reclaimed dynamic slack while preserving mixed-criticality schedulability, but did not use physical state to rank or select computation modes by diagnostic fidelity.

## 불확실한 점
1. Formal model의 `s_i`는 추상 상태이며 모든 application 공통 state representation은 없음.
2. ACC/AVS case study는 state를 steady/transient 2개로 단순화.
3. state observation delay·sensor noise가 schedulability proof에 포함 안 됨.
4. Job release 이후 state가 변하면 budget 재갱신 여부 불명확(formal model은 release 시점 `s_{i,j}` 사용).
5. state 오분류로 작은 WCET budget 선택 위험 미분석.
6. High-confidence state-conditioned WCET 도출 과정은 논문 범위 밖.
7. ADAS WCET는 hardware cycle-level이 아니라 MPC iteration count × 2 ms 가정.
8. 진동 anomaly state에 적용하려면 anomaly classification latency·error를 WCET·guarantee에 포함해야 함.
9. 개인연구에서 `H`가 바뀌면 task utilization·future release pattern도 바뀌어 fixed-`T_i` slack analysis를 그대로 못 씀.
10. Machine anomaly state가 execution cost와 diagnostic utility를 동시에 바꿀 수 있으므로, 두 mapping을 분리해 profiling해야 함.
