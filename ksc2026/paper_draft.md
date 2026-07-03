# KSC 2026 논문 초안

> **이 파일의 목적**: KSC 2026 단기 논문 전용 작업 공간.
> `manuscript/`는 학위논문(RTAS/RTCSA, 중장기) 전용이며 이 논문과 분리한다.
> 실험 데이터는 `experiments/`에서 공유, 논문 초안은 이 폴더에 작성한다.

---

## 제출 목표

- 학회: 한국소프트웨어종합학술대회 (KSC 2026)
- 제출 목표: 2026년 9월
- 분량: 4~6페이지

---

## 한 줄 주장

> Pi Zero 2W에서 다중 태스크 기반 실시간 결함 진단 파이프라인을 구동할 때,
> 부하 조건에 따라 PREEMPT_RT 커널이 deadline miss 억제에 실질적으로 필요한 조건을 정량적으로 보인다.

---

## KCC 2026 → KSC 2026 연결

KCC 2026에서 확인한 것:
- STM32F407 + Zephyr RTOS (MCU, 하드웨어 RT 보장)
- W=512, 40.3ms, deadline 64ms 만족, 정확도 99.30%
- 핵심 발견: window 축소 시 latency가 superlinear 감소 (DWConv O(W²))

KSC 2026에서 다루는 것:
- Pi Zero 2W + Raspberry Pi OS Lite (SBC, 소프트웨어 RT)
- MCU에서 SBC로 올라올 때 OS 선택(vanilla vs PREEMPT_RT)이 실시간성에 미치는 영향
- "PREEMPT_RT 없이도 되는가?" 질문에 부하 조건별로 답함

논문에서의 위치:
- KCC 결과 = motivation / 배경
- KSC 결과 = 새 기여 (SBC 플랫폼 실시간성 분석)
- KSC 결과 → 학위논문(W/H/M elastic scheduling) 예비 실험으로 연결

---

## Novelty 요약

| 항목 | 내용 |
| --- | --- |
| 플랫폼 | Pi Zero 2W (512MB, 1GHz, Cortex-A53) — 이 플랫폼에서 결함 진단 RT 분석은 선례 드묾 |
| 실험 구성 | 실제 진동 센서 + 다중 태스크 파이프라인 (sensor / inference / logger) |
| 비교 | vanilla Linux vs PREEMPT_RT, 부하 5종 (idle / CPU / mem / IO / combined) |
| 기여 | "어느 부하 조건부터 PREEMPT_RT가 필요한가"를 deadline miss rate로 정량화 |
| 연결 | KCC(MCU)→KSC(SBC) 플랫폼 전환 시 RT 요구사항 분석 |

---

## 논문 구조 (안)

```
1. 서론
   - 엣지 결함 진단의 플랫폼 선택 문제
   - MCU(Zephyr RT 보장) vs SBC(OS RT 선택 필요)
   - PREEMPT_RT가 실제 필요한가? → 본 논문의 질문

2. 배경
   2.1 KCC 2026 결과 요약 (STM32F407 + Zephyr, motivation)
   2.2 Pi Zero 2W 플랫폼 특성
   2.3 vanilla Linux vs PREEMPT_RT 개요

3. 실험 설계
   3.1 파이프라인 구조 (sensor → inference → logger, 다중 태스크)
   3.2 실험 조건 (2 커널 × 5 부하)
   3.3 측정 지표 (jitter, inference latency, E2E latency, deadline miss)

4. 실험 결과
   4.1 커널 latency 기초 검증 (cyclictest 비교)
   4.2 파이프라인 latency 분포 (부하별 박스플롯)
   4.3 deadline miss 발생 조건 분석

5. 결론 및 향후 연구
   - PREEMPT_RT가 필요한 최소 부하 조건 정리
   - W/H/M elastic scheduling(학위논문)으로의 연결
```

---

## 핵심 Figure/Table 계획

| 번호 | 유형 | 내용 |
| --- | --- | --- |
| Fig. 1 | 시스템 구성도 | 파이프라인 구조 + 측정 포인트 |
| Fig. 2 | CDF / 히스토그램 | cyclictest vanilla vs RT (idle, combined) |
| Fig. 3 | 박스플롯 | E2E latency, 부하 5종 × 2 커널 |
| Table 1 | 비교표 | deadline miss rate (%) 전체 조건 정리 |
| Table 2 | 실험 환경 | 플랫폼 스펙, 소프트웨어 버전 |

---

## 현재 상태 (2026-07-03)

### 완료
- [x] PREEMPT_RT 패치 적용
- [x] cyclictest idle 조건 RT 검증 (Max: 29/46/23/42 μs — 정상)

### 진행 중 / 예정
- [ ] 부하 5종 × cyclictest RT 측정
- [ ] vanilla Linux SD카드 준비 (비교군 필요)
- [ ] 센서 연결 및 TFLite 설치
- [ ] 파이프라인 코드 작성 (Claude Code 담당 → `experiments/pipeline/`)
- [ ] 실험 30 run (2 커널 × 5 부하 × 3 반복)
- [ ] 분석 스크립트 작성
- [ ] 논문 초안 작성

---

## 미결 질문

- vanilla Linux 비교를 위해 SD카드 두 장 방식 사용할지 확인 필요
- 실제 진동 센서 종류 확정 필요 (ADC 방식에 따라 파이프라인 달라짐)
- deadline D 값을 KCC 기준 64ms로 유지할지 Pi 환경에 맞게 조정할지 결정 필요
