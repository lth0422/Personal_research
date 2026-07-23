# 0708 면담 반영 서베이 계획

이 문서는 `decisions/personal_research_summary_0708.md`의 교수님 피드백을 서베이 작업 단위로 바꾼 실행 계획이다.

## 2026-07-21 진행 점검

상세 점검 결과는 `decisions/survey_alignment_review_0721.md`에 기록했다.
부족한 근거와 완료 기준은 `surveys/survey_gap_backlog.md`에서 관리한다.

- `papers/` PDF 57편과 paper card 57개의 대응은 완료됐다.
- Elastic scheduling 응용 가정 비교는 상당 부분 보강됐다.
- Real-Time Fault Diagnosis 분류와 PREEMPT_RT 부하 설계 근거는 아직 부분 완료다.
- 고전 실시간 개념 노트는 미완료다.
- KCC 이용률은 max 기준만 정리됐고 average, p95, p99 계산이 남았다.
- MURAL, DNN-SAM, Decntr, SCENIC 등을 고려하면 input adaptation, slack 기반 선택, period/mode co-design, condition/model/timing 결합 각각을 단독 novelty로 주장해서는 안 된다.

## 2026-07-23 외부 서베이 입력 검토

- LINER·Claude 자료에서 fault-diagnosis 후보 16편과 elastic-scheduling 후보 8편을 수집했다.
- 기존 카드와 중복을 제외하면 fault-diagnosis 14편, elastic-scheduling 5편이 신규 후보이다.
- 신규 후보는 abstract/selection rationale 단계이므로 paper card 완료로 집계하지 않는다.
- “scheduling 기반 vibration FD 0편”, “최초 적용”, `SCHED_FIFO` 확정과 같은 강한 결론은 원문 검증 전까지 보류한다.
- MCU/RTOS와 SoC/Linux 중 하나를 최상위 우선순위로 두지 않는다. 연구 질문은 S1~S6 섹션으로 분류하고, 플랫폼은 별도 태그로 관리한다. 기준은 `surveys/research_aligned_literature_taxonomy_0723.md`다.
- 원본과 후보 우선순위는 `surveys/source_reports/2026-07-21_liner_claude/`와 `surveys/liner_claude_survey_review_0723.md`에서 관리한다.

## 핵심 방향

- 방향 2, 즉 `W/H/M` 기반 elastic scheduling을 연구의 코어로 둔다.
- 방향 1, 즉 Pi Zero 2W Linux vs PREEMPT_RT 비교는 독립 논문 목표보다 방향 2를 위한 실험 환경과 원인 분석 훈련으로 둔다.
- 방향 3은 방향 2가 정리된 뒤 재개한다.

## 교수님 피드백에서 온 질문

1. 이상 징후 시 정밀 mode로 전환해도 항상 schedulable한가?
2. 그 schedulability를 어떻게 보장할 것인가?
3. 기존 real-time fault diagnosis 논문들은 RTOS와 deadline을 실제로 다루는가, 아니면 경량화로 근실시간을 주장하는가?
4. 기존 elastic scheduling 응용은 어떤 가정을 두고 있으며, 그 가정이 본 연구의 `C(W,M)` 가변 실행시간에서 깨지는가?
5. 부하 조건은 유사 논문들이 어떻게 설계했는지 보고 정해야 한다.

## 산출물

### 최근 실시간 학회 후보 백로그

위치: `surveys/recent_top_conference_relevance_backlog.md`

목표:
- `wiki/analyses/`의 RTAS 2022--2025, RTCSA 2023--2025, RTSS 2024--2025 조사 결과를 현재 `W/H/M` 연구 기준으로 재분류한다.
- abstract 수준 후보와 PDF 원문 검토가 끝난 논문을 구분한다.
- 신규 PDF 다운로드와 정독 순서를 관리한다.

### 1. Real-Time Fault Diagnosis 분류표

위치: `surveys/comparison_table_ko.md`

판정 프로토콜: `surveys/realtime_fault_diagnosis_survey_protocol.md`

원고용 압축 표: `manuscript/realtime_fault_diagnosis_related_work_table.md`

목표:
- 최근 real-time fault diagnosis 문헌을 RTOS 유무, deadline 유무, platform, 실시간성 접근 방식으로 분류한다.
- TinyML, quantization, pruning, lightweight architecture search를 `best-effort 근실시간`과 구분한다.

핵심 판정 기준:
- `진짜 실시간`: RTOS, deadline, jitter, p95/p99/max latency, deadline miss, schedulability 중 일부를 명시적으로 다룸.
- `근실시간`: 평균 inference time 또는 model size만 줄이고 deadline guarantee나 scheduling 분석이 없음.

최종 판정에서는 이를 H/W/E/B로 세분한다. RTOS 사용만으로 H로 분류하지 않고, explicit deadline, execution-time bound와 schedulability/admission 근거를 함께 확인한다.

