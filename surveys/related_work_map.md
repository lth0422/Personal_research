# Related Work Map

관련연구 분류와 원고 연결 지점을 정리하는 파일이다.

## Map

### Survey Coverage Status

- 현재 인벤토리 기준 중복 제거 후 보유 PDF는 49편이며, 49편 모두 paper card가 작성되었다.
- `Subtask-Level_Elastic_Scheduling_copy2_needs_check.pdf`는 `copy1`과 정규화 본문 해시가 같아 중복본으로 삭제했다.
- 핵심 related work 축은 `Elastic Scheduling`, `Input-Adaptive Fault Diagnosis`, `Real-Time DNN Serving`, `Platform and PREEMPT_RT`로 정리한다.
- `Miscellaneous Real-Time Scheduling`은 원고 핵심 주장이 아니라 end-to-end latency, EDF overhead, self-suspension 해석을 보조하는 배경으로 둔다.

### Elastic Scheduling

- Buttazzo et al., RTSS 1998은 periodic task의 period/rate를 elastic variable로 두고, overload 또는 task rate 변경 시 다른 task period를 조절해 schedulability를 유지하는 모델을 제안한다.
- Buttazzo et al., IEEE Transactions on Computers 2002는 elastic scheduling을 flexible workload management framework로 정리하고, current workload에 따른 rate adaptation과 overload management를 다룬다.
- Chantem et al., IEEE Transactions on Computers 2009는 elastic scheduling을 schedulability와 performance metric 사이의 optimization problem으로 일반화하고, deadline < period task와 deadline selection까지 확장한다.
- Tian and Gui, Real-Time Systems 2011은 real-time process control에서 QoC measurement와 workload constraint를 함께 고려해 control period를 조절한다.
- Sudvarg et al., Real-Time Systems 2021은 elastic scheduling의 online admission control을 linear time으로 줄이는 구현을 제시한다.
- Salman et al., ETFA 2021은 elastic task model과 reservation-based compositional scheduling을 결합해 application-level period adaptation과 system-level bandwidth adaptation을 분리한다.
- Orr et al., RTNS 2020은 finite candidate utilization을 갖는 discrete elastic task model을 제안해 period와 computational workload를 함께 조절할 수 있게 한다.
- Sudvarg et al., RTAS 2024는 harmonic period constraint가 있는 implicit-deadline task system에서 offline lookup table과 online search로 period를 재할당한다.
- Sudvarg et al., RTSS 2024는 multicore federated scheduling에서 parallel DAG task의 subtask workload와 core allocation을 elastic하게 조절한다.
- Sudvarg, PhD dissertation 2024와 Sudvarg et al., LITES 2025는 위 elastic extensions를 묶는 배경과 improved algorithm complexity를 제공한다.
- 공통점: system load, utilization, schedulability bound를 중심으로 rate/workload를 조절한다.
- 차이점: 이 계열은 general real-time scheduling 중심이며, vibration fault diagnosis의 window size W, model M, anomaly score 기반 machine condition, PREEMPT_RT/SBC 실시간성은 다루지 않는다.

### Input-Adaptive Visual Perception

- Hu et al., RTCSA 2021은 criticality 기반 machine perception에서 image resizing을 accuracy/response-time trade-off 변수로 사용한다.
- Hu et al., Real-Time Systems 2022는 LiDAR 기반 segmentation의 불완전성을 고려해 resizing과 segment merge를 함께 scheduling한다.
- Liu et al., Real-Time Systems 2023은 self-cueing, intermittent inspection, image resizing, batching을 결합해 object별 inspection quality와 frequency를 조절한다.
- Hu et al., RTAS 2024는 canvas-based attention scheduling에서 arbitrary object size, resizing, deadline, packing을 함께 다루며 spatiotemporal schedulability 관점을 제공한다.

### Real-Time DNN Serving

