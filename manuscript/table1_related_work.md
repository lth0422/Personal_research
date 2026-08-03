# Table 1 Draft: Related Work Comparison

이 파일은 `surveys/comparison_table.md`의 내부 상세 비교표를 원고용으로 압축한 초안이다.
현재 카드화한 개별 논문 80편을 모두 나열하지 않고, 관련연구 계열별 핵심 차이만 보여준다.

이 표는 관련연구 **계열** 비교용이다. Real-Time Fault Diagnosis 개별 논문의 O/△/X 비교는 `manuscript/realtime_fault_diagnosis_related_work_table.md`에서 관리한다. 최종 원고에서는 두 표의 역할과 지면을 보고 하나만 본문에 두거나 다른 하나를 부록으로 이동한다.

원고의 related-work 절 구성은 `surveys/research_aligned_literature_taxonomy_0723.md`의 RW1~RW4를 따른다. 아래 category는 보관 그룹과 세부 비교를 위한 행이며, MCU/SoC 같은 플랫폼은 독립적인 우선순위가 아니라 비교 태그다.

원고에 넣을 때는 venue/year 표기를 manuscript 스타일에 맞춰 줄이고, 정량 수치는 본문에서 검증된 경우에만 사용한다.

| Category | Representative works | Main variable | Adaptation trigger | RT/platform consideration | Limitation vs. this work |
| --- | --- | --- | --- | --- | --- |
| Elastic and rate-adaptive scheduling | Buttazzo et al. [1]; Buttazzo and Abeni [2]; Chantem et al. [3]; Orr et al. [4]; Marinoni and Buttazzo [5]; Burgio et al. [6]; Wang et al. [7]; Baruah [8]; Sudvarg et al. [9]; Xu et al. [10]; Li et al. [11]; Gifford et al. [12] | Period/rate, observed execution-time estimate, controller/mode, utilization, workload, CPU/bus mode, sampling rate, core/cache/BW allocation | Overload, estimated load, available utilization, mode-change event, control safety, shared-resource demand, message/processing-rate mismatch | EDF/RM/PDA and federated schedulability, soft feedback adaptation, TDES safe sequence, weakly-hard safety, multi-mode transition DBF, ROS 2 feedback | Measured execution-time feedback와 period 조절도 이미 존재하지만 hard bound는 아님. Vibration temporal `W`, diagnosis utility/anomaly score, inference `M`, hard-feasible mode selection과 PREEMPT_RT pipeline의 결합은 확인되지 않음 |
| Input-adaptive visual perception | Hu et al. [13]--[15]; Liu et al. [16]; Soyyigit et al. [17] | Image/segment size, LiDAR resolution, inspection frequency, canvas packing, batching | Object criticality, spatial uncertainty, workload, deadline, predicted execution time | Embedded GPU, autonomous driving/surveillance, deadline-aware perception | Vision/LiDAR spatial input 중심. Vibration window `W`, diagnosis period `H`, model `M`, machine condition 기반 utility를 함께 다루지 않음 |
| Input-adaptive fault diagnosis | Kim et al. [18]; Tang et al. [19], [20]; Jalonen et al. [21]; Zhang et al. [22]; Lima [23]; Shan et al. [24]; Sayghe [25] | Window/input/patch length, hop, sampling/compression ratio, model | Bearing parameters and fault frequency, anomaly deviation, speed, offline accuracy/resource profile | MCU/SoC target latency and fault-diagnosis accuracy, mostly offline/data-driven selection | Physics와 `W`를 연결하지만 system slack, deadline-aware runtime scheduling, `H/M` 공동 선택과 PREEMPT_RT는 확인되지 않음 |
| Deadline-aware DNN serving | Yao et al. [26]; Kang et al. [27]; Chen et al. [28]; Xu et al. [29]; Li et al. [30]; Cao et al. [31]; Han et al. [32]; He et al. [33]; Zhang et al. [34]; Raj et al. [35]; Xiang and Kim [58] | DNN stage/depth, input scale, model capability, heterogeneous mapping, exit, batch/fusion/offloading, CPU/GPU pipeline | Confidence, slack/deadline, queue/load, critical region, environment/control condition, GPU budget, heart rate, task admission | Non-preemptive EDF, fixed-priority WCRT, pipeline response-time analysis, edge GPU/server, SLO and deadline miss | Slack 기반 image scale와 profiling 기반 admission은 이미 다룸. Vibration temporal `W`, runtime machine condition + slack, `H/M`, PREEMPT_RT timing의 결합은 확인되지 않음 |
| Physical-state-aware slack management | Chwa et al. [59] | Physical-state-dependent LC/HC execution budget, runtime slack | External physical state at release, actual execution completion, budget overrun | EDF-VD mixed-criticality schedulability and safe LC/HC slack reclamation | External state + slack 자체는 이미 존재. State가 diagnostic fidelity를 정하는 구조, vibration `(W,H,M)`과 diagnosis metric은 다루지 않음 |
| Weakly-hard deadline semantics | Chen et al. [36]; Xu et al. [10] | `(m,K)` constraint, CBS parameters, safe miss pattern | Offline constraint derivation and server/schedule synthesis | Linux `SCHED_DEADLINE`, weakly-hard schedulability and control-safety analysis | Bounded miss의 대안적 보장 모델이다. Surveyed vibration FD work가 이 모델을 채택했다는 근거는 확인되지 않아 본 연구의 기본 타깃으로 전제하지 않음 |
| Deadline-miss handling and risk | Braun and Altmeyer [37]; Hawila et al. [38]; Guan et al. [39] | Kill/skip/queue, period, allowable consecutive misses, active dropping | Deadline miss/overload, stability constraint, probabilistic failure risk | STM32/ThreadX empirical fallback, fixed-priority and probabilistic EDF analysis | Miss 결과와 fallback 설계의 배경이지만 주로 control/general task domain이며 vibration diagnosis의 허용 miss를 직접 정당화하지 않음 |
| Deadline-aware classifier cascades | Agrawal et al. [40]; Baruah et al. [41] | Cascade order, classifier subset, deterministic fallback | Input history/confidence or offline deadline-constrained synthesis | Hard latency/deadline constraint, algorithmic evaluation | Model/exit 선택 비교군이지만 weakly-hard와 별개이며 vibration `W/H/M`, system slack, PREEMPT_RT는 다루지 않음 |
| Embedded fault diagnosis deployment | Thota et al. [42]; Ma et al. [43]; Lee and Kim [44]; Choi et al. [45]; Yang et al. [46]; He et al. [47]; Zhan et al. [48]; Garay et al. [49]; Langarica et al. [50] | Model architecture, fixed input/window, compression/pruning, end-edge stage | Mostly offline model/input design; 일부 confidence/fault-evidence cascade | MCU/SBC/SoC inference, TinyML, RTOS/Linux, target and end-to-end latency | Resource-constrained FD 배경과 일부 runtime cascade는 직접적이나 schedulability, deadline miss/jitter, q+S joint `W/H/M`, PREEMPT_RT 비교는 확인되지 않음 |
| PREEMPT_RT and SBC platform studies | Adam et al. [51]; Dewit et al. [52]; Vaghasiya [53]; De Marco et al. [54] | Kernel configuration, PREEMPT_RT 여부, TFLite/thread/configuration | Offline benchmarking/configuration search | Raspberry Pi/BeagleBone, cyclictest/latency, TFLite inference, CPU/temp/memory metrics | Platform timing 근거는 제공하지만 vibration FD algorithm, `W/H/M` adaptation, machine condition trigger는 다루지 않음 |
| Miscellaneous real-time scheduling | Pathan [55]; Tang et al. [56]; Guan et al. [57]; self-suspending EDF work [metadata 확인 필요] | Ready queue, priority inheritance, federated resources, analysis interval | Scheduling events, data propagation, criticality, self-suspension | EDF overhead, end-to-end latency, DAG scheduling, self-suspension analysis | Pipeline timing 해석의 보조 배경. 본 연구 novelty의 직접 비교군은 아님 |
| This work | 본 연구 | `W` window size, `H` diagnosis period/hop size, `M` model | Machine condition and system slack | Raspberry Pi Zero 2W, Linux/PREEMPT_RT, deadline-aware vibration fault diagnosis | 현재 연구에서 검증해야 할 주장 |

