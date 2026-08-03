# Pipelined Data-Parallel CPU/GPU Scheduling for Multi-DNN Real-Time Inference

- **그룹**: 3 rt_dnn_serving
- **연구 섹션**: S4 Deadline-Aware AI Inference and Mode Selection
- **플랫폼 태그**: `PL-HET-SOC` (NVIDIA TX2), `PL-SERVER-GPU` (Intel Xeon + GTX 1080)
- **실행환경 태그**: `ENV-LINUX`
- **출처/연도**: IEEE Real-Time Systems Symposium (RTSS), 2019, DOI 10.1109/RTSS46320.2019.00042
- **저자**: Yecheng Xiang, Hyoseung Kim

## 두 질문
- **가변 변수**: DNN layer의 pipeline stage partition, CPU/GPU node configuration, worker/core allocation. DNN model이나 input fidelity는 runtime에 바꾸지 않는다.
- **트리거**: 새 task가 들어올 때 admission control을 수행한다. Runtime execution-time overrun은 task class 변경과 system alert를 유발한다. Machine condition trigger는 없다.

## Abstract 3줄 요약
- 기존 DNN framework는 다수 model의 periodic/sporadic inference가 함께 실행될 때 worst-case response time과 resource utilization을 함께 다루기 어렵다.
- DART는 CPU/GPU pipeline과 data parallelism, stage/node configuration, execution-time profiling, admission control과 runtime enforcement를 결합한다.
- Intel Xeon/GTX 1080과 NVIDIA TX2 평가에서 real-time task의 최대 응답시간과 best-effort throughput을 기존 방식보다 개선했다고 보고한다.

## Conclusion 요약
- DART는 여러 DNN의 concurrent inference를 위해 inter-node pipeline과 intra-node parallelism을 구성하고, profiled execution time에 기반한 schedulability analysis와 admission control을 제공한다. 저자는 remote node, FPGA와 shared-memory interference 처리를 후속 과제로 제시한다.

## 요점
- 플랫폼: Intel Xeon E5-2620 v4 + NVIDIA GTX 1080, NVIDIA TX2. Ubuntu 16.04, Caffe v1.0.
- 도메인: Multi-DNN real-time inference scheduling.
- 핵심 방법 (2~3줄): DNN layer를 stage로 묶어 heterogeneous CPU/GPU node에 배치하고, node 안에서는 worker를 통한 data parallelism을 사용한다. Layer-wise measured maximum을 실행시간 bound로 두고 pipeline response-time analysis, admission control과 runtime overrun enforcement를 적용한다.
- 정식화/수식 (있으면): Sporadic task `tau_i=(T_i,C_i,D_i,L_i)`를 사용하며 `D_i<=T_i`인 real-time task의 end-to-end response-time bound로 admission을 판정한다. Layer 실행시간은 실행 node에 따라 `C_i,j(p_k)`로 달라진다.

## 0708 면담 기준 보강
- **실시간성 수준**: Explicit constrained deadline, pipeline worst-case response-time analysis, admission control과 runtime enforcement를 제공한다. 다만 OS/driver timing jitter를 guarantee 범위에서 명시적으로 제외한다.
- **실행시간 가정**: Layer/node별 반복 측정에서 관찰된 최대값을 WCET estimate로 사용한다. 관찰보다 긴 실행이 발생할 수 있음을 인정하고 runtime overrun을 감시한다.
- **보장 방식**: Profile bound와 scheduling/resource-arbitration model이 유효하다는 조건에서 analytical admission을 수행한다. Hardware/OS 전체의 formal WCET 보장은 아니다.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): Fixed DNN taskset의 stage/resource scheduling을 다루며 vibration `W/H`, machine condition, diagnostic accuracy 변화와 PREEMPT_RT는 다루지 않는다.
- 내 연구에 쓸 곳: Offline profiling이 online에서 무의미한 것이 아니라 admission에 필요한 mode별 cost model을 제공한다는 근거. 측정 최대 초과를 감시하는 runtime enforcement와 OS interference를 guarantee 밖에 둔 한계도 비교 가능하다.
- 인용할 문장 (있으면, 15단어 이내): 없음.

## 불확실한 점
- 확인 필요: Abstract의 최대 98.5% response-time 감소와 17.9% throughput 증가는 각 task/model/batch 조건을 함께 적을 때만 원고에 사용한다.
- 확인 필요: 관찰 최대 기반 WCET estimate를 본 연구의 formal bound로 등치하지 않는다.
