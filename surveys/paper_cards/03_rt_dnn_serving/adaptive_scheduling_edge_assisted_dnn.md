# Adaptive Scheduling for Edge-Assisted DNN Serving

- **그룹**: 3 rt_dnn_serving
- **출처/연도**: arXiv 2023
- **저자**: Jian He, Chenxi Yang, Zhaoyuan He, Ghufran Baig, Lili Qiu

## 두 질문
- **가변 변수**: batch composition, batch size bound, layer-wise batching decision, client/server offloading portion.
- **트리거**: request arrival rate, deadline/on-time objective, memory bound, network/server congestion, client/server processing time.

## 요점
- 플랫폼: edge server with NVIDIA Tesla P100 GPU and 16GB GPU memory, client with NVIDIA Jetson Nano.
- 도메인: edge-assisted DNN serving for multiple real-time video analytics clients.
- 핵심 방법: DNN request를 layer 구조에 맞춰 batch-aware scheduling하고, same DNN, different DNN, shared-layer DNN 요청을 구분해 batching opportunity를 늘린다. 이후 network delay, server/client processing time을 고려해 일부 request 또는 layer portion을 client에서 처리할지 adaptively 결정한다.
- 정식화/수식: layer `k`의 batch size `b` 실행시간을 `h_k(b)`로 두고, memory bound `B` 아래에서 completion time 또는 on-time ratio를 최적화한다.

## 내 연구 관점
- 한 줄 gap: batch/offloading 중심의 video DNN serving이며 vibration FD의 window W, diagnosis period H, machine condition trigger, PREEMPT_RT는 다루지 않는다.
- 내 연구에 쓸 곳: system slack이나 deadline 조건으로 inference execution mode를 조절하는 비교군.
- 인용할 문장: "maximize the on-time ratio"

## 불확실한 점
- 확인 필요: 현재 로컬 PDF 기준 arXiv v2 2023이다. manuscript 인용 전 출판 venue 여부를 확인해야 한다.
- 확인 필요: system capacity improvement 수치는 DNN model, request rate, deadline, baseline 조건별로 달라지므로 Figure 5, 8, 11 조건을 재확인해야 한다.
