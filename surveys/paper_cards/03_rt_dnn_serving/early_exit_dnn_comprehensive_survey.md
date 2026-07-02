# Early-Exit Deep Neural Network: A Comprehensive Survey

- **그룹**: 3 rt_dnn_serving
- **출처/연도**: ACM Computing Surveys 2024
- **저자**: Haseena Rahmath P, Vishal Srivastava, Kuldeep Chaurasia, Roberto G. Pacheco, Rodrigo S. Couto

## 두 질문
- **가변 변수**: exit point, side-branch placement, backbone/branch design, early-exit policy.
- **트리거**: prediction confidence, input complexity, latency/resource constraints, edge/cloud context parameters.

## 요점
- 플랫폼: survey paper. 특정 단일 실험 플랫폼 중심 아님.
- 도메인: early-exit DNN, multi-exit neural network, edge intelligence, inference acceleration.
- 핵심 방법: early-exit DNN은 backbone 중간에 side branch를 붙여 confidence가 충분하면 intermediate exit에서 inference를 종료한다. 논문은 architecture, training strategy, deployment/inference process, application, challenge를 체계적으로 정리한다.
- 정식화/수식: confidence threshold 또는 exit policy가 side branch별 종료 여부를 결정하는 구조로 정리된다.

## 내 연구 관점
- 한 줄 gap: exit/depth 기반 adaptive inference survey이며 vibration FD의 W/H, machine condition, system slack, RTOS/PREEMPT_RT 실측은 다루지 않는다.
- 내 연구에 쓸 곳: `M` 또는 model-depth selection 관련 background. early-exit trigger와 anomaly-score trigger의 차이를 설명하는 데 사용 가능하다.
- 인용할 문장: "adaptive inference mechanisms"

## 불확실한 점
- 확인 필요: survey 논문이므로 정량 성능 비교 근거가 아니라 분류/배경 근거로 사용해야 한다.
- 확인 필요: confidence 또는 input complexity trigger를 본 연구의 machine condition trigger와 동일시하지 않아야 한다.
