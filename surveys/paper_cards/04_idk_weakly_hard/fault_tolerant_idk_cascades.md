# Optimal Synthesis of Fault-Tolerant IDK Cascades for Real-Time Classification

- **그룹**: 4 idk_weakly_hard
- **출처/연도**: RTAS 2024
- **저자**: Sanjoy Baruah, Iain Bate, Alan Burns, Robert I. Davis

## 두 질문
- **가변 변수**: IDK cascade ordering, classifier subset, deterministic fallback classifier, latency/deadline constraint.
- **트리거**: 없음=offline cascade synthesis. Runtime adaptation은 주된 기여가 아님.

## 요점
- 플랫폼: 알고리즘 및 case-study evaluation 중심. 특정 RTOS/PREEMPT_RT platform 실험은 확인되지 않음.
- 도메인: real-time classification, IDK classifier cascade, fault-tolerant perception.
- 핵심 방법: IDK classifier가 잘못된 real class를 반환할 수 있는 fault model을 도입하고, exclusivity set과 DAG shortest-path formulation으로 fault-tolerant IDK cascade를 합성한다. deadline이 있으면 deadline을 초과하는 DAG edge를 제거해 hard deadline constraint를 반영한다.
- 정식화/수식: n개 IDK classifier와 deterministic classifier를 probability space와 execution-time model로 표현한다. cascade synthesis는 DAG shortest path 문제로 환원된다.

## 내 연구 관점
- 한 줄 gap: real-time classification의 latency/fault-tolerance trade-off를 다루지만 vibration FD, W/H/M runtime mode selection, machine condition, PREEMPT_RT는 다루지 않는다.
- 내 연구에 쓸 곳: model cascade 또는 fallback classifier를 사용하는 deadline-aware inference 비교군.
- 인용할 문장: "latency constraint"

## 불확실한 점
- 확인 필요: case study의 classifier 구성과 expected duration 수치는 원고 인용 전 Table II~VI 조건을 재확인해야 한다.
- 확인 필요: 여기서 fault tolerance는 classifier wrong output에 대한 fault model이며, mechanical fault diagnosis의 machine fault와 용어가 충돌하지 않게 구분해야 한다.
