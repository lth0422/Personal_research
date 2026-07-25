# Brief Industry Paper: STM-A Static Non-Preemptive Scheduler for NVIDIA Tegra SoCs

> NVIDIA Tegra SoC의 여러 하드웨어 엔진을 관리하는 정적 비선점 스케줄러 STM을 제안하고, 실제 자율주행차 200대·72,000km 주행 데이터로 검증

- **Conference**: RTAS 2025
- **Tags**: #rtos-kernel #resource-management #autonomous-driving

## Abstract
This paper introduces System Task Manager (STM), a static, centrally monitored, OS-agnostic, non-preemptive scheduler that manages work across hardware engines on NVIDIA Tegra System-on-Chips (SoCs). We detail the design of STM and how the various components enable it to achieve high throughput while providing timing guarantees. We demonstrate a real-world application in the domain of autonomous vehicles. This includes results from deployment to a fleet of over 200 cars with 72 000 km of cumulative driving. We conclude by discussing various future research directions for this project.

이 논문은 NVIDIA Tegra SoC의 다양한 하드웨어 엔진 작업을 관리하는 정적·중앙집중형·OS-비의존적 비선점 스케줄러 STM(System Task Manager)을 소개한다. STM의 설계와, 각 구성 요소가 높은 처리량과 동시에 타이밍 보장을 어떻게 달성하는지 상세히 설명한다. 자율주행차 도메인에서의 실제 적용 사례를 보이며, 200대 이상의 차량 플릿에 배포되어 누적 72,000km 주행한 결과를 포함한다. 마지막으로 이 프로젝트의 향후 연구 방향을 논의한다.

## Key Takeaways
- 어떤 문제를 해결하는가: SoC 내 이기종 하드웨어 엔진(카메라, GPU, 가속기 등) 간 작업을 OS에 의존하지 않고 타이밍 보장하며 스케줄링하는 문제
- 어떤 방법을 사용하는가: 정적·비선점·중앙 모니터링 방식의 SoC 레벨 태스크 매니저(STM) 설계
- 주요 결과/기여: 실제 자율주행 차량 200대, 72,000km 누적 주행 데이터로 실증한 산업 사례 (Brief Industry Paper)

## Related
- [[rtos-kernel]]
- [[resource-management]]
- [[autonomous-driving]]

## Source
- DOI: [10.1109/RTAS65571.2025.00014](https://doi.org/10.1109/RTAS65571.2025.00014)

## My Notes
<!-- This section is written only by the user. The LLM must never edit or delete this section. -->
- **Status**: Unread
- **Interest**: /10
- **Notes**: 