## Caption Draft

Comparison of related work by adaptation variable, trigger, and real-time/platform scope. Existing work already covers physical-state-aware slack management, elastic period/workload scheduling, adaptive input sizing, and deadline-aware DNN serving. In the surveyed papers, we did not find a runtime policy that separates vibration-state-driven diagnostic preference from slack-constrained feasibility while jointly selecting temporal diagnosis modes.

## Notes

- `Representative works`는 전체 인용 목록이 아니라 계열별 대표 예시다.
- `This work` 행은 원고에서 실험 결과가 준비된 뒤 표현 강도를 조정해야 한다.
- 정량 결과는 이 표에 넣지 않는다. 수치는 본문 또는 별도 result table에서 조건과 함께 제시한다.
- `Requirement-Based Analysis of Self-Suspending Tasks under EDF`는 저자 metadata 확인 후 참고문헌 번호를 부여한다.

## 참고문헌

[1] G. C. Buttazzo, G. Lipari, and L. Abeni, "Elastic Task Model for Adaptive Rate Control," *IEEE RTSS*, 1998.

[2] G. Buttazzo and L. Abeni, "Adaptive Rate Control through Elastic Scheduling," *IEEE CDC*, 2000.

[3] T. Chantem, X. S. Hu, and M. D. Lemmon, "Generalized Elastic Scheduling for Real-Time Tasks," *IEEE Transactions on Computers*, 2009.

