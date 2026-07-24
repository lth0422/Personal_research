# Related Work Map

관련연구 분류와 원고 연결 지점을 정리하는 파일이다.

## Map

### Survey Coverage Status

- 현재 인벤토리 기준 보유 PDF는 76편이며, 76편 모두 paper card가 작성되었다.
- `Subtask-Level_Elastic_Scheduling_copy2_needs_check.pdf`는 `copy1`과 정규화 본문 해시가 같아 중복본으로 삭제했다.
- 연구 질문 중심 분류는 `surveys/research_aligned_literature_taxonomy_0723.md`의 S1~S6를 기준으로 한다. 현재 아래 절은 기존 보관 그룹을 탐색하기 위한 상세 view로 유지한다.
- `Miscellaneous Real-Time Scheduling`은 원고 핵심 주장이 아니라 end-to-end latency, EDF overhead, self-suspension 해석을 보조하는 배경으로 둔다.
- 0708 면담 이후 서베이 산출물은 `real-time fault diagnosis 분류표`, `elastic scheduling 실전 응용 가정표`, `부하 설계 전략`, `고전 실시간 개념 노트`로 재정렬한다.
- 교수님 보고용 한글 비교표는 `surveys/comparison_table_ko.md`에 둔다.
- 2026-07-21 LINER·Claude 검색의 신규 fault-diagnosis 14편과 elastic-scheduling 5편은 2026-07-24 full text 판정과 카드화를 완료했다.

### Elastic Scheduling

