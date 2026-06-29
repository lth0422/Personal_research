# CLAUDE.md

이 repo는 이태훈의 석사 개인연구(실시간 결함 진단 + elastic scheduling) 작업 공간이다.

## 작업 시작 전 필수

- **항상 `PROJECT_CONTEXT.md`를 먼저 읽고** 연구 배경·핵심 식·용어를 파악한 뒤 작업한다.
- 논문 정리는 `prompts/paper_card_prompt.md` 규칙을 따른다.
- 연구 주장은 `surveys/claim_bank.md`를 기준으로 한다.
- 불확실하거나 판단이 필요한 내용은 `decisions/open_questions.md`에 남긴다.

## 작성 규칙

- 한국어로 작업한다.
- 학술 문서에 괄호 사용을 자제한다 (지도교수 지침).
- 교수님 보고용 문서는 개조식으로 간결하게, 내부 노트는 상세하게.
- 단정적 표현을 피하고, 근거가 약하면 그렇게 표시한다.
- 논문 요약 중 확인하지 못한 정보는 paper card의 `불확실한 점` 섹션에 명시한다.

## 협업 규칙

- 한 번에 한 파일만 수정하고, 의미 있는 단위로 git commit 한다.
- 큰 변경 전에는 무엇을 바꿀지 먼저 요약하고 진행한다.
- 다른 에이전트(Codex 등)와 같은 파일을 동시에 건드리지 않는다.

## 폴더 역할

- `surveys/` — 논문 카드, 비교표, 관련연구 맵 (머리 트랙)
- `papers/` — PDF 원본 (그룹 1~8, PROJECT_CONTEXT 10절 참고)
- `experiments/` — Pi Zero 2W / PREEMPT_RT / 파이프라인 / 측정 결과 (손 트랙)
- `manuscript/` — KSC 논문 초안
- `prompts/` — 재사용 프롬프트
- `decisions/` — 미해결 질문 로그

## 핵심 서베이 원칙

각 논문을 읽을 때 두 질문에 반드시 답한다:
1. **가변 변수가 무엇인가?** (period / 입력크기 / model / batch / exit ...)
2. **적응을 무엇이 트리거하는가?** (부하 / 자원경합 / criticality / 없음=offline / 기계상태)

답이 "입력 window + 기계 상태"인 논문이 나오면 즉시 알리고 차별점을 재점검한다.
