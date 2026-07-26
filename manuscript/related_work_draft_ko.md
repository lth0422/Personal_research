# Related Work 초안

> 상태: 교수님 검토용 한글 초안
> 기준일: 2026-07-26
> 대상 연구: Raspberry Pi Zero 2W와 PREEMPT_RT 기반 machine- and slack-aware vibration fault diagnosis
> 인용 형식: 본문 `[번호]`와 문서 하단 참고문헌 목록을 1:1로 연결한다.

## 1. 실시간·임베디드 결함 진단

진동 기반 결함 진단 연구는 경량 모델과 신호처리 파이프라인을 MCU, SBC와 edge SoC에 배포하며 실시간 처리 가능성을 평가해 왔다. FRFconv-TDSNet은 경량 구조와 noise robustness를 제시하고 Raspberry Pi 4B에서 추론 시간을 평가했지만, 입력 길이와 모델은 배포 전에 고정되며 deadline 기반 runtime scheduling은 다루지 않는다 [1]. Jalonen 등은 시변 회전속도 조건에서 고정 길이 진동 segment의 처리시간을 acquisition interval과 비교했으나, 실제 hardware deadline과 tail latency 또는 runtime mode 전환을 제시하지 않는다 [2]. Zhang 등은 STM32H743과 FreeRTOS에서 짧은 16 ms frame을 처리하는 진동 모니터링 기법을 구현했지만, 평균 처리시간 중심의 평가이며 task deadline, jitter, miss와 schedulability analysis는 제공하지 않는다 [3].

일부 연구는 진단 결과에 따라 처리 위치나 후속 단계를 바꾸는 runtime 구조를 제안한다. Yang 등은 local confidence와 allowable latency를 이용해 end와 edge 사이의 진단 경로를 선택한다 [4]. 이는 기계 상태에 가까운 confidence와 timing 조건을 함께 사용한다는 점에서 직접적인 비교 대상이다. 다만 해당 조건은 system-wide slack이나 schedulability test가 아니며, 물리 MCU와 network에서의 timing guarantee도 명확하지 않다. 따라서 현재 검토한 결함 진단 문헌은 경량화와 평균 실행시간, online 동작을 주로 다루며, explicit deadline, tail 또는 miss, system scheduling과 admission을 함께 제시한 사례는 제한적이다. 이 판단은 현재 확보한 문헌 집합에 한정한다.

## 2. 진단 입력 크기와 품질 적응

진동 window는 단순한 연산량 변수가 아니라 결함 정보를 담는 시간 구간이다. Tang 등은 bearing parameter, sampling frequency, speed와 fault characteristic frequency를 사용해 adaptive input length를 계산하고 noisy condition에서 진단 성능을 평가한다 [5]. Kim 등은 variability, cycle과 local spike에서 anomaly deviation을 계산해 fault diagnosis에 적합한 window를 선택한다 [6]. 두 연구는 진동 신호의 특성에 따라 입력 길이를 정해야 한다는 근거를 제공하지만, 주된 선택은 offline 또는 data-driven design 단계에서 수행되며 현재 system slack을 반영한 runtime admission은 아니다.

Sayghe는 sampling frequency와 최소 fault frequency에서 physics-aware patch 크기를 도출하고 lightweight transformer를 Raspberry Pi 4에서 평가한다 [7]. 이 결과는 window 또는 patch를 줄일 때 fault-related temporal information이 보존되어야 한다는 물리적 하한의 근거가 된다. 그러나 이 구성도 deployment 시 고정되며 deadline, tail latency와 runtime `W/H/M` 선택은 포함하지 않는다. 따라서 본 연구에서는 `W`를 latency를 낮추기 위한 자유 변수로만 보지 않고, physics-derived admissibility 또는 condition-dependent diagnostic utility와 함께 정의할 필요가 있다.

## 3. Deadline-aware AI 추론과 mode 선택

Real-time perception 분야에서는 deadline이나 slack에 따라 input 또는 model fidelity를 runtime에 조절하는 방법이 이미 제안되었다. DNN-SAM은 object detection을 mandatory critical-region 처리와 optional full-image 처리로 나누고, mandatory 실행 후 남은 slack으로 optional input scale을 선택한다 [8]. MURAL은 input별 resolution-dependent execution time을 예측하고 deadline 안에서 실행 가능한 LiDAR resolution을 선택한다 [9]. 따라서 `system slack -> input fidelity` 자체는 본 연구의 새로운 요소로 주장할 수 없다.

