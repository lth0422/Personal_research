# Mixed-Criticality Federated Scheduling for Relaxed-Deadline DAG Tasks

- **그룹**: 8 misc_realtime_scheduling
- **출처/연도**: RTSS 2024
- **저자**: Fei Guan, Jinkyu Lee, Chun Jason Xue, Jen-Ming Wu, Nan Guan

## 두 질문
- **가변 변수**: core/resource assignment for federated scheduling.
- **트리거**: mixed-criticality mode/criticality requirements, schedulability constraint.

## 요점
- 플랫폼: algorithm/simulation paper.
- 도메인: mixed-criticality scheduling for relaxed-deadline DAG tasks.
- 핵심 방법: deadline이 period보다 긴 relaxed-deadline DAG task를 dual-criticality system에서 federated scheduling하는 알고리즘을 제안한다. High-utilization/low-utilization task를 다루고 capacity augmentation bound 4를 보인다.
- 정식화/수식: sporadic parallel DAG task model with two criticality levels.

## 내 연구 관점
- 한 줄 gap: mixed-criticality DAG theory이며 vibration FD utility, machine condition, PREEMPT_RT pipeline은 다루지 않는다.
- 내 연구에 쓸 곳: deadline > period 또는 parallel task scheduling 배경이 필요할 때 제한적으로 참고.
- 인용할 문장: "relaxed-deadline DAG tasks"

## 불확실한 점
- 확인 필요: capacity augmentation bound와 acceptance ratio 결과를 원고에 쓰려면 task generation 조건을 확인해야 한다.
