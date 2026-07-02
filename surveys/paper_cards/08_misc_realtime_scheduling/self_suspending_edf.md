# Requirement-Based Analysis of Self-Suspending Tasks under EDF

- **그룹**: 8 misc_realtime_scheduling
- **출처/연도**: RTSS 2025
- **저자**: 확인 필요

## 두 질문
- **가변 변수**: analysis interval extension, suspension accounting.
- **트리거**: self-suspension behavior, infeasibility requirement validation.

## 요점
- 플랫폼: analysis paper. Specific embedded platform 중심 아님.
- 도메인: EDF schedulability analysis for dynamic self-suspending tasks.
- 핵심 방법: self-suspending task가 EDF에서 deadline miss를 만들기 위한 workload requirement를 formalize하고, requirement validation이 어려운 경우 dynamic interval extension procedure를 적용한다.
- 정식화/수식: requirement-based infeasibility analysis and dynamic interval extension.

## 내 연구 관점
- 한 줄 gap: schedulability analysis 이론이며 vibration FD inference adaptation과 PREEMPT_RT 실측은 다루지 않는다.
- 내 연구에 쓸 곳: sensing/I/O wait 또는 offloading이 self-suspension처럼 보일 때 배경으로 제한적 참고 가능.
- 인용할 문장: "self-suspending tasks"

## 불확실한 점
- 확인 필요: 첫 페이지 텍스트 추출에서 저자명이 깨져 확인되지 않았다. PDF 원본 첫 페이지를 직접 확인해야 한다.
- 확인 필요: RTSS 2025 문헌이므로 manuscript 인용 전 bibliographic status와 full author list를 확인해야 한다.
