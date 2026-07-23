# Real-Time Fault Diagnosis 체계적 서베이 프로토콜

- 작성일: 2026-07-21
- 최근 검색 입력 검토: 2026-07-23
- 근거: `decisions/personal_research_summary_0708.md`
- 목적: “real-time”이라는 표현을 모델 경량화, 경험적 시간 충족, deadline-aware execution, schedulability guarantee로 분리하고, fault diagnosis를 scheduling 문제로 다룬 선행연구가 실제로 드문지 검증한다.

## 1. 이 서베이의 질문

| ID | 질문 | 답 형식 |
| --- | --- | --- |
| RQ1 | 실제 장치에서 fault diagnosis를 수행하는가? | O/△/X/? + 플랫폼 |
| RQ2 | 실행 환경이 bare metal, RTOS, 일반 Linux, PREEMPT_RT 중 무엇인가? | 환경 종류 + OS/kernel 이름과 version |
| RQ3 | deadline 또는 task period를 명시하는가? | O/△/X/? + 수치/정의 |
| RQ4 | real-time을 무엇으로 달성하는가? | 모델 경량화 / 시스템 최적화 / scheduling / 혼합 |
| RQ5 | latency를 average만 측정하는가, tail/jitter/miss까지 측정하는가? | 측정 지표 목록 |
| RQ6 | hard 또는 weakly-hard guarantee가 있는가? | H/W/E/B/? 등급 + 근거 |
| RQ7 | runtime에 window, period, model을 조절하는가? 무엇이 trigger인가? | `W/H/M`, `q/S/load/deadline/offline` |

RQ6과 RQ7이 교수님 피드백의 핵심이다. RTOS 사용 여부나 짧은 평균 latency만으로 hard real-time이라고 판정하지 않는다.

### 플랫폼 태그

문헌의 주 섹션과 우선순위는 연구 질문으로 정하고, 플랫폼은 별도 태그로 기록한다. MCU/RTOS는 KCC 선행 결과와 deterministic execution을, SoC/SBC/Linux는 현재 Pi Zero 2W 실험과 OS interference를 설명한다. 어느 한 플랫폼만을 조사 대상으로 제한하지 않는다.

| 태그 | 예시 | 주로 제공하는 근거 |
| --- | --- | --- |
| `PL-MCU` | STM32, ESP32, Cortex-M | Task 구조와 resource constraint |
| `PL-SBC-SOC` | Raspberry Pi, ARM Cortex-A SBC | OS scheduling, interference, tail latency |
| `PL-HET-SOC` | Jetson 등 CPU/GPU SoC | Heterogeneous runtime과 resource contention |
| `PL-SERVER-GPU` | x86와 discrete GPU | DNN scheduling mechanism |
| `PL-DESKTOP` | Desktop/laptop evaluation | Algorithm timing 참고 |

실행환경은 `ENV-BAREMETAL`, `ENV-RTOS`, `ENV-LINUX`, `ENV-PREEMPT_RT`, `ENV-OTHER`로 별도 기록한다. 세부 분류는 `surveys/research_aligned_literature_taxonomy_0723.md`를 따른다.

## 2. 조사 범위

### 기간

- 핵심 검색 범위: 2021년 1월부터 2026년 7월까지
- 예외: 현재 논문의 개념적 기반이 되는 고전 scheduling 또는 mode-change 논문

### 문헌 집합

| 집합 | 포함 대상 | 용도 |
| --- | --- | --- |
| A. Direct RT-FD | vibration/machine fault diagnosis와 deadline, RTOS 또는 scheduling을 함께 다룸 | 본 연구의 직접 비교군 |
| B. Embedded best-effort FD | TinyML, quantization, pruning, NAS, lightweight model로 on-device latency를 줄임 | 교수님이 예상한 주류 접근을 검증하는 대조군 |
| C. Scheduling bridge | fault diagnosis는 아니지만 input/model/period를 deadline 또는 slack으로 조절 | 방법론 비교군. Direct RT-FD 수에 포함하지 않음 |

세 집합을 섞어 “관련 논문이 많다” 또는 “없다”고 세지 않는다. 특히 vision DNN scheduling 논문은 C 집합이지 fault-diagnosis scheduling의 직접 증거가 아니다.

### 포함 기준

