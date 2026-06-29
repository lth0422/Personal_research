# Session Log

## 2026-06-29

### 1. 오늘 수행한 작업

- repo 기본 구조를 정리했다.
- `papers/` 아래 논문 그룹별 디렉토리를 만들고 `.gitkeep`으로 빈 폴더를 추적 가능하게 했다.
- `paper_card_prompt.md` 경로를 `prompts/paper_card_prompt.md` 기준으로 정리했다.
- `.papre` 오타를 `paper`로 수정했다.
- `papers/` 아래 PDF 목록을 확인하고 `surveys/paper_inventory.md`를 만들었다.
- PDF 파일명을 통일성 있게 정리하고, PROJECT_CONTEXT 10절 기준으로 논문을 임시 분류했다.
- 중복 의심 PDF는 확인했지만, 완전 중복으로 확정하지 못한 파일은 삭제하지 않았다.
- `02_input_adaptive` 그룹의 핵심 논문 7편을 paper card로 정리했다.
- `01_elastic_scheduling` 그룹의 핵심 논문 3편을 paper card로 정리했다.
- `surveys/comparison_table.md`를 정형화하고, paper card 기반 행을 추가했다.
- `surveys/claim_bank.md`, `surveys/related_work_map.md`, `decisions/open_questions.md`에 survey 결과를 반영했다.
- 변경 사항을 커밋하고 GitHub `origin/main`에 푸쉬했다.

### 2. 수정한 파일 목록

- `AGENTS.md`
- `CLAUDE.md`
- `PROJECT_CONTEXT.md`
- `prompts/paper_card_prompt.md`
- `decisions/open_questions.md`
- `surveys/claim_bank.md`
- `surveys/comparison_table.md`
- `surveys/related_work_map.md`
- `surveys/paper_inventory.md`
- `surveys/paper_cards/01_elastic_scheduling/elastic_task_model_adaptive_rate_control.md`
- `surveys/paper_cards/01_elastic_scheduling/elastic_scheduling_flexible_workload.md`
- `surveys/paper_cards/01_elastic_scheduling/subtask_level_elastic_scheduling.md`
- `surveys/paper_cards/02_input_adaptive/anomaly_deviation_window_size.md`
- `surveys/paper_cards/02_input_adaptive/canvas_attention_resizing.md`
- `surveys/paper_cards/02_input_adaptive/exploring_image_resizing.md`
- `surveys/paper_cards/02_input_adaptive/generalized_self_cueing_resizing.md`
- `surveys/paper_cards/02_input_adaptive/integrating_adaptive_input_length_noisy_tl.md`
- `surveys/paper_cards/02_input_adaptive/novel_tl_adaptive_input_lightweight.md`
- `surveys/paper_cards/02_input_adaptive/realtime_task_scheduling_resizing.md`
- `papers/01_elastic_scheduling/.gitkeep`
- `papers/02_input_adaptive/.gitkeep`
- `papers/03_rt_dnn_serving/.gitkeep`
- `papers/04_idk_weakly_hard/.gitkeep`
- `papers/05_fault_diagnosis_app/.gitkeep`
- `papers/06_platform_preempt_rt/.gitkeep`
- `papers/07_platform_pi_zero2w/.gitkeep`
- `papers/08_misc_realtime_scheduling/.gitkeep`

### 3. 각 파일을 왜 수정했는지

