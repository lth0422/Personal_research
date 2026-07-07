# paper_card_prompt

논문 한 편을 정리할 때 아래 형식으로 `surveys/paper_cards/{그룹번호_그룹명}/{짧은제목}.md`에 작성한다.
정리 후 `surveys/comparison_table.md`의 표에 한 행을 추가한다.

---

## 카드 형식

```md
# {논문 제목}

- **그룹**: 1~8 (PROJECT_CONTEXT 10절)
- **출처/연도**:
- **저자**:

## 두 질문
- **가변 변수**: (period / 입력크기 / model / batch / exit / 없음 ...)
- **트리거**: (부하 / 자원경합 / criticality / 없음=offline / 기계상태 ...)

## Abstract 3줄 요약
- 
- 
- 

## Conclusion 요약
- 

## 요점
- 플랫폼:
- 도메인:
- 핵심 방법 (2~3줄):
- 정식화/수식 (있으면):

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것):
- 내 연구에 쓸 곳: (related work ○절 / 수식 근거 / 비교군 / 방법론)
- 인용할 문장 (있으면, 15단어 이내):

## 불확실한 점
- 확인 필요:
```

---

## 작성 원칙

- 길게 쓰지 않는다. 카드 한 장 = 비교표 한 행이 목표.
- 정확도/시간 trade-off를 다루는 논문은 "무엇을 줄여 무엇을 얻나"를 명확히.
- 수식이 있으면 핵심 식 한두 개만 옮기고, 변수 정의를 PROJECT_CONTEXT 기호와 맞춘다.
- 원문 장기 인용 금지. 요약은 자기 말로.
- 논문 출처, venue, year, dataset, metric, result, 실험 환경이 불확실하면 임의로 채우지 않고 `확인 필요`로 표시한다.
- `Abstract 3줄 요약`은 abstract에 명시된 문제, 방법, 평가 또는 주장만 자기 말로 압축한다.
- `Conclusion 요약`은 conclusion 또는 마지막 discussion에서 확인 가능한 결론과 future work만 적는다. 결론 섹션이 확인되지 않으면 `확인 필요`로 둔다.
- paper card 작성 후 남는 불확실한 점은 카드의 `불확실한 점` 섹션에 명시한다.