Machine 또는 environment condition을 model capability와 연결하는 연구도 존재한다. Li 등은 instantaneous heart rate와 이에 따른 deadline을 이용해 서로 다른 CNN complexity 또는 anytime exit를 선택한다 [10]. SCENIC은 plant와 environment condition, DNN capability, CPU/GPU mapping과 fixed-priority response time을 offline에서 공동 최적화한다 [11]. 전자는 condition-aware model selection을 제공하지만 system slack에 따른 feasible mode filtering이 약하고, 후자는 schedulability와 application capability를 연결하지만 runtime condition adaptation은 future work로 남긴다. 본 연구가 검증해야 할 차이는 condition-aware 또는 slack-aware 선택 각각이 아니라, 진동 신호의 temporal fidelity와 machine condition으로 mode utility를 정의하고 system feasibility로 admissible mode를 먼저 제한하는 결합 구조다.

## 4. Elastic scheduling과 mode-change guarantee

고전 elastic task model은 periodic task의 period를 elastic variable로 두고 overload나 rate-change request가 발생하면 utilization bound 안에서 task period를 조절한다 [12]. 이 원형은 diagnosis period `H`를 elastic variable로 보는 이론적 출발점이지만 execution time `C`를 고정한다. Buttazzo와 Abeni는 kernel에서 관측한 mean과 maximum execution time으로 estimated load를 계산해 period를 조절하는 feedback 구조를 제안했다 [13]. 그러나 관측 maximum은 formal WCET가 아니며 transient 또는 sporadic deadline miss를 허용하므로 hard-feasibility 근거와 구분해야 한다.

이후 연구는 discrete workload와 constrained deadline으로 elastic model을 확장했다. Orr 등은 parallel real-time task에 대해 finite discrete utilization과 workload mode를 선택하는 문제를 다룬다 [14]. 이는 `(W,H,M)`을 사전 profiling한 discrete mode bank로 구성하는 근거가 된다. Baruah는 `D<T`인 constrained-deadline elastic task에 processor-demand analysis를 적용하여 utilization-only approximation보다 직접적인 EDF feasibility 조건을 제시한다 [15]. 따라서 본 연구에서 diagnosis deadline을 period보다 짧게 정의한다면 단순 `C/T` 조건만으로 충분하지 않을 수 있다.

실제 multi-mode system에서는 mode endpoint뿐 아니라 transition demand도 검증해야 한다. Decntr는 controller, sampling period와 multicore resource allocation을 offline에서 공동 설계하고 old/new mode job의 demand를 포함해 transition schedulability를 확인한다 [16]. 구조적으로는 feasible mode set과 runtime mode-change event를 분리한다는 점에서 본 연구와 가깝지만, linear control safety와 known mode graph를 대상으로 하며 vibration window와 diagnosis utility를 다루지 않는다. ATER은 ROS 2 pipeline의 message drop, processing rate와 backlog를 관측해 sensor sampling rate를 runtime에 조절한다 [17]. 이는 diagnosis period `H`의 runtime regulation과 직접 연결되지만 formal deadline admission이나 application utility guarantee는 제공하지 않는다.

종합하면 period, workload, resource allocation과 transition을 조절하는 선행연구는 존재한다. 본 연구의 차별점은 elastic scheduling 자체가 아니라, mode-dependent execution cost `C(W,M)`, vibration-specific diagnostic utility, machine condition과 PREEMPT_RT에서 관측한 system slack을 하나의 feasibility-first 정책으로 연결하는지에 달려 있다.

## 5. Linux/PREEMPT_RT와 Pi 기반 실행환경

Application-class edge platform에서는 model inference time 외에 Linux scheduling latency와 interference를 별도로 측정해야 한다. Adam 등은 ARM 기반 embedded device에서 일반 Linux와 PREEMPT_RT kernel의 response latency를 비교하여 kernel configuration이 timing behavior에 미치는 영향을 평가한다 [18]. Dewit 등은 Raspberry Pi 5에서 stock kernel과 PREEMPT_RT kernel의 scheduling latency를 stress condition 아래 비교한다 [19]. 이 결과들은 cyclictest와 tail 또는 maximum latency를 이용한 kernel-level characterization의 근거지만, Raspberry Pi Zero 2W의 vibration diagnosis pipeline 결과로 직접 일반화할 수 없다.

