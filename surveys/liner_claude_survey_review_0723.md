# LINER·Claude 서베이 비판적 검토

- 검토일: 2026-07-23
- 원본 위치: `surveys/source_reports/2026-07-21_liner_claude/`
- 기준 문서: `surveys/realtime_fault_diagnosis_survey_protocol.md`

## 1. 자료 성격과 반영 원칙

새 자료는 fault-diagnosis 후보 16편, elastic-scheduling 후보 8편과 이를 종합한 보고서 4종으로 구성된다. 후보 탐색과 연구 질문 구체화에는 유용하지만, AI가 만든 selection rationale과 종합 문장은 원 논문의 대체물이 아니다.

두 CSV에는 platform과 abstract는 있지만 bare metal, RTOS, 일반 Linux와 PREEMPT_RT를 독립적으로 기록한 열이 없다. Selection rationale에 FreeRTOS 또는 MCU가 언급된 경우도 있으나, MCU 사용만으로 RTOS를 추정하지 않는다. 신규 후보는 원문에서 실행 환경과 정확한 OS/kernel를 다시 추출해야 한다.

반영 수준은 다음과 같이 구분한다.

| 수준 | 사용 가능 범위 |
| --- | --- |
| 원문 PDF와 paper card 확인 완료 | comparison table, claim bank, manuscript 근거로 사용 가능 |
| DOI/URL과 abstract만 확보 | 후보 백로그와 검색 coverage에만 반영 |
| 종합 보고서의 해석 또는 설계 제안 | open question 또는 decision candidate로만 반영 |

이번 입력만으로 신규 paper card를 만들거나 원고 표의 `O/X` 셀을 확정하지 않는다.

## 2. 수집 결과

| 집합 | CSV 행 | 기존 보유·카드화 | 신규 후보 | 현재 판정 |
| --- | ---: | ---: | ---: | --- |
| Real-time/embedded fault diagnosis | 16 | 2 | 14 | 원문 검증 대기 |
| Elastic scheduling | 8 | 3 | 5 | 원문 검증 대기 |

기존 fault-diagnosis 논문은 Thota et al.의 TinyML bearing FD와 Jalonen et al.의 time-varying-speed FD다. 기존 elastic 논문은 Orr et al. 2020, Salman et al. 2021, Sudvarg et al. 2024다.

## 3. 유효한 관찰

다음 내용은 현재 보유 카드와 신규 후보 집합이 같은 방향을 가리키는 **작업 가설**로 받아들일 수 있다.

1. Embedded fault diagnosis에서는 quantization, pruning, lightweight architecture, TinyML과 짧은 inference latency를 real-time 근거로 제시하는 연구가 많이 검색된다.
2. RTOS 이름이 나오더라도 explicit deadline, tail latency, deadline miss와 schedulability analysis가 함께 확인되는 경우는 드물 가능성이 있다.
3. Elastic scheduling의 discrete mode, offline feasibility test와 저비용 online selection은 본 연구의 mode-bank 설계와 비교할 가치가 있다.
4. Fault diagnosis의 domain utility와 real-time scheduling의 feasibility를 연결하는 직접 비교군을 집중적으로 찾아야 한다.

“많다”, “드물다”는 현재 후보 집합에 대한 표현이다. 체계적 검색의 recall과 원문 판정이 끝나기 전에는 문헌 전체의 사실로 단정하지 않는다.

## 4. 강한 주장 검토

