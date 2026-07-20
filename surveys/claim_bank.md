# Claim Bank

연구 주장 후보를 정리하는 파일이다.

## Claims

- 0708 면담 이후 본 연구의 핵심 claim은 "정밀 mode를 선택한다"가 아니라 "feasible mode set 안에서 가장 진단적으로 유용한 mode를 선택한다"로 정리한다.
  - 근거 후보: `decisions/personal_research_summary_0708.md`, `manuscript/problem_formulation.md`.
  - 본 연구 연결: schedulability guarantee를 문제 정식화의 1번 질문으로 둔다.
  - 주의: 아직 formal guarantee와 empirical feasibility 중 어디까지 주장할지는 확정되지 않았다.

- 기존 elastic scheduling은 대체로 execution time `C`를 고정하고 period 또는 utilization을 조절한다. 본 연구의 확장 지점은 diagnosis mode에 따라 `C(W,M)`도 함께 바뀐다는 점이다.
  - 근거 후보: Buttazzo et al. 1998/2002; Chantem et al. 2009; Orr et al. 2020; Sudvarg 계열.
  - 본 연구 연결: `τ_diag = (C(W,M), T=H/f_s)`로 확장해 `W/H/M` mode bank를 admission 또는 feasibility filtering 대상으로 본다.
  - 주의: "기존 연구가 전혀 없다"가 아니라, 현재 보유 문헌 범위에서 `C(W,M)`와 vibration diagnosis utility를 함께 다룬 사례가 확인되지 않았다는 식으로 써야 한다.

- classic elastic scheduling은 periodic task의 period/rate를 조절해 overload나 workload 변화에서 schedulability를 유지하는 시스템 축의 대표 관련연구다.
  - 근거 후보: Buttazzo et al. RTSS 1998, Buttazzo et al. IEEE Transactions on Computers 2002, Chantem et al. IEEE Transactions on Computers 2009, Tian and Gui Real-Time Systems 2011.
  - 본 연구 연결: 본 연구의 `H` 또는 diagnosis period를 elastic variable로 정식화할 때 기본 비교군으로 활용 가능하다.
  - 주의: 이 계열은 general real-time scheduling 중심이며, vibration fault diagnosis의 window W, model M, machine condition trigger, PREEMPT_RT/SBC 실험을 직접 다루지는 않는다.

- 최신 elastic scheduling 계열은 task 단위 period 조절을 넘어 discrete utilization, harmonic period assignment, parallel DAG subtask workload와 core allocation까지 확장된다.
  - 근거 후보: Orr et al. RTNS 2020; Salman et al. ETFA 2021; Sudvarg PhD dissertation 2024; Sudvarg et al. RTAS 2024; Sudvarg et al. RTSS 2024; Sudvarg et al. LITES 2025.
  - 본 연구 연결: system slack과 schedulability 제약을 보고 workload 또는 period를 조절하는 최신 비교군으로 사용할 수 있다. 특히 discrete candidate mode는 본 연구의 `(W,H,M)` mode set 정식화와 연결 가능하다.
  - 주의: 이 계열의 trigger는 overload, available utilization, schedulability/resource constraint 중심이며, machine condition과 fault-diagnosis utility를 함께 쓰는 구조는 현재 카드 기준 확인되지 않았다.

- real-time DNN serving 계열에서도 runtime에 batch 구성과 model 내부 처리량을 조절해 deadline과 perception quality의 trade-off를 다루는 연구가 있다.
  - 근거 후보: Yao et al. RTCSA 2020, Imprecise DL Services; Xu et al. RTSS 2024, FLEX; Li et al. RTCSA 2025, AMS Heart Disease; Cao et al. arXiv 2026, EdgeServing; Han et al. MobiSys 2024, Pantheon; Laskaridis et al. EMDL 2021; He et al. arXiv 2023; Zhang et al. arXiv 2023 BCEdge; Raj et al. arXiv 2025; Rahmath P et al. ACM Computing Surveys 2024.
  - 본 연구 연결: system slack/deadline 조건으로 runtime mode를 선택한다는 점은 본 연구의 `S -> (W,H,M)` 정책과 비교 가능하다.
  - 주의: Yao et al.은 DNN stage/depth를 imprecise computation으로 조절하고, FLEX는 batch/fusion configuration, Li et al.은 heart rate 기반 model complexity/anytime exit path를 선택하며, EdgeServing은 model/exit/batch, Pantheon은 GPU runtime preemption과 early-exit variant adaptation, He et al.은 layer-wise batching/offloading, BCEdge는 batch/concurrency, Raj et al.은 edge/cloud placement와 dropping/migration, early-exit survey들은 exit/depth policy를 다룬다. 이 계열은 vibration fault diagnosis의 window W, diagnosis period H, anomaly score trigger, PREEMPT_RT 커널 실시간성은 다루지 않는다.

