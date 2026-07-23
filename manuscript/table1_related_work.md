# Table 1 Draft: Related Work Comparison

이 파일은 `surveys/comparison_table.md`의 내부 상세 비교표를 원고용으로 압축한 초안이다.
개별 논문 50편을 모두 나열하지 않고, 관련연구 계열별 핵심 차이만 보여준다.

이 표는 관련연구 **계열** 비교용이다. Real-Time Fault Diagnosis 개별 논문의 O/△/X 비교는 `manuscript/realtime_fault_diagnosis_related_work_table.md`에서 관리한다. 최종 원고에서는 두 표의 역할과 지면을 보고 하나만 본문에 두거나 다른 하나를 부록으로 이동한다.

원고의 related-work 절 구성은 `surveys/research_aligned_literature_taxonomy_0723.md`의 RW1~RW4를 따른다. 아래 category는 보관 그룹과 세부 비교를 위한 행이며, MCU/SoC 같은 플랫폼은 독립적인 우선순위가 아니라 비교 태그다.

원고에 넣을 때는 venue/year 표기를 manuscript 스타일에 맞춰 줄이고, 정량 수치는 본문에서 검증된 경우에만 사용한다.

| Category | Representative works | Main variable | Adaptation trigger | RT/platform consideration | Limitation vs. this work |
| --- | --- | --- | --- | --- | --- |
| Elastic and rate-adaptive scheduling | Buttazzo et al.; Chantem et al.; Orr et al.; Sudvarg et al.; Xu et al.; Li et al.; Gifford et al. | Period/rate, controller/mode, utilization, workload, sampling rate, core/cache/BW allocation | Overload, available utilization, mode-change event, control safety, message/processing-rate mismatch | EDF/RM and federated schedulability, weakly-hard safety, multi-mode transition DBF, ROS 2 feedback | Period+mode+resource co-design은 이미 존재함. Vibration temporal `W`, diagnosis utility/anomaly score, inference `M`, runtime slack과 PREEMPT_RT pipeline의 결합은 확인되지 않음 |
| Input-adaptive visual perception | Hu et al.; Liu et al.; Soyyigit et al. | Image/segment size, LiDAR resolution, inspection frequency, canvas packing, batching | Object criticality, spatial uncertainty, workload, deadline, predicted execution time | Embedded GPU, autonomous driving/surveillance, deadline-aware perception | Vision/LiDAR spatial input 중심. Vibration window `W`, diagnosis period `H`, model `M`, machine condition 기반 utility를 함께 다루지 않음 |
| Input-adaptive fault diagnosis | Kim et al.; Tang et al.; Jalonen et al. | Window size, input length, segment length | Bearing parameters, sampling frequency, anomaly deviation, speed variation | Fault diagnosis accuracy and processing-time evaluation, mostly offline/data-driven selection | `W`를 다루지만 system slack, deadline-aware runtime scheduling, `H/M` 공동 선택, RTOS/PREEMPT_RT는 확인되지 않음 |
| Deadline-aware DNN serving | Yao et al.; Kang et al.; Chen et al.; Xu et al.; Li et al.; Cao et al.; Han et al.; He et al.; Zhang et al.; Raj et al. | DNN stage/depth, input scale, model capability, heterogeneous mapping, exit, batch/fusion/offloading | Confidence, slack/deadline, queue/load, critical region, environment/control condition, GPU budget, heart rate | Non-preemptive EDF, fixed-priority WCRT, edge GPU/server, SLO and deadline miss | Slack 기반 image scale와 condition-aware capability는 이미 다룸. Vibration temporal `W`, runtime machine condition + slack, `H/M`, PREEMPT_RT timing의 결합은 확인되지 않음 |
| Weakly-hard, cascade, and deadline-risk scheduling | Chen et al.; Braun and Altmeyer; Agrawal et al.; Baruah et al.; Hawila et al.; Guan et al. | CBS parameters, miss-handling policy, cascade ordering, period, active dropping | Weakly-hard constraint, deadline miss/overload, confidence/history, stability constraint, probabilistic failure risk | Linux `SCHED_DEADLINE`, STM32/ThreadX empirical fallback, fixed-priority/EDF analysis | Deadline miss와 fallback/model selection 배경은 제공하지만 machine condition + system slack 기반 feasible `W/H/M` runtime policy는 확인되지 않음 |
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
