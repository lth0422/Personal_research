# TSI: A Time-Semantic Instruction Set for Deterministic Data-Flow Execution in Real-Time Embedded Systems

> 주소와 타임스탬프 기반 메모리 접근을 지원하는 새 RISC-V 확장 명령어셋 TSI로, 명령어 순서 강제 없이 데이터플로우 결정성을 확보

- **Conference**: RTSS 2025
- **Tags**: #rtos-kernel

## Abstract
Real-Time Embedded Systems (RTES) are widely used in safety-critical devices, where deterministic data flow is essential to system verification and reliable execution. It requires that each consumer task instance reads data from the deterministic producer task instance. In software based on general-purpose computing instruction sets, communication-related instruction execution order couples data flow among tasks, necessitating a deterministic execution order of these instructions to preserve data-flow determinism. However, enforcing this order complicates software, and suffers from priority inversion and variable execution overheads, which significantly increases task worst-case response times (WCRT) and response time variability. This paper identifies the cause of above issues as the semantics of general-purpose instruction sets, under which data-flow determinism relies on the deterministic execution order of communication-related instructions. To address this, we make the following contributions. First, we propose Time-Semantic Instruction set (TSI), which supports memory access using both addresses and timestamps. TSI enables data-flow determinism without strict instruction ordering. Second, we design a TSI-enabled implementation compatible with conventional memory systems. Third, we provide two TSI-based deterministic data-flow programming paradigms, along with correctness proofs. Finally, we evaluate TSI hardware cost and implement a cycle-accurate simulator based on a TSI-extended RISC-V. Experiments demonstrate that, under reasonable memory overhead, our approach reduces programming complexity and achieves up to 21.6× reduction in WCRT and up to 89.6× reduction in response time variability compared to existing methods.

실시간 임베디드 시스템(RTES)은 안전critical 기기에 널리 쓰이며, 여기서 결정론적 데이터플로우는 시스템 검증과 신뢰성 있는 실행에 필수적이다. 이는 각 소비자 태스크 인스턴스가 결정론적 생산자 태스크 인스턴스로부터 데이터를 읽어야 함을 요구한다. 범용 컴퓨팅 명령어셋 기반 소프트웨어에서는 통신 관련 명령어의 실행 순서가 태스크 간 데이터플로우를 결합시켜, 데이터플로우 결정성을 유지하려면 이런 명령어들의 결정론적 실행 순서가 필요하다. 그러나 이 순서를 강제하면 소프트웨어가 복잡해지고 우선순위 역전과 가변 실행 오버헤드가 발생해 태스크 최악 응답시간(WCRT)과 응답시간 가변성이 크게 늘어난다. 이 논문은 이런 문제의 원인이 범용 명령어셋의 시맨틱스, 즉 데이터플로우 결정성이 통신 관련 명령어의 결정론적 실행 순서에 의존한다는 점에 있음을 규명한다. 이를 해결하기 위해, 첫째로 주소와 타임스탬프 모두를 이용한 메모리 접근을 지원하는 시간-시맨틱 명령어셋(TSI)을 제안한다. TSI는 엄격한 명령어 순서 없이도 데이터플로우 결정성을 가능하게 한다. 둘째로 기존 메모리 시스템과 호환되는 TSI 지원 구현을 설계한다. 셋째로 정확성 증명과 함께 TSI 기반 결정론적 데이터플로우 프로그래밍 패러다임 두 가지를 제공한다. 마지막으로 TSI의 하드웨어 비용을 평가하고 TSI 확장 RISC-V 기반의 사이클-정확 시뮬레이터를 구현한다. 실험 결과, 합리적인 메모리 오버헤드 하에서 이 접근법은 프로그래밍 복잡도를 줄이고 기존 방법 대비 WCRT를 최대 21.6배, 응답시간 가변성을 최대 89.6배 줄인다.

## Key Takeaways
- 어떤 문제를 해결하는가: 범용 명령어셋에서 통신 명령어의 결정론적 실행 순서 강제로 인한 WCRT 및 응답시간 가변성 증가 문제
- 어떤 방법을 사용하는가: 주소+타임스탬프 기반 메모리 접근을 지원하는 RISC-V 확장 명령어셋 TSI, 이를 활용한 결정론적 데이터플로우 프로그래밍 패러다임
- 주요 결과/기여: 기존 방법 대비 WCRT 최대 21.6배, 응답시간 가변성 최대 89.6배 감소

## Related
- [[rtos-kernel]]

## Source
- DOI: [10.1109/RTSS66672.2025.00048](https://doi.org/10.1109/RTSS66672.2025.00048)

## My Notes
<!-- This section is written only by the user. The LLM must never edit or delete this section. -->
- **Status**: Unread
- **Interest**: /10
- **Notes**: 
