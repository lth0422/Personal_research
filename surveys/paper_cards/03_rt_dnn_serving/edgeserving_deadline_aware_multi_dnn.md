# EdgeServing: Deadline-Aware Multi-DNN Serving at the Edge

- **그룹**: 3 rt_dnn_serving
- **출처/연도**: arXiv:2605.05527v1, 7 May 2026
- **저자**: Jiahe Cao, Xiaomeng Li, Qiang Liu, Tao Han, Ning Zhang, Weisong Shi

## 두 질문
- **가변 변수**: model/service queue selection, early-exit point, batch size.
- **트리거**: per-request SLO deadline, queue backlog/queuing time, predicted system-wide SLO impact, remaining latency budget.

## 요점
- 플랫폼: RTX 3080, GTX 1650, NVIDIA Jetson Orin Nano 평가가 확인됨.
- 도메인: edge multi-DNN serving, latency-sensitive inference.
- 핵심 방법 (2~3줄): EdgeServing은 single shared GPU에서 time-division sharing을 사용해 latency predictability를 확보한다. offline profiling으로 model-exit-batch 조합의 latency를 측정하고, runtime scheduler가 stability score를 이용해 model, exit point, batch size를 함께 선택한다.
- 정식화/수식 (있으면): task total latency는 queuing time과 inference latency의 합으로 보고, `T_i > tau`이면 SLO violation으로 정의한다. scheduler는 후보 decision이 모든 queue의 urgency/stability에 미치는 영향을 예측한다.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): vibration fault diagnosis의 window size W와 diagnosis period H, anomaly score 기반 machine condition, PREEMPT_RT/RTOS 실시간성은 다루지 않는다.
- 내 연구에 쓸 곳: deadline-aware inference와 model/exit/batch runtime selection 비교군. 본 연구에서 M을 runtime mode로 선택하는 논리와 비교 가능하다.
- 인용할 문장 (있으면, 15단어 이내): "selects the model, exit point, and batch size"

## 불확실한 점
- 확인 필요: 현재 로컬 PDF는 arXiv v1 기준이다. manuscript 인용 전 최신 arXiv version 또는 출판 venue 여부를 확인해야 한다.
- 확인 필요: 정량 수치인 SLO violation ratio, P95 latency, accuracy 값은 figure별 workload와 platform 조건을 재확인해야 한다.
