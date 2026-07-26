# 연구 질문 중심 문헌 분류 체계

- 작성일: 2026-07-23
- 기준: `PROJECT_CONTEXT.md`, `decisions/personal_research_summary_0708.md`
- 목적: 현재 10개 보관 폴더, 0708 서베이 산출물과 원고 related-work 섹션을 하나의 연구 논리로 연결한다.

## 1. 분류 원칙

논문은 MCU 또는 SoC라는 플랫폼만으로 최상위 분류하지 않는다. 본 연구의 핵심 질문은 진동 결함 진단의 품질 변수와 real-time schedulability를 어떻게 연결하는가이기 때문이다.

각 논문에는 다음 세 종류의 정보를 따로 붙인다.

1. **주 섹션**: 논문이 본 연구의 어떤 질문에 답하는가
2. **연구 축 태그**: 가변 변수, trigger, guarantee
3. **플랫폼·실행환경 태그**: MCU/SBC/heterogeneous SoC와 bare metal/RTOS/Linux/PREEMPT_RT를 독립적으로 기록

논문 하나가 여러 섹션과 연결될 수 있지만, 보관 폴더는 가장 강한 기여 하나를 기준으로 유지한다.

## 2. 서베이의 여섯 섹션

### S1. Embedded Real-Time Fault Diagnosis

**질문**: Fault-diagnosis 연구가 “real-time”을 어떻게 정의하고 달성하는가?

- Model compression, quantization, pruning, TinyML
- Embedded deployment와 end-to-end pipeline
- Average latency와 deadline/tail/miss의 구분
- RTOS 사용 여부와 system-level scheduling 유무

이 섹션에는 MCU와 SoC/SBC를 모두 포함한다. 플랫폼별 논문 수를 따로 보고하되, 핵심 분류는 `model-level best-effort`, `empirical deadline-aware`, `schedulability-backed`다.

대표 문헌: embedded vibration diagnosis와 end-edge diagnosis 사례 [1]--[4].

현재 보관 그룹:

- `05_fault_diagnosis_app`
- `06_platform_preempt_rt`, `07_platform_pi_zero2w`의 fault-diagnosis 직접 사례 일부

0708 산출물 연결: **산출물 1, Real-Time Fault Diagnosis 분류표**

### S2. Adaptive Diagnostic Fidelity

**질문**: 진단 품질을 위해 입력과 모델을 무엇에 따라 바꾸는가?

- Window/input length `W`
- Model 또는 exit `M`
- Sampling frequency와 signal semantics
- Machine condition, anomaly score와 confidence `q`
- Offline design과 runtime adaptation 구분

현재 보관 그룹:

- `02_input_adaptive`
- `05_fault_diagnosis_app`의 adaptive input/model 논문

본 연구 연결: `q -> diagnostic utility(W,M)`를 정의하는 근거

대표 문헌: adaptive input length, anomaly-based window selection과 physics-aware input design [5]--[7].

### S3. Elastic Rate and Workload Scheduling

**질문**: System load와 resource constraint 아래에서 period와 computation을 어떻게 탄력적으로 조절하는가?

- Period/rate `T`, diagnosis hop/period `H`
- Execution demand와 workload `C`
- Discrete utilization mode
- System load와 slack `S`
- Offline feasibility와 online adaptation

현재 보관 그룹:

- `01_elastic_scheduling`

0708 산출물 연결: **산출물 2, Elastic Scheduling 실전 응용과 가정**

본 연구 연결: `C(W,M)`과 `T=H/f_s`가 함께 변하는 task model

대표 문헌: elastic period/rate, discrete workload, constrained-deadline feasibility, multi-mode transition과 runtime rate regulation [12]--[17], [28].

### S4. Deadline-Aware AI Inference and Mode Selection

**질문**: Deadline 또는 slack을 이용해 inference quality와 configuration을 어떻게 선택하는가?

- Input resolution, model, exit, batch, mapping
- Deadline, queue, resource contention와 slack
- Mandatory/optional execution
- Admission, fallback와 runtime mode selection

현재 보관 그룹:

- `03_rt_dnn_serving`
- `02_input_adaptive`의 deadline-aware perception 일부

본 연구 연결: `S -> feasible modes`와 그 안에서의 quality selection

