# Decntr: Optimizing Safety and Schedulability with Multi-Mode Control and Resource Allocation Co-Design

- **그룹**: 1 elastic_scheduling
- **출처/연도**: IEEE 30th Real-Time and Embedded Technology and Applications Symposium, RTAS 2024, DOI 10.1109/RTAS61025.2024.00032
- **저자**: Robert Gifford, Felipe Galarza-Jimenez, Linh Thi Xuan Phan, Majid Zamani

## 두 질문
- **가변 변수**: Mode별 control implementation/controller, safe sampling period, task-to-core mapping, core별 cache와 memory-bandwidth allocation이다. Mode transition에서는 carry-over job 또는 첫 new-mode job의 deadline을 safe period 범위 안에서 늦출 수 있다.
- **트리거**: Runtime의 mode-change request다. 논문은 detected obstacle 같은 event를 예로 들며 mode가 바뀌면 사전에 합성한 mode/transition allocation을 적용한다. 어떤 controller, period와 resource allocation이 feasible한지는 known mode graph, task set, safety model과 profiled WCET를 사용하는 offline co-design에서 결정한다.

## Abstract 3줄 요약
- Multi-mode CPS는 mode와 load가 바뀔 때 control safety, robustness와 multi-core schedulability를 동시에 유지해야 한다.
- Decntr는 서로 다른 safe controller와 sampling period, task/core/shared-resource allocation, transition deadline relaxation을 공동 설계한다.
- Automotive control case study와 resource-sensitive benchmark 평가에서 safety를 유지하면서 기존 multi-mode allocation보다 schedulability와 robustness를 개선했다고 보고한다.

## Conclusion 요약
- Decntr는 controller switching과 multi-mode resource allocation을 결합해 mode별 task period를 조정하고, transition carry-over load를 safe deadline relaxation으로 완화한다. Linear CPS safety condition과 mode/transition schedulability analysis를 만족하는 allocation을 찾으며, 향후 nonlinear plant로 확장하는 것을 과제로 남긴다.

## 요점
- 플랫폼: Resource-sensitive benchmark profiling은 16-core Intel Xeon E5-2683 v4, 40 MB L3 cache, Intel CAT와 MemGuard에서 수행한다. Automotive controller WCET profiling에는 Raspberry Pi 3 Model B+를 사용한다.
- 도메인: Multi-mode cyber-physical control on multi-core platforms.
- 핵심 방법 (2~3줄): Mode마다 safety가 보장되는 controller/period 후보를 구성하고 resource sensitivity에 따라 task를 core에 배치한 뒤 cache와 bandwidth를 분배한다. Schedulable하지 않으면 task를 split/migrate하거나 safe 범위 안에서 period를 늘린다. Transition overload는 carry-over/new job deadline relaxation을 먼저 시도하고 필요하면 new-mode period를 늘린다.
- 정식화/수식 (있으면): Task WCET는 할당 resource에 따른 `e_i(c,w)`이고 mode utilization은 `sum e_i^m/p_i^m`이다. 각 mode는 EDF demand-bound test를, 각 transition은 carry-over demand와 new-mode demand를 포함한 DBF test를 통과해야 한다. Controller-switching invariant set으로 허용 period와 delayed deadline의 safety를 제한한다.

## 0708 면담 기준 보강
- **실시간성 수준**: Periodic task, EDF demand-bound schedulability, multi-core partition, cache/memory-bandwidth interference, carry-over job과 mode-transition deadline을 다룬다.
- **실행시간 가정**: `C`는 task와 cache/bandwidth allocation에 따라 달라지는 `e_i(c,w)`다. Benchmark를 resource configuration별로 profiling해 WCET table을 구성하므로 allocation-dependent cost지만 measurement 기반이다.
- **보장 방식**: Linear plant와 controlled invariant set 가정 아래 controller switching safety를 증명하고, 각 isolated mode와 모든 transition에 DBF schedulability test를 적용한다. Guarantee는 사전 정의된 mode, transition, WCET table과 safe controller/period set에 조건부다.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): Application mode와 resource 상태에 맞춘 controller/period/resource co-design은 다루지만 vibration diagnosis의 temporal window `W`, diagnosis utility, anomaly score, inference model semantics, PREEMPT_RT runtime measurement는 다루지 않는다.
- 내 연구에 쓸 곳: Feasible mode set을 offline에서 합성하고 runtime mode-change event에 적용하는 가장 가까운 구조적 비교군이다. 본 연구는 control invariant safety 대신 fault-detection utility/risk를 정의하고, `C(W,M)` profile과 system slack을 이용해 diagnosis mode를 선택하는 차이를 명확히 해야 한다.
- 인용할 문장 (있으면, 15단어 이내): "co-optimizing safety, robustness, and schedulability"

## 불확실한 점
- 확인 필요: Abstract의 schedulability 최대 11x 개선은 mode 수, utilization과 maximum-period-factor 조건에 따라 달라지므로 원고 인용 시 Figure 5 조건을 함께 명시한다.
- 확인 필요: Resource allocation 결과를 runtime에 적용하는 실제 mode-switch overhead와 OS/RTOS 구현 비용은 평가 범위에서 분리해 확인해야 한다.
- 확인 필요: Linear plant invariant-set safety를 vibration fault-detection utility로 직접 대체할 수 없으며 별도 application constraint가 필요하다.
- 확인 필요: Profiling 기반 WCET table이 unseen interference에서 유지되는지와 PREEMPT_RT에서 cache/bandwidth isolation을 어떻게 구현할지는 본 연구의 별도 문제다.
