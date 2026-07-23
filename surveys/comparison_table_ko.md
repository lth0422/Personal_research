# 한글 논문 비교표

이 문서는 교수님 보고와 서베이 방향 정리를 위한 한글 비교표이다.
상세한 논문별 내부 표는 `surveys/comparison_table.md`를 유지하고, 이 문서는 연구 방향 판단에 필요한 축만 압축한다.

Real-Time Fault Diagnosis의 체계적 판정 규칙과 O/△/X 예비 matrix는 `surveys/realtime_fault_diagnosis_survey_protocol.md`를 사용한다. 원고용 압축본은 `manuscript/realtime_fault_diagnosis_related_work_table.md`에 분리한다.

2026-07-21 LINER·Claude 검색에서 신규 fault-diagnosis 후보 14편이 추가됐지만 원문 미확인 상태다. 후보와 강한 주장에 대한 검토는 `surveys/liner_claude_survey_review_0723.md`를 사용하며, 아래 표에는 full text 판정이 끝난 논문만 추가한다.

MCU/RTOS와 SoC/Linux는 우선순위가 아니라 플랫폼 태그로 구분한다. 아래 논문은 플랫폼과 관계없이 real-time의 정의, 적응 변수, trigger와 guarantee를 기준으로 비교한다.

## 1. Real-Time Fault Diagnosis 분류표

| 논문 | 연도 | 도메인 | 플랫폼 | 실행 환경 | 실시간성 접근 | 진짜 실시간성 판단 | 본 연구와의 연결 |
| --- | ---: | --- | --- | --- | --- | --- | --- |
| Choi et al., Low-Cost MCU Shaft FD | 2025 | 회전기계 축 결함 진단 | STM32F401RET6 | Bare metal + X-CUBE-AI | sensing, inference, output 실행시간 측정 | 근실시간에 가까움. deadline, jitter, schedulability는 확인되지 않음 | KSC 2025 기반 시스템. KCC Zephyr RTOS 작업의 선행 baseline |
| Thota et al., TinyML Bearing Fault Classification | 2025 | motor bearing fault classification | ESP32 계열 MCU | MCU runtime/RTOS 확인 필요 | TinyML, quantization, model size와 latency 평가 | best-effort 근실시간. deadline miss와 RTOS scheduling은 확인되지 않음 | 경량화 계열 비교군. 본 연구와 달리 runtime scheduling은 없음 |
| Ma et al., Lightweight Architecture Search FD | 2023 | rotating machinery fault diagnosis | Desktop CPU | 일반 OS, 세부 확인 필요 | architecture search에 계산 시간 objective 포함 | best-effort 근실시간. per-task deadline이나 RTOS는 확인되지 않음 | `M` 후보를 offline으로 가볍게 설계하는 비교군 |
| Lee and Kim, FRFconv-TDSNet | 2024 | vibration machine fault diagnosis | Raspberry Pi 4B SoC/SBC | Linux 계열, RT extension 확인 필요 | edge inference time 평가 | edge inference 가능성은 보이나 deadline scheduling은 없음 | KCC 모델 배경, noise robustness, `M` 후보 |
| Jalonen et al., Real-Time Vibration-Based Bearing FD | 2024 | time-varying speed bearing FD | MacBook Pro M1 Pro | Desktop OS, 세부 확인 필요 | acquisition duration 대비 processing time 평가 | 실시간 processing 가능성 평가. RTOS/deadline miss는 없음 | `W` 또는 segment length가 real-time processing과 연결된 사례 |
| 본 연구 KCC 2026 | 2026 | shaft fault diagnosis | STM32F407 MCU | Zephyr RTOS | deadline, jitter, task pipeline 측정 | deadline 기반 실시간성에 가까움 | `W` 축소와 `C(W)` 측정의 출발점 |
| 본 연구 방향 2 | TBD | vibration FD runtime mode selection | Pi Zero 2W SoC/SBC | Linux + PREEMPT_RT 계획 | `W/H/M` mode feasibility와 schedulability 보장 | 검증해야 할 핵심 주장 | machine condition + system slack 기반 mode selection |

## 2. Elastic Scheduling 가정 비교표