- Buttazzo et al., RTSS 1998은 periodic task의 period/rate를 elastic variable로 두고, overload 또는 task rate 변경 시 다른 task period를 조절해 schedulability를 유지하는 elastic task model을 최초 제안한다.
- Buttazzo et al., IEEE Transactions on Computers 2002는 1998년 원형의 journal extension 계열이다. 같은 핵심 모델과 HARTIK 실험을 바탕으로 decompression/rescaling, SRP 기반 resource constraint와 blocking, 안전한 period transition을 보강한다. 두 논문을 별개의 독립 방법으로 중복 집계하지 않는다.
- 두 논문의 현재 방법은 모두 execution time `C`를 고정하고 period `T`를 조절한다. 2002년 결론의 measured execution-time estimator는 future work이므로 현재 기법의 trigger나 가정으로 쓰지 않는다.
- Buttazzo and Abeni, CDC 2000은 별도 논문으로, 커널에서 task별 mean execution time과 observed maximum을 측정해 `Q_i`를 만들고 estimated load에 따라 period를 조절한다. 이는 measured `C` feedback와 `H/T` 조절을 결합한 직접 비교군이지만, observed maximum은 formal WCET가 아니며 transient와 sporadic deadline miss를 허용하는 soft real-time 접근이다.
- Chantem et al., IEEE Transactions on Computers 2009는 elastic scheduling을 schedulability와 performance metric 사이의 optimization problem으로 일반화하고, deadline < period task와 deadline selection까지 확장한다.
- Tian and Gui, Real-Time Systems 2011은 real-time process control에서 QoC measurement와 workload constraint를 함께 고려해 control period를 조절한다.
- Sudvarg et al., Real-Time Systems 2021은 elastic scheduling의 online admission control을 linear time으로 줄이는 구현을 제시한다.
- Salman et al., ETFA 2021은 elastic task model과 reservation-based compositional scheduling을 결합해 application-level period adaptation과 system-level bandwidth adaptation을 분리한다.
- Orr et al., RTNS 2020은 finite candidate utilization을 갖는 discrete elastic task model을 제안해 period와 computational workload를 함께 조절할 수 있게 한다.
- Sudvarg et al., RTAS 2024는 harmonic period constraint가 있는 implicit-deadline task system에서 offline lookup table과 online search로 period를 재할당한다.
- Xu et al., RTCSA 2023은 서로 다른 control-task sampling period를 common period로 boosting 또는 compressing하고, 일부 deadline miss를 허용하는 weakly-hard schedule을 plant safety margin 아래에서 합성한다.
- Xu et al.의 방법은 `H/T`와 application safety를 연결하는 직접 비교군이지만, fixed WCET와 offline model-based synthesis를 사용한다. Vibration diagnosis의 `W/M`, anomaly score와 runtime slack은 다루지 않는다.
- Li et al., RTCSA 2025 ATER은 ROS 2 executor 사이의 publish/subscribe-rate mismatch를 runtime에 관측하고, message drop과 execution-time distribution을 이용해 task-chain 선두의 sensor sampling rate를 높이거나 낮춘다.
- ATER은 본 연구의 diagnosis period `H`와 pipeline-state feedback을 연결하는 최신 비교군이다. 다만 formal schedulability/admission, fault-diagnosis utility, `W/M`, anomaly-based machine condition과 PREEMPT_RT 실측은 제공하지 않는다.
- Gifford et al., RTAS 2024 Decntr는 multi-mode CPS에서 safe controller와 sampling period, task-to-core mapping, cache/memory-bandwidth allocation 및 transition deadline relaxation을 공동 합성한다.
- Decntr는 known mode-change event에 precomputed feasible allocation을 적용하고 mode와 transition 모두의 schedulability를 검사한다는 점에서 본 연구 구조와 가깝다. 다만 linear control invariant safety가 중심이며 vibration `W`, diagnosis utility, anomaly-score feedback과 PREEMPT_RT execution은 다루지 않는다.
- Sudvarg et al., RTSS 2024는 multicore federated scheduling에서 parallel DAG task의 subtask workload와 core allocation을 elastic하게 조절한다.
- Sudvarg, PhD dissertation 2024와 Sudvarg et al., LITES 2025는 위 elastic extensions를 묶는 배경과 improved algorithm complexity를 제공한다.
- Marinoni and Buttazzo, IEEE TII 2007은 discrete DVS mode와 elastic task period를 함께 조절하고 early completion을 reclaim한다. `C`를 frequency-scalable/non-scalable 부분으로 나누지만 diagnosis mode에 따른 `C(W,M)`는 아니다.
- Burgio et al., ICCD 2010은 MPSoC에서 TDMA bus allocation별 WCET table과 ERIKA elastic scheduler를 결합해 bus slot과 task period를 runtime에 함께 바꾼다. Shared-resource interference가 execution cost에 미치는 영향을 mode table로 다룬다는 점이 중요하다.
- Wang et al., IEEE TII 2016은 initial safe sequence set이 비면 multiple period로 TDES supervisor를 다시 합성해 safe execution sequence를 열거한다. Static mode feasibility와 transition feasibility를 분리하는 S5 근거다.
- Baruah, RTNS 2023은 constrained-deadline elastic sporadic task에서 utilization 근사 대신 exact processor-demand analysis로 period를 정한다. 본 연구가 `D<T`를 사용하면 `U=C/T`만으로 충분하지 않을 수 있음을 보여준다.
- 공통점: system load, utilization, schedulability bound를 중심으로 rate/workload를 조절한다.
- 차이점: 이 계열은 general real-time scheduling 중심이며, vibration fault diagnosis의 window size W, model M, anomaly score 기반 machine condition, PREEMPT_RT/SBC 실시간성은 다루지 않는다.
- 0708 면담 이후 핵심 확인점: 기존 elastic scheduling이 `C` 고정 가정에 얼마나 의존하는지, 그리고 본 연구처럼 `C(W,M)`가 mode에 따라 바뀌는 경우 어떤 보장 조건이 필요한지 정리해야 한다.

### Input-Adaptive Visual Perception

