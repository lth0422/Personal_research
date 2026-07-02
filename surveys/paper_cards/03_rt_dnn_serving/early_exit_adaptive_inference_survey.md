# Adaptive Inference through Early-Exit Networks: Design, Challenges and Directions

- **그룹**: 3 rt_dnn_serving
- **출처/연도**: EMDL 2021, arXiv 2021
- **저자**: Stefanos Laskaridis, Alexandros Kouris, Nicholas D. Lane

## 두 질문
- **가변 변수**: exit point, executed network depth, exit policy, early-exit placement.
- **트리거**: prediction confidence, input difficulty, device capability/load, application SLO. Machine condition trigger는 아님.

## 요점
- 플랫폼: survey/design paper. 특정 실험 플랫폼 중심 아님.
- 도메인: adaptive DNN inference, early-exit networks, mobile/embedded deep learning.
- 핵심 방법: early-exit network는 backbone 중간에 classifier를 붙이고, inference 중 confidence 또는 SLO 조건을 만족하면 나머지 layer 실행을 건너뛴다. 논문은 architecture design, training, exit policy, target hardware co-design 관점을 정리한다.
- 정식화/수식: end-to-end early-exit training loss와 IC-only training loss를 설명한다. exit policy는 rule-based 또는 learnable 방식으로 구분된다.

## 내 연구 관점
- 한 줄 gap: model depth/exit를 runtime variable로 다루지만 vibration FD의 window W, diagnosis period H, machine condition, PREEMPT_RT는 다루지 않는다.
- 내 연구에 쓸 곳: 본 연구의 `M` 또는 computation quality selection을 설명하는 background/survey.
- 인용할 문장: "exit policy"

## 불확실한 점
- 확인 필요: survey 성격이라 정량 결과를 비교표 근거로 사용하지 않는다.
- 확인 필요: confidence 기반 exit trigger를 본 연구의 anomaly score trigger와 동일하게 표현하면 안 된다.
