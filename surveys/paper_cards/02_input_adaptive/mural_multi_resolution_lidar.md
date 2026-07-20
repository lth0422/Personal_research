# MURAL: A Multi-Resolution Anytime Framework for LiDAR Object Detection Deep Neural Networks

- **그룹**: 2 input_adaptive
- **출처/연도**: IEEE 31st International Conference on Embedded and Real-Time Computing Systems and Applications, RTCSA 2025, DOI 10.1109/RTCSA66114.2025.00014
- **저자**: Ahmet Soyyigit, Shuochao Yao, Heechul Yun

## 두 질문
- **가변 변수**: LiDAR point cloud를 pillar로 인코딩할 때의 input resolution, 즉 pillar size. 작은 pillar는 높은 resolution이고 실행시간이 길며, 큰 pillar는 낮은 resolution이고 실행시간이 짧다. DNN backbone을 교체하거나 early exit를 선택하는 방식은 아니며, shared weights와 resolution-aware batch normalization을 사용하는 단일 model을 runtime에 재구성한다.
- **트리거**: 동적으로 주어진 deadline과 현재 input point cloud에 대해 resolution별로 예측한 execution time. Scheduler는 deadline을 만족할 것으로 예측되는 후보 중 가장 높은 resolution을 선택한다. Machine condition이나 multi-task system slack을 직접 trigger로 사용하지는 않는다.

## Abstract 3줄 요약
- LiDAR 기반 3D object detection DNN은 자원 제약 embedded platform에서 latency와 detection utility를 함께 만족시키기 어렵다.
- MURAL은 하나의 shared-weight DNN에서 input resolution을 동적으로 조절하고, resolution-aware normalization과 runtime latency prediction을 결합한다.
- Deadline-aware scheduler는 입력별 예측 실행시간을 이용해 deadline 안에 가능한 최고 resolution을 선택하며, nuScenes와 embedded Jetson platform에서 기존 anytime 접근과 비교된다.

## Conclusion 요약
- 논문은 multi-resolution training, arbitrary resolution을 위한 batch-normalization parameter interpolation, deadline-aware scheduling을 결합해 LiDAR detection의 accuracy-latency trade-off를 runtime에 조절한다. PillarNet과 PointPillars 평가에서 여러 deadline에 대응하면서 multiple single-resolution model을 저장하지 않는 memory-efficient anytime framework라고 결론짓는다.

## 요점
- 플랫폼: NVIDIA Jetson AGX Xavier와 Jetson AGX Orin, 두 장치 모두 30 W power profile.
- 도메인: autonomous driving, LiDAR 3D object detection.
- 핵심 방법 (2~3줄): Scheduler는 PFE, sparse CNN, dense CNN, post-processing latency를 분리해 resolution별 total latency를 예측한다. 고정적 구성요소는 offline benchmark의 p99를 사용하고, input-dependent PFE와 sparse CNN은 입력 point/pillar 구조를 이용해 runtime에 예측한다. 선택된 pillar size에 맞춰 encoder, resolution-aware BN, post-processing을 재구성한다.
- 정식화/수식 (있으면): `L = L_PFE + L_SC + L_DC + L_PP`. 현재 input에 대해 predicted latency가 deadline 이하인 후보 중 가장 작은 pillar size, 즉 최고 resolution을 선택한다.

## 0708 면담 기준 보강
- **실시간성 수준**: dynamically given deadline, deadline-aware scheduler, input-dependent execution-time prediction, deadline miss evaluation을 다룬다. 평가에서 late output은 버리고 이전 buffered result를 사용해 job abortion을 모사한다.
- **실행시간 가정**: resolution과 input point-cloud sparsity에 따라 달라지는 mode-dependent, input-dependent `C(resolution, input)`이다. 일부 구성요소는 offline p99, 일부는 runtime prediction을 사용한다.
- **보장 방식**: static scheduler는 offline benchmark에서 얻은 WCET라는 표현을 사용하고, dynamic scheduler는 predicted latency로 admission-like resolution selection을 수행한다. 원문의 WCET는 측정 기반 값이므로 formal analytical WCET와 구분해야 한다.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): deadline-aware input resolution selection은 다루지만 vibration time window `W`, diagnosis period `H`, model `M`, machine anomaly condition, multi-task system slack, PREEMPT_RT는 다루지 않는다.
- 내 연구에 쓸 곳: runtime input-fidelity selection의 가장 직접적인 최신 비교군. 본 연구에서 `C(W,M)`을 mode별 상수로만 볼지 input/condition-dependent cost까지 고려할지 논의하는 근거로 활용할 수 있다.
- 인용할 문장 (있으면, 15단어 이내): "selects the highest possible resolution"

## 불확실한 점
- 확인 필요: 논문에서 사용하는 WCET는 offline benchmarking 기반이다. 원고에서는 formal WCET guarantee로 표현하지 않는다.
- 확인 필요: dynamically given deadline이 상위 application에서 어떻게 결정되는지는 본 논문의 핵심 scheduler 밖의 입력으로 보인다.
- 확인 필요: runtime latency prediction error가 deadline guarantee로 이어지는 안전 margin 또는 conservative correction을 어떻게 포함하는지 세부 구현을 재확인해야 한다.
- 확인 필요: LiDAR pillar resolution과 vibration time window `W`는 신호 의미가 다르므로 동일 변수로 직접 등치하지 않는다.
