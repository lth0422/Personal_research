# Elastic Task Model For Adaptive Rate Control

- **그룹**: 1 elastic_scheduling
- **연구 섹션**: S3 elastic rate/workload (이론 원형), S5 schedulability
- **플랫폼 태그**: `PL-DESKTOP` (HARTIK real-time kernel; 물리 board·CPU 사양 미보고)
- **실행환경 태그**: `ENV-RTOS` (HARTIK kernel + high-priority QoS manager task)
- **출처/연도**: Proceedings of the 19th IEEE Real-Time Systems Symposium (RTSS 1998), Madrid, Spain, pp. 286-295, December 1998
- **저자**: Giorgio C. Buttazzo, Giuseppe Lipari, Luca Abeni
- **분석 노트**: `papers/01_elastic_scheduling/reviews/Elastic_Task_Model_정독_분석_Notion수식수정.pdf`, `.../Elastic_Utilization_재분배와_Period_Transition_설명.pdf`

## 두 질문
- **가변 변수**: periodic task의 period/rate `T_i`. Computation time `C_i`는 고정하고 period를 `[T_imin, T_imax]` 범위에서 조절해 utilization `U_i = C_i/T_i`를 바꾼다. 개인연구 `a=(W,H,M)` 중 **`H`(diagnosis period)에만 대응**하며 `W`, `M`은 다루지 않는다.
- **트리거**: task가 요구 rate를 바꾸는 경우(period-change request), 새 task admission, overload에 따른 QoS 조절. System load 기반이며 machine condition은 아니다.

## 2002년 확장판과의 관계
- 이 논문은 elastic task model을 최초 제안한 RTSS 1998 원형이다.
- Buttazzo et al., IEEE Transactions on Computers 2002 `Elastic Scheduling for Flexible Workload Management`는 이 논문을 직접 인용하며 같은 핵심 모델과 HARTIK 실험을 확장한다.
- 2002년판은 단순 플랫폼 변경이 아니라 nominal=minimum period 재정리, uniform rescaling, SRP 기반 resource constraint와 blocking 분석, 안전한 period transition 규칙을 보강한다.

## Abstract 3줄 요약
- Multimedia와 adaptive control은 고정 주기 real-time model보다 유연한 execution rate와 QoS 조정을 요구한다.
- 각 periodic task를 elastic coefficient와 period 범위를 가진 spring처럼 모델링해, 한 task의 rate 변경이 생기면 다른 task period를 자동 재조정한다.
- Overload를 유연하게 처리하고 current system load에 따라 QoS를 제어하는 단순·효율적 mechanism을 제공한다.

## Conclusion 요약
- Elasticity와 period range를 가진 spring 모델로 system을 underloaded 상태로 유지하고, 새 task를 즉시 reject하지 않고 기존 period를 늘려 admission을 시도할 수 있다. Overload가 끝나면 nominal period 방향으로 복구한다. Elastic coefficient가 solution-selection policy를 암묵적으로 인코딩하며, fixed/dynamic priority kernel 위에 구현 가능하다. Execution-time estimator 기반 자동 bandwidth 할당은 future work다.

## 요점
- 플랫폼: HARTIK kernel에 high-priority QoS manager를 구현해 실험. 물리 board·CPU·clock·timer resolution·QoS manager overhead는 미보고.
- 도메인: general real-time scheduling, multimedia, adaptive control systems.
- 핵심 방법 (2~3줄): 각 task를 `τ_i(C_i, T_i0, T_imin, T_imax, e_i)`로 두고, feasible하면 요청을 수락, infeasible하면 elastic coefficient에 비례해 다른 task utilization을 감소시킨다. `T_imax`에 도달한 task는 더 늘릴 수 없는 fixed task로 처리한다.
- 정식화/수식 (있으면): utilization bound는 scheduler별로 `U_p ≤ U_lub` (`EDF: 1`, `RM: n(2^{1/n}−1)`). 최소 가능 utilization `U_min = Σ C_i/T_imax`이고 `U_d < U_min`이면 infeasible. Elastic 재분배는 `U_i = U_i0 − (U_v0 − U_d + U_f)·e_i/E_v`, `T_i > T_imax`인 task는 `T_imax`로 고정 후 나머지에 대해 재계산한다.