- Hu et al., RTCSA 2021은 criticality 기반 machine perception에서 image resizing을 accuracy/response-time trade-off 변수로 사용한다.
- Hu et al., Real-Time Systems 2022는 LiDAR 기반 segmentation의 불완전성을 고려해 resizing과 segment merge를 함께 scheduling한다.
- Liu et al., Real-Time Systems 2023은 self-cueing, intermittent inspection, image resizing, batching을 결합해 object별 inspection quality와 frequency를 조절한다.
- Hu et al., RTAS 2024는 canvas-based attention scheduling에서 arbitrary object size, resizing, deadline, packing을 함께 다루며 spatiotemporal schedulability 관점을 제공한다.
- Soyyigit et al., RTCSA 2025 MURAL은 single shared-weight LiDAR DNN에서 pillar resolution을 runtime에 바꾸고, 현재 input의 resolution별 execution time을 예측해 deadline 안에 가능한 최고 resolution을 선택한다.
- MURAL은 input-fidelity selection과 mode-dependent cost의 강한 비교군이지만, trigger는 machine condition이 아니라 주어진 deadline과 predicted execution time이다. Diagnosis period `H`, model `M` 공동 선택, multi-task slack, PREEMPT_RT는 다루지 않는다.

### Real-Time DNN Serving

- Yao et al., RTCSA 2020은 DNN workflow를 mandatory/optional stages가 있는 imprecise computation으로 보고, deadline 안에서 confidence/accuracy utility가 높은 stage를 선택한다.
- Kang et al., RTAS 2022 DNN-SAM은 object-detection inference를 critical RoI mandatory subtask와 scaled full-image optional subtask로 분리하고, actual mandatory cost 이후 남은 slack으로 optional scale을 선택한다.
- DNN-SAM은 `system slack + input fidelity`를 이미 직접 결합하고 sufficient non-preemptive EDF condition을 제시한다. 본 연구와의 차이는 vibration temporal `W`, machine condition과 slack의 동시 trigger, `H/M` 공동 선택 및 PREEMPT_RT 환경에 있다.
- Chen et al., RTSS 2024 SCENIC은 DNN complexity, heterogeneous layer mapping, task priority와 WCRT를 environment-aware physical control capability에 연결하고 configuration을 offline co-design한다.
- SCENIC은 단순 ML accuracy 대신 application performance를 mode utility로 사용한다는 점에서 직접적이다. 그러나 runtime에는 fixed configuration을 실행하며 online condition-aware mode switch는 future work다.
- Xu et al., RTSS 2024 FLEX는 multi-modal multi-view machine perception에서 elastic fusion과 adaptive batching을 결합한다.
- FLEX의 가변 변수는 batch 구성과 modality fusion configuration이며, trigger는 view criticality, runtime sensing context, GPU time budget, deadline/schedulability 조건이다.
- Li et al., RTCSA 2025 AMS Heart Disease는 real-time ECG anomaly detection에서 instantaneous heart rate와 `D(HR)`를 기준으로 advanced, moderate, lightweight model 또는 anytime exit path를 선택한다.
- 이 논문의 직접적인 비교 가치는 condition에 따라 `M`을 고른다는 점이다. 다만 task arrival/period와 inference threshold의 관계, 평균 latency 기반 평가, deadline 초과 후 fallback 비용, independent-model AMS 대비 Anytime AMS의 runtime memory 및 tail-latency 우위는 충분히 분리되어 있지 않다.
- Cao et al., arXiv 2026 EdgeServing은 single shared GPU에서 model/service queue, early-exit point, batch size를 함께 선택해 per-request SLO violation과 tail latency를 줄이는 방향의 scheduler를 제안한다.
- Han et al., MobiSys 2024 Pantheon은 mobile edge GPU에서 concurrent real-time DNN task 간 chunk-level preemption과 early-exit variant adaptation을 결합한다.
- Laskaridis et al., EMDL 2021은 early-exit network의 architecture, training, exit policy, hardware co-design 요소를 정리한다.
- He et al., arXiv 2023은 edge server에서 layer-wise batching-aware DNN scheduling을 사용해 completion time 또는 on-time ratio를 개선하고, network/server congestion 시 client-side processing/offloading을 결합한다.
- Zhang et al., arXiv 2023 BCEdge는 request SLO와 model interference를 고려해 batch size와 concurrent model instance 수를 조절한다.
- Raj et al., arXiv 2025 DEMS-A/GEMS는 UAV fleet의 deadline-sensitive DNN task를 edge/cloud에 배치하며 dropping, migration, work stealing, cloud variability adaptation, windowed QoE completion rate를 다룬다.
- Ji et al., RTSS 2022 Demand Layering은 model parameter를 layer 단위로 load/execute해 embedded GPU DNN inference의 memory usage를 줄이고 memory-delay trade-off를 다룬다.
- Rahmath P et al., ACM Computing Surveys 2024는 early-exit DNN의 architecture, training, deployment, application, challenge를 포괄적으로 정리한다.
- 본 연구와의 연결: runtime에 제한된 계산 자원을 어떤 perception task와 configuration에 배분할지 정한다는 점에서 system slack 기반 mode selection 비교군으로 활용 가능하다.
- 차이점: 이 계열은 GPU serving, perception workload, ECG/health monitoring 중심이며, vibration window W, diagnosis period H, model M의 공동 선택과 PREEMPT_RT 실시간성은 다루지 않는다. 특히 AMS Heart Disease는 condition-aware이지만 현재 system slack을 함께 쓰는 정책으로 확인되지는 않았다.

