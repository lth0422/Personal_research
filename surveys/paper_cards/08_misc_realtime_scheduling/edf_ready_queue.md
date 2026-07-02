# Design of an Efficient Ready Queue for Earliest-Deadline-First EDF Scheduler

- **그룹**: 8 misc_realtime_scheduling
- **출처/연도**: DATE 2016
- **저자**: Risat Mahmud Pathan

## 두 질문
- **가변 변수**: ready queue data structure/operation design.
- **트리거**: scheduling event, job release/preemption/completion.

## 요점
- 플랫폼: simulation with randomly generated task sets.
- 도메인: EDF scheduler implementation overhead.
- 핵심 방법: EDF ready queue를 위한 data structure와 insert/remove operation을 제안한다. Preempted job insertion과 highest-priority job removal을 constant time으로 처리해 ready-queue management overhead를 낮추는 것이 목표다.
- 정식화/수식: sporadic task model `(C_i, D_i, T_i)` under EDF.

## 내 연구 관점
- 한 줄 gap: scheduler ready queue overhead 연구이며 fault diagnosis inference, W/H/M adaptation, PREEMPT_RT measurement는 다루지 않는다.
- 내 연구에 쓸 곳: EDF/SCHED_DEADLINE 논의에서 scheduling overhead가 deadline miss에 영향을 줄 수 있다는 배경.
- 인용할 문장: "ready queue"

## 불확실한 점
- 확인 필요: overhead improvement 수치는 simulation setup과 baseline을 확인한 뒤 사용해야 한다.
