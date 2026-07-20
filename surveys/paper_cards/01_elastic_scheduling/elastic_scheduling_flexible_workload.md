# Elastic Scheduling for Flexible Workload Management

- **그룹**: 1 elastic_scheduling
- **출처/연도**: IEEE Transactions on Computers, Vol. 51, No. 3, March 2002
- **저자**: Giorgio C. Buttazzo, Giuseppe Lipari, Marco Caccamo, and Luca Abeni

## 두 질문
- **가변 변수**: periodic task의 execution rate/period. 논문의 현재 방법은 computation time `C`를 고정하고 period `T`를 허용 범위 안에서 조절한다.
- **트리거**: task의 period/rate 변경 요청, 새로운 task admission, overload 또는 underload에 따른 workload 재구성. Measured execution-time estimator는 현재 방법이 아니라 conclusion의 future work다.

## 1998년 원형과의 관계
- RTSS 1998 `Elastic Task Model for Adaptive Rate Control`의 journal extension 계열이다. 2002년 논문은 1998년 논문을 직접 인용한다.
- spring analogy, elastic coefficient, period compression, HARTIK QoS manager와 두 실험의 기본 구조는 상당 부분 이어받는다.
- 추가된 핵심은 decompression과 uniform rescaling의 체계화, SRP 기반 shared-resource blocking 분석, resource constraint가 있을 때의 compression 및 period-change 규칙이다.

## Abstract 3줄 요약
- multimedia와 adaptive control 같은 real-time application은 고정 period 중심의 classical real-time theory보다 더 큰 유연성을 요구한다.
- 논문은 task를 elastic coefficient를 가진 spring처럼 모델링해, 각 periodic task의 execution rate와 period를 조절하는 scheduling framework를 제안한다.
- overload 상황에서는 task period를 조절해 system utilization을 낮추고, current load에 따라 performance와 QoS를 제어한다.

## Conclusion 요약
- 결론은 elastic coefficient가 solution selection policy를 암묵적으로 인코딩하며, feasible configuration이 존재하면 task period를 조절해 underload 상태를 유지할 수 있다고 정리한다. 이 모델은 multimedia와 control application의 동적 rate tuning에 유용하고, fixed 또는 dynamic priority kernel 위에 구현 가능하다고 제시한다. 실행시간 estimator를 이용한 bandwidth 자동 할당은 구현된 기법이 아니라 future work다.

## 요점
- 플랫폼: HARTIK real-time kernel에 high-priority QoS manager로 elastic guarantee mechanism을 구현한다. 특정 상용 embedded board 비교가 목적은 아니다.
- 도메인: real-time scheduling, overload management, rate adaptation.
- 핵심 방법 (2~3줄): elastic task model을 flexible workload management framework로 확장해 task를 elastic coefficient가 있는 spring처럼 다룬다. 시스템 부하가 커지면 period를 늘려 utilization을 낮추고, 여유가 생기면 compressed task를 nominal period 방향으로 복원한다. SRP와 blocking term을 포함해 shared resource가 있을 때의 compression과 안전한 period transition도 분석한다.
- 정식화/수식 (있으면): task utilization `U_i=C_i/T_i`를 period로 조절해 전체 utilization을 schedulable bound 아래로 유지한다. Resource constraint가 있으면 blocking factor를 feasibility/compression 식에 포함한다.

## 0708 면담 기준 보강
- **실시간성 수준**: uniprocessor periodic task의 EDF/RM schedulability와 utilization bound를 다루며 HARTIK에서 동적 period 변경을 실험한다.
- **실행시간 가정**: 현재 모델은 `C` 고정, `T` 가변이다. Variable/measured execution time 대응은 future work다.
- **보장 방식**: elastic compression feasibility, utilization bound, SRP blocking 분석, period reconfiguration 시점 규칙을 사용한다.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): vibration fault diagnosis의 W/H/M 공동 선택, anomaly score 기반 machine condition trigger, PREEMPT_RT 실험은 다루지 않는다.
- 내 연구에 쓸 곳: system slack 또는 current workload를 보고 `H`를 늘리거나 줄이는 elastic scheduling 관련연구의 대표 근거.
- 인용할 문장 (있으면, 15단어 이내): "controlling a system's performance as a function of the current load"

## 불확실한 점
- 확인 필요: 정량 evaluation 항목과 수치는 manuscript에 넣기 전 원문 후반부에서 재확인.
- 확인 필요: 1998년판과 실험 및 설명이 상당 부분 겹치므로 두 논문을 정량 근거 두 개로 중복 집계하지 않는다.