[4] J. Orr et al., "Elastic Scheduling of Parallel Real-Time Tasks with Discrete Utilizations," *RTNS*, 2020.

[5] M. Marinoni and G. Buttazzo, "Elastic DVS Management in Processors With Discrete Voltage/Frequency Modes," *IEEE Transactions on Industrial Informatics*, 2007.

[6] P. Burgio et al., "Adaptive TDMA Bus Allocation and Elastic Scheduling," *IEEE ICCD*, 2010.

[7] X. Wang, Z. Li, and W. M. Wonham, "Dynamic Multiple-Period Reconfiguration of Real-Time Scheduling Based on Timed DES Supervisory Control," *IEEE Transactions on Industrial Informatics*, 2016.

[8] S. Baruah, "Improved Uniprocessor Scheduling of Systems of Sporadic Constrained-Deadline Elastic Tasks," *RTNS*, 2023.

[9] M. Sudvarg et al., "Elastic Scheduling for Harmonic Task Systems," *IEEE RTAS*, 2024.

[10] S. Xu et al., "Safety-Aware Implementation of Control Tasks via Scheduling with Period Boosting and Compressing," *IEEE RTCSA*, 2023.

[11] R. Li et al., "ATER: Adaptive Task Execution Rate Regulation for Enhanced Real-Time Performance in ROS 2," *IEEE RTCSA*, 2025.

[12] R. Gifford et al., "Decntr: Optimizing Safety and Schedulability with Multi-Mode Control and Resource Allocation Co-Design," *IEEE RTAS*, 2024.

[13] Y. Hu et al., "On Exploring Image Resizing for Optimizing Criticality-Based Machine Perception," *IEEE RTCSA*, 2021.

[14] Y. Hu et al., "Real-Time Task Scheduling with Image Resizing for Criticality-Based Machine Perception," *Real-Time Systems*, 2022.

[15] Y. Hu et al., "Algorithms for Canvas-Based Attention Scheduling with Resizing," *IEEE RTAS*, 2024.

[16] S. Liu et al., "Generalized Self-Cueing Real-Time Attention Scheduling with Intermittent Inspection and Image Resizing," *Real-Time Systems*, 2023.

[17] A. Soyyigit, S. Yao, and H. Yun, "MURAL: A Multi-Resolution Anytime Framework for LiDAR Object Detection Deep Neural Networks," *IEEE RTCSA*, 2025.

