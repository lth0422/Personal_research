# 최근 실시간 학회 논문 연구 연관성 백로그

이 문서는 `wiki/analyses/`의 RTAS 2022--2025, RTCSA 2023--2025, RTSS 2024--2025 조사와 ESL 2025 보조 조사를 현재 개인연구 관점에서 다시 분류한 목록이다.

`wiki/`는 원본 조사 자료이므로 수정하지 않는다. 아래 판단은 wiki에 기록된 제목과 abstract 또는 한 줄 요약만을 근거로 한 임시 판단이다. 저자, 세부 방법, 플랫폼, 정량 결과, formal guarantee는 PDF 원문을 확보한 뒤 확인한다.

## 재분류 기준

- 직접성: `(W,H,M)`, 입력 해상도 또는 길이, model/exit, task rate/period를 조절하는가?
- 트리거: machine/physical condition, criticality, confidence, workload, system slack, deadline miss를 사용하는가?
- 보장: schedulability, utilization, admission, fallback, deadline miss 또는 tail latency를 다루는가?
- 적용성: vibration fault diagnosis와 직접 같지 않더라도 condition-aware mode selection 또는 feasibility-first 정책의 비교군이 되는가?
- 주의: wiki의 기존 별점은 당시 시스템 소프트웨어와 아키텍처 관심도를 반영하므로 현재 연구 우선순위로 그대로 사용하지 않는다.

## 원문 확보 최우선 후보

| 순위 | 논문 | 출처 | Abstract 수준 가변 변수 | Abstract 수준 트리거 | 우리 연구에서 확인할 핵심 | PDF 상태 |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | MURAL: A Multi-Resolution Anytime Framework for LiDAR Object Detection Deep Neural Networks | RTCSA 2025 | input resolution/pillar size. 단일 shared-weight DNN을 사용하며 early exit는 아님 | dynamically given deadline, input별 predicted execution time | deadline 안에서 최고 input fidelity를 선택하며 `C(resolution,input)`을 예측하는 구조 | 카드 완료 |
| 2 | Safety-Aware Implementation of Control Tasks via Scheduling with Period Boosting and Compressing | RTCSA 2023 | sampling period/common scheduling slot, controller gain 재설계 선택 | runtime trigger 없음. WCET, plant model, safety margin 기반 offline synthesis | `H/T` 변경과 weakly-hard miss pattern을 application-level safety로 제한하는 직접 비교군 | 카드 완료 |
| 3 | ATER: Adaptive Task Execution Rate Regulation for Enhanced Real-Time Performance in ROS 2 | RTCSA 2025 | sensor sampling rate/timer period, downstream task activation rate | message drop, publish/subscribe rate, observed execution-time distribution | Runtime `H/T` regulation의 직접 비교군. 단 formal deadline guarantee와 application utility는 없음 | 카드 완료 |
| 4 | Handling System Overloads: An Empirical Evaluation of Deadline-Miss Handling Strategies | RTAS 2025 | Kill/Skip-Next/Queue, Fixed/Shift-On-Miss/Instant actuation timing | temporary overload로 발생한 controller deadline miss | 실제 MCU fallback 비교군. 전략 효과가 utilization, overload model, task organization에 민감함을 확인 | 카드 완료 |
| 5 | DNN-SAM: Split-and-Merge DNN Execution for Real-Time Object Detection | RTAS 2022 | optional full-image scale, mandatory critical-RoI subtask | actual mandatory execution 후 available deadline slack, RoI time-to-collision | `system slack -> input fidelity`의 강한 직접 비교군. Vibration `W/H/M`과는 구분 필요 | 카드 완료 |
| 6 | Decntr: Optimizing Safety and Schedulability with Multi-Mode Control and Resource Allocation Co-Design | RTAS 2024 | controller, safe period, task/core/cache/BW allocation, transition deadline | runtime mode-change request; offline mode/transition co-design | Feasible mode-set synthesis와 runtime mode event 적용의 가장 가까운 구조적 비교군 | 카드 완료 |

