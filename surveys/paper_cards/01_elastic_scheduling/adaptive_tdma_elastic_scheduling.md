# Adaptive TDMA Bus Allocation and Elastic Scheduling

- **그룹**: 1 elastic_scheduling
- **연구 섹션**: S3 elastic rate/workload, S5 schedulability/mode transition, S6 platform/interference
- **플랫폼 태그**: `PL-HET-SOC`
- **실행환경 태그**: `ENV-RTOS`
- **출처/연도**: 2010 IEEE International Conference on Computer Design, 2010, DOI 10.1109/ICCD.2010.5647792
- **저자**: Paolo Burgio, Martino Ruggiero, Francesco Esposito, Mauro Marinoni, Giorgio Buttazzo, Luca Benini

## 두 질문
- **가변 변수**: core별 TDMA bus slot/bandwidth와 periodic task period.
- **트리거**: processor workload 변화가 bus-bandwidth 변경 요청을 만들고, 중앙 master가 요청을 조정한 뒤 각 core가 period를 다시 계산한다.

## Abstract 3줄 요약
- MPSoC에서 elastic period 변화와 fixed TDMA bus allocation이 서로의 predictability를 저해하는 문제를 다룬다.
- QoS-aware bus service와 OS elastic scheduler가 bus slot과 task period를 함께 조정하는 구조를 제안한다.
- ERIKA RTOS가 실행되는 virtual MPSoC와 real-time benchmark에서 coordination overhead와 QoC를 평가한다.

## Conclusion 요약
- TDMA wheel과 task period의 runtime 공동 조정이 workload 변화에 대응하며, 실험에서 coordination overhead는 task computation time의 5% 미만이었다.

## 요점
- 플랫폼: STBus 기반 multiprocessor virtual platform, ERIKA RTOS, EDF.
- 도메인: shared-bus MPSoC real-time control.
- 핵심 방법 (2~3줄): 중앙 master가 core의 bandwidth 요청을 모아 TDMA slot을 공정하게 재배분한다. 각 core는 bus allocation별 offline WCET table을 사용해 elastic period를 계산한다.
- 정식화/수식 (있으면): `tau_i(C_i,T_i,min,T_i,max,E_i)`, `C_i`는 bus bandwidth별 offline table에서 선택한다.

## 0708 면담 기준 보강
- **실시간성 수준**: RTOS/EDF 기반이며 TDMA predictability와 workload 대응을 함께 다룬다.
- **실행시간 가정**: bus allocation별 WCET를 offline profiling/static analysis로 미리 구한다.
- **보장 방식**: TDMA isolation, WCET table, elastic utilization bound를 조합한다.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): vibration `W/M`, machine condition, PREEMPT_RT는 없고 중앙 master와 사전 WCET table을 요구한다.
- 내 연구에 쓸 곳: system slack뿐 아니라 shared-resource contention이 `C` mode를 바꿀 수 있다는 S6 비교군.
- 인용할 문장 (있으면, 15단어 이내): "TDMA Time Wheel and task periods are adjusted at run-time"

## 불확실한 점
- 확인 필요: 실제 silicon이 아니라 accurate virtual platform 검증이므로 physical MPSoC 결과로 표현하지 않는다.
