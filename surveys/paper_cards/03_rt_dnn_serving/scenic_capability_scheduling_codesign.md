# SCENIC: Capability and Scheduling Co-Design for Intelligent Controller on Heterogeneous Platforms

- **그룹**: 3 rt_dnn_serving
- **출처/연도**: IEEE Real-Time Systems Symposium, RTSS 2024, DOI 10.1109/RTSS62706.2024.00026
- **저자**: Jintao Chen, An Zou, Yuankai Xu, Yehan Ma

## 두 질문
- **가변 변수**: DNN controller complexity인 layer depth와 width, layer별 CPU/GPU mapping, concurrent control-task fixed priority다. Sampling period는 task parameter이며 현재 optimization decision variable은 아니다.
- **트리거**: Runtime adaptation trigger는 없다. Plant dynamics, environment condition, deadline, resource와 profiling table을 입력으로 DRL optimizer가 configuration을 offline에서 선택한다. Runtime에는 sensor input이 periodic task를 release하고 사전에 정한 fixed priority와 mapping으로 실행한다. 저자도 runtime co-design은 future work로 남긴다.

## Abstract 3줄 요약
- Heterogeneous platform의 intelligent control은 DNN complexity와 accuracy뿐 아니라 computation latency, physical dynamics와 concurrent resource contention을 함께 고려해야 한다.
- SCENIC은 controller complexity, response time, plant/environment property와 실제 control performance를 연결하는 capability function을 구성한다.
- 이 function을 이용해 DNN capability, CPU/GPU layer allocation과 scheduling을 공동 최적화하고 Jetson TX2와 AirSim 기반 quadcopter control로 평가한다.

## Conclusion 요약
- SCENIC은 ML accuracy나 latency 하나만 최소화하지 않고, intelligent-controller complexity와 end-to-end timing이 physical control performance에 미치는 영향을 capability function으로 통합한다. Offline configuration optimization과 runtime fixed-priority execution을 결합한 HIL case study에서 비교 방식보다 control performance가 좋았다고 결론짓는다.

## 요점
- 플랫폼: Intelligent controller는 NVIDIA Jetson TX2의 ARM Cortex-A57 CPU와 Pascal GPU에서 실행한다. AirSim은 Intel i5-12490F와 NVIDIA RTX 3060 desktop에서 실행하며 Ethernet으로 연결한다.
- 도메인: Multiple autonomous-quadcopter intelligent control on heterogeneous edge computing.
- 핵심 방법 (2~3줄): DNN complexity `c_i`, response time `R_i`, plant property `theta_i`, environment `epsilon_i`와 control performance `J_i`의 관계를 data-driven capability function으로 회귀한다. Layer-level CPU/GPU mapping과 segmented-task WCRT model을 구성하고, DQN으로 model candidate, mapping과 fixed priority를 offline 최적화한다.
- 정식화/수식 (있으면): `J_i = C_i(c_i, theta_i, R_i(c_i,z_i,s), epsilon_i)`. 전체 `sum w_i J_i`를 최소화하면서 task별 `R_i <= D_i`와 CPU/GPU utilization constraints를 만족시킨다.

## 0708 면담 기준 보강
- **실시간성 수준**: Periodic task, end-to-end response time, deadline, fixed-priority WCRT analysis, CPU/GPU utilization과 HIL actual/theoretical response time을 다룬다.
- **실행시간 가정**: DNN layer computation과 CPU-GPU copy를 profiling한 PWCET로 segmented-task EWCET를 계산한다. Controller complexity와 mapping에 따른 `C(M,allocation)` 형태이며, empirical profile이 실제 worst case를 포괄하지 않을 수 있음을 논문이 명시한다.
- **보장 방식**: Optimization constraint로 analytical WCRT가 deadline 이하이고 CPU/GPU utilization이 bound 이하가 되게 한다. Empirical PWCET 불확실성에는 CPU/GPU EWCET safety margin `lambda_C`, `lambda_A`를 적용하므로 guarantee는 profile과 margin의 유효성에 조건부다.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): Environment-aware capability와 model/scheduling co-design은 다루지만 online machine-state adaptation, vibration temporal window `W`, diagnosis period `H`, fault-detection utility, PREEMPT_RT는 다루지 않는다.
- 내 연구에 쓸 곳: Accuracy만이 아니라 condition, model capability와 response time을 application utility로 묶어야 한다는 가장 직접적인 방법론 근거다. 본 연구에서는 `U_diag(q,W,M,R,H)`를 정의하고 offline mode-bank design과 runtime `(q,S)` selection을 분리하는 참고가 된다.
- 인용할 문장 (있으면, 15단어 이내): "control performance is coupled with the model scale/complexity"

## 불확실한 점
- 확인 필요: Environment condition별 configuration은 offline으로 다시 최적화한 결과이며 현재 system이 runtime에 condition 변화를 감지해 model/mapping을 전환한 것은 아니다.
- 확인 필요: SCENIC의 control capability function은 HIL 데이터로 회귀한 application-specific model이므로 vibration diagnosis에 그대로 사용할 수 없다.
- 확인 필요: Control-performance 개선 수치는 environment condition, candidate complexity set과 baseline objective에 따라 달라지므로 원고 인용 전에 Figure 12~15 조건을 확인한다.
- 확인 필요: PWCET safety margin을 어떻게 calibration해야 unseen contention에도 deadline을 지키는지는 본 연구에서 별도로 검증해야 한다.
