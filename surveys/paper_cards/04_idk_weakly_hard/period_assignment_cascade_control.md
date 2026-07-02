# Period Assignment for Real-Time Cascade Control Tasks Under Stability and Schedulability Constraints

- **그룹**: 4 idk_weakly_hard
- **출처/연도**: ECRTS 2025
- **저자**: Ismail Hawila, Liliana Cucu-Grosjean, Slim Ben Amor

## 두 질문
- **가변 변수**: control task period `Ti`, allowable consecutive deadline misses `m`.
- **트리거**: 없음=offline co-design/period assignment. Runtime slack 기반 adaptation은 확인되지 않음.

## 요점
- 플랫폼: PX4 drone use-case, Pixhawk microcontroller 기반 실행시간 측정 언급.
- 도메인: real-time cascade control tasks, control-scheduling co-design.
- 핵심 방법: cascade control task의 period 선택이 physical stability와 schedulability에 함께 영향을 준다고 보고, stable period region을 구한 뒤 control cost와 utilization/schedulability 제약을 만족하는 period를 선택한다.
- 정식화/수식: control cost `J = integral t |e(t)| dt`. period는 `[Ti_min, Ti_max]` stability interval 안에서 선택하며, fixed-priority schedulability bound와 inner/outer loop period ordering을 제약으로 둔다.

## 내 연구 관점
- 한 줄 gap: period `H`와 deadline miss를 stability와 연결하지만 vibration FD, window W, model M, anomaly score, PREEMPT_RT는 다루지 않는다.
- 내 연구에 쓸 곳: diagnosis period/hop size `H`를 system-only parameter가 아니라 application utility/stability와 함께 봐야 한다는 비교 배경.
- 인용할 문장: "stability and schedulability"

## 불확실한 점
- 확인 필요: drone/PX4 평가의 구체 period, utilization, cost 수치는 Table 4~7 조건을 재확인한 뒤 사용해야 한다.
- 확인 필요: control stability에서의 allowable deadline misses를 fault diagnosis utility로 직접 옮겨 해석하면 안 된다.
