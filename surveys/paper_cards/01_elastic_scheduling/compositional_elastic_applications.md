# Scheduling Elastic Applications in Compositional Real-Time Systems

- **그룹**: 1 elastic_scheduling
- **출처/연도**: ETFA 2021
- **저자**: Shaik Mohammed Salman, Saad Mubeen, Filip Markovic, Alessandro V. Papadopoulos, Thomas Nolte

## 두 질문
- **가변 변수**: application task period, application utilization, reservation bandwidth.
- **트리거**: execution-time exceedance, task period change request, insufficient reservation bandwidth.

## 요점
- 플랫폼: uniprocessor compositional scheduling evaluation. Specific embedded board 확인 필요.
- 도메인: hierarchical/compositional real-time systems with elastic applications.
- 핵심 방법: elastic task model과 periodic resource model 기반 compositional framework를 결합한 two-level adaptive scheduling을 제안한다. 우선 application level에서 period를 조절하고, 실패할 때 system reservation bandwidth adaptation을 요청해 다른 application에 미치는 영향을 줄인다.
- 정식화/수식: elastic application의 utilization bound와 PRM resource supply utilization 조건을 함께 사용한다.

## 내 연구 관점
- 한 줄 gap: hierarchical reservation과 period adaptation 중심이며 vibration FD W/H/M, anomaly trigger, PREEMPT_RT pipeline은 다루지 않는다.
- 내 연구에 쓸 곳: fault diagnosis task가 다른 tasks와 co-running될 때 local mode adaptation과 system-level bandwidth/slack 조정의 분리 근거.
- 인용할 문장: "two-level adaptive scheduling"

## 불확실한 점
- 확인 필요: evaluation 결과의 bandwidth adjustment reduction 수치는 Section IV 조건을 재확인해야 한다.
- 확인 필요: reservation bandwidth와 본 연구의 system slack S 사이의 mapping은 별도 정의가 필요하다.