## 핵심 메커니즘 해석
- **`e_i` 해석**: `e_i`가 큰 task는 더 중요한 task가 아니라 **더 많이 양보할 수 있는(더 유연한) task**다. 줄여야 할 총 utilization을 `e_i/E_v` 비율로 분배하므로, 중요한 task를 보호하려면 `e_i`를 작게 둔다. `e_i=0`은 system이 그 task period를 강제로 늘리지 않는다는 뜻이다.
- **period 변경 ≠ execution cost 변경**: period를 늘려도 한 job의 execution cost는 그대로다. 단지 job release 빈도와 장기 processor utilization이 줄어든다. 개인연구의 `C(W,M)`처럼 설정이 실행시간 자체를 바꾸는 구조가 이 논문에는 없다.

## 실험 (Section 6)
- **실험 1 (Dynamic period change)**: 4 task, 모든 nominal period 100 ms, 모든 `C_i`=24 ms. `t`=10 s에서 τ_1이 100→33 ms 감소 요청 → QoS manager가 나머지를 재조정: `T_1`=33, `T_2`=175, `T_3`=277, `T_4`=500 ms. `t`=20 s에서 전부 100 ms로 복귀.
- **실험 2 (Admission control)**: 3 task nominal 시작, `t`=10 s에 4번째 task 도착(현재 config는 infeasible) → 기존 task period를 늘려 admission: `T_1`:100→177, `T_2`:200→353, `T_3`:300→500, `T_4`=50 ms.

## 0708 면담 기준 보강
- **실시간성 수준**: uniprocessor periodic task의 EDF/RM utilization bound와 EDF demand 조건을 사용하고, period transition에 processor-demand criterion(Theorem 1)을 적용한다. Period 증가는 즉시, period 감소는 timing safety를 위해 해당 task의 next release에서 적용한다. HARTIK 실험은 period/instance 수를 시각화할 뿐 deadline-miss distribution이나 latency 통계는 측정하지 않는다.
- **실행시간 가정**: `C` 고정, `T` 가변. Window/mode에 따른 `C(W,M)` 변화 개념이 없다.
- **보장 방식**: **제한된 모델 안의 formal hard 보장**. Utilization bound + EDF demand theorem으로 스케줄 가능성을, Theorem 1로 period transition의 no-miss 조건을 정형 제시한다. 단 이 보장은 고정 `C_i`, periodic, implicit deadline(`D_i=T_i`), 단일 processor, resource constraint 없음이라는 가정에 한정된다.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): fault diagnosis의 window size `W`, model `M`, machine condition 기반 trigger, resource constraint, PREEMPT_RT/SBC 실험은 다루지 않는다. `D_i < T_i`인 constrained-deadline task도 다루지 않는다.
- 내 연구에 쓸 곳: `H`(diagnosis period)를 elastic variable로 보는 이론 원형이자 formal 보장의 골격. `e_i/E_v` 재분배 논리는 여러 진단 task 간 slack 양보 정책의 참조가 된다. 정책 사상 `π: (q, S) → (W, H, M)`과 비교하면 이 논문은 `H` 부분만, 그것도 system load trigger로만 담당한다.
- 인용할 문장 (있으면, 15단어 이내): "tasks' periods are treated as springs"

## 불확실한 점
- 확인 필요: 정확한 학회 DOI는 원문 서지에서 확인이 필요하다.
- 확인 필요: 원고에서는 1998년판을 최초 제안 출처로, 2002년판을 확장된 대표 근거로 구분하고 동일한 독립 방법 두 개처럼 세지 않는다.
- 확인 필요: HARTIK 실험의 실제 processor/hardware 사양은 원문에 기재되지 않아 개인연구 Pi Zero 2W/PREEMPT_RT platform 근거로 직접 쓸 수 없다.
