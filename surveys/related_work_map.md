# Related Work Map

관련연구 분류와 원고 연결 지점을 정리하는 파일이다.

## Map

### Elastic Scheduling

- Buttazzo et al., RTSS 1998은 periodic task의 period/rate를 elastic variable로 두고, overload 또는 task rate 변경 시 다른 task period를 조절해 schedulability를 유지하는 모델을 제안한다.
- Buttazzo et al., IEEE Transactions on Computers 2002는 elastic scheduling을 flexible workload management framework로 정리하고, current workload에 따른 rate adaptation과 overload management를 다룬다.
- Sudvarg et al., RTSS 2024는 multicore federated scheduling에서 parallel DAG task의 subtask workload와 core allocation을 elastic하게 조절한다.
- 공통점: system load, utilization, schedulability bound를 중심으로 rate/workload를 조절한다.
- 차이점: 이 계열은 general real-time scheduling 중심이며, vibration fault diagnosis의 window size W, model M, anomaly score 기반 machine condition, PREEMPT_RT/SBC 실시간성은 다루지 않는다.

### Input-Adaptive Visual Perception

- Hu et al., RTCSA 2021은 criticality 기반 machine perception에서 image resizing을 accuracy/response-time trade-off 변수로 사용한다.
- Hu et al., Real-Time Systems 2022는 LiDAR 기반 segmentation의 불완전성을 고려해 resizing과 segment merge를 함께 scheduling한다.
- Liu et al., Real-Time Systems 2023은 self-cueing, intermittent inspection, image resizing, batching을 결합해 object별 inspection quality와 frequency를 조절한다.
- Hu et al., RTAS 2024는 canvas-based attention scheduling에서 arbitrary object size, resizing, deadline, packing을 함께 다루며 spatiotemporal schedulability 관점을 제공한다.

### 본 연구와의 연결

- 관련연구에서 비교 대상으로 활용 가능하다.
- 공통점: 입력 크기 조절이 inference latency와 perception quality 사이의 trade-off를 만든다.
- 차이점: 이 계열은 vision object/segment/focus locale 중심이며, 본 연구의 vibration window size W, hop size H, model M, machine condition, system slack 조합과는 문제 구조가 다르다.

### Input-Adaptive Fault Diagnosis

- Kim et al., Mathematics 2026은 anomaly deviation score를 이용해 fault diagnosis용 time-series window size를 선택한다.
- Tang et al., Applied Soft Computing 2023은 noisy bearing transfer learning에서 bearing parameter와 sampling frequency에 기반한 adaptive input length를 사용한다.
- Tang et al., Engineering Applications of Artificial Intelligence 2023은 adaptive input length와 lightweight transfer network를 결합한다.
- 공통점: window size W가 anomaly visibility, feature separability, fault classification performance에 직접 영향을 준다는 문제의식을 공유한다.
- 차이점: 이 계열은 window/input length selection 또는 lightweight model 설계에 초점을 두며, deadline-aware inference, system slack 기반 mode selection, RTOS/PREEMPT_RT 실시간성은 다루지 않는다.

### Comparison Axes for Manuscript

- `Variable`: 입력 크기, window/input length, inspection frequency, batching, model.
- `Trigger`: criticality, uncertainty, anomaly deviation, bearing parameter, workload, deadline.
- `Runtime/Offline`: runtime scheduling인지 offline selection인지 구분한다.
- `RT Constraint`: deadline, latency, jitter, schedulability, RTOS/PREEMPT_RT 고려 여부를 분리한다.
- 이 축은 `surveys/comparison_table.md`와 맞춰 유지한다.
