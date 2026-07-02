# Improved Elastic Scheduling Algorithms for Implicit-Deadline Tasks

- **그룹**: 1 elastic_scheduling
- **출처/연도**: Leibniz Transactions on Embedded Systems 2025
- **저자**: Marion Sudvarg, Christopher Gill, Sanjoy Baruah

## 두 질문
- **가변 변수**: task utilization, task period, compression amount.
- **트리거**: system overload, new task admission, available computational resource change.

## 요점
- 플랫폼: algorithm/evaluation paper. Specific embedded target 중심 아님.
- 도메인: implicit-deadline elastic scheduling on uniprocessor and multiprocessor systems.
- 핵심 방법: 기존 elastic scheduling의 quadratic-time compression을 개선해 utilization bound에서는 quasilinear 또는 admission-control linear time으로 계산한다. Partitioned EDF에는 bound compression과 binary search를 적용하고, global EDF/RM에는 proxy task 변환으로 exact polynomial-time algorithm을 제시한다.
- 정식화/수식: elastic task의 utilization compression을 `U_i^min <= U_i <= U_i^max` 범위와 elastic coefficient 관계 아래에서 계산한다.

## 내 연구 관점
- 한 줄 gap: elastic scheduling algorithm 효율성 연구이며 vibration FD W/H/M, anomaly score, PREEMPT_RT measurement는 다루지 않는다.
- 내 연구에 쓸 곳: runtime mode switch를 실제 scheduler에 넣을 때 알고리즘 overhead를 고려해야 한다는 배경.
- 인용할 문장: "online adaptation"

## 불확실한 점
- 확인 필요: 현재 로컬 PDF 기준 LITES 2025로 표기되어 있지만 accepted/published date가 미래 시점이다. 인용 전 bibliographic status를 확인해야 한다.
- 확인 필요: speedup/runtime 수치는 Section 3~5 evaluation 조건을 확인한 뒤 사용해야 한다.