### Weakly-Hard and Bounded Deadline Miss

- Chen et al., RTSS 2025 WiP는 Linux `SCHED_DEADLINE`의 Constant Bandwidth Server를 이용해 `(m,K)` weakly-hard task를 kernel modification 없이 실행하는 user-space API framework를 제안한다.
- Braun and Altmeyer, RTAS 2025는 STM32와 ThreadX에 rotary-pendulum controller를 구현하고, temporary overload에서 Kill, Skip-Next, Queue와 actuation timing을 비교한다. 전략 효과가 utilization, overload model과 task organization에 민감하며 보편적으로 최적인 조합은 없다고 보고한다.
- Braun and Altmeyer의 결과는 deadline miss 이후 fallback을 실제 구현에서 비교한다는 점이 중요하다. 다만 proactive schedulability/admission이나 vibration inference의 late-result semantics는 다루지 않으므로 특정 전략의 우위를 본 연구로 일반화하지 않는다.
- Agrawal et al., RTSS 2024는 time-series input stream에서 연속 입력 간 dependence를 학습해 IDK cascade의 expected response time을 줄이는 runtime algorithm을 제안한다.
- Baruah et al., RTAS 2024는 classifier가 잘못된 real class를 반환할 수 있는 fault model을 고려해 fault-tolerant IDK cascade를 offline으로 합성한다.
- Hawila et al., ECRTS 2025는 cascade control task의 period assignment를 stability와 fixed-priority schedulability 제약 아래에서 함께 최적화한다.
- Guan et al., RTSS 2025는 EDF scheduling에서 worst-case deadline failure probability 분석의 pessimism을 줄이고 active-dropping을 결합한다.
- 본 연구와의 연결: KSC 2026 실험의 deadline miss rate를 해석할 때 hard real-time zero-miss 관점과 bounded-miss QoS 관점을 구분하는 배경으로 활용 가능하다.
- 차이점: 이 계열은 task timing guarantee, classifier confidence, cascade synthesis 중심이며, vibration fault diagnosis의 W/H/M 선택, anomaly score trigger, PREEMPT_RT 비교 실험은 다루지 않는다.

### 본 연구와의 연결

- 관련연구에서 비교 대상으로 활용 가능하다.
- 공통점: 입력 크기 조절이 inference latency와 perception quality 사이의 trade-off를 만든다.
- 차이점: 이 계열은 vision object/segment/focus locale 중심이며, 본 연구의 vibration window size W, hop size H, model M, machine condition, system slack 조합과는 문제 구조가 다르다.

### Input-Adaptive Fault Diagnosis

