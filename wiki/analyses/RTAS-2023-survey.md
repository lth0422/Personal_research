# RTAS 2023 Survey

> Interest areas used for scoring (from interests.md): 시스템 소프트웨어/컴퓨터 구조 관점의 실시간 시스템 연구(OS 커널, 메모리/캐시, 하드웨어-소프트웨어 co-design 등), Edge AI/AI 경량화. 이론·수식 중심의 스케줄링 분석(schedulability 증명, WCRT 유도, 확률론적 타이밍 분석)은 감점. 보안(공격/방어/CFI/TEE/사이드채널 등)은 사실상 제외 대상. 네트워킹(TSN, 무선 프로토콜, network calculus 등)도 관심 거의 없음+배경지식 부족으로 감점.

| Select | Paper Title | Interest | Summary (KR) | Reason |
|---|---|---|---|---|
| [ ] | Hardware Compute Partitioning on NVIDIA GPUs | ★★★★★ | NVIDIA GPU 컴퓨팅 유닛을 투명하게 공간 분할하는 libsmctrl 라이브러리 | GPU 하드웨어 스케줄링 파이프라인 심층 분석, 관심분야 1에 정확히 부합 |
| [ ] | Work In Progress: A New Task Model for Real-Time DNNs over GPU | ★★★★★ | CPU-GPU 아키텍처와 DNN 특성을 함께 고려한 새 태스크 모델 DTM 제안 | GPU 아키텍처 인식 + DNN 실행시간 분석, edge AI·아키텍처 두 관심분야 동시 부합 |
| [ ] | MultiSSE: Static Syscall Elision and Specialization for Event-Triggered Multi-Core RTOS | ★★★★★ | 컴파일 타임 전역 분석으로 멀티코어 RTOS의 시스템콜을 제거·특수화하는 MultiSSE | RTOS 컴파일러/시스템 최적화, 이론보다 정적 분석 도구 구현 중심 |
| [ ] | ROSGM: A Real-Time GPU Management Framework with Plug-In Policies for ROS 2 | ★★★★★ | ROS 2용 플러그인 방식 GPU 자원 관리 프레임워크 ROSGM | GPU 자원 관리 시스템 소프트웨어, 런타임 정책 전환 구현 중심 |
| [ ] | Shedding Light on Static Partitioning Hypervisors for Arm-based Mixed-Criticality Systems | ★★★★★ | Jailhouse, Xen, Bao, seL4 등 정적 파티셔닝 하이퍼바이저를 실증 비교 평가 | 하이퍼바이저 아키텍처 실증 평가, 오픈소스 실제 구현체 비교 중심 |
| [ ] | Work in Progress: Real-time Transformer Inference on Edge AI Accelerators | ★★★★★ | Coral Edge TPU에 Transformer 모델을 배포하는 방법론과 지연·전력 비교 | 엣지 AI 가속기 대상 Transformer 경량화 배포, edge AI 경량화에 정확히 부합 |
| [ ] | ZeroCost-LLC: Shared LLCs at No Cost to WCL | ★★★★★ | 캐시 무효화를 없애 WCL 증가 없이 공유 LLC를 구현하는 ZCLLC | 캐시 계층 아키텍처 설계, 관심분야 1에 정확히 부합 |
| [ ] | MemPol: Policing Core Memory Bandwidth from Outside of the Cores | ★★★★★ | 코어 외부에서 마이크로초 단위로 메모리 대역폭을 규제하는 MemPol | 온칩 디버그 기능 활용 메모리 대역폭 규제, 실보드 실증 중심 |
| [ ] | On the QNX IPC: Assessing Predictability for Local and Distributed Real-Time Systems | ★★★★☆ | QNX OS의 동기 IPC 메커니즘 행동을 실험으로 정형화하고 모델링 | OS IPC 메커니즘 실증 분석이 핵심, 응답시간 분석 이론도 일부 포함 |
| [ ] | G(IP)2C: Temporally Isolated Multiprocessor Real-Time IPC with Server-to-Server Invocations | ★★★★☆ | 서버 간 호출을 지원하며 시간 격리를 보장하는 멀티프로세서 IPC 프로토콜 | 마이크로커널 IPC 프로토콜 설계, LITMUS-RT 프로토타입 구현 중심 |
| [ ] | Work in Progress: Towards a statistical worst-case energy consumption model | ★★★☆☆ | 소프트웨어·하드웨어 이벤트를 반영한 통계적 최악 에너지 소비 모델 프레임워크 | 하드웨어 이벤트 기반 측정 프레임워크이나 통계 모델링이 핵심이라 애매함 |
| [ ] | Timing Analysis and Priority-driven Enhancements of ROS 2 Multi-threaded Executors | ★★★☆☆ | ROS 2 멀티스레드 익스큐터의 타이밍 분석과 우선순위 기반 개선 기법 | ROS 2 시스템 스케줄링 개선이나 응답시간 분석 이론 비중도 커서 애매함 |
| [ ] | Schedulability Analysis of Non-preemptive Sporadic Gang Tasks on Hardware Accelerators | ★★★☆☆ | 멀티 Edge TPU 상에서 비선점 갱 태스크 스케줄가능성을 분석하는 기법 | Edge TPU 가속기 소재라 edge AI에 가까우나 응답시간 분석·지식배낭 문제 이론이 핵심이라 애매함 |
| [ ] | Cache Bank-Aware Denial-of-Service Attacks on Multicore ARM Processors | ★★☆☆☆ | LLC 캐시 뱅크 경합을 이용해 캐시 파티셔닝을 우회하는 DoS 공격 기법 | 보안(DoS 공격) 논문이라 관심분야 제외 대상으로 감점. ARM 실기기 실증이라는 아키텍처적 요소는 남아있어 ★2 |
| [ ] | ISC-FLAT: On the Conflict Between Control Flow Attestation and Real-Time Operations | ★★☆☆☆ | ARM TrustZone-M TEE로 인터럽트 허용 CFA를 구현한 ISC-FLAT | 보안(제어흐름 검증/TEE) 논문이라 관심분야 제외 대상으로 감점. TEE 하드웨어 MCU 프로토타입 구현이라는 아키텍처적 요소는 남아있어 ★2 |
| [ ] | Virtualized DDS Communication for Multi-Domain Systems: Architecture and Performance Evaluation of Design Alternatives | ★★☆☆☆ | Xen 하이퍼바이저 기반 가상화 DDS 통신 아키텍처 설계와 성능 평가 | DDS를 전송 계층으로 쓰는 네트워킹 중심 주제라 관심분야 제외 대상으로 감점. 하이퍼바이저 가상화 아키텍처 요소는 남아있어 ★2 |
| [ ] | Minimizing Probabilistic End-to-end Latencies of Autonomous Driving Systems | ★★☆☆☆ | Autoware 실제 스택 기반 다중 태스크 시퀀스의 확률적 종단 지연 최소화 | 실제 AD 스택 평가가 있으나 스케줄 합성 다목적 최적화 이론이 핵심 |
| [ ] | Scheduling Periodic Segmented Self-Suspending Tasks without Timing Anomalies | ★★☆☆☆ | 세그먼트 자가유예 태스크의 타이밍 이상 현상을 없애는 스케줄링 기법 | RTEMS 구현이 있으나 WCRT 분석 이론이 핵심 |
| [ ] | Work-in-Progress: Securing Safety-Critical Control Tasks with Attack-aware Multi-Rate Scheduling | ★★☆☆☆ | 스케줄 기반 사이드채널 공격을 막는 공격 인식 우선순위 랜덤화 정책 | 보안 관점은 있으나 스케줄링 정책 설계·이론이 핵심 |
| [ ] | A General and Scalable Method for Optimizing Real-Time Systems with Continuous Variables | ★★☆☆☆ | 스케줄가능성을 블랙박스로 취급하는 경사 기반 수치 최적화 프레임워크 NORTH | 범용 최적화 알고리즘·수치해석 이론이 핵심 |
| [ ] | Demo: Simulation and Security Toolbox for Cyber-Physical Systems | ★★☆☆☆ | CPS를 위한 시뮬레이션·보안 툴박스 데모 | 정보가 매우 짧은 데모라 판단 근거 부족, 시스템/아키텍처 요소 약함 |
| [ ] | Work-in-Progress: Deadline-Aware Named Data Networking for Time-Sensitive IoT Applications | ★☆☆☆☆ | 마감시한 기반 우선순위 스케줄러를 적용한 deadline-aware NDN 프로토콜 | 네트워킹 프로토콜 설계 중심, 시스템/아키텍처 요소 없음 |
| [ ] | ATLAS: Aging-Aware Task Replication for Multicore Safety-Critical Systems | ★☆☆☆☆ | 노화 인식 태스크 복제로 신뢰성 목표를 만족시키는 ATLAS 기법 | DBF 기반 신뢰성·스케줄가능성 수식 분석이 핵심 |
| [ ] | Compositional Mixed-Criticality Systems with Multiple Executions and Resource-Budgets Model | ★☆☆☆☆ | 다중 실행 추정·자원예산 공급을 고려한 컴포지셔널 MC 시스템 모델 | DBF 기반 스케줄가능성 테스트 이론이 핵심 |
| [ ] | Precise Response Time Analysis for Multiple DAG Tasks with Intra-task Priority Assignment | ★☆☆☆☆ | 다중 DAG 태스크의 intra/inter-task 간섭을 정밀하게 분석하는 응답시간 기법 | DAG 응답시간 분석 이론이 핵심 |
| [ ] | Work in Progress: Response Time Analysis of Real-Time Quantum Computing Systems | ★☆☆☆☆ | 양자 컴퓨팅 프로그램의 응답시간 분석을 FRP 모델로 시도 | 응답시간 분석 이론을 새 도메인에 적용하는 이론 중심 연구 |
| [ ] | Continuous-Emission Markov Models for Real-Time Applications: Bounding Deadline Miss Probabilities | ★☆☆☆☆ | 연속 방출 분포 Markov 모델로 마감 초과 확률을 상한하는 기법 | 확률론적 타이밍 분석 이론의 전형 |
| [ ] | Work in Progress: Schedulability Analysis of CAN and CAN FD Authentication | ★☆☆☆☆ | CAN/CAN FD 메시지 인증 추가에 따른 응답시간 영향 분석 | 스케줄가능성 실험 분석 이론 중심 |
| [ ] | Average Task Execution Time Minimization under (m, k) Soft Error Constraint | ★☆☆☆☆ | Markov 체인/강화학습 기반 (m,k) 소프트 에러 제약 하 실행시간 최소화 | 확률 모델·강화학습 기반 이론적 스케줄링 정책 설계 |
| [ ] | Real-Time Scheduling of Autonomous Driving System with Guaranteed Timing Correctness | ★☆☆☆☆ | ILP 기반 멀티레이트 DAG 스케줄가능성·종단 지연 공동 분석 프레임워크 | ILP 최적화·스케줄가능성 분석 이론이 핵심 |
| [ ] | Efficient and Accurate Handling of Periodic Flows in Time-Sensitive Networks | ★☆☆☆☆ | 유한 구간 근사로 UPP 곡선 기반 TFA의 계산 불가능성 문제를 해결 | 네트워크 캘큘러스 수학 이론이 핵심 |
| [ ] | Real-Time Performance Analysis of Processing Systems on ROS 2 Executors | ★☆☆☆☆ | ROS 2 DAG 모델의 타이밍 성능을 더 정밀하게 분석하는 기법 | 응답시간 분석 이론이 핵심, 시스템 구현 요소 약함 |
| [ ] | Real-Time Data-Predictive Attack-Recovery for Complex Cyber-Physical Systems | ★☆☆☆☆ | 비선형 시스템 대상 데이터 예측 기반 공격 복구 프레임워크 | 비선형 제어 이론·수학적 보장 증명이 핵심 |
