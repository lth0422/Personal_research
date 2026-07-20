# Manuscript Draft

이 문서는 논문 초안의 중심 파일이다.
확인되지 않은 실험 결과, 정량값, venue 표현은 `TBD`로 둔다.

## Working Title

Machine- and Slack-Aware Runtime Mode Selection for Deadline-Aware Vibration Fault Diagnosis on Resource-Constrained Edge Devices

## Korean Title Candidates

1. 제한된 엣지 디바이스에서 기계 상태와 시스템 slack을 고려한 실시간 진동 결함 진단
2. 기계 상태와 시스템 slack 기반 런타임 모드 선택을 통한 실시간 진동 결함 진단
3. PREEMPT_RT 기반 엣지 환경에서 deadline-aware 진동 결함 진단을 위한 적응형 윈도우 및 모델 선택

## Abstract Draft

Vibration-based fault diagnosis on resource-constrained edge devices must balance diagnostic quality and timing predictability. Prior work has studied elastic scheduling for adapting task periods under system overload, adaptive input sizing for perception or fault diagnosis, and deadline-aware DNN serving for selecting model depth, batching, or offloading policies. However, these directions usually treat machine condition, input window size, diagnosis period, model selection, and operating-system timing behavior separately.

This paper studies a runtime mode-selection approach for deadline-aware vibration fault diagnosis on embedded and edge platforms. The target diagnosis task is represented by a mode tuple consisting of window size `W`, diagnosis period or hop size `H`, and model `M`. The key idea is to select the diagnosis mode using both machine condition and system slack: normal conditions can use lighter modes to preserve slack, while suspicious conditions can switch to more informative modes when timing constraints allow. The formulation connects diagnostic utility with real-time feasibility by considering the execution cost `C(W,M)`, deadline `D`, and elastic utilization constraint.

The implementation and evaluation are planned on `TBD` platforms, including Raspberry Pi Zero 2W with Linux and PREEMPT_RT. The evaluation will compare timing behavior under different load conditions using latency, jitter, deadline miss, and diagnostic performance metrics. The goal is not to propose a new fault diagnosis neural network, but to provide a system-level runtime policy that coordinates diagnosis fidelity and real-time schedulability for vibration fault diagnosis.

## Abstract Notes

- 정량 결과는 아직 넣지 않는다.
- KCC 2026의 STM32F407 + Zephyr 결과를 배경 또는 motivation으로 쓸 수 있지만, 이 초록에서는 새 논문의 결과처럼 쓰지 않는다.
- Pi Zero 2W, Linux, PREEMPT_RT 실험 결과가 확정되면 마지막 문단을 결과 중심으로 바꾼다.
- venue 전략과 실험 설계는 `decisions/rtas_rtcsa_dual_track_runtime_mode_selection_plan.md`를 참고하되, 공식 일정과 미검증 성과는 원고에 단정적으로 쓰지 않는다.
- 0708 면담 이후 초록의 중심 질문은 "정밀 mode로 전환해도 schedulability를 어떻게 보장하는가"로 둔다.
- 방향 1 결과는 독립 contribution으로 과장하지 않고, 방향 2의 timing characterization과 mode feasibility 근거로 사용한다.

## Korean Abstract Draft

제한된 엣지 디바이스에서 진동 기반 결함 진단을 수행하려면 진단 품질과 시간 예측 가능성을 함께 고려해야 한다. 기존 연구는 시스템 과부하 상황에서 task period를 조절하는 elastic scheduling, perception 또는 fault diagnosis를 위한 adaptive input sizing, 그리고 model depth, batching, offloading 정책을 선택하는 deadline-aware DNN serving을 각각 다루어 왔다. 그러나 이러한 연구들은 대체로 기계 상태, 입력 window size, 진단 주기, 모델 선택, 운영체제 수준의 timing behavior를 분리된 문제로 다룬다.

본 연구는 embedded 및 edge platform에서 deadline-aware 진동 결함 진단을 위한 runtime mode-selection 접근을 다룬다. 대상 진단 task는 window size `W`, diagnosis period 또는 hop size `H`, model `M`으로 구성된 mode tuple로 표현된다. 핵심 아이디어는 machine condition과 system slack을 함께 사용하여 진단 mode를 선택하는 것이다. 정상 상태에서는 가벼운 mode를 사용해 slack을 보존하고, 이상 징후가 있는 상태에서는 timing constraint가 허용하는 범위 안에서 더 많은 정보를 사용하는 mode로 전환할 수 있다. 이 정식화는 실행 비용 `C(W,M)`, deadline `D`, elastic utilization constraint를 함께 고려하여 diagnostic utility와 real-time feasibility를 연결한다.

