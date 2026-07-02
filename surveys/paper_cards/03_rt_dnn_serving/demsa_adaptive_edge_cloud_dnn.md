# Adaptive Heuristics for Scheduling DNN Inferencing on Edge and Cloud for Personalized UAV Fleets

- **그룹**: 3 rt_dnn_serving
- **출처/연도**: arXiv 2025
- **저자**: Suman Raj, Radhika Mittal, Harshil Gupta, Yogesh Simmhan

## 두 질문
- **가변 변수**: edge/cloud execution target, task dropping, migration, work stealing, rescheduling for QoE.
- **트리거**: task deadline, benefit/utility, network variability, compute variability, cloud variability, task completion rate in a window.

## 요점
- 플랫폼: emulated Jetson Nano edges with AWS Lambda cloud functions, real Tello drone with Jetson Orin Nano edge accelerator.
- 도메인: DNN inferencing for personalized UAV fleets and assistive drone applications.
- 핵심 방법: DEMS-A는 deadline-sensitive DNN task stream을 edge와 cloud에 배치하면서 dropping, migration, work stealing, cloud variability adaptation을 사용한다. GEMS는 QoE 관점에서 task type별 window 내 completion rate를 보장하도록 rescheduling한다.
- 정식화/수식: QoS utility와 on-time task completion count를 최대화하고, QoE는 window 내 task completion rate 목표로 정의한다.

## 내 연구 관점
- 한 줄 gap: edge/cloud offloading과 QoS/QoE scheduling 중심이며 vibration FD의 W/H/M 공동 선택, anomaly score trigger, PREEMPT_RT kernel latency는 다루지 않는다.
- 내 연구에 쓸 곳: deadline-aware inference scheduling과 windowed completion-rate QoE를 비교축으로 사용할 수 있다.
- 인용할 문장: "deadline-driven scheduling"

## 불확실한 점
- 확인 필요: 현재 로컬 PDF 기준 arXiv v2 2025이다. manuscript 인용 전 출판 venue 여부를 확인해야 한다.
- 확인 필요: task completion rate, QoS utility, QoE utility, real-drone utility 수치는 workload, edge/cloud setup, FPS 조건별로 재확인해야 한다.
- 확인 필요: QoE의 window는 application-level completion window이며, 본 연구의 vibration window W 또는 hop size H와 혼동하지 않아야 한다.
