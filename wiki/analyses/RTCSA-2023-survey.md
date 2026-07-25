# RTCSA 2023 Survey

> Interest areas used for scoring (from interests.md): 시스템 소프트웨어/컴퓨터 구조 관점의 실시간 시스템 연구(OS 커널, 메모리/캐시, 하드웨어-소프트웨어 co-design 등), Edge AI/AI 경량화. 이론·수식 중심의 스케줄링 분석(schedulability 증명, WCRT 유도, 확률론적 타이밍 분석)은 감점. 보안(공격/방어/CFI/TEE/사이드채널 등)은 사실상 제외 대상. 네트워킹(TSN, 무선 프로토콜, network calculus 등)도 관심 거의 없음+배경지식 부족으로 감점.
>
> "Message from the Chairs: RTCSA 2023" 항목은 논문이 아닌 개회사라 서베이 대상에서 제외했습니다.

| Select | Paper Title | Interest | Summary (KR) | Reason |
|---|---|---|---|---|
| [ ] | RDMA-Based Deterministic Communication Architecture for Autonomous Driving | ★★★★★ | Soft-RoCE 기반 RDMA에 결정론적 스케줄러를 얹은 자율주행용 통신 아키텍처 | 통신 스택·하드웨어 아키텍처 설계, 실기기 실험 중심 |
| [ ] | PELSI: Power-Efficient Layer-Switched Inference | ★★★★★ | CPU-GPU 레이어 스위칭과 DVFS로 CNN 추론 전력 효율을 최적화하는 PELSI | HMPSoC 아키텍처 인식 + CNN 추론 최적화, 두 관심분야 동시 부합 |
| [ ] | Hardware Acceleration with Zero-Copy Memory Management for Heterogeneous Computing | ★★★★★ | ROS2용 이기종 컴퓨팅 zero-copy 메모리 관리 프레임워크 Hazcat | GPU/FPGA 메모리 관리 시스템 소프트웨어, 이론보다 프레임워크 구현 중심 |
| [ ] | IRQ Coloring and the Subtle Art of Mitigating Interrupt-Generated Interference | ★★★★★ | QoS 기반 인터럽트 컬러링으로 혼합 크리티컬리티 간섭을 완화하는 기법 | 인터럽트 처리 하드웨어 메커니즘, Xilinx ZCU102 실보드 구현·평가 |
| [ ] | Improving Read Performance for LDPC-Based SSDs with Adaptive Bit Labeling on Vth States | ★★★★★ | 셀 문턱전압 상태에 적응적 비트 라벨링을 적용해 LDPC SSD 읽기 성능을 개선 | 플래시 메모리 하드웨어 아키텍처 최적화, 관심분야 1에 정확히 부합 |
| [ ] | Machine Learning Techniques for Understanding and Predicting Memory Interference in CPU-GPU Embedded Systems | ★★★★★ | Jetson Xavier에서 CPU-GPU 메모리 간섭을 ML로 특성화·예측하는 연구 | CPU-GPU 메모리 아키텍처 간섭 분석, 임베디드 실기기 실증 중심 |
| [ ] | BandWatch: A System-Wide Memory Bandwidth Regulation System for Heterogeneous Multicore | ★★★★★ | Linux 커널 모듈로 CPU-GPU 메모리 대역폭을 시스템 전역에서 규제하는 BandWatch | 커널 모듈 구현, Jetson Nano 실기기 평가, 관심분야 1에 정확히 부합 |
| [ ] | Memory-Aware DVFS Governing Policy for Improved Energy-Saving in the Linux Kernel | ★★★★★ | 메모리 스톨 사이클을 반영해 Linux schedutil 거버너를 개선한 DVFS 정책 | Linux 커널 스케줄러/거버너 개선, 시스템 소프트웨어 구현 중심 |
| [ ] | Accelerating Permute and N-Gram Operations for Hyperdimensional Learning in Embedded Systems | ★★★★★ | SIMD 활용으로 하이퍼차원 컴퓨팅의 permute/n-gram 연산을 가속 | SIMD 아키텍처 최적화 + 임베디드 경량 ML 프레임워크, 두 관심분야에 가까움 |
| [ ] | Traffic Injection Regulation Protocol Based on Free Time-Slots Requests | ★★★★☆ | 런타임 정보를 활용해 NoC 트래픽 주입을 동적으로 규제하는 프로토콜 | Network-on-Chip 인터커넥트 아키텍처 메커니즘 설계 |
| [ ] | Extending ROS Transform Library for Massive Autonomous Robots | ★★★★☆ | SQL 기반 인터페이스로 ROS TF 라이브러리의 락 병목과 팬텀 이상을 해결 | ROS 미들웨어 라이브러리 시스템 설계 개선이 핵심 |
| [ ] | ILP Based Mapping for Elastic CGRAs | ★★★★☆ | ILP 기반 매핑으로 Elastic CGRA의 매핑 시간을 단축하는 기법 | 재구성 가능 하드웨어 아키텍처(CGRA) 대상 최적화 |
| [ ] | Timing-Aware ROS 2 Architecture and System Optimization | ★★★★☆ | ROS 2 타이머·버퍼 설정을 분석해 콜백 우선순위화로 종단 지연을 줄이는 최적화 | ROS 2 시스템 아키텍처·설정 최적화가 핵심, 실용적 튜닝 중심 |
| [ ] | Shared Dictionary Compression for Efficient Mobile Software Distribution | ★★★☆☆ | IR 레이어에서 공유 사전을 추출해 모바일 소프트웨어 크기를 줄이는 압축 기법 | 소프트웨어 배포 최적화 기법이나 OS/하드웨어 아키텍처보다는 컴파일러 기법에 가까워 애매함 |
| [ ] | Make PLOR Real-Time and Fairly Decentralized | ★★★☆☆ | 스레드 ID 기반 타임스탬프로 Plor 동시성 제어 프로토콜의 중앙집중 병목을 해소 | 데이터베이스 동시성 제어 시스템이나 OS/하드웨어 아키텍처와는 결이 달라 애매함 |
| [ ] | Timing Analysis of Embedded Software Updates | ★★★☆☆ | 업데이트 영향만 재분석하는 차분 타이밍 분석 도구 ReTA/Delta | 산업용 aiT 도구 통합 등 실용적이나 WCET 분석 이론이 핵심이라 애매함 |
| [ ] | TEEVseL4: Trusted Execution Environment for Virtualized seL4-Based Systems | ★★☆☆☆ | seL4 마이크로커널 기반 가상화 게스트에 TrustZone 호환 TEE 서비스를 제공 | TrustZone 기반 TEE 보안 아키텍처가 핵심이라 관심분야(보안) 제외 대상이나, seL4 마이크로커널 가상화 구현은 참고할 만함 |
| [ ] | DDS Implementations as Real-Time Middleware - A Systematic Evaluation | ★★☆☆☆ | DDS-Perf로 4개 벤더 DDS 구현체의 실시간 성능·신뢰성을 실증 비교 | DDS 전송 계층(네트워킹) 중심 주제라 관심분야 제외 대상이나, 실사용 벤더 구현 실증 벤치마킹은 참고할 만함 |
| [ ] | Time-Sensitive Networking's Scheduled Traffic Implementation on IEEE 802.11 COTS Devices | ★★☆☆☆ | IEEE 802.11 COTS 장비에 TSN 스케줄드 트래픽을 구현·실증 평가 | TSN·무선 프로토콜(IEEE 802.11) 중심 주제라 네트워킹 관심분야 제외 대상이나, 실기기 구현 실증은 참고할 만함 |
| [ ] | Improved Bus Contention Analysis for 3-Phase Tasks | ★★☆☆☆ | 캐시 미스 상한을 반영해 3-phase 태스크의 버스 경합 분석을 개선 | 메모리 버스 소재이나 WCRT 바운드 개선이라는 이론 분석이 핵심 |
| [ ] | Analyzing Digital Services Across the Compute Continuum Using iFogSim | ★★☆☆☆ | 디바이스-엣지-포그-클라우드 연속체의 QoS·에너지를 iFogSim으로 분석 | 컴퓨트 연속체 소재이나 정보가 짧고 시뮬레이션 도구 활용이 초점 |
| [ ] | Accelerating Scan Transaction with Node Locking | ★★☆☆☆ | 리프 노드 락킹으로 팬텀을 방지하는 트랜잭션 SCAN 가속 프로토콜 | 데이터베이스 동시성 제어 기법, 시스템/아키텍처·edge AI 요소 약함 |
| [ ] | Self-Supervised Multi-LiDAR Object View Generation Using Single LiDAR | ★★☆☆☆ | 다중 LiDAR 데이터로 단일 LiDAR 포인트클라우드를 보완하는 자기지도 학습 기법 | 인식 모델 학습 기법 중심, edge AI 경량화보다는 데이터 보완 방법론에 가까움 |
| [ ] | Dynamic Deterministic Quality of Service Model with Behavior-Adaptive Latency Bounds | ★★☆☆☆ | 초과 트래픽에도 점진적 성능 저하를 허용하는 동적 QoS 모델 DPTB | 네트워크 QoS 모델·토큰버킷 설계 이론이 핵심 |
| [ ] | LAG-Based Analysis for Preemptive Global Scheduling with Dynamic Cache Allocation | ★★☆☆☆ | 동적 캐시 할당을 지원하는 전역 EDF의 LAG 기반 스케줄가능성 분석 | 캐시 소재이나 스케줄가능성 분석 이론이 핵심 |
| [ ] | Parameterized Workload Adaptation for Fork-Join Tasks with Dynamic Workloads and Deadlines | ★★☆☆☆ | 포크-조인 태스크의 워크로드를 파라미터화해 조정하는 Pareto 최적 기법 | 실제 위성 미션 적용이 있으나 최적화 이론이 핵심 |
| [ ] | Safety-Aware Implementation of Control Tasks via Scheduling with Period Boosting and Compressing | ★★☆☆☆ | 제어 안전성을 고려해 샘플링 주기를 boost/compress하는 AUTOSAR 스케줄링 기법 | 자동차 제어-스케줄링 co-design이나 스케줄링 정책 설계 자체가 핵심 |
| [ ] | A Comparison of Transformer and AR-SI Oracle For Control-CPS Software Fault Localization | ★★☆☆☆ | Transformer와 AR-SI 오라클의 CPS 결함 위치추정 성능을 비교 | ML 모델 비교 연구이나 edge AI 경량화보다 결함 진단 방법론에 가까움 |
| [ ] | Advanced Modeling and Analysis of Individual and Combined TSN Shapers in OMNeT++ | ★☆☆☆☆ | OMNeT++로 TSN 셰이퍼 조합의 지연을 시뮬레이션하고 NC 상한과 비교 | 네트워크 캘큘러스·시뮬레이션 이론 중심 |
| [ ] | T2Remoter: a Remote Table Tennis Coaching System Combining VR and Robotics | ★☆☆☆☆ | VR과 로봇팔을 결합한 원격 탁구 코칭 시스템 | HCI/원격 협업 애플리케이션, 관심분야와 무관 |
| [ ] | Reducing Response-Time Bounds via Global Fixed Preemption Point EDF-Like Scheduling | ★☆☆☆☆ | 우선순위 지점을 도입한 G-FPP-EL 스케줄링과 응답시간 상한 분석 | 응답시간 분석 이론이 핵심 |
| [ ] | Response-time Analysis of Fault-Tolerant Hard Real-Time Systems Under Global Scheduling | ★☆☆☆☆ | 시간 중복 기반 결함 허용 하드 실시간 시스템의 응답시간 분석 | 응답시간 분석 이론 중심, 정보도 짧음 |
| [ ] | Parameter Optimization for EDF-Like Scheduling of Self-Suspending Tasks | ★☆☆☆☆ | 상대 우선순위 지점 튜닝으로 자가유예 태스크 스케줄가능성을 개선 | 스케줄링 파라미터 최적화 이론 중심 |
| [ ] | Efficient Response Time Bound for Typed DAG Tasks | ★☆☆☆☆ | 다항 시간 복잡도의 typed DAG 태스크 응답시간 상한 기법 | DAG 응답시간 분석 이론 중심 |
| [ ] | Designing a 3D Human Pose Estimation-Based VR Tennis Training System | ★☆☆☆☆ | 단일 영상 3D 스켈레톤 추정으로 VR 테니스 서브 훈련을 지원하는 시스템 | HCI/스포츠 훈련 애플리케이션, 관심분야와 무관 |
| [ ] | Investigating Requirements and Expectations of Wearable Telexistence Robotic Systems | ★☆☆☆☆ | 웨어러블 텔레이그지스턴스 로봇 Piton의 사용성 요구사항 탐색 | HCI/사용성 연구, 관심분야와 무관 |
| [ ] | An Integrated Real-Time and Security Scheduling Framework for CPS | ★☆☆☆☆ | 보안-실시간 co-design을 배낭 문제로 정식화하고 FPTAS로 근사하는 프레임워크 | 스케줄링·근사 알고리즘 이론이 핵심 |
| [ ] | Visualization System Using Virtual Reality for Work Improvement in Small and Medium Manufacturing Industries | ★☆☆☆☆ | 중소 제조업 공정 개선을 위한 VR 시각화 시스템 | HCI/제조 시각화 애플리케이션, 관심분야와 무관 |
| [ ] | A Robot Arm-based Haptic Feedback System for Augmented Reality Applications | ★☆☆☆☆ | 웨어러블 로봇팔로 AR 환경에 햅틱 피드백을 제공하는 시스템 | HCI/AR 애플리케이션, 관심분야와 무관 |