구현과 평가는 Raspberry Pi Zero 2W, Linux, PREEMPT_RT를 포함한 `TBD` platform에서 수행할 예정이다. 평가는 서로 다른 부하 조건에서 latency, jitter, deadline miss, diagnostic performance metric을 사용해 timing behavior를 비교한다. 본 연구의 목표는 새로운 fault diagnosis neural network를 제안하는 것이 아니라, 진동 결함 진단에서 diagnosis fidelity와 real-time schedulability를 조율하는 system-level runtime policy를 제시하는 것이다.

## Related Work Draft

### Paragraph 1: Elastic Scheduling

Elastic scheduling provides a system-level mechanism for adapting real-time workloads under overload or changing resource availability. Classical elastic task models adjust task periods or utilizations to preserve schedulability, and later work extends this idea to optimization-based formulations, discrete utilization modes, harmonic task systems, compositional scheduling, and parallel DAG tasks. These studies provide the scheduling foundation for treating the diagnosis period `H` as an elastic variable. However, they are mostly formulated for general real-time workloads and do not directly address vibration fault diagnosis, input window size `W`, model selection `M`, or machine-condition-driven adaptation.

### Paragraph 2: Input-Adaptive Perception and Fault Diagnosis

Input-adaptive perception studies show that changing input size can trade accuracy or utility for execution time. In visual perception, image resizing, inspection frequency, and canvas packing have been used to satisfy deadline or workload constraints. In fault diagnosis, adaptive input length and window-size selection have been explored to improve diagnostic performance under noise, speed variation, or anomaly-related signal changes. These works support the view that the input window is a meaningful diagnostic variable rather than a simple preprocessing parameter. However, most fault diagnosis studies select window or input length offline or from signal characteristics alone, without incorporating system slack, deadline miss behavior, or PREEMPT_RT-level timing constraints.

### Paragraph 3: Deadline-Aware DNN Serving

Deadline-aware DNN serving systems adapt model execution to meet SLOs or deadlines by selecting exits, stages, batch sizes, fusion configurations, or offloading targets. DNN-SAM further connects system slack to input and model selection, while SCENIC co-designs controller capability, heterogeneous mapping, and scheduling using environment and timing parameters offline. These systems are useful comparisons because they demonstrate quality-aware configuration under resource constraints. However, the surveyed systems mainly target vision, edge GPU serving, cloud-edge inference, or intelligent control rather than vibration fault diagnosis where the temporal window `W`, diagnosis period `H`, and model `M` jointly affect diagnostic utility and real-time feasibility.

### Paragraph 4: PREEMPT_RT and Edge Platform Studies

PREEMPT_RT and single-board-computer studies show that Linux kernel configuration, scheduling latency, and workload interference can significantly affect timing predictability. Raspberry Pi and other ARM-based platforms have been evaluated with cyclictest, response-latency measurements, and lightweight inference workloads. These works motivate evaluating not only average inference latency, but also jitter, tail latency, and deadline misses under load. However, platform studies usually benchmark kernel timing or application latency separately from adaptive diagnosis policy.

### Paragraph 5: Positioning

Building on these lines of work, this study investigates runtime mode selection for vibration fault diagnosis where `W`, `H`, and `M` are selected using both machine condition and system slack. The intended contribution to be validated is a system-level policy that connects diagnostic fidelity with real-time schedulability on resource-constrained edge devices, rather than a claim that condition-aware or slack-aware adaptation is itself new.

## Korean Related Work Draft

### Paragraph 1: Elastic Scheduling

Elastic scheduling은 과부하 또는 가용 자원 변화가 있는 real-time system에서 workload를 조절하기 위한 system-level mechanism을 제공한다. 고전적인 elastic task model은 schedulability를 유지하기 위해 task period 또는 utilization을 조절하며, 이후 연구들은 이를 optimization-based formulation, discrete utilization mode, harmonic task system, compositional scheduling, parallel DAG task로 확장해 왔다. 이러한 연구들은 diagnosis period `H`를 elastic variable로 다루기 위한 scheduling 기반을 제공한다. 그러나 대부분 일반적인 real-time workload를 대상으로 정식화되어 있으며, vibration fault diagnosis, input window size `W`, model selection `M`, 또는 machine-condition-driven adaptation을 직접 다루지는 않는다.