- Kim et al., Mathematics 2026은 anomaly deviation score를 이용해 fault diagnosis용 time-series window size를 선택한다.
- Tang et al., Applied Soft Computing 2023은 noisy bearing transfer learning에서 bearing parameter와 sampling frequency에 기반한 adaptive input length를 사용한다.
- Tang et al., Engineering Applications of Artificial Intelligence 2023은 adaptive input length와 lightweight transfer network를 결합한다.
- Jalonen et al., ICIT 2024는 time-varying speed bearing dataset에서 2000-sample, 100 ms vibration segment를 사용해 lightweight CNN의 real-time inference 가능성을 보인다.
- Thota et al., GLSVLSI 2025는 ESP32 계열 microcontroller에서 raw triaxial vibration 기반 1D-CNN TinyML inference를 평가한다.
- Ma et al., Engineering Applications of Artificial Intelligence 2023은 실제 계산 시간 기반 objective를 포함한 architecture search로 lightweight mechanical fault diagnosis model을 찾는다.
- Lee and Kim, IEEE TIM 2024 FRFconv-TDSNet은 full-receptive-field convolution과 time-domain statistics를 결합해 noisy vibration fault diagnosis와 Raspberry Pi 4B edge inference를 평가한다.
- Choi et al., 한국소프트웨어종합학술대회 2025는 STM32F401RET6에서 FRFconv-TDSNet 기반 회전기계 축 결함 진단 시스템을 구현하고 sensing, inference, output 시간을 측정한다.
- Zhang et al., arXiv 2025는 STM32H743/FreeRTOS에서 fixed 16 ms frame의 high-resolution Root-MUSIC processing을 수행한다. 짧은 `W`와 spectral resolution을 직접 연결하지만 deadline/tail/miss는 없고 timing/memory 수치가 일부 불일치한다.
- Yang et al., CSCWD 2023은 local confidence와 allowable latency로 end 결과 수용 또는 edge diagnosis를 선택한다. Machine evidence와 timing constraint를 함께 쓰지만 schedulability나 explicit slack은 없다.
- He et al., IEEE TIM 2023은 STM32F407 online motor-bearing diagnosis의 전체 pipeline이 10.294 s임을 단계별로 제시한다. "real-time/online" 표기와 deadline 충족을 분리해야 하는 사례다.
- Lima, LCIoT 2025는 window, hop, sampling rate, model과 quantization을 offline 탐색해 nRF52840에 배포하며 subtle fault에서 quantization utility가 급락할 수 있음을 보인다.
- Shan et al., Sensors 2022는 Zynq MPSoC/Linux에서 4800-point window를 compressed sensing으로 줄여 DKELM diagnosis cost를 낮춘다. Physical average 0.17 s는 본문의 100 ms real-time 주장과 구분해야 한다.
- Sayghe, AIE 2026은 `P*=ceil(f_s/f_min)`으로 patch 크기를 정하고 Raspberry Pi 4에서 fixed `W/H` latency를 측정한다. Fault physics가 mode bank의 최소 정보량을 제한한다는 S2 근거다.
- Zhan et al., IEEE TIM 2026의 adaptive pruning은 training-time 구조 최적화이며 runtime `M` switching으로 세지 않는다.
- Garay et al., Sensors 2026은 target Cortex-M4F model latency와 cloud p95/p99를 분리해 edge-first inference 필요성을 보이지만 local deadline-aware mode selection은 없다.
- Langarica et al., IEEE TASE 2020은 DIPCA/RBC가 vibration fault를 가리킬 때 CNN stage를 실행하는 machine-evidence cascade다. System slack과 stage timing model은 없다.
- 나머지 신규 TinyML/dual-MCU/Raspberry Pi 사례도 실제 deployment 또는 replay를 제공하지만 모두 fixed configuration과 평균 latency 중심의 `B` 등급이다.
- 공통점: window size W가 anomaly visibility, feature separability, fault classification performance에 직접 영향을 준다는 문제의식을 공유한다.
- 차이점: 이 계열은 window/input length selection 또는 lightweight model 설계에 초점을 두며, 이번 14편 원문에서도 explicit deadline, tail/miss, schedulability와 q+S 기반 joint `W/H/M`은 확인되지 않았다. 이 결론은 현재 판정 집합에 한정한다.

### Platform and PREEMPT_RT

