# AGENTS.md

이 repo는 이태훈의 석사 개인연구 작업 공간이다.
Codex는 이 저장소에서 논문 서베이, 연구 주장 정리, 실험 로그 정리, 원고 초안 생성을 보조한다.

## 0. 가장 중요한 원칙

이 repo는 단순 논문 저장소가 아니다.
**논문 트랙이 두 개**이며 반드시 구분한다.

| 트랙 | 폴더 | 목표 | 제출 시기 |
| --- | --- | --- | --- |
| **단기** | `ksc2026/` | Pi Zero 2W Linux vs PREEMPT_RT 실시간성 비교 | KSC 2026, 9월 |
| **중장기** | `manuscript/` | W/H/M elastic scheduling 학위논문 | RTAS/RTCSA 2027 |

`experiments/`는 두 트랙이 **공유**한다. 실험 코드와 결과는 여기에, 논문 초안은 각 트랙 폴더에 분리해서 작성한다.

목표는 다음 흐름을 빠르게 반복하는 것이다.

논문 서베이 → 비교표 정리 → 연구 gap 도출 → claim_bank 업데이트 → 실험 아이디어 도출 → 각 트랙 초안 반영

작업할 때는 항상 “이 내용이 내 연구 주장 또는 논문 원고에 어떻게 연결되는가?”를 기준으로 판단한다.

---

## 1. 작업 시작 전 반드시 읽을 파일

Codex는 작업 시작 전에 아래 파일을 먼저 확인한다.

1. `PROJECT_CONTEXT.md`

   * 연구 배경, 핵심 식, 용어, novelty, repo 구조의 단일 기준점이다.

2. `prompts/paper_card_prompt.md`

   * 논문 카드 작성 규칙이다.

3. 작업 목적에 따라 필요한 파일

   * 논문 정리: `surveys/comparison_table.md`, `surveys/paper_cards/`
   * 연구 주장 정리: `surveys/claim_bank.md`
   * 관련연구 정리: `surveys/related_work_map.md`
   * 실험 관련 작업: `experiments/`
   * 원고 관련 작업: `manuscript/`
   * 미해결 질문: `decisions/open_questions.md`

---

## 2. 연구 주제 요약

현재 연구는 제한된 엣지 디바이스에서 기계 상태와 시스템 상태를 동시에 고려하여 실시간 결함 진단을 안정적으로 수행하는 방법을 다룬다.

핵심 방향은 다음과 같다.

* STM32F407 + Zephyr RTOS 기반 MCU 실시간 추론 결과를 출발점으로 삼는다.
* Pi Zero 2W, 일반 Linux, PREEMPT_RT 환경에서 실시간성을 비교한다.
* 진동 센서 기반 fault diagnosis에서 입력 window size, 진단 주기, 모델을 조절 가능한 변수로 본다.
* machine condition과 system slack을 함께 고려하는 runtime mode selection 또는 elastic scheduling 정책으로 확장한다.
* 연구 관점은 AI 모델 자체 최적화보다 RTOS, scheduling, deadline, jitter, resource constraint에 가깝다.

---

## 3. Codex 작업 규칙

### 3.1 추측 금지

다음 정보는 절대 추측하지 않는다.

* 논문 출처
* venue
* year
* dataset
* metric
* 정량 결과
* 저자 주장
* 실험 환경

확실하지 않으면 `TBD`, `unknown`, `확인 필요`로 표시하고 `decisions/open_questions.md`에 기록한다.

### 3.2 과장 금지

내 연구와 논문의 연결을 과장하지 않는다.

좋은 표현:

* “관련연구에서 비교 대상으로 활용 가능하다.”
* “window size와 latency trade-off 논의에 참고 가능하다.”
* “본 연구의 문제의식과 일부 연결된다.”

피해야 할 표현:

* “이 논문이 본 연구를 직접 뒷받침한다.”
* “본 연구의 novelty를 완전히 증명한다.”
* “기존 연구는 전혀 다루지 않았다.”

강한 주장은 반드시 근거 논문 또는 실험 로그와 연결한다.

### 3.3 한 번에 한 작업 단위

큰 변경을 한 번에 하지 않는다.

권장 작업 단위:

* 논문 카드 1개 작성
* comparison_table 1행 추가
* claim_bank 일부 정리
* related_work_map 한 섹션 정리
* experiment_log 1개 정리
* manuscript 한 섹션 초안 작성

작업 후에는 수정 파일 목록을 요약한다.

### 3.4 파일 삭제 금지

사용자가 명시적으로 요청하지 않는 한 기존 파일을 삭제하지 않는다.
대규모 구조 변경 전에는 먼저 변경 계획을 요약한다.

### 3.5 Git 기준

작업 전후에 다음을 확인하는 습관을 유지한다.

```bash
git status
git diff
```

작업 결과를 설명할 때는 다음을 포함한다.

* 수정한 파일
* 왜 수정했는지
* 아직 불확실한 점
* 다음 작업 제안

---

## 4. 논문 서베이 규칙

논문 한 편을 정리할 때는 반드시 다음 두 질문에 답한다.

1. 가변 변수가 무엇인가?
   예: period, 입력크기, window size, model, batch, exit, 없음

