# ParRP: Enabling Space Isolation in Caches with Shared Data

> 캐시 교체 정보(replacement info)를 파티셔닝해 공유 데이터에 대해서도 캐시 공간 격리를 지원하는 하드웨어 기법 ParRP

- **Conference**: RTAS 2025
- **Tags**: #memory-management

## Abstract
This work presents an approach to isolate cache space while supporting shared data. Enabling shared data caching is challenging because it causes interference making it unsuitable for real-time multicores. Unlike prior works, we aim to introduce isolation, but our approach enables caching of shared data, and promotes isolated cache analysis for individual cores. The crux behind our approach is that shared data isolation can be achieved by partitioning the replacement information instead of the cache's data storage. Consequently, this work introduces ParRP, a novel hardware cache partitioning scheme for realtime cache-coherent multicores. Our evaluation using the gem5 simulator shows that, by providing isolation for shared data, the worst-case execution time of multi-threaded tasks can be lower by 2.4× at the cost of a 16.5% decrease in average-case performance.

이 연구는 공유 데이터 캐싱을 지원하면서도 캐시 공간을 격리하는 방법을 제시한다. 공유 데이터 캐싱은 간섭을 유발해 실시간 멀티코어에 부적합하다는 문제가 있었다. 기존 연구와 달리, 이 연구는 격리를 도입하면서도 공유 데이터 캐싱을 가능하게 하고 코어별 격리된 캐시 분석을 지원한다. 핵심 아이디어는 캐시의 데이터 저장소가 아니라 교체 정보(replacement information)를 파티셔닝함으로써 공유 데이터 격리를 달성할 수 있다는 것이다. 이를 바탕으로 실시간 캐시-일관성 멀티코어를 위한 새로운 하드웨어 캐시 파티셔닝 기법 ParRP를 제안한다. gem5 시뮬레이터 평가 결과, 공유 데이터 격리를 제공함으로써 멀티스레드 태스크의 최악 실행 시간을 2.4배 낮출 수 있었으며, 대신 평균 성능은 16.5% 감소했다.

## Key Takeaways
- 어떤 문제를 해결하는가: 공유 데이터를 캐싱하면서도 코어 간 캐시 간섭 없이 격리를 보장하는 문제
- 어떤 방법을 사용하는가: 캐시 데이터가 아닌 교체 정보(replacement info)를 파티셔닝하는 하드웨어 캐시 기법 ParRP
- 주요 결과/기여: gem5 시뮬레이션으로 WCET 2.4배 감소(평균 성능 16.5% 저하 대가) 검증

## Related
- [[memory-management]]

## Source
- DOI: [10.1109/RTAS65571.2025.00020](https://doi.org/10.1109/RTAS65571.2025.00020)

## My Notes
<!-- This section is written only by the user. The LLM must never edit or delete this section. -->
- **Status**: Unread
- **Interest**: /10
- **Notes**: 