## 다음 단계 후보

| 우선순위 | 논문 | 출처 | 연결 지점 | 한계 또는 확인 사항 |
| --- | --- | --- | --- | --- |
| High | SCENIC: Capability and Scheduling Co-Design for Intelligent Controller on Heterogeneous Platforms | RTSS 2024 | DNN controller capability, environment, response time과 scheduling의 공동 설계 | 카드 완료. 현재 configuration optimization은 offline이고 runtime adaptation은 future work |
| High | Parameterized Workload Adaptation for Fork-Join Tasks with Dynamic Workloads and Deadlines | RTCSA 2023 | workload와 deadline이 함께 변하는 task model은 `C(W,M)` mode bank 비교에 유용 | 위성 응용과 Pareto 최적화 중심이며 machine condition은 확인 필요 |
| Medium | Self-Cueing Real-Time Attention Scheduling in Criticality-Aware Visual Machine Perception | RTAS 2022 | criticality 기반 입력 영역 선택과 GPU scheduling | 후속 self-cueing/resizing 논문을 이미 보유하므로 선행 관계와 중복 범위 확인 후 다운로드 |
| Medium | Compressing VAE-Based Out-of-Distribution Detectors for Embedded Deployment | RTCSA 2024 | embedded anomaly/OOD detection과 실행시간-품질 trade-off | static compression 방법론이며 runtime `W/H/M` selection은 abstract에서 확인되지 않음 |
| Medium | Real-Time Multitasking of Deep Neural Networks With Nvidia TensorRT | RTSS 2025 | DNN chunk와 limited-preemptive scheduling을 이용한 timing predictability | GPU multi-DNN 중심이며 Pi Zero 2W CPU와 직접 비교하기 어려움 |
| Medium | RT-Swap: Addressing GPU Memory Bottlenecks for Real-Time Multi-DNN Inference | RTAS 2024 | memory-feasible task set과 timing guarantee의 결합 | GPU swap scheduling 중심이며 `W/H/M`과 machine condition은 없음 |
| Medium | CF-DETR: Coarse-to-Fine Transformer for Real-Time Object Detection | RTSS 2025 | coarse-to-fine inference와 전용 scheduler는 model depth/quality adaptation 비교군 후보 | 실제 가변 변수와 runtime trigger를 원문에서 확인해야 함 |
| Low | Work-in-Progress: Real-Time Deep Neural Inference on Resource-Constrained Edge Devices | RTSS 2025 | 자원 제약 edge와 deadline-aware inference | WIP이며 분산/협력 추론 중심으로 보여 현재 단일 SBC 연구와 거리가 있음 |

## ESL 2025 보조 후보

ESL은 RTAS, RTCSA, RTSS와 성격이 다르므로 핵심 실시간 스케줄링 근거가 아니라 구현 또는 모델 구성 보조 자료로만 본다.

| 논문 | 연결 지점 | 판단 |
| --- | --- | --- |
| Software-Hardware Exploration of Early-Exit Neural Networks on Edge Accelerators | early-exit `M` 후보와 hardware configuration 공동 탐색 | Anytime 구조를 실제 연구 범위에 넣을 때만 확보 |
| Combining Early Exit and Selective Prediction for Convolutional Neural Networks | confidence 기반 exit/escalation | uncertainty-aware escalation을 후속 ablation으로 진행할 때 확보 |
| TinyTNAS: Time-Bound, GPU-Independent Hardware-Aware Neural Architecture Search for TinyML Time-Series Classification | time bound를 고려한 TinyML time-series model 설계 | `M` 후보를 새로 탐색할 때 보조 비교군. 현재 scheduling core보다 우선순위 낮음 |
| Compressing Runtime Memory Usage via Activation Remapping for Deploying Deep Neural Networks on MCUs | MCU activation memory 제약 | STM32 mode별 memory feasibility가 문제가 될 때 참고 |

## 이미 보유한 직접 관련 논문

