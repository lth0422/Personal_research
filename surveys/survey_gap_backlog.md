# 서베이 부족 영역 및 보강 백로그

- 작성일: 2026-07-21
- 기준: `decisions/personal_research_summary_0708.md`
- 상태 점검: `decisions/survey_alignment_review_0721.md`

이 문서는 카드 개수를 늘리기 위한 목록이 아니다. 교수님 피드백에 답하고 `W/H/M` 연구 가설을 검증하는 데 현재 부족한 근거와 완료 조건을 관리한다.

## 현재 분포

점검 시점 기준 PDF와 paper card는 각각 57개다. 카드 그룹은 elastic scheduling 14편, real-time DNN serving 13편, input-adaptive 8편, weakly-hard 6편, platform/PREEMPT_RT 5편, fault diagnosis application 5편, miscellaneous real-time scheduling 4편, Pi Zero 2W platform 2편이다.

양적으로는 elastic scheduling과 DNN serving 쪽이 크다. 반면 연구 도메인에 직접 해당하는 fault diagnosis의 deadline/RTOS 근거와 Pi Zero 2W 부하 설계 근거는 상대적으로 부족하다.

## P0: 교수님 피드백에 직접 필요한 부족 영역

| ID | 부족한 서베이 | 현재 상태 | 필요한 근거 | 완료 기준 | 반영 위치 |
| --- | --- | --- | --- | --- | --- |
| GAP-01 | Real-time fault diagnosis의 실시간성 수준 | 관련 카드 5편이 있으나 RTOS, deadline, miss, tail latency가 확인된 직접 비교군이 적음 | Fault diagnosis application이 RTOS task, deadline, jitter, p95/p99/max, deadline miss 또는 schedulability를 실제로 다루는지 보여주는 원문 근거 | 각 논문을 `보장형`, `측정형`, `best-effort`로 구분하고 최소한 RTOS/deadline/평가 지표를 확인 | `comparison_table_ko.md` 1절, `related_work_map.md` |
| GAP-02 | `C(W,M)`와 `H/T` 동시 변화의 schedulability | 기존 elastic 문헌은 `C` 고정과 `T` 가변 가정이 중심이며 인접 연구는 일부 축만 결합 | 실행시간과 period가 mode에 따라 함께 변할 때 사용하는 feasibility test, admission rule 또는 mode-transition 분석 | 본 연구가 기존 식을 그대로 쓸 수 있는 범위와 새로 정식화해야 하는 범위를 구분 | `problem_formulation.md`, `classic_rt_concepts_note.md` |
| GAP-03 | KCC mode별 실행시간 분포 | 현재 max 기반 이용률만 문서화됨 | 같은 실험 조건에서 각 `W/M`의 average, p95, p99, max execution/response time | 값의 출처 로그, 단위, 부하 조건을 연결하고 `U=C/T`를 동일 기준으로 계산 | `problem_formulation.md`, 향후 교수님 보고 자료 |
| GAP-04 | Mode transition의 보장과 fallback | Decntr, Safety-Aware, overload 대응 논문은 있으나 vibration diagnosis mode 전환 규칙은 미정 | 전환 중 deadline, queue/backlog, stale data, fallback mode, hysteresis를 다루는 이론 또는 시스템 근거 | 정상/의심/결함 mode 전환 시 허용 가능한 실행과 실패 대응을 명시 | `classic_rt_concepts_note.md`, `open_questions.md` |

## P1: 실험 설계 전에 필요한 부족 영역

