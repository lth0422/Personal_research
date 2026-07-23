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

### Paragraph 1: Real-Time and Embedded Fault Diagnosis

Embedded fault-diagnosis studies deploy lightweight models and signal-processing pipelines on platforms ranging from microcontrollers and RTOSs to Linux-based single-board computers. Their real-time claims must be separated into model-level best-effort latency, empirical deadline-aware execution, and schedulability-backed guarantees. MCU and SoC studies provide different implementation evidence, but platform type alone does not determine the strength of a real-time claim. In the currently verified papers, model compression and inference-time reporting are more common than explicit deadlines, tail metrics, runtime scheduling, or admission analysis.

### Paragraph 2: Adaptive Input and Diagnostic Fidelity

Input-adaptive perception and fault-diagnosis studies show that changing input size or model configuration can trade diagnostic utility for execution cost. Adaptive input length, window selection, and model design connect `W` and `M` to noise, speed variation, anomaly representation, or accuracy. These studies establish the diagnostic meaning of temporal input size. However, many select the configuration offline or from signal characteristics alone, without combining machine condition with system feasibility at runtime.

### Paragraph 3: Elastic Scheduling and Mode-Change Guarantees

Elastic scheduling adjusts task periods, rates, utilizations, or computational workloads under changing resource demand. Discrete utilization modes, compositional scheduling, harmonic task systems, weakly-hard constraints, and mode-change analysis provide foundations for treating diagnosis period `H`, execution demand `C(W,M)`, and transitions as schedulability variables. These methods largely target general real-time or control workloads. Their assumptions and guarantees must therefore be checked before applying them to vibration diagnosis utility and mode-dependent execution cost.

### Paragraph 4: Deadline-Aware AI Inference

Deadline-aware AI systems select input resolution, model, exit, stage, batch, mapping, or offloading according to slack, deadlines, queues, and resource contention. DNN-SAM connects reclaimed slack to input fidelity, and SCENIC connects controller capability, heterogeneous mapping, and timing in an offline co-design. This line establishes that `system slack -> quality mode` is not itself new. The remaining research question is how diagnosis-specific temporal fidelity, machine condition, feasible mode selection, and transition guarantees should be combined and validated across real-time execution platforms.

### Paragraph 5: Positioning

Building on these lines of work, this study investigates runtime mode selection for vibration fault diagnosis where `W`, `H`, and `M` are selected using both machine condition and system slack. The intended contribution to be validated is a system-level policy that connects diagnostic fidelity with real-time schedulability on resource-constrained edge devices, rather than a claim that condition-aware or slack-aware adaptation is itself new.

## Korean Related Work Draft

### Paragraph 1: Real-Time and Embedded Fault Diagnosis

Embedded fault diagnosis 연구는 microcontroller와 RTOS부터 Linux 기반 single-board computer까지 다양한 플랫폼에 lightweight model과 signal-processing pipeline을 배포한다. 이때 real-time 주장은 model-level best-effort latency, empirical deadline-aware execution, schedulability-backed guarantee로 구분해야 한다. MCU와 SoC 연구는 서로 다른 구현 근거를 제공하지만 플랫폼 종류만으로 real-time claim의 강도가 정해지지는 않는다. 현재 원문이 확인된 범위에서는 explicit deadline, tail metric, runtime scheduling과 admission analysis보다 model compression과 inference-time 보고가 더 일반적이다.

### Paragraph 2: Adaptive Input and Diagnostic Fidelity

Input-adaptive perception과 fault diagnosis 연구는 input size 또는 model configuration을 바꾸어 diagnostic utility와 execution cost를 조절한다. Adaptive input length, window selection과 model design은 `W/M`을 noise, speed variation, anomaly representation 또는 accuracy와 연결한다. 이 계열은 temporal input size가 진단적 의미를 가진다는 근거를 제공한다. 그러나 많은 연구가 configuration을 offline으로 고르거나 signal characteristic만 사용하며, machine condition과 runtime system feasibility를 함께 고려하지 않는다.

### Paragraph 3: Elastic Scheduling and Mode-Change Guarantees

Elastic scheduling은 resource demand 변화에 따라 task period, rate, utilization 또는 computational workload를 조절한다. Discrete utilization mode, compositional scheduling, harmonic task system, weakly-hard constraint와 mode-change analysis는 diagnosis period `H`, execution demand `C(W,M)`, transition을 schedulability 변수로 보는 기반을 제공한다. 다만 주된 대상은 general real-time 또는 control workload다. 따라서 이를 vibration diagnosis utility와 mode-dependent execution cost에 적용하기 전에 task assumption과 guarantee 조건을 확인해야 한다.

### Paragraph 4: Deadline-Aware AI Inference

Deadline-aware AI system은 slack, deadline, queue와 resource contention에 따라 input resolution, model, exit, stage, batch, mapping 또는 offloading을 선택한다. DNN-SAM은 reclaimed slack을 input fidelity와 연결하고, SCENIC은 controller capability, heterogeneous mapping과 timing을 offline에서 공동 설계한다. 따라서 `system slack -> quality mode` 자체는 새로운 주장이 될 수 없다. 남은 질문은 diagnosis-specific temporal fidelity, machine condition, feasible mode selection과 transition guarantee를 어떻게 결합하고 여러 real-time execution platform에서 검증할 것인가이다.

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