| 논문/계열 | 응용 도메인 | 가변 변수 | 주된 가정 | 우리에게 적용 가능? | 가정이 깨지는 지점 |
| --- | --- | --- | --- | --- | --- |
| Buttazzo et al., Elastic Task Model / Elastic Scheduling | multimedia, adaptive control, general real-time | period/rate `T` | RTSS 1998 원형과 IEEE TC 2002 확장판. `C` 고정, `T` 가변이며 2002년판은 SRP/resource constraint를 보강 | `H/T`를 elastic variable로 보는 데 직접 유용 | 본 연구는 `C=C(W,M)`도 mode에 따라 바뀜. 두 논문은 별도 독립 기법으로 중복 집계하지 않음 |
| Chantem et al., Generalized Elastic Scheduling | control-oriented periodic tasks | period, utilization, deadline | task model과 performance metric 사이 최적화 | utility와 schedulability를 함께 보는 틀로 유용 | fault diagnosis utility, window `W`, model `M`은 없음 |
| Tian and Gui, QoC Elastic Scheduling | process control | control period, task utilization | QoC feedback과 workload constraint | diagnosis utility 개념과 비교 가능 | QoC는 control 성능이며 anomaly score와 다름 |
| Orr et al., Discrete Utilizations | parallel real-time / RTHS | discrete utilization, workload, period | 후보 utilization mode 집합 | `(W,H,M)`을 discrete mode set으로 보는 근거 | mode가 vibration signal semantics를 갖지는 않음 |
| Sudvarg et al., Harmonic/Subtask Elastic 계열 | FIMS, SLAM, multicore DAG | period, subtask workload, core allocation | schedulability bound와 resource allocation 중심 | 최신 elastic scheduling 비교군 | machine condition과 diagnostic utility는 없음 |
| Xu et al., Safety-Aware Period Boosting/Compressing | safety-critical feedback control | sampling period, common scheduling slot, controller gain 선택 | WCET와 plant safety margin 기반 offline schedule synthesis | `H/T` 변경과 weakly-hard deadline miss를 application safety로 제한하는 직접 비교군 | `C_i` 고정, offline 방식이며 vibration `W/M`, anomaly trigger, runtime slack, PREEMPT_RT는 없음 |
| Li et al., ATER | ROS 2 autonomous-system task chain | sensor sampling rate, timer period, downstream activation rate | message drop, publish/subscribe rate, execution-time distribution | runtime `H/T` 조절과 pipeline 처리율 정렬의 직접 비교군 | empirical feedback이며 deadline/schedulability 보장과 application utility가 없음. Vibration `W/M`, anomaly trigger, explicit slack, PREEMPT_RT도 없음 |
| Gifford et al., Decntr | multi-mode CPS control | controller, safe sampling period, task/core/cache/BW allocation, transition deadline | mode-change request와 offline safety/resource model | Feasible mode set 합성과 mode 전환 적용의 가장 가까운 구조적 비교군 | Control invariant safety와 known mode graph 중심. Vibration `W`, diagnosis utility/anomaly score, inference `M`, PREEMPT_RT 실측은 없음 |
| 본 연구 | vibration FD | `W`, `H`, `M` | `C(W,M)`과 `T=H/fs`가 함께 변함 | 기존 elastic scheduling의 확장 대상 | schedulability guarantee를 새로 정리해야 함 |

## 3. Deadline-Miss 대응 비교표

| 논문 | 도메인 | 대응 변수 | 트리거 | 실시간 평가 | 본 연구와의 연결 | 한계 |
| --- | --- | --- | --- | --- | --- | --- |
| Braun and Altmeyer, Handling System Overloads | embedded feedback control | Kill, Skip-Next, Queue, actuation timing | temporary overload에 따른 deadline miss | STM32+ThreadX, 2 ms implicit deadline, utilization, jitter, data age | 예상하지 못한 overload 이후 inference fallback 설계 비교군 | 한 control system의 empirical 결과이며 proactive `W/H/M` admission과 PREEMPT_RT는 없음 |

## 4. Deadline-Aware DNN / Model Selection 비교표