1. Bearing, rotating machinery, motor, gearbox 또는 vibration-based condition monitoring을 다룬다.
2. 논문이 real-time, embedded, edge, on-device 또는 timing requirement를 명시한다.
3. 원문에서 플랫폼, 실행시간 또는 scheduling 방법 중 하나 이상을 확인할 수 있다.
4. 리뷰가 아닌 primary research paper다. 리뷰는 backward/forward snowballing에만 사용한다.

### 제외 기준

1. Offline accuracy만 보고하고 deployment 또는 timing 평가가 없다.
2. Fault diagnosis가 아니라 일반 IoT monitoring만 다룬다.
3. 초록만 접근 가능하여 핵심 판정을 검증할 수 없다. 이 경우 제외하지 않고 `후보/원문 필요`로 분리한다.
4. 같은 연구의 preprint와 출판본이 중복되면 출판본을 대표로 두고 중복 관계를 기록한다.

## 3. 검색 전략

모든 조건을 하나의 긴 AND 검색식에 넣으면 scheduling 논문을 놓칠 수 있다. 아래 query family를 별도로 실행하고 결과를 합친 뒤 DOI와 제목으로 중복을 제거한다.

### Q1. Real-time 표현을 쓰는 fault diagnosis

```text
("real-time" OR "real time" OR deadline OR latency OR jitter OR schedulability)
AND ("fault diagnosis" OR "fault detection" OR "condition monitoring")
AND (vibration OR bearing OR motor OR gearbox OR "rotating machinery")
```

### Q2. RTOS와 real-time Linux

```text
(RTOS OR "real-time operating system" OR Zephyr OR FreeRTOS OR ThreadX
 OR "PREEMPT_RT" OR "SCHED_FIFO" OR "SCHED_DEADLINE")
AND ("fault diagnosis" OR "condition monitoring")
AND (vibration OR bearing OR motor OR "rotating machinery")
```

### Q2-SOC. Application-class SoC/SBC 직접 비교군

```text
("embedded Linux" OR "real-time Linux" OR PREEMPT_RT OR Raspberry Pi
 OR Jetson OR "single-board computer" OR SBC OR "ARM Cortex-A" OR "edge SoC")
AND ("fault diagnosis" OR "fault detection" OR "condition monitoring")
AND (vibration OR bearing OR motor OR gearbox OR "rotating machinery")
AND (deadline OR latency OR jitter OR scheduling OR "real-time")
```

### Q3. Scheduling으로 접근한 fault diagnosis

```text
(scheduling OR schedulability OR "task period" OR "sampling period"
 OR "runtime adaptation" OR "mode change" OR elastic OR "admission control")
AND ("fault diagnosis" OR "fault detection" OR "condition monitoring")
AND (embedded OR edge OR vibration OR bearing OR machinery)
```

### Q4. 경량화 중심 대조군

```text
(TinyML OR quantization OR pruning OR "lightweight neural network"
 OR "architecture search" OR NAS OR compression)
AND ("fault diagnosis" OR "condition monitoring")
AND (latency OR "real-time" OR embedded OR edge OR microcontroller)
```

### Q5. 본 연구 변수와 가까운 문헌

```text
("window size" OR "input length" OR "hop size" OR "model selection"
 OR "adaptive sampling")
AND ("fault diagnosis" OR "condition monitoring")
AND (deadline OR scheduling OR runtime OR adaptive)
```

권장 검색원은 IEEE Xplore, ACM Digital Library, Scopus 또는 Web of Science다. Google Scholar와 Semantic Scholar는 누락 논문 탐색과 인용 추적에 사용하되, 최종 서지정보와 본문 판정은 출판본 원문에서 확인한다.

### 2026-07-21 LINER 검색 입력

- 원본: `surveys/source_reports/2026-07-21_liner_claude/`
- 검색원 표기: Semantic Scholar
- Fault-diagnosis CSV: 16편. 기존 카드 2편, 신규 후보 14편
- Elastic-scheduling CSV: 8편. 기존 카드 3편, 신규 후보 5편
- 비판 검토: `surveys/liner_claude_survey_review_0723.md`

CSV의 abstract와 selection rationale은 후보 선별 자료다. 신규 후보의 original full text가 없으므로 O/△/X/? matrix, paper card와 manuscript 근거에는 아직 반영하지 않는다.

