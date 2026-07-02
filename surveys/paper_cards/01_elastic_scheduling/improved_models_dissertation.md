# Improved Models of Elastic Scheduling

- **그룹**: 1 elastic_scheduling
- **출처/연도**: PhD dissertation 2024
- **저자**: Marion Baumli Sudvarg

## 두 질문
- **가변 변수**: task period, task utilization, workload, subtask workload, harmonic period.
- **트리거**: overload, admission/change of computational resources, available utilization change.

## 요점
- 플랫폼: dissertation. FIMS, ORB-SLAM3, synthetic/evaluation chapters 포함.
- 도메인: elastic scheduling models, constrained-deadline tasks, harmonic tasks, subtask-level elasticity.
- 핵심 방법: elastic scheduling을 새 scheduling model로 확장하고, system outcome을 고려한 elasticity 및 improved execution time complexity를 다룬다. 목차 기준으로 constrained-deadline, harmonic period, subtask-level workload, FIMS/ORB-SLAM3 application을 포함한다.
- 정식화/수식: chapter별로 utilization compression, harmonic elastic problem, subtask-level elastic scheduling, optimization formulation을 다룬다.

## 내 연구 관점
- 한 줄 gap: elastic scheduling 전반의 확장 문헌이지만 vibration FD의 W/H/M semantic, anomaly score trigger, PREEMPT_RT/SBC 실측은 다루지 않는다.
- 내 연구에 쓸 곳: elastic scheduling 계열을 넓게 정리할 때 배경 문헌. 개별 논문 카드와 중복되는 내용은 논문별 인용을 우선한다.
- 인용할 문장: "adaptive scheduling"

## 불확실한 점
- 확인 필요: dissertation은 여러 published/preprint work를 포함하므로 원고에서는 가능한 한 해당 chapter의 출판 논문을 우선 인용해야 한다.
- 확인 필요: chapter별 실험 수치와 platform은 개별 논문 또는 chapter 본문에서 따로 재확인해야 한다.