- condition-aware mode selection만으로는 실시간 실행 가능성을 보장할 수 없으며, 같은 기계 상태에서도 가용 system slack에 따라 feasible mode가 달라질 수 있다.
  - 근거 후보: Li et al. RTCSA 2025 AMS Heart Disease의 HR 기반 model selection과 EDF 정식화에 대한 비판적 검토.
  - 본 연구 연결: `A_feasible(S_k)`를 먼저 계산하고, 그 안에서 machine condition에 대한 diagnostic utility가 가장 높은 `(W,H,M)`을 선택하는 feasibility-first 정책으로 확장한다.
  - 주의: Li et al.이 system slack을 고려하지 않는다는 사실만으로 본 연구의 novelty가 확정되지는 않는다. 다른 condition-aware 및 slack-aware mode-selection 문헌을 추가 확인해야 한다.

- embedded DNN inference에서는 memory footprint도 latency/deadline과 함께 고려해야 할 resource constraint가 될 수 있다.
  - 근거 후보: Ji et al., RTSS 2022 Demand Layering.
  - 본 연구 연결: Pi Zero 2W 또는 SBC 환경에서 model size, memory, loading 방식이 실시간 inference에 영향을 줄 수 있음을 설명하는 배경으로 활용 가능하다.
  - 주의: Demand Layering은 Jetson AGX Xavier + integrated GPU + NVMe SSD 구조에 최적화된 방법이므로 MCU 또는 Pi Zero 2W CPU inference에 직접 적용한다고 쓰면 안 된다.

- weakly-hard real-time 문헌은 deadline miss를 무조건 실패가 아니라 `(m,K)` bounded miss constraint로 다루는 비교축을 제공한다.
  - 근거 후보: Chen et al., RTSS 2025 WiP.
  - 본 연구 연결: KSC 2026의 deadline miss rate와 학위논문의 utility/deadline trade-off를 설명할 때 hard deadline, soft deadline, weakly-hard deadline을 구분하는 배경으로 활용 가능하다.
  - 주의: 해당 논문은 Linux `SCHED_DEADLINE`과 CBS parameter mapping 중심이며, vibration FD utility, W/H/M runtime selection, PREEMPT_RT 비교는 다루지 않는다.

- IDK cascade 계열은 classification을 빠른 classifier부터 시도하고 confidence가 부족하면 더 강한 classifier로 넘어가는 방식으로 latency/accuracy trade-off를 다룬다.
  - 근거 후보: Agrawal et al., RTSS 2024; Baruah et al., RTAS 2024.
  - 본 연구 연결: 본 연구의 `M` 또는 fallback model 선택을 설명할 때 cascade/early-exit 계열의 비교군으로 활용 가능하다.
  - 주의: IDK의 trigger는 confidence/history/dependence 또는 offline synthesis 조건이며, vibration anomaly score와 system slack을 함께 쓰는 W/H/M runtime policy는 확인되지 않았다.

- period assignment와 probabilistic deadline failure 문헌은 `H` 또는 deadline miss를 시스템 스케줄링 변수로 다룰 때 참고할 수 있다.
  - 근거 후보: Hawila et al., ECRTS 2025; Guan et al., RTSS 2025.
  - 본 연구 연결: diagnosis period/hop size `H`와 deadline miss rate를 단순 구현 지표가 아니라 utility/risk와 연결하는 배경으로 활용 가능하다.
  - 주의: Hawila et al.은 control stability, Guan et al.은 probabilistic EDF analysis 중심이다. vibration FD utility, machine condition, PREEMPT_RT 실측은 직접 다루지 않는다.

- 입력 크기 조절은 vision perception 분야에서 latency/accuracy/deadline trade-off를 만드는 scheduling variable로 사용되어 왔다.
  - 근거 후보: Hu et al. RTCSA 2021, Hu et al. Real-Time Systems 2022, Liu et al. Real-Time Systems 2023, Hu et al. RTAS 2024.
  - 본 연구 연결: vibration fault diagnosis에서는 image size가 아니라 window size W가 입력 크기 역할을 하며, window는 latency뿐 아니라 결함 정보 보존과도 연결된다.
  - 주의: 위 논문들은 vision domain과 embedded GPU 중심이므로, 본 연구의 MCU/SBC, PREEMPT_RT, vibration FD novelty를 직접 증명하는 근거로 쓰면 안 된다.