- Yao et al., RTCSA 2020은 DNN workflow를 mandatory/optional stages가 있는 imprecise computation으로 보고, deadline 안에서 confidence/accuracy utility가 높은 stage를 선택한다.
- Xu et al., RTSS 2024 FLEX는 multi-modal multi-view machine perception에서 elastic fusion과 adaptive batching을 결합한다.
- FLEX의 가변 변수는 batch 구성과 modality fusion configuration이며, trigger는 view criticality, runtime sensing context, GPU time budget, deadline/schedulability 조건이다.
- Cao et al., arXiv 2026 EdgeServing은 single shared GPU에서 model/service queue, early-exit point, batch size를 함께 선택해 per-request SLO violation과 tail latency를 줄이는 방향의 scheduler를 제안한다.
- Han et al., MobiSys 2024 Pantheon은 mobile edge GPU에서 concurrent real-time DNN task 간 chunk-level preemption과 early-exit variant adaptation을 결합한다.
- Laskaridis et al., EMDL 2021은 early-exit network의 architecture, training, exit policy, hardware co-design 요소를 정리한다.
- He et al., arXiv 2023은 edge server에서 layer-wise batching-aware DNN scheduling을 사용해 completion time 또는 on-time ratio를 개선하고, network/server congestion 시 client-side processing/offloading을 결합한다.
- Zhang et al., arXiv 2023 BCEdge는 request SLO와 model interference를 고려해 batch size와 concurrent model instance 수를 조절한다.
- Raj et al., arXiv 2025 DEMS-A/GEMS는 UAV fleet의 deadline-sensitive DNN task를 edge/cloud에 배치하며 dropping, migration, work stealing, cloud variability adaptation, windowed QoE completion rate를 다룬다.
- Ji et al., RTSS 2022 Demand Layering은 model parameter를 layer 단위로 load/execute해 embedded GPU DNN inference의 memory usage를 줄이고 memory-delay trade-off를 다룬다.
- Rahmath P et al., ACM Computing Surveys 2024는 early-exit DNN의 architecture, training, deployment, application, challenge를 포괄적으로 정리한다.
- 본 연구와의 연결: runtime에 제한된 계산 자원을 어떤 perception task와 configuration에 배분할지 정한다는 점에서 system slack 기반 mode selection 비교군으로 활용 가능하다.
- 차이점: 이 계열은 GPU serving과 perception workload 중심이며, vibration window W, diagnosis period H, model M의 공동 선택과 PREEMPT_RT 실시간성은 다루지 않는다.

### Weakly-Hard and Bounded Deadline Miss

- Chen et al., RTSS 2025 WiP는 Linux `SCHED_DEADLINE`의 Constant Bandwidth Server를 이용해 `(m,K)` weakly-hard task를 kernel modification 없이 실행하는 user-space API framework를 제안한다.
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
- 공통점: window size W가 anomaly visibility, feature separability, fault classification performance에 직접 영향을 준다는 문제의식을 공유한다.
- 차이점: 이 계열은 window/input length selection 또는 lightweight model 설계에 초점을 두며, deadline-aware inference, system slack 기반 mode selection, RTOS/PREEMPT_RT 실시간성은 다루지 않는다.

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

### Miscellaneous Real-Time Scheduling

- Pathan, DATE 2016은 EDF scheduler의 ready queue data structure를 개선해 scheduling overhead를 낮추는 방법을 제안한다.
- Tang et al., RTSS 2023은 sporadic cause-effect chain의 maximum reaction time과 data age를 줄이기 위해 dynamic priority inheritance를 제안한다.
- Guan et al., RTSS 2024는 relaxed-deadline DAG task를 mixed-criticality federated scheduling에서 다룬다.
- Requirement-Based Analysis of Self-Suspending Tasks under EDF, RTSS 2025는 EDF에서 self-suspending task의 infeasibility requirement와 interval extension analysis를 다룬다.
- 본 연구와의 연결: pipeline end-to-end latency, EDF overhead, sensing/I/O wait 해석에 보조 배경으로 사용할 수 있다.
- 차이점: 이 그룹은 본 연구의 핵심인 machine condition + system slack 기반 W/H/M runtime selection을 직접 다루지 않는다.

### Comparison Axes for Manuscript

- `Variable`: 입력 크기, window/input length, inspection frequency, batching, model.
- `Trigger`: criticality, uncertainty, anomaly deviation, bearing parameter, workload, deadline.
- `Runtime/Offline`: runtime scheduling인지 offline selection인지 구분한다.
- `RT Constraint`: deadline, latency, jitter, schedulability, RTOS/PREEMPT_RT 고려 여부를 분리한다.
- 이 축은 `surveys/comparison_table.md`와 맞춰 유지한다.
- 원고용 압축 표 초안은 `manuscript/table1_related_work.md`에 둔다. 기존 `surveys/comparison_table.md`는 내부 상세표로 유지한다.
