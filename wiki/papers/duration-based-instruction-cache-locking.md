# Duration-based Instruction Cache Locking

> LRU age bit를 활용해 코드 수정 없이 캐시 라인을 시간 단위로 동적 락킹하는 하드웨어 명령어 캐시 메커니즘

- **Conference**: RTCSA 2024
- **Tags**: #memory-management

## Abstract
Cache locking is a commonly used mechanism to improve both performance and predictability for embedded programs. Dynamic cache locking methods proposed in the literature, where the locked content is modified during execution, require inserting locking and unlocking instructions in the program's code. In this paper, we introduce a novel hardware mechanism that leverages the LRU age bits to perform duration-based locking. Our proposed mechanism dynamically locks and unlocks cache lines for different durations at run-time, without the need to modify the program's code. We further devise a heuristic that analyzes a program's loop structure and selects the set of addresses to be locked in a L1 instruction cache alongside their locking durations. Evaluation results show that our duration-based locking mechanism achieves comparable results to the dynamic approach while substantially reducing the initialization overhead and avoiding program code modifications.

캐시 락킹은 임베디드 프로그램의 성능과 예측성을 동시에 개선하기 위해 흔히 쓰이는 기법이다. 기존에 제안된 동적 캐시 락킹 기법은 실행 중 락킹 대상을 변경하기 위해 프로그램 코드에 락킹·언락킹 명령어를 삽입해야 했다. 이 논문은 LRU age bit를 활용해 시간 기반(duration-based) 락킹을 수행하는 새로운 하드웨어 메커니즘을 제안한다. 제안 메커니즘은 프로그램 코드 수정 없이 런타임에 캐시 라인을 서로 다른 지속 시간 동안 동적으로 락/언락한다. 또한 프로그램의 루프 구조를 분석해 L1 명령어 캐시에 락킹할 주소 집합과 락킹 지속 시간을 선정하는 휴리스틱을 고안했다. 평가 결과, 이 시간 기반 락킹 메커니즘은 기존 동적 기법과 비슷한 성능을 내면서도 초기화 오버헤드를 크게 줄이고 프로그램 코드 수정을 피할 수 있었다.

## Key Takeaways
- 어떤 문제를 해결하는가: 기존 동적 캐시 락킹이 요구하는 코드 수정과 초기화 오버헤드 문제
- 어떤 방법을 사용하는가: LRU age bit 기반 시간 단위(duration-based) 하드웨어 캐시 락킹 메커니즘과 루프 구조 분석 휴리스틱
- 주요 결과/기여: 코드 수정 없이 기존 동적 락킹과 동등한 성능, 초기화 오버헤드 대폭 감소

## Related
- [[memory-management]]

## Source
- DOI: [10.1109/RTCSA62462.2024.00021](https://doi.org/10.1109/RTCSA62462.2024.00021)

## My Notes
<!-- This section is written only by the user. The LLM must never edit or delete this section. -->
- **Status**: Unread
- **Interest**: /10
- **Notes**: 
