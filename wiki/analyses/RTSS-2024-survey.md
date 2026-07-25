# RTSS 2024 Survey

> Interest areas used for scoring (from interests.md): 시스템 소프트웨어/컴퓨터 구조 관점의 실시간 시스템 연구(OS 커널, 메모리/캐시, 하드웨어-소프트웨어 co-design 등), Edge AI/AI 경량화. 이론·수식 중심의 스케줄링 분석(schedulability 증명, WCRT 유도, 확률론적 타이밍 분석)은 감점. 보안(공격/방어/CFI/TEE/사이드채널 등)은 사실상 제외 대상. 네트워킹(TSN, 무선 프로토콜, network calculus 등)도 관심 거의 없음+배경지식 부족으로 감점.

| Select | Paper Title | Interest | Summary (KR) | Reason |
|---|---|---|---|---|
| [ ] | ROTA-I/O: Hardware/Algorithm Co-design for Real-Time I/O Control with Improved Timing Accuracy and Robustness | ★★★★★ | ETS와 2단계 스케줄러 기반 견고한 타이밍 정확 I/O 코프로세서 하드웨어 설계 | 하드웨어/알고리즘 co-design, 관심분야 1에 정확히 부합 |
| [ ] | Interference-free Operating System: A 6 Years' Experience in Mitigating Cross-Core Interference in Linux | ★★★★★ | Linux 커널의 크로스코어 간섭 이슈를 6년간 수정한 산업 실천 경험 정리 | 리눅스 커널 실무 개선, 이론보다 시스템 구현·업스트림 기여 중심 |
| [ ] | MESC: Re-thinking Algorithmic Priority and/or Criticality Inversions for Heterogeneous MCSs | ★★★★★ | DNN 가속기에 명령어 수준 선점을 도입해 MC 우선순위 역전을 해결하는 MESC | SoC·ISA·OS 커널 전 계층 co-design, 관심분야 1에 정확히 부합 |
| [ ] | Coherence-Aided Memory Bandwidth Regulation | ★★★★★ | FPGA 캐시 코히런스 인터페이스를 활용한 나노초 정밀 메모리 대역폭 규제 MemCoRe | CPU+FPGA 아키텍처 활용 메모리 규제, 관심분야 1에 정확히 부합 |
| [ ] | Work-in-Progress: Real-Time Neural Network Inference on a Custom RISC-V Multicore Vector Processor | ★★★★★ | 예측 가능한 코어와 컴파일러 스케줄로 NN 추론을 지원하는 RISC-V 벡터 프로세서 아키텍처 | 커스텀 하드웨어 아키텍처 + NN 추론 최적화, 두 관심분야 동시 부합 |
| [ ] | Per-Bank Bandwidth Regulation of Shared Last-Level Cache for Real-Time Systems | ★★★★★ | 뱅크별 대역폭 규제로 캐시 뱅크 DoS 공격을 방어하는 RISC-V SoC 구현 | 캐시 아키텍처 메커니즘, RISC-V SoC 실증, 관심분야 1에 정확히 부합 |
| [ ] | Jigsaw: Taming BEV-centric Perception on Dual-SoC for Autonomous Driving | ★★★★★ | 듀얼 SoC에서 BEV/PV 모델의 GPU 자원을 타임슬롯 필링으로 관리하는 Jigsaw | GPU 자원 관리 시스템 + BEV 인식 최적화, 두 관심분야 동시 부합 |
| [ ] | Argus: Real-Time HQ Video Decoding with CPU Coordinating on Consumer Devices | ★★★★☆ | 유휴 CPU 자원과 경량 신경망으로 실시간 고화질 비디오 디코딩을 개선하는 Argus | 시스템 자원 활용 스케줄링이 핵심, 경량 NN은 보조적 활용 |
| [ ] | Exploring Real-Time Satellite Computing: From Energy and Thermal Perspectives | ★★★★☆ | 실제 궤도 위성에서 COTS 기기의 에너지·열 특성을 측정하고 ProScale로 관리 | 실기기(위성) 하드웨어 특성 실측 연구, 이론보다 측정·시스템 중심 |
| [ ] | RT-BEV: Enhancing Real-Time BEV Perception for Autonomous Vehicles | ★★★★☆ | ROI 인식 통신과 객체탐지를 공동 최적화해 BEV 인식 종단 지연을 줄이는 RT-BEV | 인식 파이프라인 시스템 최적화, edge AI 인식 관심분야에 가까움 |
| [ ] | DuoJoule: Accurate On-Device Deep Reinforcement Learning for Energy and Timeliness | ★★★★☆ | DVFS 기반으로 온디바이스 DRL의 에너지·지연·성능을 실시간 공동 최적화 | 온디바이스 DRL + 시스템 주파수 조정, edge AI·시스템 관심분야에 가까움 |
| [ ] | Work-in-Progress: Towards Real-time Collaborative 3D Object Detection Systems with Request-free Communication | ★★★★☆ | 요청-응답 없이 통신 효율을 높인 협력 3D 객체 탐지 프레임워크 PORG | Jetson Orin 임베디드 실구현, edge AI 인식 파이프라인에 가까움 |
| [ ] | FLEX: Adaptive Task Batch Scheduling with Elastic Fusion in Multi-Modal Multi-View Machine Perception | ★★★★☆ | GPU 배치 스케줄링으로 멀티모달 멀티뷰 인식 처리량을 최적화하는 FLEX | Jetson Orin GPU 처리량 최적화, edge AI 인식 시스템에 가까움 |
| [ ] | BOXR: Body and head motion Optimization framework for eXtended Reality | ★★★★☆ | C2D 지연 개념을 도입해 XR 바디·헤드 모션 지연을 공동 최적화하는 BOXR | 실기기 다중 플랫폼 스케줄링 최적화, 시스템 구현 중심 |
| [ ] | SCENIC: Capability and Scheduling Co-Design for Intelligent Controller on Heterogeneous Platforms | ★★★☆☆ | 이기종 플랫폼에서 DNN 컨트롤러의 역량과 스케줄링을 공동 설계하는 SCENIC | 이기종 플랫폼 소재이나 역량함수·최적화 이론 정식화가 핵심이라 애매함 |
| [ ] | Response-Time Analysis of a Soft Real-time NVIDIA Holoscan Application | ★★★☆☆ | NVIDIA Holoscan SDK DAG 앱의 종단 응답시간을 정적 분석하는 기법 | NVIDIA SoC 실제 애플리케이션 기반이나 정적 응답시간 분석 이론이 핵심이라 애매함 |
| [ ] | Work-in-Progress: Exploring Limited Preemption Approaches for the Phased Execution Model | ★★★☆☆ | 로컬 메모리 기반 phased 실행 모델의 제한 선점 스케줄링 접근을 평가 | 로컬 메모리 관리 요소가 있으나 선점 임계값 분석 이론이 핵심이라 애매함 |
| [ ] | Partial Context-Sensitive Pointer Integrity for Real-time Embedded Systems | ★★☆☆☆ | 여유 시간을 활용해 Arm PA 기반 포인터 무결성 보호를 강화하는 ParCSPI | CFI/포인터 무결성 중심의 보안 논문이라 관심분야 제외 대상 (Arm PA 하드웨어 + LLVM 컴파일러 구현은 참고할 만함) |
| [ ] | Job-Level Batching for Software-Defined Radio on Multi-Core | ★★☆☆☆ | 샘플 배칭의 한계비용을 반영한 SDR 실시간 스케줄링 모델 확장 | SDR/무선 통신 중심 주제라 관심분야 제외 대상 (GNU Radio 실제 프레임워크 검증은 참고할 만함) |
| [ ] | IDK Cascades for Time-Series Input Streams | ★★☆☆☆ | 유사 입력 시퀀스에 대해 IDK 캐스케이드 응답시간을 줄이는 런타임 알고리즘 | 분류 알고리즘 설계 중심, 시스템/아키텍처 요소 약함 |
| [ ] | Burst-MAC: A MAC Protocol for Handling Burst Traffic in LoRa Network | ★★☆☆☆ | 버스트 트래픽 발생 시 가상 그룹 기반 TDMA로 전환하는 LoRa MAC 프로토콜 | 무선 네트워크 프로토콜 설계 중심, 시스템/아키텍처 요소 약함 |
| [ ] | Performance Optimization and Stability Guarantees for Multi-tier Real-Time Control Systems | ★★☆☆☆ | TSUF 가치함수와 VCS 스케줄링으로 멀티티어 제어 시스템 성능·안정성을 최적화 | 엣지-디바이스 멀티티어 소재이나 제어-스케줄링 이론이 핵심 |
| [ ] | Work-In-Progress: Energy and Thermal-Aware Scheduling based on HMARL for OpenMP DAG Workloads | ★★☆☆☆ | 계층적 다중 에이전트 강화학습으로 코어·주파수를 할당하는 에너지·열 인식 스케줄링 | DVFS 활용은 있으나 RL 기반 스케줄링 정책 설계가 핵심 |
| [ ] | Work-in-Progress: Multi-Deadline DAG Scheduling Model for Autonomous Driving Systems | ★★☆☆☆ | Autoware 종단 타이밍을 서브 DAG 로컬 데드라인으로 분해하는 스케줄링 모델 | ROS 2/Autoware 소재이나 GEDF 확장 스케줄링 모델링 이론이 핵심 |
| [ ] | Work-in-Progress: Analyzing Worst-Case DDoS Traffic Scrub Effect and Recovery Delay via Attack Vector Combination | ★☆☆☆☆ | 공격 벡터 조합을 조합 최적화로 모델링해 최악 트래픽 스크럽 효과를 분석 | 조합 최적화 이론 중심, 시스템/아키텍처 요소 없음 |
| [ ] | Drawing Lines for Measurement-Based Probabilistic Timing Analysis | ★☆☆☆☆ | (n, T(n)) 튜플과 심층신경망을 활용한 새 MBPTA 접근 DBL-MBPTA | 확률론적 타이밍 분석 이론의 전형 |
| [ ] | An Improved Worst-Case Response Time Analysis for AVB Traffic in Time-Sensitive Networks | ★☆☆☆☆ | 기존 WCRTA의 낙관 오류를 수정한 새 AVB 트래픽 응답시간 분석 | 네트워크 응답시간 분석 이론 중심 |
| [ ] | Work-in-Progress: Dynamic Modeling and Real-time Simulation for Performance Analysis of Electric Vehicle Powertrain | ★☆☆☆☆ | MATLAB/CANoe 기반 전기차 파워트레인 통합 모델링 및 실시간 시뮬레이션 | 차량 시뮬레이션 검증 중심, 시스템/아키텍처·edge AI 요소 없음 |
| [ ] | Work-in-Progress: Using Interaction Between Vehicles to Reduce Deadline Tardiness from a Route Assignment Perspective | ★☆☆☆☆ | 차량 상호작용 페널티를 반영한 교통 라우팅 비용함수 확장 | 교통 라우팅 알고리즘 중심, 시스템/아키텍처 요소 없음 |
| [ ] | Energy-Efficient Real-Time Job Mapping and Resource Management in Mobile-Edge Computing | ★☆☆☆☆ | MEC 잡 오프로딩·자원 할당을 근사 알고리즘(LHJS)과 휴리스틱(LBS)으로 최적화 | ILP 근사 알고리즘 이론이 핵심 |
| [ ] | Towards Principled Budget Enforcement in Real-Time Systems | ★☆☆☆☆ | 평균·표준편차만으로 예산 초과 실패율을 상한하는 분석 기법 | 확률론적 예산 집행 분석 이론 중심 |
| [ ] | Mixed-Criticality Federated Scheduling for Relaxed-Deadline DAG Tasks | ★☆☆☆☆ | 완화된 데드라인 DAG MC 태스크의 듀얼 크리티컬리티 페더레이티드 스케줄링 | 용량증폭 상한 증명 등 스케줄링 이론 중심 |
| [ ] | Priority Optimization for Autonomous Driving Systems to Meet End-to-End Latency Constraints | ★☆☆☆☆ | 멀티레이트 DAG의 반응시간 상한과 우선순위 할당 전략을 이론적으로 제시 | 반응시간 분석·우선순위 이론 중심 |
| [ ] | Deadline-Safe Reach-Avoid Control Synthesis for Cyber-Physical Systems with Reinforcement Learning | ★☆☆☆☆ | 데드라인 준수를 위한 R-MDP 정식화와 보상함수 설계로 RL 컨트롤러 합성 | RL 알고리즘·MDP 정식화 이론 중심 |
| [ ] | A Distribution-Agnostic and Correlation-Aware Analysis of Periodic Tasks | ★☆☆☆☆ | 태스크 간 상관관계를 고려한 최초의 분포 무관 확률론적 분석 CAA | 확률론적 타이밍 분석 이론의 전형 |
| [ ] | Work-in-Progress: Response-Time Analysis of Partitioned and Clustered Systems with the Schedule-Abstraction Framework | ★☆☆☆☆ | 스케줄 추상화 프레임워크를 파티션·클러스터 시스템으로 확장하는 분석 | 응답시간 분석 프레임워크 확장 이론 중심 |
| [ ] | Work-in-Progress: Utilizing Probabilistic Analysis to Fine-Tune Optimal IDK Cascades | ★☆☆☆☆ | 확률 분석으로 정적 IDK 캐스케이드를 동적으로 개선해 최대 17% 속도 향상 | 확률적 분석·캐스케이드 알고리즘 이론 중심 |
| [ ] | Subtask-Level Elastic Scheduling | ★☆☆☆☆ | 서브태스크 단위 탄성 상수를 도입한 DAG 탄성 압축 스케줄링 모델 | MIQP·동적 프로그래밍 최적화 이론 중심 |
| [ ] | Optimizing Quantum Assignment for DRR in TSN: A Network Calculus-Based Method | ★☆☆☆☆ | 네트워크 캘큘러스 기반 수치 근사로 DRR 퀀텀 할당을 최적화 | 네트워크 캘큘러스 최적화 이론 중심 |
| [ ] | Response-Time Analysis for Limited-Preemptive Self-Suspending and Event-Driven Delay-Induced Tasks | ★☆☆☆☆ | 제한 선점 EDD 태스크의 전역 멀티코어 최초 응답시간 분석 | 응답시간 분석 이론 중심 |
| [ ] | FRAP: A Flexible Resource Accessing Protocol for Multiprocessor Real-Time Systems | ★☆☆☆☆ | MCMF 기반 블로킹 분석으로 유연한 스핀 우선순위를 지원하는 FRAP 프로토콜 | 블로킹 분석·최적화 이론 중심 |
| [ ] | In Search of Butterflies: Exceedance Analysis for Real-Time Systems under Transient Overload | ★☆☆☆☆ | NET 초과가 응답시간에 미치는 영향을 체계적으로 분석하는 초과 분석 기법 | 응답시간 초과 분석 이론 중심 |
