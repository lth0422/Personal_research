# Generalized Elastic Scheduling for Real-Time Tasks

- **그룹**: 1 elastic_scheduling
- **출처/연도**: IEEE Transactions on Computers 2009
- **저자**: Thidapat Chantem, Xiaobo Sharon Hu, Michael D. Lemmon

## 두 질문
- **가변 변수**: task period, task utilization, task deadline.
- **트리거**: temporal overload, changing workload/environment, schedulability constraint.

## 요점
- 플랫폼: analytical framework and simulation/workload evaluation. Specific embedded platform 중심 아님.
- 도메인: periodic real-time tasks, overload adaptation, control-oriented real-time systems.
- 핵심 방법: elastic scheduling을 task schedulability와 performance metric 사이의 optimization problem으로 일반화한다. 기존 task compression algorithm이 desired utilization에서의 squared deviation을 최소화하는 quadratic programming 문제를 푼다는 점을 보이고, deadline < period task의 period selection 및 fixed-period system의 deadline selection까지 확장한다.
- 정식화/수식: `min sum_i w_i (U_i^max - U_i)^2` subject to utilization and bound constraints. EDF schedulability를 중심으로 period/deadline selection 문제를 다룬다.

## 내 연구 관점
- 한 줄 gap: system overload에 따른 period/deadline 조절 이론이며 vibration FD의 window W, model M, anomaly score, PREEMPT_RT 실험은 다루지 않는다.
- 내 연구에 쓸 곳: 본 연구의 utility 또는 slack-aware `(W,H,M)` 선택 문제를 optimization 형태로 정리할 때 기본 수식 배경.
- 인용할 문장: "trade-off between task schedulability and a specific performance metric"

## 불확실한 점
- 확인 필요: 실험에서 heuristic이 global optimal 또는 feasible solution을 찾는 비율은 workload/utilization level 조건별로 재확인해야 한다.
- 확인 필요: 이 논문의 deadline selection은 control task deadline 조절이며 본 연구의 diagnosis deadline과 직접 동일시하지 않아야 한다.