대표 문헌: slack/deadline/condition 기반 input·model 선택 [8]--[11]과 deadline-aware classifier cascade [26], [27].

### S5. Schedulability, Mode Transition, and Miss Semantics

**질문**: Mode를 바꾸거나 overload가 발생할 때 어떤 deadline 보장을 제공하는가?

- Schedulability analysis와 admission control
- Mode-change protocol과 carry-over job
- Weakly-hard deadline과 bounded miss
- Deadline-miss handling, fallback, drop/skip/queue
- Cyclic executive와 imprecise computation

현재 보관 그룹:

- `09_weakly_hard_realtime`
- `10_deadline_miss_handling_risk`
- `08_misc_realtime_scheduling`
- `01_elastic_scheduling`의 transition/guarantee 논문 일부

`04_cascade_inference`는 deadline-aware model/fallback 선택을 다루므로 주로 S4에 두고, hard deadline 또는 fallback semantics가 필요한 경우에만 S5로 교차 태그한다. Weakly-hard는 S5의 한 보장 모델일 뿐이며, 본 연구나 fault diagnosis 분야 전체의 기본 가정으로 사용하지 않는다.

0708 산출물 연결: **산출물 4, 고전 실시간 개념 노트**

본 연구 연결: Static mode feasibility와 transition feasibility를 구분하는 근거

대표 문헌: weakly-hard semantics [21], [22], deadline-miss handling과 risk [23]--[25], mode-transition·schedulability [15], [16], [28], general scheduling mechanisms [29]--[31].

### S6. Runtime Platform and Interference Characterization

**질문**: 제안한 방법을 실제 실행 환경에서 어떻게 검증하고 timing variation의 원인을 설명하는가?

- MCU + Zephyr/FreeRTOS/ThreadX
- Application-class SoC/SBC + Linux/PREEMPT_RT
- CPU/GPU heterogeneous SoC
- Scheduler policy, affinity, priority와 framework runtime
- CPU, memory, I/O, network interference
- Jitter, p95/p99/max, miss, temperature와 resource usage

현재 보관 그룹:

- `06_platform_preempt_rt`
- `07_platform_pi_zero2w`
- `08_misc_realtime_scheduling`의 pipeline/OS timing 논문 일부

0708 산출물 연결: **산출물 3, 부하 설계 전략**

이 섹션은 방법의 novelty보다 evaluation validity와 원인 분석을 담당한다. MCU와 SoC 중 하나를 배제하지 않고, 각 플랫폼에서 얻을 수 있는 근거를 구분한다.

대표 문헌: ARM/PREEMPT_RT latency characterization과 Raspberry Pi inference deployment [18]--[20].

## 3. 플랫폼은 태그로 관리

| 플랫폼 태그 | 의미 | 본 연구에서의 역할 |
| --- | --- | --- |
| `PL-MCU` | STM32/ESP32/Cortex-M | KCC 계보, low-level resource constraint |
| `PL-SBC-SOC` | Raspberry Pi/ARM Cortex-A SBC | 현재 Pi Zero 2W 평가 환경 |
| `PL-HET-SOC` | Jetson 등 CPU/GPU heterogeneous SoC | DNN runtime과 resource interference 비교 |
| `PL-SERVER-GPU` | Edge server/cloud GPU | Scheduling mechanism bridge |
| `PL-DESKTOP` | Desktop/laptop evaluation | Algorithm timing 참고, embedded 직접 비교 제한 |

| 실행환경 태그 | 의미 |
| --- | --- |
| `ENV-BAREMETAL` | OS 없이 직접 실행 |
| `ENV-RTOS` | Zephyr, FreeRTOS, ThreadX, QNX, VxWorks 등 |
| `ENV-LINUX` | 일반 Linux kernel |
| `ENV-PREEMPT_RT` | PREEMPT_RT가 적용된 Linux |
| `ENV-OTHER` | macOS, Windows, custom runtime 또는 확인 필요 |

플랫폼과 실행환경 태그는 검색 coverage와 external validity를 판단하는 데 사용한다. 예를 들어 같은 Raspberry Pi라도 일반 Linux와 PREEMPT_RT는 다른 실행환경이다. 문헌의 이론적 관련성 우선순위는 플랫폼 일치 여부만으로 결정하지 않는다.

## 4. 기존 보관 폴더 매핑