### Paragraph 2: Input-Adaptive Perception and Fault Diagnosis

Input-adaptive perception 연구는 input size를 바꾸면 accuracy 또는 utility와 execution time 사이의 trade-off를 조절할 수 있음을 보여준다. Visual perception에서는 image resizing, inspection frequency, canvas packing 등을 사용해 deadline 또는 workload constraint를 만족시키려는 연구가 진행되었다. Fault diagnosis에서는 noise, speed variation, anomaly-related signal change 상황에서 diagnostic performance를 높이기 위해 adaptive input length와 window-size selection이 연구되었다. 이러한 연구들은 input window가 단순한 preprocessing parameter가 아니라 의미 있는 diagnostic variable이라는 관점을 뒷받침한다. 그러나 대부분의 fault diagnosis 연구는 window 또는 input length를 offline으로 선택하거나 signal characteristic만을 기준으로 선택하며, system slack, deadline miss behavior, PREEMPT_RT 수준의 timing constraint를 함께 고려하지 않는다.

### Paragraph 3: Deadline-Aware DNN Serving

Deadline-aware DNN serving system은 SLO 또는 deadline을 만족시키기 위해 exit, stage, batch size, fusion configuration, offloading target 등을 선택하여 model execution을 조절한다. DNN-SAM은 system slack을 input 및 model selection과 연결하고, SCENIC은 environment와 timing parameter를 사용하여 controller capability, heterogeneous mapping, scheduling을 offline에서 공동 설계한다. 이 계열은 resource constraint 아래의 quality-aware configuration을 보여주는 유용한 비교 대상이다. 그러나 조사한 시스템의 주요 대상은 vision, edge GPU serving, cloud-edge inference 또는 intelligent control이며, temporal window `W`, diagnosis period `H`, model `M`이 diagnostic utility와 real-time feasibility에 동시에 영향을 주는 vibration fault diagnosis 문제와는 구분된다.

### Paragraph 4: PREEMPT_RT and Edge Platform Studies

PREEMPT_RT 및 single-board-computer 관련 연구는 Linux kernel configuration, scheduling latency, workload interference가 timing predictability에 큰 영향을 줄 수 있음을 보여준다. Raspberry Pi 및 ARM-based platform은 cyclictest, response-latency measurement, lightweight inference workload 등을 통해 평가되어 왔다. 이러한 연구들은 평균 inference latency뿐 아니라 jitter, tail latency, load 상황에서의 deadline miss를 함께 평가해야 한다는 점을 뒷받침한다. 그러나 platform study는 대체로 kernel timing 또는 application latency를 adaptive diagnosis policy와 분리해서 benchmark한다.

### Paragraph 5: Positioning

이러한 연구 흐름을 바탕으로, 본 연구는 machine condition과 system slack을 함께 사용하여 `W`, `H`, `M`을 선택하는 vibration fault diagnosis runtime mode selection을 검토한다. 검증할 기여 후보는 새로운 neural network architecture나 condition-aware/slack-aware adaptation 자체가 아니라, 제한된 edge device에서 diagnostic fidelity와 real-time schedulability를 연결하는 system-level policy이다.

## Table Reference

원고용 관련연구 압축 표는 `manuscript/table1_related_work.md`를 사용한다.

## Planning Reference

- `decisions/rtas_rtcsa_dual_track_runtime_mode_selection_plan.md`: RTAS/RTCSA dual-track 전략, W/H/M coupling, mode feasibility, baseline policy, evaluation metrics를 정리한 내부 기획 문서.
- `manuscript/problem_formulation.md`: `a=(W,H,M)`, `T=H/f_s`, `U=C/T`, feasible mode set, slack definition을 정리한 문제정의 초안.
- `decisions/personal_research_summary_0708.md`: 교수님 면담 피드백. 방향 2 집중, 방향 1 재포지셔닝, schedulability guarantee, 서베이 표 4종을 정리한 기준 문서.
- `surveys/survey_plan_0708_feedback.md`: 0708 피드백을 실제 서베이 산출물과 카드화 전략으로 바꾼 실행 계획.
- `surveys/comparison_table_ko.md`: 교수님 보고용 한글 비교표 초안.