## 4. 기호와 판정 규칙

### 기능 기호

| 기호 | 의미 | 사용 조건 |
| --- | --- | --- |
| O | 확인됨 | 원문 method/result에서 명시적 근거를 확인함 |
| △ | 부분 충족 또는 proxy | acquisition time 대비 processing time처럼 직접 deadline은 아니지만 시간 예산을 사용함 |
| X | 해당 없음 | 고정 offline 설계이거나 원문 구성상 해당 기능이 없음을 확인함 |
| ? | 확인 불가 | 초록/카드만으로 판단할 수 없거나 원문 근거가 모호함 |
| P | 본 연구의 계획 | 아직 구현 또는 검증되지 않은 proposed feature |

`?`를 억지로 `X`로 바꾸지 않는다. `P`도 실험이 끝나기 전에는 `O`로 바꾸지 않는다.

### 실시간성 등급

| 등급 | 이름 | 최소 판정 기준 |
| --- | --- | --- |
| H | hard/firm guarantee | 명시적 deadline, 보수적 execution-time bound, schedulability/admission 분석, 관련 mode와 transition의 deadline 보장 |
| W | weakly-hard guarantee | `(m,K)` 또는 이에 준하는 bounded miss constraint와 검증/분석 |
| E | empirical deadline-aware | deadline이 명시되고 miss, tail, jitter 또는 max를 실험하지만 formal guarantee는 없음 |
| B | best-effort 또는 throughput real-time | 평균 latency, throughput, acquisition interval 대비 처리시간 또는 모델 크기만 보고 |
| ? | 판정 보류 | deadline 정의나 원문 근거가 불충분 |

RTOS 사용은 H 판정의 충분조건이 아니다. 반대로 범용 OS를 사용하더라도 execution bound와 schedulability가 입증되면 H 후보가 될 수 있다.

## 5. 원문에서 추출할 데이터

각 셀은 가능하면 `section/page/table/figure` 근거를 함께 저장한다.

| 필드 | 기록 내용 |
| --- | --- |
| Citation | title, authors, venue, year, DOI |
| Domain | bearing/motor/gearbox/shaft, vibration 여부 |
| Platform | MCU/SBC/CPU/GPU, board와 processor |
| Platform tag | `PL-MCU` / `PL-SBC-SOC` / `PL-HET-SOC` / `PL-SERVER-GPU` / `PL-DESKTOP` |
| Execution environment | bare metal / RTOS / general Linux / PREEMPT_RT / other |
| OS/kernel | 정확한 이름, version, kernel configuration |
| Task model | periodic/sporadic/pipeline, period, priority, scheduler |
| Deadline | 정의, 값, implicit/constrained 여부 |
| Timing evidence | average, p95, p99, max, jitter, miss rate, WCET |
| Model optimization | quantization, pruning, NAS, lightweight architecture, fixed model |
| System intervention | RTOS task화, priority, affinity, admission, period control, resource allocation |
| Runtime adaptation | `W/H/M` 중 무엇을 언제 바꾸는가 |
| Trigger | machine condition `q`, slack `S`, load, confidence, deadline, offline |
| Guarantee | utilization/RTA/DBF/admission/weakly-hard/empirical/없음 |
| RT grade | H/W/E/B/? |
| Evidence | 해당 판정의 짧은 근거와 page/section |
| Uncertainty | 원문에서 확인하지 못한 항목 |

## 6. 현재 보유 논문의 예비 판정

아래 표는 현재 paper card에서 확인한 범위의 초안이다. 최종 원고 표에 넣기 전 GAP-01 재검토를 거쳐야 한다.