PDF와 paper-card 보관 그룹은 주된 방법론을 기준으로 관리하고, 아래처럼 연구 섹션 태그를 추가해 사용한다.

| 기존 그룹 | 주 섹션 | 보조 섹션 | 대표 참고문헌 |
| --- | --- | --- | --- |
| `01_elastic_scheduling` | S3 | S5 | [12]--[17], [28] |
| `02_input_adaptive` | S2 | S4 | [5]--[7], [9] |
| `03_rt_dnn_serving` | S4 | S5, S6 | [8], [10], [11] |
| `04_cascade_inference` | S4 | S5 | [26], [27] |
| `05_fault_diagnosis_app` | S1 | S2, S6 | [1]--[7] |
| `06_platform_preempt_rt` | S6 | S1 | [18], [19] |
| `07_platform_pi_zero2w` | S6 | S1 | [20] |
| `08_misc_realtime_scheduling` | S5 또는 S6 | S3 | [29]--[31], self-suspending EDF 논문 metadata 확인 필요 |
| `09_weakly_hard_realtime` | S5 | 없음 | [21], [22] |
| `10_deadline_miss_handling_risk` | S5 | S3 | [23]--[25] |

## 5. 원고용 Related Work 구조

여섯 서베이 섹션을 원고에서 그대로 여섯 절로 만들 필요는 없다. 학위논문 또는 RTAS/RTCSA 원고에서는 다음 네 절로 압축하는 것이 자연스럽다.

### RW1. Real-Time and Embedded Fault Diagnosis

- S1의 model-level best-effort와 deadline-aware 구분
- S6의 MCU/RTOS 및 SoC/Linux 구현 근거 중 fault diagnosis 직접 사례
- 결론: Embedded deployment는 많지만 scheduling guarantee의 수준은 별도 판정이 필요

### RW2. Adaptive Input and Diagnostic Fidelity

- S2의 window/input/model adaptation
- Machine condition과 diagnostic utility
- 결론: `W/M`은 품질 변수지만 대부분 offline이거나 system feasibility와 분리

### RW3. Elastic Scheduling and Mode-Change Guarantees

- S3의 period/workload elasticity
- S5의 admission, transition과 weakly-hard semantics
- 결론: `H/C` 조절과 guarantee 기반은 풍부하지만 vibration diagnosis utility와의 결합은 확인 필요

### RW4. Deadline-Aware AI Inference

- S4의 slack/deadline 기반 model/input/exit 선택
- GPU/vision 중심 scheduling bridge
- 결론: `S -> quality mode`는 이미 존재하며, 본 연구는 vibration temporal semantics와 diagnosis utility, mode feasibility를 검증해야 함

Platform characterization 자체는 long-term manuscript의 독립 related-work 절보다 evaluation methodology에 가깝다. KSC/PREEMPT_RT 트랙에서는 S6가 핵심 related-work 절이 된다.

## 6. 후보 우선순위 기준

플랫폼이 아니라 다음 점수로 원문 확보 순서를 정한다.

| 축 | 0점 | 1점 | 2점 |
| --- | --- | --- | --- |
| Domain | FD 아님 | 인접 condition monitoring | Vibration/machine FD |
| Variable | 고정 | `W/H/M` 중 하나 | 둘 이상 또는 `C/T` 결합 |
| Trigger | 없음/offline | `q` 또는 `S/load` | `q`와 system condition 결합 |
| Guarantee | latency만 | deadline/tail 측정 | schedulability/admission/transition 분석 |
| Evidence | abstract만 | full text 확보 | full text + 재현 가능한 task/platform 조건 |

Platform tag는 동점일 때 현재 evaluation 환경과의 직접성을 판단하는 보조 기준이다.

## 7. 현재 연구 위치

현재 조사 범위에서 연구의 연결 구조는 다음과 같다.

```text
S2: q와 diagnostic utility가 W/M의 선호도를 결정
                    +
S3/S4: S와 deadline이 feasible W/H/M을 제한
                    +
S5: static mode와 transition의 timing condition을 보장
                    +
S6: MCU/RTOS 선행 결과를 motivation으로 사용하고 Pi Zero 2W/Linux/PREEMPT_RT에서 검증
```

이 구조가 최종 novelty를 보장하지는 않는다. 각 연결이 기존 문헌에 있는지와 실제 실험에서 utility 및 deadline 개선이 나타나는지를 계속 검증해야 한다.

