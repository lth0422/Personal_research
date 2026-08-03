# Physical-State-Aware Dynamic Slack Management for Mixed-Criticality Systems

> 보관 기록: 상세 재검토본인 `surveys/paper_cards/08_misc_realtime_scheduling/physical_state_aware_slack.md`로 대체되었다. 활성 paper card로 집계하지 않는다.

- **그룹**: 8 misc_realtime_scheduling
- **연구 섹션**: S5 Schedulability, Mode Transition, and Miss Semantics
- **플랫폼 태그**: `PL-DESKTOP` (MATLAB case study and simulation)
- **실행환경 태그**: `ENV-OTHER`
- **출처/연도**: IEEE Real-Time and Embedded Technology and Applications Symposium (RTAS), 2018, DOI 10.1109/RTAS.2018.00023
- **저자**: Hoon Sung Chwa, Kang G. Shin, Hyeongboo Baek, Jinkyu Lee

## 두 질문
- **가변 변수**: Physical state별 low/high-criticality execution-time budget, LC/HC-mode slack 사용량, mode-switch timing. Period나 input/model fidelity는 조절하지 않는다.
- **트리거**: Job release 시 관측한 external physical state, job completion 시 실제 사용한 execution time, high-criticality job의 budget overrun과 계산된 runtime slack.

## Abstract 3줄 요약
- Classic mixed-criticality model은 physical state에 따라 execution demand가 변해도 고정된 pessimistic WCET를 사용해 resource under-utilization과 불필요한 low-criticality job drop을 일으킬 수 있다.
- 논문은 physical-state-dependent WCET를 갖는 mixed-criticality task model, LC/HC-mode slack과 EDF-VD 기반 dynamic slack management를 제안한다.
- ADAS case study와 synthetic task-set 평가에서 mixed-criticality schedulability를 유지하며 baseline EDF-VD보다 low-criticality job drop을 크게 줄였다고 보고한다.

## Conclusion 요약
- Physical state에 따라 execution budget을 할당하고 release/completion event에서 unused resource를 reclaim하는 framework를 제시한다. EDF-VD의 mixed-criticality guarantee를 유지하면서 low-criticality service degradation을 줄였고, physical-state-aware dynamic virtual-deadline assignment를 future work로 남긴다.

## 요점
- 플랫폼: Adaptive cruise control과 autonomous vehicle steering MATLAB case study, uniprocessor synthetic task-set simulation.
- 도메인: Physical-state-aware mixed-criticality scheduling.
- 핵심 방법 (2~3줄): Task `tau_i`의 low/high-criticality WCET를 physical state `s_i`의 함수로 정의한다. Job release 시 현재 state에 해당하는 budget만 예약해 차이를 reclaim하고, completion 시 실제 미사용분을 다시 LC/HC-mode slack으로 계산해 mode switch 지연 또는 LC job 실행에 사용한다.
- 정식화/수식 (있으면): `tau_i=(T_i,C_i,D_i,L_i)`, `C_i={C_i^L(s_i),C_i^H(s_i)}`. EDF with Virtual Deadlines의 feasible scaling condition을 먼저 만족시킨 뒤 runtime slack의 safe lower bound를 계산한다.

## 0708 면담 기준 보강
- **실시간성 수준**: Implicit-deadline mixed-criticality task model, physical-state-dependent WCET, EDF-VD schedulability condition과 runtime slack lemmas를 제공한다.
- **실행시간 가정**: Physical state별 `C_i^L(s_i)`와 `C_i^H(s_i)` bound가 사전에 주어진다고 가정한다. Future job의 state를 알기 전에는 state 전체의 maximum budget을 사용한다.
- **보장 방식**: Feasible EDF-VD virtual deadline을 전제로 runtime slack의 lower bound를 계산하고, high-criticality deadline을 침해하지 않는 범위에서 budget을 재배분한다.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): External physical state와 dynamic slack을 이미 결합하지만 mixed-criticality control workload의 execution demand 관리이며, vibration diagnostic fidelity나 `W/H/M` 선택은 아니다.
- 내 연구에 쓸 곳: `machine/physical state + system slack` 조합 자체를 novelty로 주장할 수 없다는 직접 반증. State별 execution bound, future state를 모를 때 maximum을 예약하는 방식과 event-driven slack update를 본 연구의 feasibility 설계와 비교할 수 있다.
- 인용할 문장 (있으면, 15단어 이내): 없음.

## 불확실한 점
- 확인 필요: 본 연구의 anomaly score는 diagnostic requirement를 나타내는 연속 신호이고, 이 논문의 physical state는 state별 WCET budget을 결정한다. 두 trigger를 동일한 개념으로 표현하지 않는다.
- 확인 필요: 본 연구가 mixed-criticality를 채택하지 않는다면 LC/HC slack 식을 직접 가져오지 않고 설계 원칙만 비교한다.
