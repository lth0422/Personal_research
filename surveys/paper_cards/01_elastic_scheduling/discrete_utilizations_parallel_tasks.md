# Elastic Scheduling of Parallel Real-Time Tasks with Discrete Utilizations

- **그룹**: 1 elastic_scheduling
- **출처/연도**: RTNS 2020
- **저자**: James Orr, Johnny Condori Uribe, Chris Gill, Sanjoy Baruah, Kunal Agrawal, Shirley Dyke, Arun Prakash, Iain Bate, Christopher Wong, Sabina Adhikari

## 두 질문
- **가변 변수**: discrete utilization candidate, task period, computational workload, mode of operation.
- **트리거**: utilization demand change, mode change, schedulability/resource constraint.

## 요점
- 플랫폼: virtual real-time hybrid simulation experiment. Hardware details require recheck before citation.
- 도메인: parallel real-time tasks under federated scheduling, real-time hybrid simulation.
- 핵심 방법: 기존 continuous elastic model 대신 각 task가 finite candidate tuple을 갖는 discrete elastic model을 제안한다. 각 tuple은 period와 workload를 포함하므로 period elasticity와 computational elasticity를 함께 표현할 수 있다.
- 정식화/수식: federated scheduling에서 parallel discrete elastic task scheduling이 NP-hard임을 보이고, pseudo-polynomial dynamic programming algorithm을 제시한다.

## 내 연구 관점
- 한 줄 gap: period와 workload/mode를 함께 조절하지만 vibration FD의 W/H/M semantic, machine condition trigger, PREEMPT_RT 실측은 다루지 않는다.
- 내 연구에 쓸 곳: 본 연구의 `(W,H,M)` mode set을 discrete candidate mode로 정식화할 때 비교 가능한 elastic model.
- 인용할 문장: "discrete set of possible utilizations"

## 불확실한 점
- 확인 필요: virtual RTHS 실험의 hardware, controller mode, utilization loss 수치는 Section 4/5 기준으로 재확인해야 한다.
- 확인 필요: discrete utilization의 workload 변화가 본 연구의 model M 또는 window W 변화와 정확히 어떻게 대응되는지는 별도 정식화가 필요하다.
