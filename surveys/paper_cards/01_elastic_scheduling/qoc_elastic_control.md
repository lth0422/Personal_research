# QoC Elastic Scheduling for Real-Time Control Systems

- **그룹**: 1 elastic_scheduling
- **출처/연도**: Real-Time Systems 2011
- **저자**: Yu-Chu Tian, Li Gui

## 두 질문
- **가변 변수**: control period, task utilization.
- **트리거**: QoC measurement, workload constraint, runtime resource/change in control mode.

## 요점
- 플랫폼: process control examples. Specific embedded board 중심 아님.
- 도메인: real-time process control systems, feedback scheduling, quality-of-control management.
- 핵심 방법: elastic scheduling을 QoC management와 workload adaptation을 함께 포함하는 constrained optimization problem으로 만든다. Period adjustment solution을 QoC measurement 기반 closed form으로 표현해 QoC를 scheduler에 feedback한다.
- 정식화/수식: control period selection을 system constraints 아래 QoC improvement를 최대화하는 constrained optimization으로 둔다.

## 내 연구 관점
- 한 줄 gap: control QoC 기반 period scheduling이며 vibration FD의 anomaly utility, window W, model M, PREEMPT_RT는 다루지 않는다.
- 내 연구에 쓸 곳: diagnosis utility와 scheduling variable을 함께 최적화해야 한다는 논리의 control-domain 비교군.
- 인용할 문장: "QoC elastic scheduling"

## 불확실한 점
- 확인 필요: examples의 plant/control task 설정과 QoC metric은 Section 7에서 확인 후 사용해야 한다.
- 확인 필요: QoC measurement를 본 연구의 anomaly score와 동일한 의미로 쓰면 안 된다.