- Adam et al., Electronics 2021은 Raspberry Pi 3와 BeagleBone AI에서 PREEMPT_RT 적용 여부에 따른 response latency와 cyclictest latency를 비교한다.
- Adam, Computers 2021은 Raspberry Pi 3와 BeagleBone Black에서 PREEMPT_RT patched kernel의 response latency와 periodic task latency를 측정한다.
- Dewit et al., 2024 Raspberry Pi 5 preliminary assessment는 stress-ng와 iperf3 부하 하에서 cyclictest scheduling latency를 측정해 stock kernel과 PREEMPT_RT kernel을 비교한다.
- Vaghasiya, M.Sc. thesis 2025는 Raspberry Pi에서 Xenomai 3, Xenomai 4, PREEMPT-RT를 object detection workload와 함께 비교하는 thesis이다.
- Wang et al., Engineering Structures 2023은 Raspberry Pi 4 기반 low-cost real-time displacement measurement system을 제시한다.
- De Marco et al., Robotics 2025는 Raspberry Pi Zero 2W에서 TFLite CNN을 이용한 real-time acoustic detection을 구현하고, thread count에 따른 latency, throughput, CPU load, temperature를 측정한다.
- Jeya Agastin K et al., IRJAEM 2025는 Raspberry Pi Zero 2W에서 YOLOv5n INT8/TFLite object detection pipeline을 제시한다.
- 본 연구와의 연결: KSC 2026 실험에서 `cyclictest -> pipeline latency -> deadline miss` 순서로 실시간성을 검증하는 구조를 뒷받침한다.
- 차이점: PREEMPT_RT 문헌은 kernel benchmark 중심이고, Pi Zero 2W TFLite 문헌은 acoustic detection 중심이므로 vibration FD pipeline 결과는 본 연구에서 별도로 측정해야 한다.
- 0708 면담 이후 방향 1의 역할: 독립 논문 목표보다 방향 2를 위한 platform characterization과 원인 분석 자료로 둔다. 부하 조건은 문헌의 stress design을 확인한 뒤 확정한다.

### Miscellaneous Real-Time Scheduling

- Pathan, DATE 2016은 EDF scheduler의 ready queue data structure를 개선해 scheduling overhead를 낮추는 방법을 제안한다.
- Tang et al., RTSS 2023은 sporadic cause-effect chain의 maximum reaction time과 data age를 줄이기 위해 dynamic priority inheritance를 제안한다.
- Guan et al., RTSS 2024는 relaxed-deadline DAG task를 mixed-criticality federated scheduling에서 다룬다.
- Requirement-Based Analysis of Self-Suspending Tasks under EDF, RTSS 2025는 EDF에서 self-suspending task의 infeasibility requirement와 interval extension analysis를 다룬다.
- 본 연구와의 연결: pipeline end-to-end latency, EDF overhead, sensing/I/O wait 해석에 보조 배경으로 사용할 수 있다.
- 차이점: 이 그룹은 본 연구의 핵심인 machine condition + system slack 기반 W/H/M runtime selection을 직접 다루지 않는다.

### Comparison Axes for Manuscript

- `Section`: S1 real-time FD, S2 diagnostic fidelity, S3 elastic rate/workload, S4 deadline-aware inference, S5 guarantee/transition, S6 platform characterization.
- `Variable`: 입력 크기, window/input length, inspection frequency, batching, model.
- `Trigger`: criticality, uncertainty, anomaly deviation, bearing parameter, workload, deadline.
- `Runtime/Offline`: runtime scheduling인지 offline selection인지 구분한다.
- `RT Constraint`: deadline, latency, jitter, schedulability, RTOS/PREEMPT_RT 고려 여부를 분리한다.
- `Platform Tag`: MCU/RTOS, SBC/Linux, heterogeneous SoC, server/GPU, desktop을 별도 기록하며 관련성 우선순위로 사용하지 않는다.
- 이 축은 `surveys/comparison_table.md`와 맞춰 유지한다.
- 원고용 압축 표 초안은 `manuscript/table1_related_work.md`에 둔다. 기존 `surveys/comparison_table.md`는 내부 상세표로 유지한다.
