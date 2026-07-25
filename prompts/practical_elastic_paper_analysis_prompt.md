# Practical Elastic Scheduling 논문 분석 프롬프트

> 사용 대상: elastic scheduling을 실제 시스템에 적용한 논문 분석  
> 대상 논문 예시: Decntr [17], Salman [16], Burgio [15], Safety-Aware [18], ATER [19]  
> 출력: Notion 붙여넣기용 마크다운

---

## 사용 방법

1. 아래 "== 컨텍스트 ==" 블록을 맨 앞에 붙인다.
2. "== 분석 요청 ==" 블록을 이어 붙인다.
3. 논문 PDF를 첨부하거나 페이지 이미지를 붙여넣는다.

---

## == 컨텍스트 ==

나는 석사 과정 연구자로, 실시간 진동 기반 결함 진단(vibration fault diagnosis) 시스템을 엣지 디바이스(Raspberry Pi Zero 2W, PREEMPT_RT)에서 실행하는 연구를 하고 있다.

**내 연구의 핵심 구조:**

각 진단 설정을 모드 튜플 `a = (W, H, M)`으로 정의한다.
- W: 입력 진동 신호의 윈도우 크기
- H: 연속 진단 창 간 hop 크기. 진단 주기 `T = H / f_s`
- M: 추론 모델 또는 추론 설정
- 모드마다 실행시간이 달라진다: `C(W, M)`

**정책 정식화:**
```
A_feasible(k) = { a ∈ A | R_a_tail ≤ D_a  AND  U_bg + U_a ≤ U_bound }
a*_k = argmax Q(a, z_k),   a ∈ A_feasible(k)
```
- `z_k`: 현재 기계 상태 (anomaly score 후보)
- `S_k = D - p99(R_recent)`: tail 기반 슬랙

**서베이 분류 체계 (6섹션):**
- S3: 탄력적 주기·부하 스케줄링
- S4: 데드라인 인식 AI 추론
- S6: 모드 전환·Weakly-Hard

**투고 목표:** RTAS 2027 (stretch) / RTCSA 2027 (main)

**논문 정리 시 항상 답해야 할 두 질문:**
1. 가변 변수가 무엇인가? (period T / 입력 크기 W / model M / batch / ...)
2. 적응을 무엇이 트리거하는가? (시스템 부하 / 자원경합 / criticality / 기계 상태 / offline only)

---

## == 분석 요청 ==

첨부한 논문을 읽고 아래 형식으로 분석해줘. 출력은 Notion에 바로 붙여넣을 수 있는 마크다운으로 작성해줘.

---

### 1. 기본 정보

- **논문 제목:**
- **저자:**
- **출처/연도/venue:**
- **DOI:**

---

### 2. 한 줄 요약

이 논문이 해결하는 문제를 한 문장으로 정리해줘.

---

### 3. 두 핵심 질문 답변

**가변 변수는 무엇인가?**
(구체적으로: period T인지, 입력 크기인지, 모델인지, 자원 배분인지)

**적응 트리거는 무엇인가?**
(runtime인지 offline인지, 무엇을 관측해서 언제 바꾸는지)

---

### 4. 주된 가정

아래 항목별로 이 논문이 무엇을 가정하는지 정리해줘.

| 가정 항목 | 이 논문의 가정 |
|---|---|
| task 실행시간 C | (고정 WCET / runtime 관측값 / 자원 배분별 table / ...) |
| 실시간 보장 수준 | (hard / soft / empirical) |
| 플랫폼 | |
| mode/configuration 공간 | (사전 열거 / runtime 생성) |
| 트리거 | (runtime event / offline only) |
| 선형성·수학적 가정 | (linear plant / 정규분포 / 없음 / ...) |

---

### 5. 접근 방법 단계별 정리

offline phase와 runtime phase를 구분해서 각 단계를 순서대로 설명해줘. 핵심 알고리즘이나 수식이 있으면 함께 써줘.

**Offline phase:**

**Runtime phase:**

---

### 6. 보장 방식

schedulability, safety, utility 등을 어떻게 보장하는지, 그 보장이 어떤 조건에 의존하는지 써줘.

---

### 7. 내 연구 관점 분석

**유사점 — 내 연구에서 참고할 수 있는 것:**
(구조, 알고리즘, 정식화, 실험 방법 등)

**차이점 / gap — 내 연구의 차별화 지점:**
(내 연구에 있고 이 논문에 없는 것, 또는 반대로 이 논문이 다루지 않는 것)

**이 논문을 related work로 쓸 때 적합한 섹션:**
(S3 / S4 / S6 중 어디에 배치할지, 어떤 맥락에서 인용할지)

---

### 8. 서베이 표 항목 (한 줄 요약)

내 서베이 표에 바로 쓸 수 있도록 각 항목을 15단어 이내로 채워줘.

| 항목 | 내용 |
|---|---|
| 가변 변수 | |
| 트리거 | |
| 플랫폼·환경 | |
| 보장 수준 | |
| 본 연구와의 gap | |

---

### 9. 내가 꼭 이해해야 할 핵심 포인트 3가지

이 논문에서 내 연구를 위해 반드시 이해해야 할 개념이나 기법 3가지를 골라서, 각각 왜 중요한지 설명해줘.

---

### 10. 불확실한 점 / 추가 확인 필요 사항

논문에서 명확하지 않거나 내 연구에 적용할 때 별도 확인이 필요한 사항을 적어줘.

---

## [17] Decntr 전용 추가 지시사항

*(이 섹션은 Decntr 분석 시에만 프롬프트에 추가한다. 다른 논문은 제거.)*

위 공통 항목에 더해 아래를 추가로 분석해줘:

**A. mode-change semantics 4단계**
논문의 Step 0~3을 그대로 정리하고, 각 단계에서 내 연구의 mode transition (예: (W=1024,H=512,M1) → (W=512,H=256,M0))에 적용했을 때 어떤 의미인지 대응시켜줘.

**B. carry-over job과 delayed deadline**
내 연구에서 진단 태스크가 mode 전환할 때 carry-over job이 생기는 상황은 언제인지, Decntr의 d_i^c(m',m) 개념을 어떻게 참고할 수 있는지 설명해줘.

**C. WCET = e_i(c, w) 구조**
이 논문은 WCET가 cache/BW 배분에 따라 달라진다. 내 연구의 C(W,M)와 어떻게 유사하고 어떻게 다른지 비교해줘.

**D. controlled invariant set vs. diagnosis utility**
이 논문의 linear plant safety constraint(X_S)를 내 연구의 진단 utility Q(a, z_k)로 교체한다면 무엇이 달라지는지, 그 차이가 본 연구의 novelty 측면에서 어떤 의미인지 설명해줘.