## 8. 참고문헌

[1] S. Lee and T. Kim, "FRFconv-TDSNet: Lightweight, Noise-Robust Convolutional Neural Network Leveraging Full-Receptive-Field Convolution and Time-Domain Statistics for Intelligent Machine Fault Diagnosis," *IEEE Transactions on Instrumentation and Measurement*, 2024.

[2] T. Jalonen, M. Al-Sa'd, S. Kiranyaz, and M. Gabbouj, "Real-Time Vibration-Based Bearing Fault Diagnosis Under Time-Varying Speed Conditions," *IEEE International Conference on Industrial Technology*, 2024, doi: 10.1109/ICIT58233.2024.10540813.

[3] H. Zhang, B. Liu, W. Feng, and Z. Li, "A Novel Fast Short-Time Root-MUSIC Method for Vibration Monitoring of High-Speed Spindles," arXiv:2506.17600, 2025.

[4] C. Yang, Z. Lai, Y. Wang, S. Lan, L. Wang, and L. Zhu, "A Novel Bearing Fault Diagnosis Method Based on Stacked Autoencoder and End-Edge Collaboration," *IEEE CSCWD*, 2023, doi: 10.1109/CSCWD57460.2023.10152598.

[5] G. Tang, C. Yi, L. Liu, Z. Xing, Q. Zhou, and J. Lin, "Integrating Adaptive Input Length Selection Strategy and Unsupervised Transfer Learning for Bearing Fault Diagnosis Under Noisy Conditions," *Applied Soft Computing*, vol. 148, 2023.

[6] M. Kim, S. Lee, D. Oh, B. Park, J. Jo, and C. Lee, "Anomaly Deviation-Based Window Size Selection of Sensor Data for Enhanced Fault Diagnosis Efficiency in Autonomous Manufacturing Systems," *Mathematics*, vol. 14, article 471, 2026.

[7] A. Sayghe, "A Physics-Aware Lightweight Transformer Network for Intelligent Bearing Fault Diagnosis Under Variable Operating Conditions," *Artificial Intelligence for Engineering*, 2026, doi: 10.1049/aie2.70014.

[8] W. Kang, S. Chung, J. Y. Kim, Y. Lee, K. Lee, J. Lee, K. G. Shin, and H. S. Chwa, "DNN-SAM: Split-and-Merge DNN Execution for Real-Time Object Detection," *IEEE RTAS*, 2022, doi: 10.1109/RTAS54340.2022.00021.

[9] A. Soyyigit, S. Yao, and H. Yun, "MURAL: A Multi-Resolution Anytime Framework for LiDAR Object Detection Deep Neural Networks," *IEEE RTCSA*, 2025, doi: 10.1109/RTCSA66114.2025.00014.

[10] Y. Li, Z. Li, A. A. Arafat, D. Johnson, N. Sui, A. Gehi, and Z. Guo, "Adaptive Model Selection for Real-Time Heart Disease Detection on Embedded Systems," *IEEE RTCSA*, 2025, doi: 10.1109/RTCSA66114.2025.00028.

[11] J. Chen, A. Zou, Y. Xu, and Y. Ma, "SCENIC: Capability and Scheduling Co-Design for Intelligent Controller on Heterogeneous Platforms," *IEEE RTSS*, 2024, doi: 10.1109/RTSS62706.2024.00026.

[12] G. C. Buttazzo, G. Lipari, and L. Abeni, "Elastic Task Model for Adaptive Rate Control," *IEEE RTSS*, 1998, pp. 286--295.

[13] G. Buttazzo and L. Abeni, "Adaptive Rate Control through Elastic Scheduling," *39th IEEE Conference on Decision and Control*, 2000, doi: 10.1109/CDC.2001.914704.

[14] J. Orr, J. Condori Uribe, C. Gill, S. Baruah, K. Agrawal, S. Dyke, A. Prakash, I. Bate, C. Wong, and S. Adhikari, "Elastic Scheduling of Parallel Real-Time Tasks with Discrete Utilizations," *RTNS*, 2020.

[15] S. Baruah, "Improved Uniprocessor Scheduling of Systems of Sporadic Constrained-Deadline Elastic Tasks," *RTNS*, 2023, doi: 10.1145/3575757.3575759.

