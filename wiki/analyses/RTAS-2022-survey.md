# RTAS 2022 Survey

> Interest areas used for scoring (from interests.md): 시스템 소프트웨어/컴퓨터 구조 관점의 실시간 시스템 연구(OS 커널, 메모리/캐시, 하드웨어-소프트웨어 co-design 등), Edge AI/AI 경량화. 이론·수식 중심의 스케줄링 분석(schedulability 증명, WCRT 유도, 확률론적 타이밍 분석)은 감점. 보안(공격/방어/CFI/TEE/사이드채널 등)은 사실상 제외 대상. 네트워킹(TSN, 무선 프로토콜, network calculus 등)도 관심 거의 없음+배경지식 부족으로 감점.

| Select | Paper Title | Interest | Summary (KR) | Reason |
|---|---|---|---|---|
| [ ] | Work in Progress: Automatic Construction of Pipeline Datapaths from High-Level HDL Code | ★★★★★ | Chisel/FIRRTL로 오픈소스 RISC-V 프로세서의 파이프라인 데이터패스 모델을 자동 생성 | 하드웨어 기술 언어 기반 아키텍처 모델링 자동화, 관심분야 1에 정확히 부합 |
| [ ] | Compiler-Directed High-Performance Intermittent Computation with Power Failure Immunity | ★★★★★ | 컴파일러 정적 분석으로 전력 실패 면역성을 보장하는 롤백 프리 간헐 컴퓨팅 ROCKCLIMB | 배터리리스 임베디드 시스템 컴파일러/시스템 co-design, 관심분야 1에 정확히 부합 |
| [ ] | FLYOS: Integrated Modular Avionics for Autonomous Multicopters | ★★★★★ | 분리 커널 기반 IMA로 이기종 멀티코어 항공 플랫폼의 혼합 크리티컬리티 기능을 통합 | 분리 커널·하이퍼바이저 아키텍처 설계, 관심분야 1에 정확히 부합 |
| [ ] | Jumpstart: Fast Critical Service Resumption for a Partitioning Hypervisor in Embedded Systems | ★★★★★ | 저전력 서스펜드 상태에서 파티셔닝 하이퍼바이저의 웨이크업 지연을 최소화하는 Jumpstart | 하이퍼바이저 전원 관리 시스템 기법, 관심분야 1에 정확히 부합 |
| [ ] | Memory Utilization-Based Dynamic Bandwidth Regulation for Temporal Isolation in Multi-Cores | ★★★★★ | 피드백 기반 커널 모듈로 메모리 대역폭을 동적 규제하는 시간 격리 메커니즘 | Linux 커널 모듈 구현, NXP 실보드 실증, 관심분야 1에 정확히 부합 |
| [ ] | DNN-SAM: Split-and-Merge DNN Execution for Real-Time Object Detection | ★★★★☆ | 안전 critical 영역과 다운스케일 영역으로 DNN 추론을 분할·병합하는 DNN-SAM | 실시간 DNN 추론 분할 실행 최적화, edge AI 관심분야에 가까움 |
| [ ] | Self-Cueing Real-Time Attention Scheduling in Criticality-Aware Visual Machine Perception | ★★★★☆ | 옵티컬 플로우 기반 영역 우선순위화로 GPU 인식 처리를 최적화하는 BPB 스케줄링 | Jetson Xavier GPU 실시간 인식 최적화, edge AI 관심분야에 가까움 |
| [ ] | FA2: Fast, Accurate Autoscaling for Serving Deep Learning Inference with SLA Guarantees | ★★★★☆ | 그래프 기반 모델과 동적 프로그래밍으로 DL 추론 서빙을 오토스케일링하는 FA2 | AI 추론 서빙 시스템 최적화, edge AI 관심분야에 가까움 |
| [ ] | Brief Industry Paper: Enabling Level-4 Autonomous Driving on a Single $1k Off-the-Shelf Card | ★★★★☆ | 소프트웨어 최적화로 저가 상용 카드에서 레벨4 자율주행 워크로드를 실현 | 임베디드 플랫폼 AD 워크로드 최적화, edge AI 관심분야에 가까움 |
| [ ] | End-to-End Analysis of Event Chains under the QNX Adaptive Partitioning Scheduler | ★★★☆☆ | QNX APS 예약 메커니즘을 최초로 규명하고 이벤트 체인 응답시간을 분석 | 실제 QNX 플랫폼 실증이 있으나 응답시간 분석 이론 도출이 핵심이라 애매함 |
| [ ] | Minimizing DAG Utilization by Exploiting SMT | ★★★☆☆ | SMT로 DAG 노드를 동시 실행해 총 이용률을 최소화하는 최적화 기법 | SMT 하드웨어 기능 활용이나 이용률 최적화 이론이 핵심이라 애매함 |
| [ ] | SBIs: Application Access to Safe, Baremetal Interrupt Latencies | ★★☆☆☆ | TrustZone-M 하드웨어 가속 인터럽트 전달로 격리를 유지하며 지연을 95% 감소 | TrustZone 기반 보안 아키텍처가 핵심이라 관심분야 제외 대상(인터럽트 지연 최적화 관점은 참고할 만함) |
| [ ] | PAC-PL: Enabling Control-Flow Integrity with Pointer Authentication in FPGA SoC Platforms | ★★☆☆☆ | ARM PA와 FPGA 팹릭을 결합해 이기종 SoC에 CFI를 구현하는 PAC-PL | CFI(제어 흐름 무결성) 보안 메커니즘이 핵심이라 관심분야 제외 대상(FPGA SoC co-design 관점은 참고할 만함) |
| [ ] | RT-WiFi on Software-Defined Radio: Design and Implementation | ★★☆☆☆ | SDR 기반으로 RT-WiFi를 재구현해 완전한 스택 설정 가능성을 제공하는 SRT-WiFi | 네트워킹(RT-WiFi) 중심 주제라 관심분야 제외 대상(SDR 아키텍처 구현 관점은 참고할 만함) |
| [ ] | Guaranteeing Safety Despite Physical Errors in Cyber-Physical Systems | ★★☆☆☆ | 타임월과 세이프티백업으로 물리 오류 발생 시 CPS 안전을 보장하는 메커니즘 | 제어 메커니즘 설계 중심, 시스템/아키텍처 요소 약함 |
| [ ] | Work in Progress: KDBench - towards open source benchmarks for measurement-based multicore WCET estimators | ★★☆☆☆ | 측정 기반 WCET 추정기를 위한 오픈소스 벤치마크 제안 | 벤치마크 제안 중심, 시스템/아키텍처 요소 약함 |
| [ ] | Brief Industry Paper: The Necessity of Adaptive Data Fusion in Infrastructure-Augmented Autonomous Driving System | ★★☆☆☆ | 노변-차량 협력 자율주행에서 적응적 데이터 퓨전 방법을 제안 | 실차 시스템 개요이나 네트워크 조건 대응 퓨전 전략이 초점, 아키텍처 깊이는 얕음 |
| [ ] | Deadline-Miss-Adaptive Controller Implementation for Real-Time Control Systems | ★★☆☆☆ | 연속 마감 실패 횟수에 따라 컨트롤러 파라미터를 적응시키는 기법 | 제어 적응 알고리즘 설계 중심, 시스템/아키텍처 요소 약함 |
| [ ] | The Thundering Herd: Amplifying Kernel Interference to Attack Response Times | ★☆☆☆☆ | seL4의 우선순위·예산 인식 IPC가 오히려 시간 격리를 위협할 수 있음을 실증 | 보안 취약점(IPC 공격) 분석이 핵심이라 관심분야 제외 대상 |
| [ ] | Work in Progress: Exploring Schedule-Based Side-Channels in TrustZone-Enabled Real-Time Systems | ★☆☆☆☆ | TrustZone 보안 모드 전환 타이밍을 추론하는 스케줄 기반 사이드채널 공격 | 사이드채널 공격 분석이 핵심이라 관심분야 제외 대상 |
| [ ] | Demo Abstract: Open RT-WiFi Platform on Software-Defined Radio | ★☆☆☆☆ | SDR 기반 RT-WiFi 오픈 플랫폼 데모 | 네트워킹(RT-WiFi) 중심 주제라 관심분야 제외 대상 |
| [ ] | Analysis-Runtime Co-design for Adaptive Mixed Criticality Scheduling | ★☆☆☆☆ | AMC 런타임 프로토콜을 수정해 스케줄가능성 분석의 비관성을 줄이는 기법 | 스케줄링 프로토콜·분석 이론 중심 |
| [ ] | Work In Progress: A Solution Based on Dynamic User Equilibrium Toward the Selfless Traffic Routing Model | ★☆☆☆☆ | DUE와 STR 모델 기반 차량 라우팅 알고리즘 예비 구현 | 교통 라우팅 알고리즘 중심, 시스템/아키텍처 요소 없음 |
| [ ] | MSRP-FT: Reliable Resource Sharing on Multiprocessor Mixed-Criticality Systems | ★☆☆☆☆ | 결함 허용 멀티프로세서 자원 공유 프로토콜과 스케줄가능성 분석 | 스케줄가능성 분석 이론 중심 |
| [ ] | Work in Progress: Automatic Response-Time Analysis for Arbitrary Real-Time Linux Workloads | ★☆☆☆☆ | 산업 현장의 RTA 활용 실태를 조사하고 자동화 방향을 제시 | 응답시간 분석 실태조사, 정보도 짧고 이론 중심 |
| [ ] | Partial-Order Reduction for Schedule-Abstraction-based Response-Time Analyses of Non-Preemptive Tasks | ★☆☆☆☆ | 부분순서 축소로 SAG 응답시간 분석의 상태공간 폭발을 완화 | 응답시간 분석 확장성 개선 이론 중심 |
| [ ] | A Mixed-Criticality Approach to Fault Tolerance: Integrating Schedulability and Failure Requirements | ★☆☆☆☆ | 드로핑 관계를 도입해 결함 허용성과 스케줄가능성을 통합하는 MC 확장 | 스케줄가능성·신뢰성 분석 이론 중심 |
| [ ] | A Formal Correctness Proof for an EDF Scheduler Implementation | ★☆☆☆☆ | Coq으로 EDF 스케줄러 구현의 정형 정확성을 증명 | 정형 검증 이론 중심 |
| [ ] | WeaklyHard.jl: Scalable Analysis of Weakly-Hard Constraints | ★☆☆☆☆ | 지배 관계를 활용해 weakly-hard 제약을 확장 가능하게 분석하는 도구 | 확장 가능한 분석 이론·도구 중심 |
| [ ] | Response Time Analysis for Hybrid Task Sets under Fixed Priority Scheduling | ★☆☆☆☆ | 각도 위상을 고려한 하이브리드 태스크셋의 최초 정확한 응답시간 분석 | 응답시간 분석 이론 중심 |