[18] M. Kim et al., "Anomaly Deviation-Based Window Size Selection of Sensor Data for Enhanced Fault Diagnosis Efficiency in Autonomous Manufacturing Systems," *Mathematics*, 2026.

[19] G. Tang et al., "Integrating Adaptive Input Length Selection Strategy and Unsupervised Transfer Learning for Bearing Fault Diagnosis Under Noisy Conditions," *Applied Soft Computing*, 2023.

[20] G. Tang et al., "A Novel Transfer Learning Network with Adaptive Input Length Selection and Lightweight Structure for Bearing Fault Diagnosis," *Engineering Applications of Artificial Intelligence*, 2023.

[21] T. Jalonen et al., "Real-Time Vibration-Based Bearing Fault Diagnosis Under Time-Varying Speed Conditions," *IEEE ICIT*, 2024.

[22] H. Zhang et al., "A Novel Fast Short-Time Root-MUSIC Method for Vibration Monitoring of High-Speed Spindles," arXiv:2506.17600, 2025.

[23] J. P. B. Lima, "Real-Time Fault Detection in Induction Motors Using TinyML: An Evaluation of the Edge Impulse Platform," *IEEE Latin Conference on IoT*, 2025.

[24] N. Shan et al., "Fast Fault Diagnosis in Industrial Embedded Systems Based on Compressed Sensing and Deep Kernel Extreme Learning Machines," *Sensors*, 2022.

[25] A. Sayghe, "A Physics-Aware Lightweight Transformer Network for Intelligent Bearing Fault Diagnosis Under Variable Operating Conditions," *Artificial Intelligence for Engineering*, 2026.

[26] S. Yao et al., "Scheduling Real-Time Deep Learning Services as Imprecise Computations," *IEEE RTCSA*, 2020.

[27] W. Kang et al., "DNN-SAM: Split-and-Merge DNN Execution for Real-Time Object Detection," *IEEE RTAS*, 2022.

[28] J. Chen et al., "SCENIC: Capability and Scheduling Co-Design for Intelligent Controller on Heterogeneous Platforms," *IEEE RTSS*, 2024.

[29] Y. Xu et al., "FLEX: Adaptive Task Batch Scheduling with Elastic Fusion in Multi-Modal Multi-View Machine Perception," *IEEE RTSS*, 2024.

[30] Y. Li et al., "Adaptive Model Selection for Real-Time Heart Disease Detection on Embedded Systems," *IEEE RTCSA*, 2025.

[31] J. Cao et al., "EdgeServing: Deadline-Aware Multi-DNN Serving at the Edge," arXiv:2605.05527, 2026.

[32] L. Han, Z. Zhou, and Z. Li, "Pantheon: Preemptible Multi-DNN Inference on Mobile Edge GPUs," *ACM MobiSys*, 2024.

[33] J. He et al., "Adaptive Scheduling for Edge-Assisted DNN Serving," arXiv, 2023.

[34] Z. Zhang et al., "BCEdge: SLO-Aware DNN Inference Services with Adaptive Batching on Edge Platforms," arXiv, 2023.

[35] S. Raj et al., "Adaptive Heuristics for Scheduling DNN Inferencing on Edge and Cloud for Personalized UAV Fleets," arXiv, 2025.

[36] M. Chen, P. Reich, Y. Wang, and H. Choi, "Work-in-Progress: A Practical Linux Framework for Weakly-Hard Tasks with Constant Bandwidth Server," *IEEE RTSS Work-in-Progress*, 2025.

[37] T. Braun and S. Altmeyer, "Handling System Overloads: An Empirical Evaluation of Deadline-Miss Handling Strategies," *IEEE RTAS*, 2025.

[38] I. Hawila, L. Cucu-Grosjean, and S. Ben Amor, "Period Assignment for Real-Time Cascade Control Tasks Under Stability and Schedulability Constraints," *ECRTS*, 2025.

[39] F. Guan, X. Jiang, W. Jing, and N. Guan, "Reducing Worst-Case Deadline Failure Probability for EDF Scheduling," *IEEE RTSS*, 2025.

[40] K. Agrawal, S. Baruah, A. Burns, and J. Zhao, "IDK Cascades for Time-Series Input Streams," *IEEE RTSS*, 2024.