| 논문 | 현재 상태 | 비고 |
| --- | --- | --- |
| Adaptive Model Selection for Real-Time Heart Disease Detection on Embedded Systems | PDF, card, critical review 보유 | condition-aware `M` selection 직접 비교군 |
| MURAL: A Multi-Resolution Anytime Framework for LiDAR Object Detection Deep Neural Networks | PDF와 card 보유 | deadline-aware input resolution selection 직접 비교군 |
| DNN-SAM: Split-and-Merge DNN Execution for Real-Time Object Detection | PDF와 card 보유 | system slack 기반 optional input-scale selection 직접 비교군 |
| Decntr: Optimizing Safety and Schedulability with Multi-Mode Control and Resource Allocation Co-Design | PDF와 card 보유 | feasible mode/transition allocation과 safety-schedulability co-design 비교군 |
| SCENIC: Capability and Scheduling Co-Design for Intelligent Controller on Heterogeneous Platforms | PDF와 card 보유 | condition/model/timing을 application capability로 묶는 직접 비교군 |
| Elastic Scheduling for Harmonic Task Systems | PDF와 card 보유 | feasible period mode와 최신 elastic scheduling 비교군 |
| Algorithms for Canvas-Based Attention Scheduling with Resizing | PDF와 card 보유 | input resizing과 schedulability 비교군 |
| FLEX: Adaptive Task Batch Scheduling with Elastic Fusion | PDF와 card 보유 | runtime context와 GPU budget 기반 configuration 선택 비교군 |
| Subtask-Level Elastic Scheduling | PDF와 card 보유 | workload compression과 elastic scheduling 확장 비교군 |
| IDK Cascades for Time-Series Input Streams | PDF와 card 보유 | confidence/history 기반 escalation 비교군 |
| A Practical Linux Framework for Weakly-Hard Tasks with Constant Bandwidth Server | PDF와 card 보유 | bounded deadline miss와 Linux runtime 비교군 |

## 현재 우선 확보하지 않을 계열

- LLM inference, GPU swap, cache locking, GPU pub/sub만을 핵심으로 하는 논문은 실시간 DNN 배경에는 유용하지만 현재 `W/H/M + machine condition + slack` 문제와 직접 연결이 약하다.
- TSN, 무선 네트워크, 보안 공격/방어, 순수 캐시·IOMMU·메모리 격리 논문은 현재 원고의 related work 범위를 넓히지 않는다.
- 순수 response-time bound 또는 확률론적 schedulability 논문은 구체적인 formal guarantee가 필요해지는 시점에 다시 선별한다.

## PDF를 받은 뒤 확인할 공통 항목

1. 가변 변수와 trigger를 abstract가 아니라 algorithm 기준으로 확정한다.
2. adaptation이 runtime인지 offline design인지 구분한다.
3. `C`가 고정인지 mode-dependent인지 확인한다.
4. task arrival period, end-to-end deadline, local inference budget을 구분한다.
5. schedulability test, admission, fallback, empirical deadline miss 중 실제 보장 방식을 확인한다.
6. platform, workload, dataset, metric, 정량 결과를 원문 표와 figure에서 확인한다.

## 권장 처리 순서

첫 번째 묶음 3편은 PDF 수신을 완료했다.

1. `MURAL: A Multi-Resolution Anytime Framework for LiDAR Object Detection Deep Neural Networks` - 카드 완료
2. `Safety-Aware Implementation of Control Tasks via Scheduling with Period Boosting and Compressing` - 카드 완료
3. `ATER: Adaptive Task Execution Rate Regulation for Enhanced Real-Time Performance in ROS 2` - 카드 완료

두 번째 묶음은 다음 3편이다.

1. `Handling System Overloads: An Empirical Evaluation of Deadline-Miss Handling Strategies` - 카드 완료
2. `DNN-SAM: Split-and-Merge DNN Execution for Real-Time Object Detection` - 카드 완료
3. `Decntr: Optimizing Safety and Schedulability with Multi-Mode Control and Resource Allocation Co-Design` - 카드 완료
