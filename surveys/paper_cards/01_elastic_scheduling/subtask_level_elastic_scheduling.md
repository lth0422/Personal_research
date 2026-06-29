# Subtask-Level Elastic Scheduling

- **그룹**: 1 elastic_scheduling
- **출처/연도**: 2024 IEEE Real-Time Systems Symposium (RTSS), DOI 10.1109/RTSS62706.2024.00040
- **저자**: Marion Sudvarg, Daisy Wang, Jeremy Buhler, Chris Gill

## 두 질문
- **가변 변수**: parallel DAG task의 subtask workload, task utilization, core allocation.
- **트리거**: limited resources로 인한 overload 또는 schedulability 조건 불만족. 온라인 core allocation/workload compression도 다룬다.

## 요점
- 플랫폼: federated scheduling 기반 multicore real-time system. 구현은 Gurobi solver 기반으로 확인됨.
- 도메인: parallel DAG real-time tasks, multicore real-time scheduling.
- 핵심 방법 (2~3줄): Buttazzo elastic model을 subtask-level workload compression으로 확장한다. 각 subtask에 elastic constant와 acceptable workload range를 두고, MIQP/MILP 및 pseudo-polynomial dynamic programming으로 workload compression과 core allocation을 계산한다.
- 정식화/수식 (있으면): uniprocessor elastic model의 `U_i` compression을 배경으로, federated scheduling에서는 `ceil((C_i - L_i) / (D_i - L_i))` 형태의 core demand 제약을 사용한다.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): vibration fault diagnosis, input window W, model M, anomaly score 기반 machine condition trigger, PREEMPT_RT/SBC 실험은 다루지 않는다.
- 내 연구에 쓸 곳: classic period-level elastic scheduling보다 더 세밀한 workload/core allocation 비교군. 본 연구가 단순 부하 trigger가 아니라 machine condition과 slack을 함께 쓰는 점을 설명할 때 사용 가능.
- 인용할 문장 (있으면, 15단어 이내): "Each subtask is assigned a range"

## 불확실한 점
- 확인 필요: `Subtask-Level_Elastic_Scheduling_copy1.pdf`와 `copy2_needs_check.pdf`는 PDF 크기와 텍스트 해시가 달라 완전 중복으로 삭제하지 않았다. 현재 카드는 copy1 기준으로 작성했다.