| 논문 | 플랫폼 | 실행 환경 | RTOS | PREEMPT_RT | Deadline | Tail/jitter/miss | Sched. 분석 | 모델 경량화 | 시스템 scheduling | Runtime 적응 | `W/H/M` 공동 | `q+S` | RT 등급 |
| --- | --- | --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Ma et al., Lightweight Architecture Search FD | `PL-DESKTOP` | `ENV-OTHER` | X | X | X | X | X | O | X | X | X | X | B |
| Lee and Kim, FRFconv-TDSNet | `PL-SBC-SOC` | Linux 계열 확인 필요 | X | X | X | X | X | O | X | X | X | X | B |
| Jalonen et al., Time-Varying Speed FD | `PL-DESKTOP` | `ENV-OTHER` | X | X | X | X | X | O | X | X | X | X | B |
| Thota et al., TinyML Bearing FD | `PL-MCU` | MCU runtime 확인 필요 | ? | X | X | ? | X | O | X | X | X | X | B |
| Choi et al., Low-Cost MCU Shaft FD | `PL-MCU` | `ENV-BAREMETAL` | X | X | X | X | X | O | X | X | X | X | B |
| 본 연구 KCC 2026 | `PL-MCU` | Zephyr `ENV-RTOS` | O | X | O | O | △ | O | O | X | X | X | E |
| 제안 연구 | `PL-SBC-SOC` | Linux + `ENV-PREEMPT_RT` | X | P | P | P | P | - | P | P | P | P | 목표 H 또는 조건부 H |

해석할 때 `모델 경량화 O`는 real-time guarantee가 강하다는 뜻이 아니다. 현재 대조군은 대부분 모델을 가볍게 만들고 latency를 측정하지만, scheduling과 deadline guarantee는 확인되지 않는다는 가설을 보여준다. 이 가설은 추가 문헌으로 검증해야 한다.

## 7. 논문별 주관식 판정 양식

```md
### {Paper ID}: {Title}

- 포함 집합: A Direct RT-FD / B Embedded best-effort FD / C Scheduling bridge
- Real-time이라는 용어의 의미:
- 실행 환경: bare metal / RTOS / general Linux / PREEMPT_RT / other
- 정확한 OS/kernel와 task 구성:
- Deadline 정의:
- 모델을 가볍게 만든 방법:
- 시스템 또는 scheduling을 바꾼 방법:
- 측정 지표와 통계 범위:
- Schedulability 또는 deadline 보장 방법:
- Runtime 가변 변수:
- Adaptation trigger:
- RT 등급: H / W / E / B / ?
- 판정 근거: section/page/table/figure
- 불확실한 점:
```

## 8. LINER용 조사 프롬프트

아래 프롬프트는 한 번에 많은 논문을 요약시키기보다, 후보 수집과 원문 판정을 분리해서 사용한다.

```text
목표: 2021년 1월부터 2026년 7월까지 발표된 real-time vibration/machine fault diagnosis 연구를 체계적으로 조사한다.

연구 질문:
1. 실제 embedded/edge 장치에서 fault diagnosis를 수행했는가?
2. 실행 환경은 bare metal, RTOS, 일반 Linux, PREEMPT_RT 중 무엇인가? 정확한 OS/kernel와 version은 무엇인가?
3. task period 또는 deadline을 명시했는가?
4. real-time 성능을 모델 경량화, 시스템 최적화, scheduling 중 무엇으로 달성했는가?
5. average latency만 측정했는가, 아니면 p95/p99/max, jitter, deadline miss도 측정했는가?
6. schedulability analysis, WCET bound, admission control 또는 weakly-hard guarantee가 있는가?
7. window size, diagnosis period/hop size, model을 runtime에 조절하는가? trigger는 machine condition, system slack, load, confidence, deadline 중 무엇인가?

검색을 다음 네 집합으로 분리하라.
A. fault diagnosis + real-time/deadline/RTOS
B. fault diagnosis + TinyML/quantization/pruning/lightweight/NAS
C. fault diagnosis + scheduling/runtime adaptation/mode change/adaptive sampling
D. fault diagnosis + window size/input length/hop size/model selection

포함 기준:
- bearing, motor, gearbox, shaft, rotating machinery 또는 vibration condition monitoring
- primary research paper
- platform, timing 또는 scheduling 근거를 원문에서 확인 가능

제외 또는 별도 표시:
- offline accuracy만 있고 timing/deployment가 없는 논문
- review paper
- 초록만 접근 가능한 논문
- preprint와 출판본 중복

각 논문을 다음 표로 출력하라.
ID | Full citation | DOI/URL | Corpus A/B/C | Domain | Platform | Execution environment | OS/kernel/version | Task/period | Deadline | Timing metrics | Model optimization | System/scheduling intervention | Runtime variable | Trigger | Guarantee method | RT grade H/W/E/B/? | Evidence section/page | Uncertainty

판정 규칙:
- O는 원문에 명시적 근거가 있을 때만 사용한다.
- 초록에 없다는 이유만으로 X로 판정하지 말고 ?로 둔다.
- RTOS 사용이나 짧은 평균 latency만으로 hard real-time이라고 쓰지 않는다.
- H는 explicit deadline, conservative execution-time bound, schedulability/admission analysis가 모두 확인될 때만 사용한다.
- deadline과 miss/tail 실험만 있으면 E, 평균 latency/throughput만 있으면 B로 둔다.
- venue, year, metric, result를 추측하지 않는다.
- 각 핵심 판정에 page, section, table 또는 figure 근거를 붙인다.
- “scheduling 기반 fault diagnosis 논문이 없다”는 결론을 미리 가정하지 말고 반례를 적극적으로 찾는다.

마지막에 다음을 별도로 제시하라.
1. Direct RT-FD 논문 수
2. Embedded best-effort FD 논문 수
3. Scheduling을 명시적으로 사용한 Direct RT-FD 후보
4. 원문 확인이 필요한 후보
5. 검색 query와 검색일
```

