# Scheduling Elastic Applications in Compositional Real-Time Systems

- **그룹**: 1 elastic_scheduling
- **연구 섹션**: S3 elastic rate/workload (주 배치), S5 schedulability/hierarchy
- **플랫폼 태그**: `PL-DESKTOP` (분석적 프레임워크 + 시뮬레이션; 특정 embedded board 없음)
- **실행환경 태그**: `ENV-OTHER` (uniprocessor 계층적 스케줄링 모델; 900 tasksets 시뮬레이션 평가)
- **출처/연도**: IEEE ETFA 2021 (26th Int. Conf. on Emerging Technologies and Factory Automation), DOI 10.1109/ETFA45728.2021.9613375
- **저자**: Shaik Mohammed Salman, Saad Mubeen, Filip Marković, Alessandro V. Papadopoulos, Thomas Nolte (ABB / Mälardalen University)
- **분석 노트**: `papers/01_elastic_scheduling/reviews/Scheduling_Elastic_Applications_in_Compositional_Real-Time_Systems.pdf`

## 두 질문
- **가변 변수**: 두 계층에서 — (1) 앱 수준의 태스크 주기 `T` (elastic 압축), (2) 시스템 수준의 reservation 파라미터 `Γ(Θ, Π)` (자원 공급량). 핵심은 가능한 한 (1)만 쓰고 (2)는 최소화하는 것.
- **트리거**: Runtime 이벤트 — overload 또는 태스크의 새 주기 요청. 판단 기준이 정량적으로 명확함: 요청 주기 `T_new`가 no-supply interval `2(Π−Θ)`보다 크면(= `T_min` 이상이면) 앱 수준에서 흡수, 작으면 시스템 수준 재분배 필요.

## Abstract 3줄 요약
- Elastic task model(주기 조정)과 reservation 기반 격리(자원 재분배)는 타이밍 가변성을 다루는 서로 다른 두 접근이다.
- 두 접근을 결합해 elastic task model과 periodic resource model(PRM) 기반 2계층 적응형 스케줄링 프레임워크를 제안한다.
- 국소적 앱 주기 조정을 우선하고 시스템 수준 대역폭 변경을 최소화함으로써, 다른 앱에 미치는 영향을 줄이면서 스케줄 가능성을 확보한다.

## Conclusion 요약
- 고정 reservation을 유지한 채 앱이 주기로 가변성을 흡수하고, 국소 적응이 실패할 때만 시스템 대역폭을 재분배하는 2계층 구조가 대역폭 조정 횟수를 크게 줄이고 앱 간 독립성을 보존한다. 900 tasksets 실험에서 앱 수준이 요청의 큰 비율을 국소 처리함을 보인다. Spare capacity 분배 방법과 실패 처리는 기존 연구에 위임한다.

## 요점
- 플랫폼: Uniprocessor, 계층적/compositional 스케줄링(PRM), RM 또는 EDF. 특정 embedded board 없이 분석적 프레임워크 + 900 tasksets 시뮬레이션으로 평가.
- 도메인: hierarchical/compositional real-time systems에서의 elastic application.
- 핵심 방법 (2~3줄): Offline에서 각 태스크의 desired period로 초기 reservation `Γ(Θ, Π)`을 계산(Lee et al. 방법). Runtime(Algorithm 2)에서 새 주기 `T_new` 요청 시, `T_new ≥ T_min`이면 reservation 그대로 두고 elastic 압축으로 다른 태스크 주기만 조정(앱 수준), `T_new < T_min`이면 새 reservation을 생성해 GCSR manager에 요청(시스템 수준).
- 정식화/수식 (있으면): PRM utilization bound(RM/EDF 각각 식 5, 6)가 `T_min`의 함수라는 점이 핵심. 계층 분기 경계는 no-supply interval `2(Π−Θ)` vs `T_min`.

## 0708 면담 기준 보강
- **실시간성 수준**: Uniprocessor 계층적 스케줄링에서 PRM utilization bound로 스케줄 가능성을 정형 보장. Deadline miss나 tail latency 실측이 아니라 분석적 bound + 시뮬레이션.
- **실행시간 가정**: `C` 고정 WCET. Elastic은 주기만 조정하며 execution-time 가변은 논문이 명시적으로 제외한다.
- **보장 방식**: PRM utilization bound(식 5, 6)로 스케줄 가능성 정형 보장. 핵심 통찰은 bound가 `T_min`의 함수이므로 주기를 늘리는(= `T_min` 유지) 방향이면 상위 계층 reservation을 재검증할 필요가 없다는 것. 단 spare capacity 분배와 두 계층 모두 실패 시 처리는 앱에 위임하여 보장의 완결성에 공백이 있다.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): 2계층 reservation/period 적응 중심이며 vibration FD의 `W/H/M`, 기계 상태 anomaly trigger, 정확도 개념, multi-mode 전환, PREEMPT_RT는 다루지 않는다. WCET 고정 가정이라 `C(W,M)`처럼 설정이 실행시간을 바꾸는 구조가 없다.
- 내 연구에 쓸 곳: "국소 먼저, 전역 나중"의 계층 우선순위를 `2(Π−Θ)` vs `T_min`이라는 정량 경계로 정당화한 사례. `W` 범위 내 조정은 상위 재검증 없이 안전하다는 논증에 `T_min` 불변성 트릭의 형태를 빌릴 수 있다. 진단 태스크가 다른 태스크와 co-running될 때 local mode adaptation과 system-level bandwidth/slack 조정을 분리하는 근거. Q1/Q2/Q3 명시적 질문 프레이밍도 참고.
- 인용할 문장 (있으면, 15단어 이내): "two-level adaptive scheduling"

## 불확실한 점
- 확인 필요: 평가는 900 tasksets 시뮬레이션이며 앱 수준이 요청의 "큰 비율"을 국소 처리한다고 보고하나, 원문 Section IV의 구체적 대역폭 조정 감소 비율 수치는 별도 재확인이 필요하다.
- 확인 필요: reservation bandwidth와 본 연구의 system slack `S` 사이의 mapping은 별도 정의가 필요하다.
- 확인 필요: spare capacity 분배 방법을 제안하지 않고 기존 [14,15]에 위임하므로, background task에 slack을 줄 때의 분배 정책은 본 연구가 스스로 설계해야 한다.