De Marco 등은 Raspberry Pi Zero 2W에서 TFLite CNN을 이용한 acoustic detection을 수행하고 thread 수, inference latency, throughput, CPU load와 temperature를 평가한다 [20]. 이는 Pi Zero 2W에서 장시간 neural inference를 수행할 수 있다는 플랫폼 근거를 제공하지만 vibration diagnosis, PREEMPT_RT 비교와 deadline-aware scheduling은 다루지 않는다. 따라서 본 연구의 플랫폼 기여는 Pi Zero 2W가 새롭다는 주장보다, 동일 board에서 일반 Linux와 PREEMPT_RT를 통제 비교하고 CPU, memory와 I/O interference 아래 mode별 tail response time과 deadline miss를 end-to-end diagnosis pipeline에서 측정하는 데 두어야 한다.

## 6. 본 연구의 위치

기존 연구는 vibration input length와 diagnostic performance [5]--[7], slack 또는 condition에 따른 AI fidelity 선택 [8]--[11], period와 workload의 elastic feasibility 및 transition [12]--[17], Linux/PREEMPT_RT timing characterization [18]--[20]을 각각 제공한다. 그러나 현재 검토한 문헌에서는 vibration fault diagnosis의 `W/H/M` mode utility를 machine condition으로 평가하고, Pi Zero 2W의 PREEMPT_RT 환경에서 관측한 system slack과 feasibility condition으로 runtime mode를 제한하는 전체 구조는 확인되지 않았다. 이 문장은 문헌 부재의 확정이 아니라 현재 76편의 검토 범위에서 도출한 연구 가설이다.

초기 구현에서는 model `M`을 고정하고 discrete `(W,H)` mode bank부터 검증한다. 각 mode의 `C_mean`, `C_p95`, `C_p99`, `C_max`와 deadline miss를 profiling하고, feasibility를 통과한 mode 중 machine condition에 대한 utility가 높은 mode를 선택한다. 이후 mode-dependent model cost와 transition overhead를 안전하게 설명할 수 있을 때 `M`을 확장 변수로 추가한다.

## 참고문헌

[1] S. Lee and T. Kim, “FRFconv-TDSNet: Lightweight, Noise-Robust Convolutional Neural Network Leveraging Full-Receptive-Field Convolution and Time-Domain Statistics for Intelligent Machine Fault Diagnosis,” *IEEE Transactions on Instrumentation and Measurement*, 2024.

[2] T. Jalonen, M. Al-Sa'd, S. Kiranyaz, and M. Gabbouj, “Real-Time Vibration-Based Bearing Fault Diagnosis Under Time-Varying Speed Conditions,” *IEEE International Conference on Industrial Technology*, 2024, doi: 10.1109/ICIT58233.2024.10540813.

[3] H. Zhang, B. Liu, W. Feng, and Z. Li, “A Novel Fast Short-Time Root-MUSIC Method for Vibration Monitoring of High-Speed Spindles,” arXiv:2506.17600, 2025.

[4] C. Yang, Z. Lai, Y. Wang, S. Lan, L. Wang, and L. Zhu, “A Novel Bearing Fault Diagnosis Method Based on Stacked Autoencoder and End-Edge Collaboration,” *IEEE CSCWD*, 2023, doi: 10.1109/CSCWD57460.2023.10152598.

[5] G. Tang, C. Yi, L. Liu, Z. Xing, Q. Zhou, and J. Lin, “Integrating Adaptive Input Length Selection Strategy and Unsupervised Transfer Learning for Bearing Fault Diagnosis Under Noisy Conditions,” *Applied Soft Computing*, vol. 148, 2023.

[6] M. Kim, S. Lee, D. Oh, B. Park, J. Jo, and C. Lee, “Anomaly Deviation-Based Window Size Selection of Sensor Data for Enhanced Fault Diagnosis Efficiency in Autonomous Manufacturing Systems,” *Mathematics*, vol. 14, article 471, 2026.

[7] A. Sayghe, “A Physics-Aware Lightweight Transformer Network for Intelligent Bearing Fault Diagnosis Under Variable Operating Conditions,” *Artificial Intelligence for Engineering*, 2026, doi: 10.1049/aie2.70014.

[8] W. Kang, S. Chung, J. Y. Kim, Y. Lee, K. Lee, J. Lee, K. G. Shin, and H. S. Chwa, “DNN-SAM: Split-and-Merge DNN Execution for Real-Time Object Detection,” *IEEE RTAS*, 2022, doi: 10.1109/RTAS54340.2022.00021.

