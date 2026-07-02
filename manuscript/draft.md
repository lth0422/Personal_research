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

## Related Work Draft

### Paragraph 1: Elastic Scheduling

Elastic scheduling provides a system-level mechanism for adapting real-time workloads under overload or changing resource availability. Classical elastic task models adjust task periods or utilizations to preserve schedulability, and later work extends this idea to optimization-based formulations, discrete utilization modes, harmonic task systems, compositional scheduling, and parallel DAG tasks. These studies provide the scheduling foundation for treating the diagnosis period `H` as an elastic variable. However, they are mostly formulated for general real-time workloads and do not directly address vibration fault diagnosis, input window size `W`, model selection `M`, or machine-condition-driven adaptation.

### Paragraph 2: Input-Adaptive Perception and Fault Diagnosis

Input-adaptive perception studies show that changing input size can trade accuracy or utility for execution time. In visual perception, image resizing, inspection frequency, and canvas packing have been used to satisfy deadline or workload constraints. In fault diagnosis, adaptive input length and window-size selection have been explored to improve diagnostic performance under noise, speed variation, or anomaly-related signal changes. These works support the view that the input window is a meaningful diagnostic variable rather than a simple preprocessing parameter. However, most fault diagnosis studies select window or input length offline or from signal characteristics alone, without incorporating system slack, deadline miss behavior, or PREEMPT_RT-level timing constraints.

### Paragraph 3: Deadline-Aware DNN Serving

Deadline-aware DNN serving systems adapt model execution to meet SLOs or deadlines by selecting exits, stages, batch sizes, fusion configurations, or offloading targets. These systems are useful comparisons because they demonstrate runtime selection of inference quality under resource constraints. However, they mainly target vision, edge GPU serving, or cloud-edge inference workloads. They do not directly handle vibration fault diagnosis where the input window `W`, diagnosis period `H`, and model `M` jointly affect both diagnostic utility and real-time feasibility.

### Paragraph 4: PREEMPT_RT and Edge Platform Studies

PREEMPT_RT and single-board-computer studies show that Linux kernel configuration, scheduling latency, and workload interference can significantly affect timing predictability. Raspberry Pi and other ARM-based platforms have been evaluated with cyclictest, response-latency measurements, and lightweight inference workloads. These works motivate evaluating not only average inference latency, but also jitter, tail latency, and deadline misses under load. However, platform studies usually benchmark kernel timing or application latency separately from adaptive diagnosis policy.

### Paragraph 5: Positioning

In contrast to these lines of work, this study focuses on runtime mode selection for vibration fault diagnosis where `W`, `H`, and `M` are selected using both machine condition and system slack. The intended contribution is a system-level policy that connects diagnostic fidelity with real-time schedulability on resource-constrained edge devices, rather than a new neural network architecture alone.

## Table Reference

원고용 관련연구 압축 표는 `manuscript/table1_related_work.md`를 사용한다.

## Planning Reference

- `decisions/rtas_rtcsa_dual_track_runtime_mode_selection_plan.md`: RTAS/RTCSA dual-track 전략, W/H/M coupling, mode feasibility, baseline policy, evaluation metrics를 정리한 내부 기획 문서.
- `manuscript/problem_formulation.md`: `a=(W,H,M)`, `T=H/f_s`, `U=C/T`, feasible mode set, slack definition을 정리한 문제정의 초안.
