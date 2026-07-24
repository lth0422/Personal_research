# Dynamic Multiple-Period Reconfiguration of Real-Time Scheduling Based on Timed DES Supervisory Control

- **그룹**: 1 elastic_scheduling
- **연구 섹션**: S3 elastic rate/workload, S5 schedulability/mode transition
- **플랫폼 태그**: `PL-DESKTOP`
- **실행환경 태그**: `ENV-OTHER`
- **출처/연도**: IEEE Transactions on Industrial Informatics, 2016, DOI 10.1109/TII.2015.2500161
- **저자**: Xi Wang, ZhiWu Li, W. M. Wonham

## 두 질문
- **가변 변수**: periodic task의 period를 정해진 multiple-period 범위에서 선택한다.
- **트리거**: shortest-period 초기 모델의 safe execution sequence set이 비어 non-schedulable로 판정될 때 reconfiguration을 수행한다.

## Abstract 3줄 요약
- Uniprocessor hard real-time task에 multiple periods를 부여하는 timed discrete-event-system formalism을 제안한다.
- Supervisory control theory로 가능한 safe execution sequences와 reconfiguration scenarios를 합성한다.
- 두 사례에서 EDF보다 더 많은 safe execution sequence 선택지를 제공한다고 보고한다.

## Conclusion 요약
- Non-preemptive hard real-time scheduling에서 initial model이 infeasible할 때 period reconfiguration으로 모든 safe sequence 후보를 제공하며, asynchronous/sporadic task 확장은 future work다.

## 요점
- 플랫폼: TTCT synthesis tool을 사용한 formal model/case study이며 runtime OS 구현은 확인되지 않는다.
- 도메인: uniprocessor industrial hard real-time scheduling.
- 핵심 방법 (2~3줄): task의 shortest period로 initial supervisor를 합성하고, 비어 있으면 period interval 전체에서 supervisor를 다시 합성한다. 안전한 transition/execution sequence를 열거한 뒤 사용자가 선택할 수 있게 한다.
- 정식화/수식 (있으면): task별 `[T_i,min,T_i,max]`와 TDES supervisor의 nonblocking safe language.

## 0708 면담 기준 보강
- **실시간성 수준**: hard real-time, non-preemptive schedule의 formal safety를 다룬다.
- **실행시간 가정**: WCET와 period range가 주어진 discrete-event model.
- **보장 방식**: TDES supervisory control synthesis로 unsafe sequence를 제거한다.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): runtime slack 측정, `W/M`, diagnostic utility, Linux/PREEMPT_RT 실측이 없다.
- 내 연구에 쓸 곳: `(W,H,M)` 전환 시 단순 endpoint feasibility뿐 아니라 transition sequence를 검증해야 한다는 S5 근거.
- 인용할 문장 (있으면, 15단어 이내): "all the safe execution sequences are provided"

## 불확실한 점
- 확인 필요: 논문은 이를 dynamic reconfiguration이라 부르지만 supervisor 합성의 offline/online 경계를 구현 관점에서 추가 확인해야 한다.
