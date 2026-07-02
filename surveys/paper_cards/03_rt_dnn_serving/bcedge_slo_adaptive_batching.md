# BCEdge: SLO-Aware DNN Inference Services with Adaptive Batching on Edge Platforms

- **그룹**: 3 rt_dnn_serving
- **출처/연도**: arXiv 2023
- **저자**: Ziyang Zhang, Huan Li, Yang Zhao, Changyao Lin, Jie Liu

## 두 질문
- **가변 변수**: batch size, number of concurrent model instances.
- **트리거**: request SLO, queue/request state, model interference, throughput-latency utility.

## 요점
- 플랫폼: NVIDIA Xavier NX 등 edge GPU platforms. 세 heterogeneous edge GPUs 사용 언급.
- 도메인: SLO-aware edge DNN inference serving.
- 핵심 방법: BCEdge는 adaptive batching과 concurrent model instance 수를 함께 조절한다. Maximum entropy DRL scheduler가 throughput-latency utility를 높이도록 batch size와 concurrent model 수를 선택하고, lightweight NN으로 inter-model interference를 예측한다.
- 정식화/수식: request `ri = {model type, input type, input shape, SLO}`. scheduling time slot은 batch request들의 SLO와 concurrent model 수를 이용해 정의한다.

## 내 연구 관점
- 한 줄 gap: SLO-aware batch/concurrency scheduling은 다루지만 vibration FD의 W/H/M, anomaly score, PREEMPT_RT kernel 실시간성은 다루지 않는다.
- 내 연구에 쓸 곳: DNN serving에서 runtime batch/resource allocation이 deadline/SLO와 연결되는 비교군.
- 인용할 문장: "adaptive batching"

## 불확실한 점
- 확인 필요: 논문 첫 페이지 기준 arXiv v1 2023이다. manuscript 인용 전 출판 venue 여부를 확인해야 한다.
- 확인 필요: `up to 37.6%` utility improvement는 platform/model/baseline 조건을 Section V에서 재확인해야 한다.
