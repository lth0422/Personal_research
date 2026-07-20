# DNN-SAM: Split-and-Merge DNN Execution for Real-Time Object Detection

- **그룹**: 3 rt_dnn_serving
- **출처/연도**: IEEE 28th Real-Time and Embedded Technology and Applications Symposium, RTAS 2022, DOI 10.1109/RTAS54340.2022.00021
- **저자**: Woosung Kang, Siwoo Chung, Jeremy Yuhyun Kim, Youngmoon Lee, Kilho Lee, Jinkyu Lee, Kang G. Shin, Hoon Sung Chwa

## 두 질문
- **가변 변수**: Optional subtask가 처리하는 전체 image의 input scale이다. Mandatory subtask는 매 frame의 safety-critical RoI를 원래 resolution으로 처리하며, optional scale은 `0`을 포함한 finite candidate set에서 선택된다. DNN model이나 layer depth를 바꾸지는 않는다.
- **트리거**: Runtime에 계산한 deadline 이전의 available slack이다. Scheduler는 job release 또는 mandatory/optional subtask completion 때 호출되며, 실제 RoI size에 따라 남은 mandatory execution demand를 갱신하고 slack 안에서 실행 가능한 가장 큰 optional scale을 선택한다. RoI criticality 자체는 LiDAR와 IMU 기반 time-to-collision로 결정한다.

## Abstract 3줄 요약
- Multi-camera real-time object detection은 image 영역별 safety criticality가 다르지만 기존 DNN 실행은 전체 image를 동일하게 처리해 accuracy와 timeliness를 함께 만족시키기 어렵다.
- DNN-SAM은 한 inference를 critical RoI용 mandatory subtask와 down-scaled full-image용 optional subtask로 나누고, 결과를 다시 합친다.
- 두 scheduler는 mandatory task를 우선하면서 optional input scale을 deadline과 slack에 맞춰 조절하며, 평가에서 기존 방식보다 RoI accuracy와 inference latency를 개선했다고 보고한다.

## Conclusion 요약
- DNN-SAM은 기존 DNN을 수정하거나 재학습하지 않고 mandatory/optional subtask로 분리하고, criticality-aware scheduling과 runtime optional-scale selection을 제공한다. Non-preemptive EDF 충분조건 아래 timing constraint를 유지하면서 critical RoI의 빠른 결과와 전체 image accuracy를 함께 추구하며, 향후 더 다양한 driving context를 이용한 RoI 식별을 제안한다.

## 요점
- 플랫폼: NVIDIA Jetson Xavier, Ubuntu 18.04.4, CUDA 10.0, Darknet, YOLOv3. 1/10 scale self-driving car emergency-braking case study 포함.
- 도메인: Autonomous-driving real-time object detection.
- 핵심 방법 (2~3줄): Camera image를 원 resolution의 cropped RoI mandatory subtask와 scaled full-image optional subtask로 분리한다. EDF-MandFirst는 mandatory를 정적으로 우선하고, EDF-Slack은 EDF 순서와 reclaimed slack을 이용한다. Optional scale은 deadline 이전 slack에 들어가는 가장 큰 후보로 정하고 두 결과의 중복 object를 제거해 merge한다.
- 정식화/수식 (있으면): `C_i^M = c_i^RoI + c_i^Split + c_i^Infer`, `C_i^O(s) = c_i^Infer(s) + c_i^Merge`. Non-preemptive EDF의 blocking term과 mandatory utilization 합이 1 이하인 Eq. 3을 sufficient schedulability condition으로 사용한다. EDF-Slack은 `U^M(t)+U^O(t) <= 1`을 유지하며 slack 안의 최대 scale을 선택한다.

## 0708 면담 기준 보강
- **실시간성 수준**: Periodic implicit-deadline task, non-preemptive subtask-level EDF, measured maximum execution time, sufficient schedulability theorem과 deadline/FPS evaluation을 포함한다.
- **실행시간 가정**: Mandatory cost는 RoI 최대 크기의 `C_i^M`, optional cost는 scale별 `C_i^O(s)`로 mode-dependent하다. 각 component를 1,000회 실행한 최대 측정값을 WCET로 사용하므로 formal hardware WCET와는 구분해야 한다.
- **보장 방식**: Eq. 3을 만족하고 측정 기반 execution bound가 유효하다는 조건에서 EDF-MandFirst와 EDF-Slack의 subjob deadline 미스를 방지하는 sufficient condition을 증명한다. Runtime에는 완료된 mandatory subtask의 실제 cost로 slack을 reclaim한다.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): System slack 기반 input-scale selection은 직접 다루지만 spatial vision input과 GPU DNN에 한정되며, vibration temporal window `W`, diagnosis period `H`, model `M`, anomaly-based machine condition, MCU/SBC PREEMPT_RT는 다루지 않는다.
- 내 연구에 쓸 곳: `system slack -> input fidelity` 정책과 mode-dependent `C(input size)`의 강한 직접 비교군이다. 본 연구의 차별점은 image scale이 아닌 vibration information window를 조절하고, machine condition과 slack을 함께 사용하며 `H/M`까지 공동 선택하는 데 두어야 한다.
- 인용할 문장 (있으면, 15단어 이내): "adaptively selects the scales of optional sub-tasks at run-time"

## 불확실한 점
- 확인 필요: Abstract의 RoI accuracy 2.0~3.7x와 latency 4.8~9.7x 개선은 비교 baseline, task 수와 FPS 조건을 함께 명시한 뒤 원고에 인용해야 한다.
- 확인 필요: KITTI 평가에서는 IMU data가 없어 constant vehicle speed를 가정하므로 RoI identification 조건을 실제 차량 전체로 일반화하지 않는다.
- 확인 필요: 측정 최대값을 WCET로 사용한 conditional guarantee와 formal WCET guarantee를 구분해야 한다.
- 확인 필요: Vibration window는 temporal information content와 acquisition delay를 함께 바꾸므로 spatial image scaling과 직접 등치할 수 없다.
