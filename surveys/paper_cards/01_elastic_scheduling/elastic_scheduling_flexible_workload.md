# Elastic Scheduling for Flexible Workload Management

- **그룹**: 1 elastic_scheduling
- **출처/연도**: IEEE Transactions on Computers, Vol. 51, No. 3, March 2002
- **저자**: Giorgio C. Buttazzo, Giuseppe Lipari, Marco Caccamo, and Luca Abeni

## 두 질문
- **가변 변수**: periodic task의 execution rate/period. workload management를 위해 task period를 조절한다.
- **트리거**: current workload, overload, underload, deadline miss 또는 measured execution time 기반 utilization 변화.

## 요점
- 플랫폼: 일반 real-time scheduling framework. 논문 초반 기준 특정 embedded board 중심은 아님.
- 도메인: real-time scheduling, overload management, rate adaptation.
- 핵심 방법 (2~3줄): elastic task model을 flexible workload management framework로 확장해 task를 elastic coefficient가 있는 spring처럼 다룬다. 시스템 부하가 커지면 period를 늘려 utilization을 낮추고, 여유가 있으면 rate를 높여 performance/QoS를 조절한다.
- 정식화/수식 (있으면): task utilization은 period 조절로 바뀌며, 전체 processor utilization을 schedulable bound 아래로 유지하는 것이 핵심이다.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): vibration fault diagnosis의 W/H/M 공동 선택, anomaly score 기반 machine condition trigger, PREEMPT_RT 실험은 다루지 않는다.
- 내 연구에 쓸 곳: system slack 또는 current workload를 보고 `H`를 늘리거나 줄이는 elastic scheduling 관련연구의 대표 근거.
- 인용할 문장 (있으면, 15단어 이내): "controlling a system's performance as a function of the current load"

## 불확실한 점
- 확인 필요: 정량 evaluation 항목과 수치는 manuscript에 넣기 전 원문 후반부에서 재확인.
