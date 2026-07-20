# Handling System Overloads: An Empirical Evaluation of Deadline-Miss Handling Strategies

- **그룹**: 4 idk_weakly_hard
- **출처/연도**: IEEE 31st Real-Time and Embedded Technology and Applications Symposium, RTAS 2025, DOI 10.1109/RTAS65571.2025.00031
- **저자**: Tim Braun, Sebastian Altmeyer

## 두 질문
- **가변 변수**: Deadline-miss handling strategy인 Kill, Skip-Next, Queue와 actuation timing strategy인 Fixed, Shift-On-Miss, Instant다. 일부 구현에서는 deadline miss 시 actuator에 Hold 또는 Zero 값을 적용한다. 각 실험에서는 선택한 전략을 고정해 비교하며 runtime에서 전략을 자동 선택하지 않는다.
- **트리거**: Controller job의 deadline miss다. Temporary overload가 deadline miss를 발생시키며, 선택된 정책이 현재 job 종료, 다음 job skip, queue 유지 또는 actuation timing shift를 수행한다.

## Abstract 3줄 요약
- 실제 회전 진자 controller를 MCU와 RTOS에 구현하고 temporary overload에서 Kill, Skip-Next, Queue deadline-miss 처리 전략을 비교한다.
- 전략 효과는 system assumption과 parameter에 매우 민감하며, 기존 연구에서 권장한 전략이 실제 구현에서는 control behavior를 악화시킬 수 있다.
- 저자들은 deadline miss 후 가능한 output을 즉시 적용하는 Shift-On-Miss actuation timing을 제안하고 실제 시스템에서 평가한다.

## Conclusion 요약
- Deadline-miss 처리 전략의 상대적 성능은 utilization, overload 확률, task organization과 plant dynamics에 크게 의존해 보편적으로 최적인 전략이 없다고 결론짓는다. 단순 monolithic 구현과 Queue도 여러 조건에서 경쟁력 있었으며, 검증되지 않은 failure scenario에 일반적인 safeguard로 특정 전략을 적용하면 오히려 해로울 수 있다.

## 요점
- 플랫폼: STM32 B-L475E-IOT01A2, 80 MHz, ThreadX RTOS, fixed-priority preemptive scheduling, Quanser Qube Servo 2 rotary pendulum.
- 도메인: Embedded real-time feedback control under temporary overload.
- 핵심 방법 (2~3줄): Monolithic, partial LET, complete LET task organization에 Kill, Skip-Next, Queue와 actuation timing을 조합한다. NOP delay로 constant 또는 sporadic overload를 주입하고 physical pendulum의 swing-up과 balance behavior를 비교한다. Shift-On-Miss는 deadline miss 후 결과가 준비되는 즉시 actuator에 적용한다.
- 정식화/수식 (있으면): Controller period와 implicit deadline은 모두 2 ms다. Control cost `J`는 pendulum angle과 arm angle의 weighted squared error를 누적하고 non-overload optimum으로 정규화한다. 추가 지표는 actuation rate, data age, actuation-interval jitter다.

## 0708 면담 기준 보강
- **실시간성 수준**: ThreadX RTOS, fixed-priority preemptive scheduling, implicit deadline, deadline miss, measured maximum execution time, utilization과 jitter를 다룬다. Controller의 관측 최대 실행시간은 Swing-Up 474 microseconds, Balance 324 microseconds이며 SPI sensing/actuation은 87 microseconds다.
- **실행시간 가정**: 기본 실행시간은 실제 구현에서 측정하고, NOP delay로 overload utilization을 인위적으로 만든다. Constant overload는 120%, sporadic overload는 base utilization 70% 또는 100%에서 overload utilization 100~200%를 사용한다.
- **보장 방식**: Formal schedulability 또는 stability guarantee가 아니라 physical system의 empirical evaluation이다. 논문의 핵심은 정책 효과가 조건에 민감하므로 전체 구현과 overload model을 함께 검증해야 한다는 것이다.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): Deadline miss 이후 대응을 비교하지만 miss를 예방하는 feasible `W/H/M` selection, anomaly-based machine condition, system slack 기반 proactive adaptation, PREEMPT_RT는 다루지 않는다.
- 내 연구에 쓸 곳: Feasible mode filtering이 실패하거나 예상하지 못한 overload가 생겼을 때의 fallback 후보를 설계하는 근거다. KSC 2026에서도 miss rate만 보고 kernel 또는 정책을 평가하지 말고 data age, output freshness, jitter와 application utility를 함께 측정해야 한다는 근거로 사용할 수 있다.
- 인용할 문장 (있으면, 15단어 이내): "there is no universally optimal strategy combination"

## 불확실한 점
- 확인 필요: 한 종류의 rotary-pendulum system에서 얻은 전략 순위를 vibration fault diagnosis에 일반화하지 않는다.
- 확인 필요: 논문의 monolithic 구현이 여러 조건에서 우수했다는 결과는 특정 task organization, overload model과 actuation semantics에 종속된다.
- 확인 필요: 본 연구에서 inference deadline miss 시 late result 사용, drop, previous diagnosis 유지 중 어떤 fallback이 application-level risk를 최소화하는지 별도 실험이 필요하다.
