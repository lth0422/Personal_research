# Adaptive Rate Control through Elastic Scheduling

- **그룹**: 1 elastic_scheduling
- **연구 섹션**: S3 elastic rate and workload scheduling, S5 schedulability and miss semantics
- **플랫폼 태그**: 확인 필요
- **실행환경 태그**: `ENV-RTOS`
- **출처/연도**: Proceedings of the 39th IEEE Conference on Decision and Control, 2000, DOI `10.1109/CDC.2001.914704`
- **저자**: Giorgio Buttazzo, Luca Abeni

## 두 질문
- **가변 변수**: periodic task의 period/rate `T_i`. 실행시간 추정값 `Q_i`와 guarantee factor `k`는 period를 계산하는 feedback parameter다.
- **트리거**: 커널이 관측한 job 실행시간에 따른 estimated load, task 생성과 period 변경 요청. Elastic algorithm은 별도 주기 `P`로 실행된다.

## Abstract 3줄 요약
- 고정 parameter와 사전 WCET 추정에 의존하는 schedulability test가 실행시간 오차로 자원 낭비 또는 timing failure를 일으키는 문제를 다룬다.
- 커널이 실제 실행시간을 관측해 load를 추정하고 elastic task model로 periodic task rate를 자동 조절한다.
- Elastic coefficient에 따라 task utilization을 분배하여 관측 workload를 목표 utilization에 가깝게 유지한다.

## Conclusion 요약
- 실행시간을 커널에서 online 추정하여 명시적 WCET 지정 없이 task period를 조절하고, overload 시 기존 task rate를 낮춰 새 task를 수용하는 방법을 제시한다.
- HARTIK 실험에서는 실행시간 추정과 period adaptation이 deadline miss를 줄이고 utilization을 개선하지만, transient와 sporadic miss를 배제하는 hard guarantee는 제공하지 않는다.

## 요점
- 플랫폼: HARTIK real-time kernel 위 middleware. 물리 processor와 hardware 사양은 본문에서 확인되지 않았다.
- 도메인: general periodic real-time systems, multimedia와 adaptive control 사례.
- 핵심 방법 (2~3줄): 각 job이 끝날 때 task별 mean execution time과 observed maximum을 갱신한다. 두 값 사이의 `Q_i`로 load를 추정하고 elastic compression을 주기적으로 실행해 `T_i`를 허용 범위 안에서 조절한다.
- 정식화/수식 (있으면): `Q_i = C_mean,i + k(C_max,i - C_mean,i)`, `k in [0,1]`; estimated load `U_a = sum_i Q_i/T_i`; 목표는 `U_a`를 desired utilization `U_d`에 가깝게 유지하는 것이다.

## 0708 면담 기준 보강
- **실시간성 수준**: HARTIK RT kernel에서 deadline miss를 측정한다. 작은 `k`에서는 초기 overload recovery가 길고 sporadic miss가 남을 수 있으므로 soft real-time 성격이다.
- **실행시간 가정**: 사전 고정 WCET 대신 runtime mean과 observed maximum으로 `Q_i`를 갱신한다. 그러나 `Q_i`는 formal WCET bound가 아니며 diagnosis mode별 `C(W,M)` profile도 아니다.
- **보장 방식**: estimated utilization에 elastic feasibility test를 적용한다. `k=1`도 관측 최대를 사용할 뿐 미래 실행시간의 hard upper bound를 증명하지 않아 hard deadline 보장은 아니다. 근거: Sections 3--6.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): machine condition과 diagnostic utility, vibration `W`, model `M`, mode-dependent execution profile, transition carry-over와 PREEMPT_RT tail timing은 다루지 않는다.
- 내 연구에 쓸 곳: measured execution-time feedback로 diagnosis period `H`를 조절하는 직접 이론 비교군이자, empirical feedback와 hard schedulability guarantee를 구분해야 한다는 근거.
- 인용할 문장 (있으면, 15단어 이내): "Actual executions are monitored by a runtime mechanism"

## 불확실한 점
- 확인 필요: 실험에 사용한 processor와 hardware 사양은 본문에서 확인되지 않았다.
- 확인 필요: adaptation period `P`와 observed maximum을 갱신하는 history/window 정책이 실험 재현에 충분히 구체적으로 제시됐는지 추가 확인이 필요하다.