- `AGENTS.md`: paper card 저장 경로를 그룹별 하위 폴더 기준으로 맞추고, paper card의 불확실한 점 기록 규칙을 반영했다.
- `CLAUDE.md`: Codex와 같은 repo 규칙을 보도록 경로와 지시를 최소 수정했다.
- `PROJECT_CONTEXT.md`: repo 구조와 paper card 경로 기준을 현재 구조에 맞췄다.
- `prompts/paper_card_prompt.md`: paper card 템플릿에 `불확실한 점` 섹션과 그룹별 저장 경로를 반영했다.
- `decisions/open_questions.md`: paper card 작성 중 확인이 필요한 사항을 정리했다.
- `surveys/claim_bank.md`: input-adaptive, fault diagnosis adaptive window, elastic scheduling 관련 claim 후보를 정리했다.
- `surveys/comparison_table.md`: 논문 비교표를 12개 컬럼으로 정형화하고, 정리한 논문들을 행으로 추가했다.
- `surveys/related_work_map.md`: elastic scheduling, input-adaptive visual perception, input-adaptive fault diagnosis 축을 원고 연결 관점으로 정리했다.
- `surveys/paper_inventory.md`: 보유 PDF 목록, 임시 그룹, 우선순위, card 작성 상태를 추적하기 위해 만들었다.
- `surveys/paper_cards/01_elastic_scheduling/*.md`: elastic scheduling 핵심 3편을 card 형식으로 정리했다.
- `surveys/paper_cards/02_input_adaptive/*.md`: input size, window size, adaptive input length 관련 핵심 7편을 card 형식으로 정리했다.
- `papers/*/.gitkeep`: PDF 원본은 gitignore하면서도 그룹별 폴더 구조는 GitHub에 남기기 위해 추가했다.

### 4. 아직 끝나지 않은 작업

- 전체 40편 이상 논문 중 일부만 paper card로 정리했다.
- `01_elastic_scheduling`의 확장 논문들은 아직 대부분 inventory 상태다.
- `03_rt_dnn_serving`, `04_idk_weakly_hard`, `05_fault_diagnosis_app`, `06_platform_preempt_rt`, `07_platform_pi_zero2w`, `08_misc_realtime_scheduling` 그룹은 아직 card 정리가 시작되지 않았다.
- `Subtask-Level_Elastic_Scheduling_copy1.pdf`와 `copy2_needs_check.pdf`의 완전 중복 여부가 확정되지 않았다.
- comparison table의 정량 결과 수치는 원고 인용 전 원문 표/그림 기준 재확인이 필요하다.
- manuscript 초안 반영은 아직 시작하지 않았다.

### 5. 다음 Codex 세션에서 바로 이어서 할 작업

- `AGENTS.md`, `PROJECT_CONTEXT.md`, `prompts/paper_card_prompt.md`를 먼저 읽는다.
- `surveys/paper_inventory.md`에서 아직 `inventory only`인 High priority 논문을 확인한다.
- 다음 후보로 `rt_dnn_serving`의 FLEX 논문 또는 `elastic_scheduling`의 QoC/Generalized/Admission Control 계열 중 하나를 paper card로 정리한다.
- paper card를 하나 작성한 뒤 `surveys/comparison_table.md`, `surveys/claim_bank.md`, `surveys/related_work_map.md`, `decisions/open_questions.md`에 반영한다.
- 한 번에 여러 논문을 깊게 요약하지 말고, 핵심 논문 1편 단위로 진행한다.

### 6. 주의해야 할 점

- 논문 venue, year, dataset, metric, result, 실험 환경은 원문에서 확인한 경우에만 적는다.
- PDF 전문을 읽지 않은 논문은 제목 기반 inventory 수준으로만 유지한다.
- 연구 novelty를 과장하지 않는다.
- `machine condition + system slack + W/H/M` 조합이 현재 연구의 중심 비교축이다.
- PDF 원본, 로컬 텍스트 추출본, source 자료는 GitHub에 올리지 않는다.
- 중복 의심 파일은 해시나 원문 차이를 확인하기 전 삭제하지 않는다.
- 기존 파일의 사용자 변경은 임의로 되돌리지 않는다.

### 7. git commit 전에 확인해야 할 사항

- `git status -sb`로 staged/unstaged 상태를 확인한다.
- `git diff`와 `git diff --cached`로 의도하지 않은 변경이 섞였는지 확인한다.
- `git diff --check`로 공백 오류를 확인한다.
- `git ls-files --others --exclude-standard`로 새로 추적될 파일을 확인한다.
- PDF 파일과 `paper_text/` 추출본이 staged 상태에 들어가지 않았는지 확인한다.
- commit message는 작업 범위를 짧게 설명한다.
- commit 후 `git push origin main`을 수행하고 `git status -sb`가 `main...origin/main`인지 확인한다.

### 마지막 커밋

- `b8495fe Organize paper survey structure and cards`
- `origin/main`에 푸쉬 완료.
