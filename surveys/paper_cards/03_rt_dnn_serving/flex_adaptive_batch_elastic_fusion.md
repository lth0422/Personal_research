# FLEX: Adaptive Task Batch Scheduling with Elastic Fusion in Multi-Modal Multi-View Machine Perception

- **그룹**: 3 rt_dnn_serving
- **출처/연도**: 2024 IEEE Real-Time Systems Symposium (RTSS), DOI 10.1109/RTSS62706.2024.00033
- **저자**: Yuhang Xu, Zixuan Liu, Xinzhe Fu, Shengzhong Liu, Fan Wu, Guihai Chen

## 두 질문
- **가변 변수**: task batch 구성, modality fusion configuration, LiDAR temporal fusion frame 수, image feature fusion 여부.
- **트리거**: view별 criticality, runtime sensing context, object spatial distribution, GPU time budget, deadline/schedulability 조건.

## 요점
- 플랫폼: NVIDIA Jetson Orin.
- 도메인: autonomous driving, multi-modal multi-view 3D machine perception.
- 핵심 방법 (2~3줄): FLEX는 spatial view inspection task를 대상으로 elastic fusion과 adaptive batch scheduling을 결합한다. elastic fusion은 주어진 batch와 time budget에서 view별 fusion configuration을 선택하고, EDF 기반 dynamic batching은 deadline miss 없이 GPU throughput과 detection utility를 높이는 batch를 고른다.
- 정식화/수식 (있으면): scheduling problem은 batch 구성과 job별 fusion configuration을 선택해 detection utility를 최대화하되 deadline miss를 피하는 형태로 정리된다. 논문은 CEDF 기반 job sequence와 offline hierarchical schedule DAG를 이용해 online scheduling을 가속한다.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): vibration fault diagnosis의 window size W, diagnosis period H, model M 공동 선택과 machine condition 기반 anomaly trigger, RTOS/PREEMPT_RT 실험은 다루지 않는다.
- 내 연구에 쓸 곳: elastic-DNN serving 비교군. system slack/deadline 조건으로 runtime mode를 선택하는 문헌 축에 배치 가능하다.
- 인용할 문장 (있으면, 15단어 이내): "elastic fusion and adaptive batching"

## 불확실한 점
- 확인 필요: abstract의 `up to 22.0% recall`, `up to 14.7% mAP` 개선 수치는 원고 인용 전 Figure 9/10과 baseline 조건을 재확인해야 한다.
