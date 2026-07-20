# Elastic Task Model For Adaptive Rate Control

- **그룹**: 1 elastic_scheduling
- **출처/연도**: Proceedings of the 19th IEEE Real-Time Systems Symposium (RTSS 1998), Madrid, Spain, pp. 286-295, December 1998
- **저자**: Giorgio C. Buttazzo, Giuseppe Lipari, and Luca Abeni

## 두 질문
- **가변 변수**: periodic task의 period/rate. 논문 모델에서는 computation time은 고정하고 period를 `Timin`과 `Timax` 범위에서 조절한다.
- **트리거**: task가 요구 rate를 바꾸는 경우, overload 조건, current load에 따른 QoS 조절.

## 2002년 확장판과의 관계
- 이 논문은 elastic task model을 최초 제안한 RTSS 1998 원형이다.
- Buttazzo et al., IEEE Transactions on Computers 2002 `Elastic Scheduling for Flexible Workload Management`는 이 논문을 직접 인용하며 같은 핵심 모델과 HARTIK 실험을 확장한다.
- 2002년판은 단순 플랫폼 변경이 아니라 decompression/rescaling 정리, SRP 기반 resource constraint와 blocking 분석, 안전한 period transition 규칙을 보강한다.

## 요점
- 플랫폼: HARTIK kernel에 QoS manager를 구현해 실험한다.
- 도메인: general real-time scheduling, multimedia, adaptive control systems.
- 핵심 방법 (2~3줄): 각 periodic task를 elastic coefficient와 period 범위를 가진 spring처럼 모델링한다. 한 task의 rate 변경이나 overload가 생기면 다른 task들의 period를 조절해 전체 utilization을 feasible bound 아래로 유지한다. EDF/RM 기반 고정 period 모델보다 유연한 rate control을 목표로 한다.
- 정식화/수식 (있으면): task `tau_i(C_i, T_i0, T_imin, T_imax, e_i)`. 실제 period `T_i`는 `[T_imin, T_imax]` 범위에 있고, utilization은 `C_i / T_i`로 조절된다.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): fault diagnosis의 window size W, model M, machine condition 기반 trigger, PREEMPT_RT/SBC 실험은 다루지 않는다.
- 내 연구에 쓸 곳: `H` 또는 diagnosis period를 elastic variable로 보는 시스템 축의 기본 근거.
- 인용할 문장 (있으면, 15단어 이내): "tasks' periods are treated as springs"

## 불확실한 점
- 확인 필요: HARTIK 실험의 구체 지표와 수치는 manuscript에 인용하기 전 원문 section 6에서 별도 재확인.
- 확인 필요: 원고에서는 1998년판을 최초 제안 출처로, 2002년판을 확장된 대표 근거로 구분하고 동일한 독립 방법 두 개처럼 세지 않는다.