| 논문 | 도메인 | 가변 변수 | 트리거 | 실시간 제약 | 본 연구와의 연결 | 한계 |
| --- | --- | --- | --- | --- | --- | --- |
| Yao et al., Imprecise DL Services | edge DNN service | mandatory/optional stage, depth | deadline, confidence/utility | deadline miss rate | `M` 또는 computation quality 조절 비교군 | vision/object classification 중심 |
| Li et al., AMS Heart Disease | ECG anomaly detection | model complexity, anytime exit | heart rate, `D(HR)` | HR-dependent inference threshold, EDF 식, deadline miss | condition 기반 `M` 선택의 강한 비교군 | condition-only 정책이며 system slack, vibration `W/H`, PREEMPT_RT가 없음. 평균 latency 중심이고 threshold 도출 및 fallback 보장은 불명확 |
| Soyyigit et al., MURAL | LiDAR 3D object detection | input resolution/pillar size | deadline, input별 predicted execution time | deadline-aware resolution scheduling, deadline miss | deadline 안에서 최고 input fidelity를 선택하는 `W` 축 직접 비교군 | LiDAR spatial resolution이며 vibration `W/H/M`, machine condition, multi-task slack은 없음. 측정 기반 WCET 표현 주의 |
| Kang et al., DNN-SAM | autonomous-driving object detection | optional full-image scale, mandatory critical-RoI crop | actual mandatory cost 이후 deadline slack, RoI time-to-collision | non-preemptive EDF sufficient condition, implicit deadline | `system slack -> input fidelity`의 강한 직접 비교군 | Spatial vision/GPU 중심이며 vibration temporal `W`, `H/M`, anomaly trigger, PREEMPT_RT는 없음. 측정 최대를 WCET로 사용 |
| Chen et al., SCENIC | intelligent quadcopter control | DNN depth/width, layer CPU/GPU mapping, fixed priority | runtime trigger 없음. Environment/plant condition과 resource profile 기반 offline optimization | fixed-priority WCRT, deadline, CPU/GPU utilization | condition, model capability와 response time을 application utility로 연결하는 직접 비교군 | Online adaptation과 vibration `W/H`, diagnosis utility, PREEMPT_RT는 없음. Profile safety margin에 조건부 |
| EdgeServing | edge multi-DNN serving | model, exit, batch | SLO, queue, latency budget | SLO violation, p95 latency | deadline-aware model/exit/batch 선택 비교군 | GPU serving 중심 |
| Pantheon | mobile edge GPU | chunk preemption, early-exit variant | task deadline, priority | deadline miss rate | deadline 기반 DNN variant 조절 비교군 | GPU preemption이며 RTOS/PREEMPT_RT와 다름 |
| FLEX | autonomous driving perception | batch, fusion configuration | criticality, GPU time budget | EDF/CEDF schedulability | slack/deadline 기반 configuration 선택 비교군 | vibration FD가 아님 |
| 본 연구 | vibration FD | `W/H/M` | machine condition + system slack | utilization, p99/max response time, deadline miss | 세 축을 동시에 묶는 목표 | 아직 검증 필요 |

## 5. PREEMPT_RT와 부하 설계 참고표

| 논문 | 플랫폼 | 부하 또는 측정 방법 | 측정 지표 | 우리 실험에 주는 근거 | 주의 |
| --- | --- | --- | --- | --- | --- |
| Adam et al., PREEMPT_RT on ARM | Raspberry Pi 3, BeagleBone AI | cyclictest, response/periodic task measurement | user/kernel latency, worst-case latency | cyclictest만이 아니라 response task 관점도 볼 수 있음 | Pi Zero 2W 직접 결과는 아님 |
| Dewit et al., Raspberry Pi 5 RT Linux | Raspberry Pi 5 | stress-ng, iperf3, cyclictest | scheduling latency max/tail | 부하 조건을 문헌 기반으로 정해야 한다는 근거 | Pi 5 결과를 Pi Zero 2W로 일반화 금지 |
| Vaghasiya thesis | Raspberry Pi COTS | object detection workload, Xenomai/PREEMPT_RT 비교 | latency, jitter, responsiveness | inference workload와 OS timing을 함께 보는 참고 | thesis status와 세부 조건 확인 필요 |
| De Marco et al., Dolphin Whistle Pi Zero 2W | Raspberry Pi Zero 2W | TFLite thread 수 변화, 장시간 stress | latency, throughput, CPU load, temperature, memory | Pi Zero 2W에서 TFLite 측정 항목 선정 참고 | acoustic detection이며 PREEMPT_RT 비교는 아님 |
| 본 연구 방향 1 | Pi Zero 2W | idle/CPU/mem/IO/combined 후보 | cyclictest, pipeline latency, p99/max, deadline miss | 방향 2의 실험 환경과 원인 분석 기반 | 부하 조건은 추가 문헌 확인 뒤 확정 |

## 6. 카드화 보강 체크리스트

각 paper card에는 기존 항목에 더해 다음을 확인한다.

| 항목 | 질문 |
| --- | --- |
| 실시간성 수준 | RTOS, deadline, jitter, p99/max, deadline miss를 다루는가? |
| 실행시간 가정 | `C`가 고정인가, profiling 기반인가, input/model에 따라 동적으로 변하는가? |
| 주기 가정 | period 또는 hop size `H/T`를 조절하는가? |
| 입력 변수 | window/input size가 diagnostic utility와 연결되는가? |
| 모델 변수 | model, exit, depth, quantization, pruning 중 무엇을 조절하는가? |
| 트리거 | system load/slack인가, machine condition인가, confidence인가, offline profile인가? |
| 보장 방식 | utilization bound, schedulability test, admission control, fallback, empirical p99/max 중 무엇인가? |
| 본 연구 연결 | `W`, `H`, `M`, `q`, `S`, PREEMPT_RT 중 어디에 연결되는가? |