| ID | 부족한 서베이 | 현재 상태 | 필요한 근거 | 완료 기준 | 반영 위치 |
| --- | --- | --- | --- | --- | --- |
| GAP-05 | PREEMPT_RT 부하 선정 근거 | Raspberry Pi/PREEMPT_RT 관련 5편과 Pi Zero 2W 2편이 있으나 부하 축이 통일되지 않음 | CPU, memory, I/O, network, combined interference를 왜 선택하는지와 각 부하의 재현 가능한 parameter | 부하별 도구, thread/core 설정, intensity, duration, thermal control, 반복 횟수와 측정 지표를 표로 확정 | `comparison_table_ko.md` 5절, 실험 설계에는 읽기 근거로 전달 |
| GAP-06 | Tail latency와 경험적 보장의 표현 | 일부 문헌이 측정 최대값을 WCET처럼 사용함 | p95/p99/max, measurement-based WCET, analytical WCET의 차이와 주장 한계 | KSC와 학위논문에서 사용할 용어를 구분하고 hard real-time guarantee 과장을 방지 | `claim_bank.md`, 두 트랙 초안 |
| GAP-07 | Machine condition `q`의 정의 | anomaly, heart rate, safety margin 등 인접 trigger 사례는 있으나 vibration용 상태 정의가 미정 | anomaly score, confidence, health index의 계산 주기, 신뢰성, false transition 비용 | 첫 구현에서 사용할 `q`, threshold, hysteresis와 검증 metric을 정함 | `open_questions.md`, `problem_formulation.md` |
| GAP-08 | Diagnostic utility `Q(W,H,M,q)` | Window/model별 정확도 문헌은 있으나 period와 detection delay까지 묶은 utility 근거가 부족 | accuracy/F1 외에 detection delay, freshness, false alarm, missed event를 mode와 연결한 평가 방식 | mode별 utility table 또는 목적함수 후보를 데이터로 정의 | `claim_bank.md`, `problem_formulation.md` |

## P2: 원고 작성 단계에서 보강할 영역

| ID | 부족한 서베이 | 현재 상태 | 필요한 근거 | 완료 기준 | 반영 위치 |
| --- | --- | --- | --- | --- | --- |
| GAP-09 | 고전 실시간 개념의 통합 설명 | 개별 카드에 분산 | imprecise computation, mode change, cyclic executive, weakly-hard, EDF/SCHED_DEADLINE/CBS의 정의와 본 연구 적용 범위 | 개념별 핵심 가정, 보장, `W/H/M` 연결, 적용하지 않을 부분을 한 문서로 정리 | `classic_rt_concepts_note.md` |
| GAP-10 | 두 논문 트랙의 관련연구 분리 | 공통 서베이는 있으나 KSC와 학위논문이 같은 표를 공유함 | KSC는 Linux/PREEMPT_RT와 측정 방법, 학위논문은 elastic/mode-selection 이론 중심으로 인용 범위 분리 | 각 원고 related work의 필수 논문과 보조 논문 목록 확정 | `ksc2026/`, `manuscript/` |
| GAP-11 | Novelty claim의 선행연구 반증 점검 | DNN-SAM, Decntr, SCENIC이 단순 조합 주장을 약화함 | `q+S`, `W+H+M`, vibration temporal semantics, PREEMPT_RT 검증의 각 요소와 결합을 직접 비교 | “없다”가 아니라 검색 범위와 차이를 명시한 방어 가능한 claim 작성 | `claim_bank.md`, `table1_related_work.md` |

## 신규 논문 카드화 우선 조건

새 논문은 아래 질문 중 하나에 명확히 답할 때 우선 카드화한다.

1. Fault diagnosis에서 RTOS와 deadline을 실제로 어떻게 정의하고 검증했는가?
2. `C`와 `T`가 동시에 mode-dependent일 때 어떤 schedulability test를 쓰는가?
3. Mode transition 도중 backlog와 deadline을 어떻게 처리하는가?
4. PREEMPT_RT 또는 SBC에서 부하 조건과 tail latency를 어떻게 재현했는가?
5. Vibration diagnosis에서 window, hop, model이 detection utility에 미치는 영향을 어떻게 공동 평가했는가?

제목이나 abstract만으로 위 질문에 답할 수 없으면 `후보`로만 남기고, 원문 확인 전에는 comparison table의 근거 행으로 사용하지 않는다.

## 바로 수행할 순서

1. GAP-09 고전 실시간 개념 노트를 작성한다.
2. GAP-01 fault-diagnosis 카드 5편을 원문 기준으로 재검토하고 분류표의 `확인 필요`를 줄인다.
3. GAP-05 platform 카드에서 부하 도구와 조건을 추출해 부하 설계 표를 보강한다.
4. GAP-03은 실험 로그가 준비된 뒤 값과 조건을 읽어 계산한다. `experiments/` 파일은 수정하지 않는다.
5. GAP-02, GAP-04를 바탕으로 schedulability와 mode-transition 정식화 범위를 결정한다.