[41] S. Baruah, I. Bate, A. Burns, and R. I. Davis, "Optimal Synthesis of Fault-Tolerant IDK Cascades for Real-Time Classification," *IEEE RTAS*, 2024.

[42] Y. R. Thota et al., "TinyML Enabled Real-Time Bearing Fault Classification in Motors Using Vibration Signals," *GLSVLSI*, 2025.

[43] S. Ma, H. Sun, S. Gao, and G. Zhou, "A Real-Time Mechanical Fault Diagnosis Approach Based on Lightweight Architecture Search Considering Industrial Edge Deployments," *Engineering Applications of Artificial Intelligence*, 2023.

[44] S. Lee and T. Kim, "FRFconv-TDSNet: Lightweight, Noise-Robust Convolutional Neural Network Leveraging Full-Receptive-Field Convolution and Time-Domain Statistics for Intelligent Machine Fault Diagnosis," *IEEE Transactions on Instrumentation and Measurement*, 2024.

[45] S. Choi, S. Kim, and T. Kim, "저비용 마이크로컨트롤러 환경에서의 경량 딥러닝 기반 회전기계 축 결함 진단 시스템," *한국소프트웨어종합학술대회 논문집*, 2025.

[46] C. Yang et al., "A Novel Bearing Fault Diagnosis Method Based on Stacked Autoencoder and End-Edge Collaboration," *IEEE CSCWD*, 2023.

[47] C. He et al., "Real-Time Fault Diagnosis of Motor Bearing via Improved Cyclostationary Analysis Implemented onto Edge Computing System," *IEEE Transactions on Instrumentation and Measurement*, 2023.

[48] Z. Zhan, S. Zhang, J. Xu, and D. Ma, "Edge-Oriented Bearing Fault Diagnosis via Triple-Lightweight Network With Adaptive Pruning," *IEEE Transactions on Instrumentation and Measurement*, 2026.

[49] C. E. Garay et al., "A Multimodal TinyML-Based Predictive Maintenance Architecture for Industrial IoT in the 6G Era," *Sensors*, 2026.

[50] S. Langarica, C. Ruffelmacher, and F. Nunez, "An Industrial Internet Application for Real-Time Fault Diagnosis in Industrial Motors," *IEEE Transactions on Automation Science and Engineering*, 2020.

[51] G. K. Adam, N. Petrellis, and L. T. Doulos, "Performance Assessment of Linux Kernels with PREEMPT_RT on ARM-Based Embedded Devices," *Electronics*, 2021.

[52] W. Dewit, A. Paolillo, and J. Goossens, "A Preliminary Assessment of the Real-Time Capabilities of Real-Time Linux on Raspberry Pi 5," 2024, venue 확인 필요.

[53] A. J. Vaghasiya, "Evaluating Real-Time Pattern Recognition in Autonomous Systems on COTS Hardware," M.Sc. thesis, 2025.

[54] R. De Marco et al., "Real-Time Dolphin Whistle Detection on Raspberry Pi Zero 2 W with a TFLite Convolutional Neural Network," *Robotics*, 2025.

[55] R. M. Pathan, "Design of an Efficient Ready Queue for Earliest-Deadline-First EDF Scheduler," *DATE*, 2016.

[56] Y. Tang et al., "Optimizing End-to-End Latency of Sporadic Cause-Effect Chains Using Priority Inheritance," *IEEE RTSS*, 2023.

[57] F. Guan et al., "Mixed-Criticality Federated Scheduling for Relaxed-Deadline DAG Tasks," *IEEE RTSS*, 2024.

[58] Y. Xiang and H. Kim, "Pipelined Data-Parallel CPU/GPU Scheduling for Multi-DNN Real-Time Inference," *IEEE RTSS*, 2019, doi: 10.1109/RTSS46320.2019.00042.

[59] H. S. Chwa, K. G. Shin, H. Baek, and J. Lee, "Physical-State-Aware Dynamic Slack Management for Mixed-Criticality Systems," *IEEE RTAS*, 2018, doi: 10.1109/RTAS.2018.00023.