[16] R. Gifford, F. Galarza-Jimenez, L. T. X. Phan, and M. Zamani, "Decntr: Optimizing Safety and Schedulability with Multi-Mode Control and Resource Allocation Co-Design," *IEEE RTAS*, 2024, doi: 10.1109/RTAS61025.2024.00032.

[17] R. Li, Z. Song, M. Lv, J.-M. Wu, C. J. Xue, J. Wang, and N. Guan, "ATER: Adaptive Task Execution Rate Regulation for Enhanced Real-Time Performance in ROS 2," *IEEE RTCSA*, 2025, doi: 10.1109/RTCSA66114.2025.00019.

[18] G. K. Adam, N. Petrellis, and L. T. Doulos, "Performance Assessment of Linux Kernels with PREEMPT_RT on ARM-Based Embedded Devices," *Electronics*, vol. 10, article 1331, 2021.

[19] W. Dewit, A. Paolillo, and J. Goossens, "A Preliminary Assessment of the Real-Time Capabilities of Real-Time Linux on Raspberry Pi 5," 2024, venue 확인 필요.

[20] R. De Marco, F. Di Nardo, A. Rongoni, L. Screpanti, and D. Scaradozzi, "Real-Time Dolphin Whistle Detection on Raspberry Pi Zero 2 W with a TFLite Convolutional Neural Network," *Robotics*, vol. 14, article 67, 2025.

[21] G. Bernat, A. Burns, and A. Llamosi, "Weakly Hard Real-Time Systems," *IEEE Transactions on Computers*, vol. 50, no. 4, pp. 308--321, 2001, doi: 10.1109/12.919277.

[22] M. Chen, P. Reich, Y. Wang, and H. Choi, "Work-in-Progress: A Practical Linux Framework for Weakly-Hard Tasks with Constant Bandwidth Server," *IEEE RTSS Work-in-Progress*, 2025.

[23] T. Braun and S. Altmeyer, "Handling System Overloads: An Empirical Evaluation of Deadline-Miss Handling Strategies," *IEEE RTAS*, 2025, doi: 10.1109/RTAS65571.2025.00031.

[24] I. Hawila, L. Cucu-Grosjean, and S. Ben Amor, "Period Assignment for Real-Time Cascade Control Tasks Under Stability and Schedulability Constraints," *ECRTS*, 2025.

[25] F. Guan, X. Jiang, W. Jing, and N. Guan, "Reducing Worst-Case Deadline Failure Probability for EDF Scheduling," *IEEE RTSS*, 2025.

[26] K. Agrawal, S. Baruah, A. Burns, and J. Zhao, "IDK Cascades for Time-Series Input Streams," *IEEE RTSS*, 2024.

[27] S. Baruah, I. Bate, A. Burns, and R. I. Davis, "Optimal Synthesis of Fault-Tolerant IDK Cascades for Real-Time Classification," *IEEE RTAS*, 2024.

[28] S. Xu, B. Ghosh, C. Hobbs, P. S. Thiagarajan, P. Joshi, and S. Chakraborty, "Safety-Aware Implementation of Control Tasks via Scheduling with Period Boosting and Compressing," *IEEE RTCSA*, 2023.

[29] R. M. Pathan, "Design of an Efficient Ready Queue for Earliest-Deadline-First EDF Scheduler," *DATE*, 2016.

[30] Y. Tang, X. Jiang, N. Guan, S. Liu, X. Luo, and W. Yi, "Optimizing End-to-End Latency of Sporadic Cause-Effect Chains Using Priority Inheritance," *IEEE RTSS*, 2023.

[31] F. Guan, J. Lee, C. J. Xue, J.-M. Wu, and N. Guan, "Mixed-Criticality Federated Scheduling for Relaxed-Deadline DAG Tasks," *IEEE RTSS*, 2024.

### 참고문헌 주의사항

- [19]의 venue는 현재 카드에서 확인되지 않아 최종 원고 인용 전에 원문 metadata를 재확인해야 한다.
- `Requirement-Based Analysis of Self-Suspending Tasks under EDF`는 저자 metadata가 확인되지 않아 참고문헌 번호를 부여하지 않았다.
- 이 목록은 S1--S6 분류를 설명하는 대표 문헌이며 보유 논문 76편 전체 bibliography가 아니다.