- 기존 image resizing 계열은 criticality, object uncertainty, deadline, workload를 trigger로 사용하지만 machine condition과 system slack을 함께 쓰는 구조는 확인되지 않았다.
  - 근거 후보: 네 편 모두 object criticality 또는 deadline/workload 중심.
  - 본 연구 연결: anomaly score 기반 machine condition과 slack 기반 system condition을 함께 쓰는 정책의 차별점 후보.
  - 주의: fault diagnosis 쪽 adaptive window 논문을 추가로 확인한 뒤 claim 강도를 조정해야 한다.

- fault diagnosis에서도 window size W는 단순 전처리 파라미터가 아니라 anomaly representation과 diagnostic sensitivity를 좌우하는 design variable로 다뤄질 수 있다.
  - 근거 후보: Kim et al., Mathematics 2026, ADW.
  - 본 연구 연결: 본 연구의 W 선택을 fault diagnosis 성능 축과 연결하는 근거로 활용 가능하다.
  - 주의: ADW는 deviation score 기반 offline window selection에 가깝고, system slack, deadline, RTOS/PREEMPT_RT를 포함한 runtime scheduling은 다루지 않는다.

- bearing fault diagnosis 문헌에서도 fixed input length 대신 bearing parameter와 sampling frequency를 반영한 adaptive input length selection이 제안되어 있다.
  - 근거 후보: Tang et al., Applied Soft Computing 2023, AANTLN; Tang et al., Engineering Applications of Artificial Intelligence 2023, AILWTLN.
  - 본 연구 연결: window size W를 물리적 결함 정보와 연결해 정해야 한다는 문제의식을 강화하는 비교군으로 활용 가능하다.
  - 주의: 두 논문 모두 system slack, deadline, RTOS/PREEMPT_RT 기반 runtime scheduling을 다루지는 않는다.

- vibration-based bearing fault diagnosis에서도 segment/window length는 speed variation과 real-time processing 가능성에 직접 연결되는 설계 변수로 다뤄진다.
  - 근거 후보: Jalonen et al., ICIT 2024.
  - 본 연구 연결: `W`를 단순 모델 입력 크기가 아니라 motor speed variation, acquisition duration, inference time을 함께 고려하는 변수로 설명할 수 있다.
  - 주의: 해당 논문은 runtime adaptation이 아니라 offline segment length design과 real-time inference evaluation에 가깝다. system slack, H/M selection, PREEMPT_RT는 다루지 않는다.

- TinyML 및 lightweight fault diagnosis 문헌은 resource-constrained edge device에서 vibration inference를 수행할 수 있음을 보여주지만, 대부분 offline model/input design 또는 architecture search에 머문다.
  - 근거 후보: Thota et al., GLSVLSI 2025; Ma et al., Engineering Applications of Artificial Intelligence 2023; Lee and Kim, IEEE TIM 2024.
  - 본 연구 연결: 본 연구의 `M` 축과 edge deployment 배경을 설명하는 근거로 활용 가능하다.
  - 주의: 이 계열은 real-time이라는 표현을 쓰더라도 deadline miss, jitter, PREEMPT_RT, system slack 기반 runtime selection을 다루는지 별도로 구분해야 한다.

- FRFconv-TDSNet은 본 연구의 fault diagnosis model 배경으로 직접 연결되지만, KCC/KSC 실험 수치는 별도 platform에서 다시 측정한 결과로 분리해야 한다.
  - 근거 후보: Lee and Kim, IEEE TIM 2024; KCC 2026 STM32F407 + Zephyr 실험 로그.
  - 본 연구 연결: model M 후보와 noise robustness 배경 설명에 활용 가능하다.
  - 주의: 논문은 Raspberry Pi 4B + PyTorch Mobile + XNNPACK 평가이고, 본 연구의 STM32F407 + Zephyr + TFLite Micro 또는 Pi Zero 2W + PREEMPT_RT 결과와 직접 같은 수치로 비교하면 안 된다.

- STM32F401 기반 KSC 2025 시스템은 MCU에서 sensing, inference, output을 통합한 선행 baseline이며, RTOS task화와 실시간 스케줄링으로 확장할 필요성을 직접 남긴다.
  - 근거 후보: Choi et al., 한국소프트웨어종합학술대회 2025.
  - 본 연구 연결: KCC 2026 Zephyr RTOS 작업과 KSC 2026 Pi Zero 2W/PREEMPT_RT 작업의 선행 시스템 배경으로 활용 가능하다.
  - 주의: 해당 논문은 bare-metal 또는 MCU application integration 중심으로 보이며, deadline miss, jitter, schedulability analysis는 현재 카드 기준 확인되지 않았다.