[9] A. Soyyigit, S. Yao, and H. Yun, “MURAL: A Multi-Resolution Anytime Framework for LiDAR Object Detection Deep Neural Networks,” *IEEE RTCSA*, 2025, doi: 10.1109/RTCSA66114.2025.00014.

[10] Y. Li, Z. Li, A. A. Arafat, D. Johnson, N. Sui, A. Gehi, and Z. Guo, “Adaptive Model Selection for Real-Time Heart Disease Detection on Embedded Systems,” *IEEE RTCSA*, 2025, doi: 10.1109/RTCSA66114.2025.00028.

[11] J. Chen, A. Zou, Y. Xu, and Y. Ma, “SCENIC: Capability and Scheduling Co-Design for Intelligent Controller on Heterogeneous Platforms,” *IEEE RTSS*, 2024, doi: 10.1109/RTSS62706.2024.00026.

[12] G. C. Buttazzo, G. Lipari, and L. Abeni, “Elastic Task Model for Adaptive Rate Control,” *IEEE RTSS*, 1998, pp. 286--295.

[13] G. Buttazzo and L. Abeni, “Adaptive Rate Control through Elastic Scheduling,” *39th IEEE Conference on Decision and Control*, 2000, doi: 10.1109/CDC.2001.914704.

[14] J. Orr, J. Condori Uribe, C. Gill, S. Baruah, K. Agrawal, S. Dyke, A. Prakash, I. Bate, C. Wong, and S. Adhikari, “Elastic Scheduling of Parallel Real-Time Tasks with Discrete Utilizations,” *RTNS*, 2020.

[15] S. Baruah, “Improved Uniprocessor Scheduling of Systems of Sporadic Constrained-Deadline Elastic Tasks,” *RTNS*, 2023, doi: 10.1145/3575757.3575759.

[16] R. Gifford, F. Galarza-Jimenez, L. T. X. Phan, and M. Zamani, “Decntr: Optimizing Safety and Schedulability with Multi-Mode Control and Resource Allocation Co-Design,” *IEEE RTAS*, 2024, doi: 10.1109/RTAS61025.2024.00032.

[17] R. Li, Z. Song, M. Lv, J.-M. Wu, C. J. Xue, J. Wang, and N. Guan, “ATER: Adaptive Task Execution Rate Regulation for Enhanced Real-Time Performance in ROS 2,” *IEEE RTCSA*, 2025, doi: 10.1109/RTCSA66114.2025.00019.

[18] G. K. Adam, N. Petrellis, and L. T. Doulos, “Performance Assessment of Linux Kernels with PREEMPT_RT on ARM-Based Embedded Devices,” *Electronics*, vol. 10, article 1331, 2021.

[19] W. Dewit, A. Paolillo, and J. Goossens, “A Preliminary Assessment of the Real-Time Capabilities of Real-Time Linux on Raspberry Pi 5,” 2024, venue 확인 필요.

[20] R. De Marco, F. Di Nardo, A. Rongoni, L. Screpanti, and D. Scaradozzi, “Real-Time Dolphin Whistle Detection on Raspberry Pi Zero 2 W with a TFLite Convolutional Neural Network,” *Robotics*, vol. 14, article 67, 2025.

## 참고문헌 사용 위치

| 번호 | 사용 목적 |
| --- | --- |
| [1]--[4] | Embedded fault diagnosis의 실시간성 수준과 runtime cascade 비교 |
| [5]--[7] | Vibration window와 physics/diagnostic utility의 관계 |
| [8]--[11] | Slack, deadline와 condition 기반 AI mode 선택 |
| [12]--[17] | Elastic period/workload, discrete mode, feasibility와 transition |
| [18]--[20] | Linux/PREEMPT_RT와 Pi Zero 2W 평가 방법 |

## 작성 시 확인할 사항

- [3]은 arXiv preprint이므로 최종 원고의 핵심 인용으로 사용할지 결정해야 한다.
- [19]는 현재 paper card에서 venue가 확인되지 않았다. 최종 bibliography에 넣기 전 원문 metadata를 재확인해야 한다.
- “확인되지 않았다”는 표현은 현재 76편의 검토 범위를 함께 명시한다.
- KCC 2026 STM32F407 + Zephyr 결과는 본 연구의 motivation이며 이 문서의 외부 참고문헌 목록에는 아직 포함하지 않았다. 실제 원고에서는 본인 선행논문 인용 정보를 확정한 뒤 추가한다.
