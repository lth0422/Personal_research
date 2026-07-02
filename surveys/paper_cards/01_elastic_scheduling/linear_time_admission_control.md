# Linear-Time Admission Control for Elastic Scheduling

- **그룹**: 1 elastic_scheduling
- **출처/연도**: Real-Time Systems 2021
- **저자**: Marion Sudvarg, Chris Gill, Sanjoy Baruah

## 두 질문
- **가변 변수**: task utilization, task period after compression.
- **트리거**: online admission of a new task, overload/resource bound.

## 요점
- 플랫폼: algorithm note. Specific embedded platform 중심 아님.
- 도메인: preemptive uniprocessor elastic task scheduling, admission control.
- 핵심 방법: Buttazzo et al.의 O(n^2) feasibility/compression 및 admission control을 더 효율적으로 구현한다. Initialization은 O(n log n), online admission control은 O(n) 시간으로 수행한다.
- 정식화/수식: task `tau_i = (U_i^min, U_i^max, E_i)`와 elastic coefficient relation을 이용해 feasible utilization assignment를 계산한다.

## 내 연구 관점
- 한 줄 gap: admission control complexity 개선이며 vibration FD W/H/M와 machine condition trigger는 다루지 않는다.
- 내 연구에 쓸 곳: runtime mode/admission decision이 너무 무거우면 실시간성에 영향을 줄 수 있다는 scheduler overhead 배경.
- 인용할 문장: "on-line admission control"

## 불확실한 점
- 확인 필요: 짧은 note 성격이므로 원고에서 상세 algorithm 성능을 쓸 때는 follow-up LITES 2025 또는 dissertation과 함께 확인해야 한다.