### 2. Elastic Scheduling 실전 응용 가정표

위치: `surveys/comparison_table_ko.md`

목표:
- 기존 elastic scheduling 논문의 주된 가정을 정리한다.
- 특히 `C` 고정, `T` 가변이라는 가정이 본 연구의 `C(W,M)` 가변 구조와 어떻게 다른지 확인한다.

### 3. 부하 설계 전략

위치: `surveys/comparison_table_ko.md`와 `surveys/related_work_map.md`

목표:
- PREEMPT_RT, Raspberry Pi, SBC, COTS platform 문헌이 어떤 부하를 사용했는지 정리한다.
- 현재 `idle/CPU/mem/IO/combined`는 임시 후보이며, 최종 부하 조건은 문헌 근거를 보고 확정한다.

### 4. 고전 실시간 개념 노트

위치: 추후 `surveys/classic_rt_concepts_note.md` 생성 권장

포함할 개념:
- imprecise computation
- mode change protocol
- cyclic executive
- weakly-hard deadline
- EDF/SCHED_DEADLINE/CBS

## 카드화 구성 원칙

새 카드 또는 기존 카드 보강 시 다음 항목을 특히 채운다.

1. 실시간성 수준
   - RTOS 사용 여부
   - deadline 정의 여부
   - jitter, p99, max, deadline miss 측정 여부
   - 평균 latency만 있는지 여부

2. 가정
   - `C`가 고정인지, profiling table인지, runtime에 달라지는지
   - `T/H`가 바뀌는지
   - model 또는 input이 바뀌는지

3. 보장 방식
   - utilization bound
   - EDF/RM schedulability
   - admission control
   - fallback mode
   - empirical p99/max feasibility

4. 본 연구와의 직접 연결
   - `W` 근거
   - `H/T` 근거
   - `M` 근거
   - `machine condition` 근거
   - `system slack` 근거
   - PREEMPT_RT 또는 RTOS 근거

## 우선순위

### 기존 정독 및 재검토 큐

아래 목록은 0708 직후 설정한 이론 보강 큐다. 현재는 신규 카드 수를 늘리기보다 미완료 산출물을 먼저 마무리한다.

1. Buttazzo et al., `Elastic Scheduling for Flexible Workload Management`, IEEE Transactions on Computers 2002
   - 다음 정독 대상이다.
   - `C` 고정, `T` 가변, elastic coefficient, feasible utilization 조정이라는 기본 가정을 먼저 이해한다.
   - 본 연구의 `H/T` 축과 `C(W,M)` 확장 지점을 구분하기 위한 이론적 바닥으로 사용한다.
2. Hu et al., `On Exploring Image Resizing for Optimizing Criticality-based Machine Perception`, RTCSA 2021
   - input size와 model size를 criticality 및 deadline과 연결하는 직접 비교군이다.
   - dedicated smaller model과 resized input/model 조합의 품질-시간 trade-off를 AMS의 Anytime 구조와 대조한다.
3. Sudvarg et al., `Elastic Scheduling for Harmonic Task Systems`, RTAS 2024
   - 최신 elastic scheduling에서 mode feasibility와 application evaluation을 어떻게 연결하는지 확인한다.

완료: Li et al., `Adaptive Model Selection for Real-Time Heart Disease Detection on Embedded Systems`, RTCSA 2025는 paper card와 비판적 검토 메모까지 작성했다.

### 최우선

- real-time fault diagnosis 문헌 중 RTOS/deadline을 실제로 다루는지 확인할 수 있는 논문
- elastic scheduling 응용 중 실전 application assumption을 보여주는 논문
- imprecise computation, mode change, anytime/early-exit model selection 문헌

### 중간

- TinyML, pruning, quantization, lightweight model 기반 fault diagnosis
- Pi Zero 2W, Raspberry Pi, PREEMPT_RT platform benchmark
- deadline-aware DNN serving

### 낮음

- 일반 scheduling overhead 문헌
- domain이 멀고 본 연구의 `W/H/M` 또는 RTOS와 직접 연결이 약한 문헌

## 다음 2-3주 작업 순서

1. `surveys/classic_rt_concepts_note.md`를 만들고 mode change, imprecise computation, weakly-hard, EDF/SCHED_DEADLINE/CBS를 연결한다.
2. `surveys/comparison_table_ko.md`의 real-time fault diagnosis 표를 RTOS, deadline, tail metric 기준으로 보강한다.
3. PREEMPT_RT 및 SBC 문헌의 workload와 measurement를 부하 설계 근거표로 정리한다.
4. KCC 데이터로 `U=C/T`를 average, p95, p99, max 기준으로 계산한다.
5. 위 결과를 교수님 보고용 요약 문서 또는 PPT 골격으로 압축한다.

신규 paper card는 위 산출물의 빈칸을 직접 채우는 논문에 우선한다. 넓은 인접 분야 후보의 일괄 카드화는 보류한다.