| 입력 문서의 주장·결정 | 판정 | 이유와 수정 방향 |
| --- | --- | --- |
| 2021~2026 scheduling 기반 vibration FD는 0편 | 보류 | Zhang 2025가 RTOS 사용 후보이며 검색 coverage도 완결되지 않았다. “현재 검색 후보에서 schedulability까지 확인된 논문은 아직 없음”으로 제한한다. |
| 본 연구가 vibration FD에 scheduling theory를 최초 적용 | 사용 금지 | 최초성은 광범위한 검색과 반례 검토 없이는 방어할 수 없다. |
| 다수 FD 연구가 model-level best-effort에 머문다 | 잠정 지지 | 16편 후보의 rationale은 이를 지지하지만 원문에서 deadline과 timing metric을 확인해야 한다. |
| Orr 2020이 `(W,H,M)`과 정확히 대응한다 | 부분 수용 | Discrete utilization과 period/workload 결합은 구조적 비교군이다. Vibration window, model semantics와 machine trigger까지 같지는 않다. |
| SCHED_FIFO를 선택하고 SCHED_DEADLINE을 배제 | 결정 보류 | 특정 Jetson 또는 framework 결과를 Pi Zero 2W CPU pipeline에 일반화할 수 없다. 두 정책의 feasibility와 overhead를 직접 검토해야 한다. |
| Container를 사용하지 않는다 | 구현 후보 | 1 GB RAM만으로 학술적 배제를 정당화할 수 없다. 연구 질문에 불필요하면 scope 밖으로 두는 실용 결정으로 표현한다. |
| CPU-only가 이론 적용을 더 깔끔하게 만든다 | 구현 후보 | 플랫폼 제약을 줄이는 장점은 있으나 contribution은 아니다. |
| 모든 mode의 offline admission으로 schedulability가 보장된다 | 조건부 | `C` bound, 다른 task의 interference, release/deadline model과 transition carry-over가 유효할 때만 성립한다. |
| Implicit deadline `D=T`로 시작한다 | 설계 후보 | Elastic 문헌의 편의 가정만으로 정할 수 없다. Diagnosis result의 application deadline과 freshness 요구에서 정당화해야 한다. |
| KCC 결과가 3차원 `W/H/M` elasticity 필요성을 입증 | 과장 | 현재 수치는 `W` 증가와 `H/T` 조절 필요성을 보여준다. `M`의 필요성은 별도 profile과 utility 실험이 필요하다. |
| PREEMPT_RT가 hard real-time을 확보한다 | 사용 금지 | PREEMPT_RT 적용이나 observed maximum만으로 hard guarantee가 되지 않는다. |

## 5. Fault-Diagnosis 후보 우선순위

아래 title, date와 rationale은 CSV에서 가져온 후보 metadata다. 원문 확인 전 확정 인용으로 사용하지 않는다.

후보 우선순위는 플랫폼보다 `fault-diagnosis domain`, `W/H/M`, `q/S`, deadline과 guarantee에 얼마나 직접 답하는지로 정한다. 플랫폼은 별도 태그로 기록해 MCU/RTOS와 SoC/Linux의 실행 모델 차이를 비교한다.

| 우선순위 | 후보 | 확인할 핵심 |
| --- | --- | --- |
| 기존 | TinyML Enabled Real-Time Bearing Fault Classification in Motors Using Vibration Signals | 기존 카드의 latency 모순과 RTOS 여부 재검토 |
| 기존 | Real-Time Vibration-Based Bearing Fault Diagnosis Under Time-Varying Speed Conditions | 기존 카드 유지. Offline segment design과 runtime adaptation 구분 |
| P0 | A novel fast short-time root music method for vibration monitoring of high-speed spindles | FreeRTOS task 구성, deadline, period, WCET, schedulability 유무 |
| P0 | Real-Time Fault Diagnosis of Motor Bearing via Improved Cyclostationary Analysis Implemented onto Edge Computing System | MCU/OS, end-to-end timing, deadline과 online pipeline |
| P0 | A Novel Bearing Fault Diagnosis Method based on Stacked Autoencoder and End-edge Collaboration | Dynamic collaboration의 runtime 변수·trigger와 system scheduling 여부 |
| P0 | Embedded TinyML for Predictive Maintenance: Vibration Analysis on ESP32 with Real-Time Fault Detection in Industrial Equipment | Adaptive sampling이 runtime인지, venue와 원문 신뢰성, deadline 유무 |
| P0 | Vibration-Based Predictive Maintenance for Motors Using Edge AI | Raspberry Pi 4 OS/runtime, latency 조건, pipeline과 scheduling |
| S6 bridge | Choudhry et al. 2026 후보 | Raspberry Pi 5 + PREEMPT_RT의 실제 task model, scheduling latency와 DNN E2E 구분 |
| S6 bridge | Liu et al. 2022 후보 | Jetson의 scheduler 비교 조건을 Pi Zero 2W로 일반화할 수 있는지 |
| S6 bridge | Casini et al. 2020 후보 | Linux DNN timing isolation과 framework 내부 scheduling 가정 |
| P1 | Real-Time Bearing Fault Detection and Visualization Using 1D CNN | Simulated deployment, 0.03 s의 통계 범위와 hardware 부재 |
| P1 | Real-Time Fault Detection in Induction Motors Using TinyML | Quantization latency와 accuracy trade-off, RTOS/deadline 유무 |
| P1 | A Dual-Microcontroller IoT-Based Real-Time Monitoring System for Predictive Maintenance of Induction Motors | 402 ms average E2E 구성, 10 Hz 요구와 deadline 정의 |
| P1 | Edge-Oriented Bearing Fault Diagnosis via Triple-Lightweight Network with Adaptive Pruning | Adaptive가 training-time인지 runtime인지 |
| P1 | A Multimodal TinyML-Based Predictive Maintenance Architecture for Industrial IoT in the 6G Era | Inference와 communication E2E 분리, deadline/tail metric |
| P1 | Fast Fault Diagnosis in Industrial Embedded Systems Based on Compressed Sensing and Deep Kernel Extreme Learning Machines | 실제 platform, timing method, real-time 표현의 의미 |
| P2 | An Industrial Internet Application for Real-Time Fault Diagnosis in Industrial Motors | 2020 baseline. 최근 5년 핵심 집합과 분리 |
| P2 | A Physics-Aware Lightweight Transformer Network for Intelligent Bearing Fault Diagnosis | GPU 8.2 ms가 평균인지, static patch와 runtime adaptation 구분 |