## 9. 검토 절차와 완료 기준

1. Query family별 후보를 수집하고 제목/DOI 중복을 제거한다.
2. 제목과 abstract로 A/B/C 집합과 원문 확인 우선순위를 정한다.
3. 원문에서 `RTOS`, `deadline`, `period`, `jitter`, `WCET`, `schedulability`, `latency`, `runtime`, `adaptive`를 검색한다.
4. 위 주관식 양식을 먼저 채운 뒤 O/△/X 표로 압축한다.
5. Direct RT-FD의 모든 O와 X 판정을 두 번째로 검토한다. 불일치하면 ?로 되돌린다.
6. 검색일, database, query, 결과 수, 포함/제외 수를 기록한다.

GAP-01 완료 조건은 논문 수 자체가 아니다. 최근 문헌에서 real-time이라는 용어가 어떤 근거로 사용됐는지 분류하고, scheduling 기반 직접 비교군과 best-effort 경량화 대조군을 재현 가능한 규칙으로 구분하는 것이다.

## 10. 연구 스코프 축소 제안

현재 `W/H/M + q/S + MCU/SBC + RTOS/PREEMPT_RT`를 모두 한 번에 검증하면 변수와 baseline 수가 급격히 늘어난다. 첫 번째 완결 단위는 다음처럼 줄이는 것이 적절하다.

### 권장 코어

> Vibration fault diagnosis에서 machine condition `q`는 mode utility 순위를 정하고, system slack `S`는 deadline-feasible mode를 제한한다. Scheduler는 사전 검증한 이산 `(W,H)` mode 중 하나를 runtime에 선택한다.

- 고정: sampling frequency, sensor pipeline, 첫 model architecture, platform/RTOS
- 핵심 가변 변수: `W`와 `H`
- 핵심 trigger: `q`와 `S`
- 핵심 보장 질문: 선택 가능한 모든 mode와 mode transition이 정의한 deadline 조건을 만족하는가?
- 비교군: static light mode, static precise mode, `q`-only, `S`-only, proposed `q+S`

`M`은 첫 정식화에서 제거하거나 두 개의 사전 profiling된 model variant만 보조 실험으로 둔다. 모델 경량화 자체는 별도 contribution으로 주장하지 않는다. 이 구성이 성립한 뒤 `M`을 추가하면 “정책은 공통이고 mode bank는 model-specific”이라는 일반화 질문을 단계적으로 검증할 수 있다.

### 표에서 주장할 수 있는 차이

- 기존 embedded FD의 다수 후보: model optimization은 O지만 scheduling과 deadline guarantee는 X 또는 ?
- 기존 scheduling bridge: scheduling은 O지만 vibration fault diagnosis는 X
- 제안 연구의 목표: vibration FD에서 `q`와 `S`를 분리된 역할로 사용해 feasible `(W,H)` mode를 선택

최종 novelty는 표의 O 개수로 결정되지 않는다. Direct RT-FD 집합에서 scheduling 반례를 찾지 못했는지, bridge 집합과 비교해 어떤 task model과 utility가 새로 필요한지, 그리고 제안 정책이 실제로 deadline과 diagnosis utility를 개선하는지가 함께 입증되어야 한다.
