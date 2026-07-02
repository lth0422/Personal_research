# IDK Cascades for Time-Series Input Streams

- **그룹**: 4 idk_weakly_hard
- **출처/연도**: RTSS 2024
- **저자**: Kunal Agrawal, Sanjoy Baruah, Alan Burns, Jinhao Zhao

## 두 질문
- **가변 변수**: classifier cascade execution order, starting classifier, exploration strategy. 입력 window나 diagnosis period를 조절하는 논문은 아님.
- **트리거**: previous input/classification history, time-series input similarity/dependence. system slack 또는 machine condition trigger는 확인되지 않음.

## 요점
- 플랫폼: 특정 embedded target 실측 중심은 아님. Real-time classification cascade algorithm/evaluation 중심.
- 도메인: time-series input stream classification, mobile perception 예시.
- 핵심 방법: IDK classifier는 confidence가 부족하면 `I Don't Know`를 반환한다. 기존 IDK cascade가 매 입력마다 첫 classifier부터 시작하는 것과 달리, 이 논문은 연속 입력 간 dependence를 runtime에 학습하고 활용해 expected response time을 줄이는 알고리즘을 제안한다.
- 정식화/수식: 각 classifier는 execution duration과 successful classification probability를 가진다. 각 input은 hard deadline `T` 안에 classification되어야 하며, 남은 시간은 future input을 위한 exploration에 사용된다.

## 내 연구 관점
- 한 줄 gap: time-series dependency 기반 cascade execution은 다루지만 vibration FD의 W/H/M, anomaly score, system slack, RTOS/PREEMPT_RT는 다루지 않는다.
- 내 연구에 쓸 곳: model/exit 선택 또는 classifier cascade를 deadline-aware inference 비교군으로 언급 가능.
- 인용할 문장: "hard deadline of time-duration T"

## 불확실한 점
- 확인 필요: evaluation dataset과 정량 결과는 원고 인용 전 Section VI/VII와 figure/table 조건을 별도로 재확인해야 한다.
- 확인 필요: dependence parameter와 learning mechanism은 classification history 기반이며, 기계 상태 anomaly score와 동일하게 해석하면 안 된다.
