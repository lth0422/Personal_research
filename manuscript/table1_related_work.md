# Table 1 Draft: Related Work Comparison

이 파일은 `surveys/comparison_table.md`의 내부 상세 비교표를 원고용으로 압축한 초안이다.
개별 논문 50편을 모두 나열하지 않고, 관련연구 계열별 핵심 차이만 보여준다.

원고에 넣을 때는 venue/year 표기를 manuscript 스타일에 맞춰 줄이고, 정량 수치는 본문에서 검증된 경우에만 사용한다.

| Category | Representative works | Main variable | Adaptation trigger | RT/platform consideration | Limitation vs. this work |
| --- | --- | --- | --- | --- | --- |
| Elastic scheduling | Buttazzo et al.; Chantem et al.; Orr et al.; Sudvarg et al. | Period/rate, utilization, workload, subtask workload, core allocation | Overload, available utilization, schedulability/resource constraint | EDF/RM schedulability, federated scheduling, harmonic periods, some FIMS/SLAM case studies | General real-time scheduling 중심. Vibration FD의 window `W`, model `M`, machine condition, PREEMPT_RT pipeline을 함께 다루지 않음 |
| Input-adaptive visual perception | Hu et al.; Liu et al. | Image/segment size, inspection frequency, canvas packing, batching | Object criticality, spatial uncertainty, workload, deadline | Embedded GPU, autonomous driving/surveillance, deadline-aware perception | Vision object/segment 중심. Vibration window `W`와 machine condition 기반 diagnosis utility는 다루지 않음 |
| Input-adaptive fault diagnosis | Kim et al.; Tang et al.; Jalonen et al. | Window size, input length, segment length | Bearing parameters, sampling frequency, anomaly deviation, speed variation | Fault diagnosis accuracy and processing-time evaluation, mostly offline/data-driven selection | `W`를 다루지만 system slack, deadline-aware runtime scheduling, `H/M` 공동 선택, RTOS/PREEMPT_RT는 확인되지 않음 |
| Deadline-aware DNN serving | Yao et al.; Xu et al.; Li et al.; Cao et al.; Han et al.; He et al.; Zhang et al.; Raj et al. | DNN stage/depth, exit point, batch, fusion, offloading, edge/cloud placement, model complexity | Confidence, SLO/deadline, queue/load, GPU budget, network/cloud variability, heart rate | Edge GPU/server, embedded health monitoring, SLO, on-time ratio, deadline miss, throughput-latency trade-off | DNN serving/perception/ECG 중심. Vibration FD의 `W/H/M`, anomaly score trigger, PREEMPT_RT kernel timing은 다루지 않음 |
| Weakly-hard, cascade, and deadline-risk scheduling | Chen et al.; Agrawal et al.; Baruah et al.; Hawila et al.; Guan et al. | CBS parameters, cascade ordering, period, active dropping | Weakly-hard constraint, confidence/history, stability constraint, probabilistic failure risk | Linux `SCHED_DEADLINE`, fixed-priority/EDF analysis, bounded deadline miss | Deadline miss와 model/cascade 선택 배경은 제공하지만 machine condition + system slack 기반 `W/H/M` runtime policy는 확인되지 않음 |
| Embedded fault diagnosis deployment | Thota et al.; Ma et al.; Lee and Kim; Choi et al. | Model architecture, fixed input/window, lightweight model | Mostly offline model/input design | MCU/SBC inference, TinyML, Raspberry Pi, STM32, inference time measurement | Resource-constrained FD 배경은 직접적이나 runtime adaptation, deadline miss/jitter, PREEMPT_RT 비교는 제한적 |
| PREEMPT_RT and SBC platform studies | Adam et al.; Dewit et al.; Vaghasiya; De Marco et al. | Kernel configuration, PREEMPT_RT 여부, TFLite/thread/configuration | Offline benchmarking/configuration search | Raspberry Pi/BeagleBone, cyclictest/latency, TFLite inference, CPU/temp/memory metrics | Platform timing 근거는 제공하지만 vibration FD algorithm, `W/H/M` adaptation, machine condition trigger는 다루지 않음 |
| Miscellaneous real-time scheduling | Pathan; Tang et al.; Guan et al.; self-suspending EDF work | Ready queue, priority inheritance, federated resources, analysis interval | Scheduling events, data propagation, criticality, self-suspension | EDF overhead, end-to-end latency, DAG scheduling, self-suspension analysis | Pipeline timing 해석의 보조 배경. 본 연구 novelty의 직접 비교군은 아님 |
| This work | 본 연구 | `W` window size, `H` diagnosis period/hop size, `M` model | Machine condition and system slack | MCU/SBC, RTOS/PREEMPT_RT, deadline-aware vibration fault diagnosis | 현재 연구에서 검증해야 할 주장 |

## Caption Draft

Comparison of related work by adaptation variable, trigger, and real-time/platform scope. Existing work covers elastic period/workload scheduling, adaptive input sizing, deadline-aware DNN serving, and embedded real-time platforms separately. In the surveyed papers, we did not find a runtime policy that jointly selects vibration diagnosis window size, diagnosis period, and model based on both machine condition and system slack.

## Notes

- `Representative works`는 전체 인용 목록이 아니라 계열별 대표 예시다.
- `This work` 행은 원고에서 실험 결과가 준비된 뒤 표현 강도를 조정해야 한다.
- 정량 결과는 이 표에 넣지 않는다. 수치는 본문 또는 별도 result table에서 조건과 함께 제시한다.