P0는 플랫폼과 관계없이 fault diagnosis의 runtime variable, trigger와 guarantee를 직접 확인할 수 있는 후보로 정한다. S6 bridge는 platform/runtime 검증 방법을 제공한다. Zhang 후보가 FreeRTOS를 사용한다는 사실과 scheduling-based diagnosis라는 판정은 별개다.

## 6. Elastic-Scheduling 후보 우선순위

| 상태 | 후보 | 본 연구에서 확인할 항목 |
| --- | --- | --- |
| 기존 | Orr et al. 2020, Discrete Utilizations | Period와 computational workload의 후보 집합, guarantee 조건 |
| 기존 | Salman et al. 2021, Compositional Real-Time Systems | Local period adaptation과 system bandwidth 요청 |
| 기존 | Sudvarg et al. 2024, Harmonic Task Systems | Offline table과 online adaptation complexity |
| P0 | Buttazzo and Abeni 2000, Adaptive Rate Control Through Elastic Scheduling | Measured execution-time feedback가 guarantee와 어떻게 공존하는지 |
| P0 | Wang et al. 2016, Dynamic Multiple-Period Reconfiguration | Safe transition path와 mode-change transient 처리 |
| P0 | Baruah 2023, Constrained-Deadline Elastic Tasks | `D<T`, processor-demand analysis와 period selection |
| P1 | Marinoni and Buttazzo 2007, Elastic DVS Management | Discrete speed와 period mode, WCET 가정 |
| P1 | Burgio et al. 2010, Adaptive TDMA Bus Allocation | Shared-resource adaptation과 centralized coordination 가정 |

## 7. 현재 연구 스코프에 미치는 영향

신규 자료는 스코프를 즉시 `Pi Zero 2W + SCHED_FIFO + W/H/M`으로 확정하는 근거가 아니다. 오히려 다음처럼 범위를 단계적으로 고정해야 한다는 근거다.

1. 직접 비교군 판정: 플랫폼과 무관하게 fault-diagnosis 원문에서 runtime variable, trigger, deadline과 scheduling 유무를 확인한다.
2. 이론 선택: Orr, Buttazzo-Abeni, Wang, Baruah의 task model과 guarantee 조건을 비교한다.
3. 최소 mode: 고정 model에서 `(W,H)`부터 검증하고, `M`은 필요성이 데이터로 확인될 때 추가한다.
4. 플랫폼 정책: SCHED_FIFO와 SCHED_DEADLINE은 문헌 일반화가 아니라 Pi Zero 2W의 task model과 측정 결과로 선택한다.
5. 보장 범위: Static mode feasibility와 transition feasibility를 구분한다.

현재 가장 방어 가능한 연구 질문은 다음이다.

> Vibration fault diagnosis에서 machine condition으로 diagnostic utility를 구분하고 system feasibility로 admissible `(W,H)` mode를 제한할 때, static mode와 transition의 deadline 조건을 어떻게 보장하고 경험적으로 검증할 것인가?

## 8. 다음 반영 순서

1. P0 fault-diagnosis 후보 원문 확보와 판정
2. Buttazzo-Abeni 2000, Wang 2016, Baruah 2023 원문 확보
3. 원문 확인이 끝난 논문만 paper card와 O/X matrix에 추가
4. `SCHED_FIFO`, implicit deadline, CPU-only를 연구 결정으로 확정하기 전 실험·정식화 조건 검토
5. P0 판정 후 novelty 문구와 원고 related-work table 갱신
