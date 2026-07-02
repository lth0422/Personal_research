# Reducing Worst-Case Deadline Failure Probability for EDF Scheduling

- **그룹**: 4 idk_weakly_hard
- **출처/연도**: RTSS 2025
- **저자**: Fei Guan, Xu Jiang, Weipeng Jing, Nan Guan

## 두 질문
- **가변 변수**: active-dropping threshold/probability, probabilistic WCET distribution. Task period는 input model이고 runtime elastic variable은 아님.
- **트리거**: probabilistic deadline failure analysis, high-utilization condition. Machine condition 또는 system slack trigger는 확인되지 않음.

## 요점
- 플랫폼: synthetic task-set evaluation. Computation platform은 96-core AMD EPYC 9K84 CPU와 256 GB RAM로 언급됨.
- 도메인: probabilistic schedulability analysis for EDF scheduling.
- 핵심 방법: 기존 EDF worst-case deadline failure probability analysis의 pessimism을 줄이는 분석법을 제안하고, active-dropping policy를 EDF에 결합해 high-utilization task set의 analytical WCDFP를 낮춘다.
- 정식화/수식: sporadic constrained-deadline task `tau_i = <C_i, T_i, D_i>`, execution time `C_i`는 pWCET distribution. 목표는 system WCDFP upper bound를 더 tight하게 하는 것.

## 내 연구 관점
- 한 줄 gap: deadline failure probability를 다루지만 vibration FD pipeline, W/H/M adaptation, PREEMPT_RT 측정은 다루지 않는다.
- 내 연구에 쓸 곳: deadline miss rate를 deterministic pass/fail 외에 probabilistic risk로 해석하는 배경 문헌.
- 인용할 문장: "bounded probabilities"

## 불확실한 점
- 확인 필요: active-dropping은 분석상 WCDFP를 줄일 수 있지만 average-case deadline misses를 악화시킬 수 있다고 논문이 언급한다. 본 연구의 diagnosis skip/drop 정책과 연결하려면 조건을 분리해야 한다.
- 확인 필요: synthetic task-set 결과 수치는 Figure 3~8의 `UL`, `UH`, task count, pWCET cardinality 조건을 확인한 뒤 사용해야 한다.
