# Elastic DVS Management in Processors With Discrete Voltage/Frequency Modes

- **그룹**: 1 elastic_scheduling
- **연구 섹션**: S3 elastic rate/workload, S5 schedulability/mode transition
- **플랫폼 태그**: `PL-DESKTOP`
- **실행환경 태그**: `ENV-RTOS`
- **출처/연도**: IEEE Transactions on Industrial Informatics, 2007, DOI 10.1109/TII.2006.890494
- **저자**: Mauro Marinoni, Giorgio Buttazzo

## 두 질문
- **가변 변수**: task period, task utilization, processor의 discrete voltage/frequency mode. 조기 완료 시 processor speed도 online으로 낮춘다.
- **트리거**: 요구 processor utilization과 이용 가능한 discrete speed의 불일치, application이 선택한 energy/performance 정책, 실제 job의 조기 완료.

## Abstract 3줄 요약
- Classical DVS가 discrete speed에서 상위 mode를 선택해 자원을 낭비하는 문제를 다룬다.
- Elastic scheduling으로 task period를 조절해 선택한 speed의 가용 계산량을 채우는 통합 방법을 제안한다.
- AMD Athlon64와 S.Ha.R.K. kernel 구현 및 simulation으로 performance/energy 전략과 reclaiming을 평가한다.

## Conclusion 요약
- DVS와 elastic scheduling을 결합하면 제한된 operating mode에서 control performance와 energy를 조절할 수 있으며, early completion reclaiming이 추가 speed 감소에 기여한다.

## 요점
- 플랫폼: AMD Athlon64 3000+, 네 개 operating mode, S.Ha.R.K. real-time kernel.
- 도메인: hard real-time control 및 energy-aware embedded system.
- 핵심 방법 (2~3줄): 각 task의 elastic coefficient와 period 범위를 사용해 discrete processor speed에서 남는 계산 자원을 period 압축에 배분한다. Energy-oriented, performance-oriented, user-defined 전략과 online reclaiming을 제공한다.
- 정식화/수식 (있으면): `C_i(s)=phi_i/s + psi_i`; task period는 허용 범위 안에서 조정하며 task set은 최고 speed에서 feasible하다고 가정한다.

## 0708 면담 기준 보강
- **실시간성 수준**: hard real-time periodic task와 feasibility를 명시하고 real-time kernel에서 구현한다.
- **실행시간 가정**: WCET 기반이지만 frequency에 따라 scalable/non-scalable 부분을 나눈 execution-time model을 사용한다.
- **보장 방식**: 최고 speed에서의 offline feasibility와 elastic utilization allocation.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): `W/M`에 따른 진단 실행시간과 machine condition trigger는 없고 period와 CPU speed만 조절한다.
- 내 연구에 쓸 곳: `C(W,M)` mode와 CPU operating mode를 분리해야 한다는 S3/S5 비교 근거.
- 인용할 문장 (있으면, 15단어 이내): "combines DVS techniques with elastic scheduling"

## 불확실한 점
- 확인 필요: 원고에 energy 수치를 인용할 경우 Figure 6-11의 task-set 생성 조건을 다시 확인해야 한다.
