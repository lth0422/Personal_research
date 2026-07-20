# 0721 서베이 정합성 점검

- 점검일: 2026-07-21
- 기준 문서: `decisions/personal_research_summary_0708.md`
- 범위: `papers/`, `surveys/`, `manuscript/`의 서베이 산출물

## 결론

현재 아카이빙은 `PDF -> paper card -> comparison table -> claim/related-work` 흐름으로 일관되게 관리되고 있다. 점검 시점 기준 `papers/`의 PDF 57편과 `surveys/paper_cards/`의 카드 57개가 대응한다.

그러나 카드 수가 많다는 것과 0708 면담에서 요구된 산출물이 완성됐다는 것은 다르다. Elastic scheduling의 응용 가정 비교는 상당히 보강됐지만, real-time fault diagnosis 분류와 부하 설계 근거는 추가 조사가 필요하다. 고전 실시간 개념 노트와 KCC 실행시간 통계도 아직 완료되지 않았다.

## 산출물별 상태

| 항목 | 상태 | 현재 근거 | 남은 작업 |
| --- | --- | --- | --- |
| PDF 및 paper card 대응 | 완료 | PDF 57편, 카드 57개 | 신규 PDF 추가 시 같은 대응 관계 유지 |
| 논문별 가변 변수와 trigger 기록 | 완료 | 각 카드의 `두 질문` 절 | 불명확한 논문은 원문 재검토 |
| Real-Time Fault Diagnosis 분류표 | 부분 완료 | `surveys/comparison_table_ko.md` | RTOS, deadline, tail latency, miss 기준의 직접 비교군 보강 |
| Elastic Scheduling 응용 가정표 | 상당 부분 완료 | 고전 elastic, ATER, Safety-Aware, Decntr 등 반영 | application assumption과 guarantee 조건을 최종 교차검증 |
| 부하 설계 근거표 | 부분 완료 | PREEMPT_RT 및 SBC 문헌 일부 반영 | CPU, memory, I/O, combined load 선택 근거와 측정 지표 보강 |
| 고전 실시간 개념 노트 | 미완료 | 관련 내용이 개별 카드에 분산 | imprecise computation, mode change, cyclic executive, weakly-hard, EDF/SCHED_DEADLINE/CBS 통합 |
| KCC 이용률 계산 | 부분 완료 | `manuscript/problem_formulation.md`에 max 기반 값 기록 | 동일 조건의 average, p95, p99 계산 및 측정 로그 연결 |
| 원고용 관련연구 압축표 | 진행 중 | `manuscript/table1_related_work.md` | 핵심 비교축과 인용 근거 재검토 후 원고 문장과 연결 |

## 최근 추가 문헌이 바꾼 판단

| 문헌 | 이미 다루는 조합 | 본 연구 주장에 주는 제약 |
| --- | --- | --- |
| MURAL | input resolution과 real-time perception cost | input fidelity 조절 자체를 novelty로 주장할 수 없음 |
| DNN-SAM | system slack 기반 input/model 선택 | `system slack -> input fidelity`만으로는 차별화가 부족함 |
| Decntr | controller mode, period, resource allocation | period와 mode의 공동 조절 자체를 novelty로 주장할 수 없음 |
| SCENIC | environment, model capability, timing, application utility의 offline co-design | condition, model, timing의 결합 자체를 최초라고 주장할 수 없음 |
| Safety-Aware Scheduling | application safety와 period 조절 | safety/condition 기반 period adaptation 자체를 novelty로 주장할 수 없음 |
| ATER | runtime feedback 기반 rate regulation | runtime period/rate adaptation 자체를 novelty로 주장할 수 없음 |
| Handling System Overloads | overload detection과 fallback execution | overload fallback 자체를 novelty로 주장할 수 없음 |

현재 조사 범위에서 남는 차별화 후보는 vibration signal의 temporal window 의미, diagnosis utility 또는 anomaly state, runtime system slack을 함께 사용하여 `W/H/M` mode를 선택하고 PREEMPT_RT edge 환경에서 검증하는 조합이다. 이는 아직 **검증할 연구 가설**이며 novelty가 확정된 주장이 아니다.

## SCENIC 반영 결과

- PDF 위치: `papers/03_rt_dnn_serving/SCENIC_Capability_and_Scheduling_Co-Design_for_Intelligent_Controller_on_Heterogeneous_Platforms.pdf`
- 카드 위치: `surveys/paper_cards/03_rt_dnn_serving/scenic_capability_scheduling_codesign.md`
- 반영 문서: inventory, 영문/한글 comparison table, claim bank, related-work map, open questions, 원고용 Table 1
- 핵심 판정: model complexity, CPU/GPU mapping과 fixed priority를 offline에서 공동 최적화한다. Runtime condition-triggered adaptation은 하지 않는다.

## 다음 서베이 운영 기준

새로운 인접 분야 논문을 넓게 카드화하는 작업은 잠시 줄인다. 다음 조건 중 하나를 만족하는 논문만 우선 추가한다.

1. Real-time fault diagnosis 분류표의 빈칸을 직접 채운다.
2. `C(W,M)`와 `H/T`가 함께 변할 때의 schedulability 근거를 제공한다.
3. PREEMPT_RT 부하 설계나 tail-latency 평가 근거를 제공한다.
4. `W/H/M` 중 둘 이상과 runtime trigger를 명시적으로 다룬다.

다음 작업 순서는 고전 실시간 개념 노트, fault-diagnosis 분류표 보강, 부하 설계 근거 정리, KCC average/p95/p99 계산이다.

## 공유 문서 확인 필요

`PROJECT_CONTEXT.md`는 공유 읽기 파일이므로 이번 점검에서 수정하지 않았다. 최신 문헌을 반영하면 novelty 표현을 “기존에 전혀 없음”이 아니라 “현재 조사 범위에서 특정 결합을 확인하지 못함” 수준으로 유지해야 한다. 다음 공동 점검 때 Claude Code 작업과 충돌하지 않는 범위에서 문구 정합성을 확인한다.
