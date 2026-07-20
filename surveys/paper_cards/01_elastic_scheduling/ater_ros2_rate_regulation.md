# ATER: Adaptive Task Execution Rate Regulation for Enhanced Real-Time Performance in ROS 2

- **그룹**: 1 elastic_scheduling
- **출처/연도**: IEEE 31st International Conference on Embedded and Real-Time Computing Systems and Applications, RTCSA 2025, DOI 10.1109/RTCSA66114.2025.00019
- **저자**: Ruoxiang Li, Ziwei Song, Mingsong Lv, Jen-Ming Wu, Chun Jason Xue, Jianping Wang, Nan Guan

## 두 질문
- **가변 변수**: ROS 2 task chain 선두 timer task의 sensor data sampling rate `R_tmr`, 즉 timer period의 역수다. Sampling rate를 바꿔 downstream subscription task의 activation/execution rate를 간접 조절한다.
- **트리거**: Runtime observer가 observation period마다 수집한 executor 간 publishing/subscription rate, message drop 비율, buffer 상태와 task execution-time distribution이다. Message Drop Indicator가 병목을 감지하면 rate를 낮추고, drop이 없으며 processing capability가 개선됐다고 Increasing Sampling Rate Indicator가 판단하면 사전 설정 상한까지 rate를 높인다.

## Abstract 3줄 요약
- ROS 2 publish-subscribe task chain에서는 동적인 execution-time 변동과 executor 간 조정 부재 때문에 생산·소비 rate가 어긋날 수 있다.
- ATER는 source-code 수정 없이 동작하는 runtime observer와 task regulator로 이 misalignment를 탐지하고 sensor sampling rate를 조절한다.
- 저자들은 이 조절이 message drop과 불필요한 계산을 줄이고 end-to-end latency를 개선한다고 평가한다.

## Conclusion 요약
- ATER는 LTTng 기반 runtime event 관측과 rate parameter 생성을 결합해 ROS 2 task chain의 execution-rate misalignment를 완화한다. Synthetic workload를 사용하는 Autoware-inspired case study에서 message drop, CPU 낭비와 일부 resource-contention 설정의 end-to-end latency를 줄였으며, sampling-rate 감소가 multi-sensor temporal alignment와 perception robustness에 미치는 영향은 future work로 남긴다.

## 요점
- 플랫폼: Intel Core i7-10700 2.90 GHz desktop, Ubuntu 22.04.3 LTS, ROS 2 Humble Hawksbill. Python 3 구현.
- 도메인: ROS 2 기반 autonomous-system publish-subscribe task chain.
- 핵심 방법 (2~3줄): LTTng live trace에서 task/executor/message event를 observation period마다 수집한다. MDI와 ISRI로 downstream bottleneck 또는 회복을 판단하고, 예상 처리율과 buffer backlog를 이용해 새 sampling rate를 계산해 timer를 reset한다. Application source와 ROS 2 executor scheduling 자체는 변경하지 않는다.
- 정식화/수식 (있으면): `R_tmr`는 sampling rate이고 timer period의 역수다. MDI는 observation period의 drop 수를 처리 가능한 message 수와 비교해 threshold `theta_i`를 넘는지 판정한다. ISRI는 평균 실행시간이 과거 분포보다 충분히 작고 현재 publication rate보다 처리 능력이 큰 경우 rate 증가를 허용한다.

## 0708 면담 기준 보강
- **실시간성 수준**: Message drop, end-to-end average/maximum latency, latency stability, CPU time saving, timer-reset overhead를 실측한다. Timer-reset overhead는 40~100 microseconds 범위이고 대체로 80 microseconds 아래라고 보고한다. Deadline miss 또는 formal schedulability 분석은 제공하지 않는다.
- **실행시간 가정**: Executor segment의 execution time을 runtime에 관측하고 normal distribution의 mean/deviation으로 모델링한다. 평가에서는 synthetic task execution time을 normal distribution과 두 distribution 사이의 변화로 생성한다.
- **보장 방식**: Empirical feedback regulation이다. Hard deadline, utilization bound, WCET 기반 admission, worst-case message-drop bound는 확인되지 않는다. Rate 증가는 pre-defined maximum을 넘지 않지만 application utility 보장은 없다.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): Runtime `H/T` 조절은 직접 다루지만 vibration diagnosis의 `W/M`, anomaly-based machine condition, explicit system slack, feasible-mode admission, PREEMPT_RT는 다루지 않는다.
- 내 연구에 쓸 곳: Diagnosis period `H`를 pipeline production/consumption rate와 연결하고, 관측 실행시간과 backlog로 runtime regulation하는 최신 구현 비교군이다. 본 연구에서는 여기에 anomaly-driven utility와 deadline-feasible mode filtering이 추가로 필요하다.
- 인용할 문장 (있으면, 15단어 이내): "adapting the sensor data sampling rates at runtime"

## 불확실한 점
- 확인 필요: 논문의 execution rate는 downstream callback activation/processing rate까지 포함하는 ROS 2 문맥이며, CPU scheduler가 task에 배정하는 rate와 동일하지 않다.
- 확인 필요: MDI threshold와 ISRI parameter는 평가에서 empirical하게 설정되며 workload가 바뀔 때의 tuning 방법은 확립되지 않았다.
- 확인 필요: Sampling-rate 감소에 따른 sensor information loss와 perception utility는 평가하지 않았고 future work로 남긴다.
- 확인 필요: Partitioned core mapping과 synthetic execution-time workload 결과를 Pi Zero 2W의 제한된 core 및 PREEMPT_RT 환경으로 일반화할 수 없다.