2. 적응을 무엇이 트리거하는가?
   예: 부하, 자원경합, criticality, 기계상태, 없음 또는 offline

특히 다음 조합이 나오면 중요하게 표시한다.

* 입력 window + 기계 상태
* system slack + model selection
* period 또는 hop size + fault diagnosis
* deadline-aware inference + vibration signal

이 조합은 본 연구의 novelty와 직접 연결될 수 있으므로 `surveys/claim_bank.md`와 `decisions/open_questions.md`에 반영 여부를 검토한다.

---

## 5. 논문 카드 작성 규칙

논문 카드는 `prompts/paper_card_prompt.md` 형식을 따른다.
저장 위치는 기본적으로 그룹별 하위 폴더를 사용한다.

```text
surveys/paper_cards/{그룹번호_그룹명}/{짧은제목}.md
```

논문 카드를 작성한 뒤에는 반드시 다음을 검토한다.

1. `surveys/comparison_table.md`에 한 행을 추가할 수 있는가?
2. `surveys/related_work_map.md`에 연결할 claim이 있는가?
3. `surveys/claim_bank.md`에 발전시킬 연구 주장이 있는가?
4. `decisions/open_questions.md`에 남길 확인 사항이 있는가?

논문 요약 중 확인하지 못한 venue, year, dataset, metric, result, 실험 환경, 저자 주장 등은 paper card의 `불확실한 점` 섹션에 명시한다.

---

## 6. 실험 로그 작성 규칙

실험 관련 문서는 `experiments/` 아래에 작성한다.

실험 로그에는 가능하면 다음 항목을 포함한다.

* 목적
* 플랫폼
* OS 또는 RTOS
* 모델
* 입력 window
* scheduling 설정
* 부하 조건
* 측정 지표
* 결과
* 해석
* 실패 또는 이슈
* 다음 액션

정량값은 반드시 단위와 조건을 함께 적는다.
예: `40.3 ms`, `deadline 64 ms`, `p99 latency`, `stress-ng CPU load`

---

## 7. 원고 작성 규칙

`manuscript/` 파일을 수정할 때는 다음을 지킨다.

* 학술 문서에서 괄호 사용을 자제한다.
* 단정적 표현을 피한다.
* 관련연구 문장은 가능한 한 `surveys/claim_bank.md`의 claim과 연결한다.
* 실험 결과 문장은 `experiments/`의 로그와 연결한다.
* 불확실한 인용이나 정량값은 임의로 채우지 않는다.

교수님 보고용 문서는 개조식으로 간결하게 작성한다.
내부 노트는 상세하게 작성해도 된다.

---

## 8. 역할 분담 (Codex vs Claude Code)

### 8-1. 파일 소유권 — 절대 교차 금지

| 소유 에이전트 | 담당 디렉토리·파일 | 비고 |
| --- | --- | --- |
| **Codex** | `surveys/`, `decisions/`, `manuscript/`, `ksc2026/`, `prompts/` | 논문 서베이 + 두 트랙 초안 |
| **Claude Code** | `experiments/pipeline/`, `experiments/results/analysis/` | 실험 코드 + 분석 스크립트 |
| **공유 (읽기만)** | `PROJECT_CONTEXT.md`, `AGENTS.md`, `CLAUDE.md`, `experiments/experiment_design.md`, `experiments/pi_setup/`, `experiments/preempt_rt/`, `experiments/results/` (원본) | 수정 전 상대 확인 |

### 8-2. Codex 담당

**서베이 트랙**
* 논문 카드 작성 (`surveys/paper_cards/`)
* `surveys/comparison_table.md` 행 추가·수정
* `surveys/claim_bank.md`, `surveys/related_work_map.md` 업데이트
* `decisions/open_questions.md` 질문 추가

**단기 논문 (KSC 2026)**
* `ksc2026/paper_draft.md` 초안 보완
* KSC용 related work 정리 (platform/PREEMPT_RT 중심)

**중장기 논문 (학위논문)**
* `manuscript/draft.md`, `manuscript/problem_formulation.md` 보완
* W/H/M elastic scheduling 관련 섹션 작성

### 8-3. Claude Code 담당

* `experiments/pipeline/` 파이썬 코드
  * `main.py`, `sensor.py`, `inference.py`, `logger.py`, `config.py`
  * `run_experiment.sh` 자동화 스크립트
* `experiments/results/analysis/` 분석 스크립트
  * `plot_latency.py`, `calc_stats.py`, `compare_kernels.py`
* 실험 실행·디버깅 지원

### 8-4. 공통 협업 원칙

* 한 에이전트가 작업한 뒤에는 `git status`와 `git diff`로 변경 사항을 확인한다.
* 의미 있는 작업 단위마다 commit한다.
* 상대 에이전트가 수정 중인 파일은 건드리지 않는다.

---

## 9. 출력 형식

작업 완료 후 Codex는 다음 형식으로 요약한다.

```md
## 작업 요약

### 수정한 파일
- ...

### 수행한 작업
- ...

### 불확실한 점
- ...

### 다음 작업 제안
- ...
```

불확실한 점이 없다면 “현재 기준 없음”이라고 쓴다.
