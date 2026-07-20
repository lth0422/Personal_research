# Safety-Aware Implementation of Control Tasks via Scheduling with Period Boosting and Compressing

- **그룹**: 1 elastic_scheduling
- **출처/연도**: IEEE 29th International Conference on Embedded and Real-Time Computing Systems and Applications, RTCSA 2023, DOI 10.1109/RTCSA58653.2023.00031
- **저자**: Shengjie Xu, Bineet Ghosh, Clara Hobbs, P. S. Thiagarajan, Prachi Joshi, Samarjit Chakraborty

## 두 질문
- **가변 변수**: 여러 control task의 sampling period를 하나의 common period로 늘리거나 줄인다. 논문은 이를 period boosting과 compressing으로 부르며, 선택적으로 새 period에 맞춰 controller gain도 다시 계산한다.
- **트리거**: runtime trigger는 없다. Task별 WCET, 기존 period, plant model, safety margin을 입력으로 사용해 offline에서 common period와 weakly-hard schedule을 공동 합성한다.

## Abstract 3줄 요약
- 복잡한 software와 processor에서 보수적인 WCET를 사용해 모든 control-task deadline을 만족시키면 shared resource 구현이 비효율적일 수 있다.
- 논문은 모든 deadline 충족 대신 control safety를 목표로 두고, 서로 다른 sampling period를 공통 period로 boosting 또는 compressing한다.
- 공통 period의 time-triggered schedule을 safety constraint에 맞게 합성하며, 여러 automotive control model에서 접근법을 평가한다.

## Conclusion 요약
- 공통 sampling period 후보와 weakly-hard deadline hit/miss constraint를 연결해, 일부 deadline miss를 허용하면서도 plant trajectory가 safety margin 안에 머무는 schedule을 합성한다. 평가에서는 모든 deadline을 요구할 때 utilization이 1을 넘는 다섯 control task에 대해 28 ms common period에서 safe schedule을 찾았고, 40 ms에서는 controller gain 재계산이 필요했다.

## 요점
- 플랫폼: Julia 구현을 이용한 control-model 평가. 특정 embedded hardware 또는 RTOS 실험은 제시되지 않는다.
- 도메인: automotive를 포함한 safety-critical feedback control.
- 핵심 방법 (2~3줄): WCET를 내림차순으로 정렬하고 상위 `k`개 WCET의 합을 common period 후보로 만든다. 각 period에서 plant를 다시 discretize하고, 안전한 weakly-hard hit/miss constraint를 구한 뒤 automata-based time-triggered schedule을 합성한다. 원래 controller gain으로 실패하면 새 period에 맞춘 gain으로 다시 시도한다.
- 정식화/수식 (있으면): Task `i`는 `C_i`, `P_i`, `d_i^safe`를 가진다. 후보 common period는 `P_k^C = sum_{i<=k} C_i`이고, trajectory deviation이 `d(m,k) <= d_i^safe`이면 해당 weakly-hard constraint를 safe하다고 판정한다.

## 0708 면담 기준 보강
- **실시간성 수준**: WCET, period=deadline인 LET model, time-triggered schedule, weakly-hard deadline hit/miss pattern을 다룬다. Deadline miss를 모두 제거하지 않고 physical safety property로 허용 범위를 제한한다.
- **실행시간 가정**: Task별 `C_i`는 고정 WCET 입력이다. Input, machine condition 또는 model mode에 따른 `C(W,M)` 변화는 다루지 않는다.
- **보장 방식**: Finite horizon에서 plant trajectory deviation이 safety margin 이내인 weakly-hard constraint를 구하고, 모든 task의 constraint를 만족하는 schedule을 automata로 합성한다. Constraint 검사는 보수적 over-approximation을 사용하며, safe 판정은 보장을 제공하지만 실패는 unsafe를 뜻하지 않는다.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): Offline control-safety schedule synthesis이며 vibration diagnosis의 `W/H/M`, anomaly score, runtime system slack, PREEMPT_RT를 다루지 않는다.
- 내 연구에 쓸 곳: 진단 period `H`를 조절할 때 schedulability만이 아니라 application-level safety 또는 diagnosis utility constraint가 필요하다는 관련연구 근거로 활용할 수 있다. Weakly-hard miss 허용을 도입할 경우에도 유용한 비교군이다.
- 인용할 문장 (있으면, 15단어 이내): "satisfying system-level safety properties despite some deadline misses"

## 불확실한 점
- 확인 필요: 평가의 `H=100`은 finite analysis horizon이며 본 연구의 hop size 또는 diagnosis period `H`와 다른 기호다.
- 확인 필요: Safety margin과 finite initial condition에서 얻은 보장을 vibration fault diagnosis의 detection utility로 옮기려면 별도의 application model이 필요하다.
- 확인 필요: 특정 processor, OS, scheduler runtime overhead에 대한 실측은 확인되지 않았다.