- PREEMPT_RT 관련 platform 문헌은 average latency보다 worst-case latency와 latency distribution을 비교해야 한다는 실험 설계 근거를 제공한다.
  - 근거 후보: Adam et al., Electronics 2021; Dewit et al., 2024 Raspberry Pi 5 preliminary assessment.
  - 본 연구 연결: KSC 2026에서 vanilla Linux와 PREEMPT_RT를 cyclictest, stress-ng 부하, p99/max latency로 먼저 검증해야 한다는 근거.
  - 주의: 기존 문헌은 주로 kernel scheduling latency benchmark이며, 본 연구의 TFLite fault diagnosis pipeline latency와 deadline miss는 별도로 측정해야 한다.

- Pi Zero 2W에서도 TFLite 기반 실시간 inference를 수행한 사례가 있으나, 도메인과 deadline 정의는 본 연구와 다르다.
  - 근거 후보: De Marco et al., Robotics 2025; Jeya Agastin K et al., IRJAEM 2025.
  - 본 연구 연결: Pi Zero 2W + TFLite_runtime, thread count, latency, throughput, CPU load, temperature 측정 항목을 참고할 수 있다.
  - 주의: dolphin whistle acoustic detection 또는 object detection이며 PREEMPT_RT 비교와 vibration FD pipeline은 다루지 않는다. IRJAEM 2025 논문은 venue quality와 정량 결과를 특히 재확인해야 한다.

- miscellaneous real-time scheduling 문헌은 deadline, EDF overhead, cause-effect latency, self-suspension 같은 timing background를 제공하지만, 본 연구 novelty의 직접 근거는 아니다.
  - 근거 후보: Pathan DATE 2016; Tang et al. RTSS 2023; Guan et al. RTSS 2024; Requirement-Based Analysis of Self-Suspending Tasks under EDF RTSS 2025.
  - 본 연구 연결: Rx -> Inference -> Tx end-to-end latency, EDF/SCHED_DEADLINE overhead, sensing/I/O wait 해석을 보조하는 배경으로 제한적으로 활용 가능하다.
  - 주의: 이 계열은 vibration FD의 W/H/M runtime selection, anomaly score trigger, PREEMPT_RT 실측을 직접 다루지 않는다.

- 현재까지 카드화한 문헌 전체에서는 `machine condition + system slack`을 함께 사용해 `W + H + M`을 runtime에 선택하는 구조가 확인되지 않았다.
  - 근거 후보: `surveys/comparison_table.md`의 `Trigger`, `Runtime/Offline`, `RT Constraint`, `Gap` 컬럼.
  - 본 연구 연결: novelty 주장의 중심 후보. Elastic scheduling은 H/period와 schedulability를, input-adaptive fault diagnosis는 W와 machine signal을, RT-DNN serving은 deadline/SLO 기반 model/exit/batch selection을, PREEMPT_RT/platform 문헌은 kernel/pipeline timing을 각각 다루지만 네 축을 동시에 묶지는 않는다.
  - 주의: 이 claim은 현재 보유 PDF와 카드화 범위 기준이다. 원고에서는 “확인한 문헌 범위에서는”처럼 범위를 명시해야 한다.

- 본 연구의 관련연구 구조는 네 축으로 나누어 쓰는 것이 가장 자연스럽다.
  - 근거 후보: `elastic_scheduling`, `input_adaptive`, `rt_dnn_serving`, `platform_preempt_rt/platform_pi_zero2w` 카드 전체.
  - 본 연구 연결: Related Work를 `period/workload elasticity`, `input/window adaptation`, `deadline-aware DNN serving`, `embedded Linux/PREEMPT_RT platform` 순서로 구성할 수 있다.
  - 주의: `misc_realtime_scheduling`은 핵심 축이 아니라 EDF overhead, end-to-end latency, self-suspension 같은 보조 배경으로 두는 것이 적절하다.

- 원고용 비교표는 개별 논문 나열보다 계열별 variable/trigger/platform/gap을 보여주는 방식이 적절하다.
  - 근거 후보: `manuscript/table1_related_work.md`.
  - 본 연구 연결: Table 1에서 `W/H/M`, `machine condition + system slack`, `RTOS/PREEMPT_RT` 조합을 한눈에 보이게 할 수 있다.
  - 주의: 대표 논문 목록은 전체 bibliography가 아니므로 본문 related work에서 필요한 논문을 별도로 인용해야 한다.
