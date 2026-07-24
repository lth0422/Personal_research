# Improved Uniprocessor Scheduling of Systems of Sporadic Constrained-Deadline Elastic Tasks

- **그룹**: 1 elastic_scheduling
- **연구 섹션**: S3 elastic rate/workload, S5 schedulability/mode transition
- **플랫폼 태그**: `PL-DESKTOP`
- **실행환경 태그**: `ENV-OTHER`
- **출처/연도**: RTNS 2023, DOI 10.1145/3575757.3575759
- **저자**: Sanjoy Baruah

## 두 질문
- **가변 변수**: constrained-deadline sporadic task의 period `T_i`; `C_i`, `D_i`, elasticity와 period range는 입력이다.
- **트리거**: runtime trigger가 아니라 주어진 task set을 EDF-schedulable하게 만드는 offline period assignment 문제다.

## Abstract 3줄 요약
- 기존 elastic scheduling이 주로 implicit-deadline task에 한정된 문제를 지적한다.
- Constrained-deadline sporadic task를 preemptive uniprocessor EDF로 실행하기 위한 period 선택을 다룬다.
- Utilization 근사 대신 processor-demand analysis를 직접 이용하는 두 알고리즘을 제안한다.

## Conclusion 요약
- 기존 generalized elastic algorithm의 보수성을 지적하고, PDA의 monotonicity와 testing-set 구조를 이용한 더 효과적인 period assignment를 제시한다.

## 요점
- 플랫폼: 이론 및 알고리즘 분석; physical implementation 없음.
- 도메인: constrained-deadline sporadic elastic task scheduling.
- 핵심 방법 (2~3줄): elasticity parameter로 period 후보를 만들고 PDA로 EDF schedulability를 검사한다. Binary-search형 방법과 testing set을 순차 재사용하는 효율적 방법을 제시한다.
- 정식화/수식 (있으면): `tau_i=(C_i,D_i,T_i)`, `dbf_i(t)=max(0,floor((t-D_i)/T_i)+1)C_i`.

## 0708 면담 기준 보강
- **실시간성 수준**: constrained deadline과 exact EDF processor-demand criterion을 사용한다.
- **실행시간 가정**: task별 WCET `C_i` 고정.
- **보장 방식**: processor-demand analysis 기반 EDF schedulability test.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): `C(W,M)` 가변 실행시간, machine condition/runtime slack trigger와 mode transition은 없다.
- 내 연구에 쓸 곳: `D<T`인 diagnosis task를 elastic period 모델에 넣을 때 utilization만으로 충분하지 않다는 S5 근거.
- 인용할 문장 (있으면, 15단어 이내): "processor demand analysis is the preferred approach"

## 불확실한 점
- 확인 필요: 제안 알고리즘의 runtime complexity를 본 연구 online policy에 적용하려면 task 수와 period discretization별 비용을 별도 검토해야 한다.
