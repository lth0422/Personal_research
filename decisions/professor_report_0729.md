# 개인 학위연구 진행 보고

> 보고 예정일: 2026-07-29
> 정리 기준일: 2026-07-26
> 작성자: 이태훈

---

## 1. 연구 위치

### 한 줄 연구 질문

제한된 엣지 디바이스에서 진동 기반 결함 진단을 수행할 때, 현재 기계 상태와 시스템 슬랙을 함께 고려하여 입력 윈도우 크기 W와 진단 주기 H를 런타임에 선택하는 정책은 진단 품질과 실시간 스케줄 가능성을 어떻게 동시에 달성할 수 있는가. 모델 구성 M은 후속 확장 변수로 둔다.

### 기존 연구와의 차이

| 연구 계열 | 가변 변수 | 적응 트리거 | 도메인 |
|---|---|---|---|
| 고전 Elastic Scheduling | period T | 시스템 부하 | 일반 RT |
| Sudvarg 계보 RTAS/RTSS | period, subtask | 부하·멀티코어 | 일반 RT |
| Elastic DNN 계열 | batch, fusion | 자원 경합 | edge GPU, perception |
| 입력 적응 계열 CANVAS 등 | 입력 크기 | criticality | vision |
| 결함 진단 적응 계열 AIL, ADW | window | 없음, offline 설계 | 진동 FD |
| **본 연구** | **W, H 우선, M 후속 확장** | **기계 상태 + 시스템 슬랙** | **진동 FD, Pi Zero 2W** |

현재까지 조사한 범위에서, 진동 신호의 시간 창 의미와 결함 상태를 함께 사용해 W와 H mode를 런타임에 선택하고 PREEMPT_RT 환경에서 검증한 사례는 확인되지 않는다. 장기적으로 M까지 확장할 수 있지만, 현재 연구 자리는 우선 W/H와 machine condition/system slack의 결합으로 한정하며 검증할 가설 수준으로 유지한다.

---

## 2. 서베이 현황

### 규모

- 보유 논문: 76편
- 논문 카드: 76개, 논문과 1대1 대응 완료
- 최신 원문 판정 및 카드화 완료 시점: 2026년 7월 24일
- Elastic scheduling 19편의 계보·적용 비교 정리 시점: 2026년 7월 25일

### 분류 체계

논문을 플랫폼 종류가 아닌 연구 질문 기준으로 여섯 섹션에 배치한다.

| 섹션 | 질문 | 대표 논문 | 관리 기준 |
|---|---|---|---|
| S1. 임베디드 실시간 결함 진단 | 결함 진단 연구가 실시간을 어떻게 정의하고 달성하는가 | TinyML bearing, vibration PDM Pi, FRFconv-TDSNet | 카드 교차 태깅 |
| S2. 진단 품질 적응 | 진단 품질을 위해 입력과 모델을 무엇에 따라 바꾸는가 | AIL, ADW, adaptive pruning edge bearing | 카드 교차 태깅 |
| S3. 탄력적 주기·부하 스케줄링 | 시스템 부하 아래에서 주기와 연산을 어떻게 조절하는가 | Buttazzo 1998·2000·2002, Sudvarg RTAS 2024, ATER | 카드 교차 태깅 |
| S4. 데드라인 인식 AI 추론 | 슬랙과 데드라인 아래에서 모델·입력을 어떻게 선택하는가 | DNN-SAM, SCENIC, BCEdge, EdgeServing | 카드 교차 태깅 |
| S5. 스케줄 가능성·모드 전환·miss 의미 | 모드 전환 시 가능성 보장과 허용 miss 조건은 무엇인가 | Safety-Aware RTCSA 2023, Decntr, Baruah 2023, Hawila ECRTS 2025 | 카드 교차 태깅 |
| S6. 런타임 플랫폼·간섭 특성화 | PREEMPT_RT와 SBC에서 실제 지연과 분포는 어떻게 나타나는가 | OSPERT 2024, Pi 5 RT assessment, Adam 2021 | 카드 교차 태깅 |

S1~S6는 상호 배타적인 논문 수 분류가 아니다. 논문 한 편이 여러 연구 질문에 연결될 수 있으므로 정확한 전체 수량은 보관 그룹 8개의 합계 76편으로 관리한다.

---

## 3. 관련연구 계열별 핵심 발견

### S1: 임베디드 실시간 결함 진단

- 기존 연구의 실시간 주장은 세 수준으로 구분된다
  - model-level best-effort: 평균 레이턴시만 보고, 데드라인 없음
  - empirical deadline-aware: 실험으로 데드라인 충족 확인, tail 지표 없음
  - schedulability-backed: 이용률 분석이나 형식 보장 포함
- 조사한 14편 중 tail latency, 데드라인 miss rate, schedulability를 함께 다룬 사례는 확인되지 않음
- 본 연구의 비교 기준점 역할

### S2: 진단 품질 적응

- AIL, ADW 등은 window 크기를 offline에서 설계하거나 신호 특성만 사용해 선택
- 기계 상태와 시스템 슬랙을 runtime에 함께 사용하는 사례 미확인
- 물리 기반 최소 입력 길이 논거 확인: patch 크기와 샘플링 주파수, 회전수의 관계

### S3: 탄력적 주기·부하 스케줄링

- 고전 elastic scheduling은 대체로 실행시간 C를 고정하고 period T를 조절
- Buttazzo and Abeni 2000은 관측 실행시간을 feedback으로 사용하지만 transient miss를 허용하는 soft real-time 예외
- 최신 계열은 discrete mode, 병렬 DAG, harmonic period까지 확장됨
- 공통 한계: 진동 진단 특화 window 의미, 기계 상태 트리거, 진단 유용성 없음
- 본 연구 연결점: `T_a = H_a / f_s` 구조로 diagnosis period를 elastic variable로 볼 때 비교 기준

### S4: 데드라인 인식 AI 추론

- DNN-SAM: 재확보된 슬랙을 입력 품질과 연결. 슬랙 기반 입력 선택 자체는 새 주장 아님
- SCENIC: 환경, 모델 능력, 타이밍, 유용성을 offline에서 공동 설계. runtime 조건 트리거 없음
- 따라서 "슬랙→입력·모델 선택"만으로는 차별화 부족. 진단 특화 temporal fidelity, 기계 상태, feasible mode selection, transition 검증의 결합이 남는 질문

### S5: 스케줄 가능성·모드 전환·Deadline Miss Semantics

- Baruah 2023: constrained deadline elastic task에 PDA 적용, 고정 C 전제
- Decntr: controller mode와 period를 offline에서 합성. runtime 기계 상태 없음
- Hawila ECRTS 2025: 제어 안정성 구역에서 허용 miss 도출. 진동 진단 utility와 직접 대응 안 됨
- Weakly-hard는 `(m,K)` bounded miss를 제공하는 대안적 보장 모델이며, 현재 조사한 진동 고장진단 문헌에서 직접 채택한 사례는 확인되지 않음
- 본 연구 연결: 모드 전환 시 carry-over job, transition cost, feasibility 조건 설계 참고

### S6: 플랫폼·OS 타이밍 특성화

- PREEMPT_RT는 tail latency와 deadline miss 억제에 유효함을 여러 SBC 연구가 실증
- Pi Zero 2W에서 결함 진단 파이프라인을 실행하고 부하 조건별 tail·miss를 측정한 사례 미확인
- 본 실험이 이 비교군 역할

---

## 4. 연구 문제 구체화

### 모드 정의

각 진단 설정을 모드 튜플로 정의한다.

```
a = (W, H, M)
  W: 입력 윈도우 크기
  H: 연속 진단 창 간 hop 크기
  T = H / f_s: hop으로 결정되는 진단 주기
  M: 모델 또는 추론 설정
```

장기 정식화는 `M`을 포함하지만 첫 구현에서는 `M`을 고정하고 `(W,H)` mode bank를 검증한다.

### 핵심 인사이트: W 축소가 항상 유리하지 않다

직관적 이해는 틀릴 수 있다.

```
[일반적 기대]
  W 감소 → C 감소 → 데드라인 여유 증가

[실제 이용률]
  U_a = C_a / T_a,  T_a = H_a / f_s

  W 감소 + H도 함께 감소 → T 감소
  → U = C/T 는 오히려 증가 가능
```

KCC 2026 STM32F407 측정값 기준 이용률 확인:

| W | C max | T 비중첩 기준 | U = C/T |
|---:|---:|---:|---:|
| 512 | 40.3 ms | 64 ms | 0.63 |
| 1024 | 129.8 ms | 128 ms | 1.01 |
| 2048 | 460.3 ms | 256 ms | 1.80 |

W와 H를 독립적으로 고르기보다 이산 mode tuple 집합에서 선택해야 하는 이유다. 이후 M을 추가할 때도 같은 mode-bank 구조를 유지한다.

### 정책 정식화

후보 모드 집합 A가 주어졌을 때, 단계 k에서 현재 기계 상태 z_k와 슬랙 정보를 사용하여 실시간 가능성을 만족하는 모드 중 진단 유용성이 가장 높은 모드를 선택한다.

```
A_feasible(k) = { a ∈ A | R_a_tail ≤ D_a  및  U_bg + U_a ≤ U_bound }

a*_k = argmax Q(a, z_k)
       a ∈ A_feasible(k)
```

- `Q(a, z_k)`: 모드 a의 기계 상태 z_k에서의 진단 유용성
- `R_a_tail`: 실측 tail response time (p99 또는 최대값 기준)
- `U_bound`: 이용률 상한

슬랙은 평균이 아닌 tail 기반으로 정의한다.

```
S_k = D - p99(R_recent)
```

### 정책 구조 개요

```
1. 최근 응답시간 이력으로 실시간 가능 모드 집합 구성
2. 가능 모드 집합이 비어 있으면 사전 정의된 fallback 실행
3. 가능 모드 중 현재 기계 상태에서 진단 유용성 최대 모드 선택
4. 모드 전환 잦음 방지를 위해 hysteresis 조건 적용
```

---

## 5. 남은 과제

### 즉시 처리 필요

- 후보 모드 집합 A 확정: W와 H 값 조합, 초기 고정 M
- Pi Zero 2W에서 모드별 실행시간 프로파일링 구현: C_mean, p95, p99, max
- 모드 가능성 표 작성: W/H/M별 U, R_tail, deadline miss ratio

### 연구 설계 미결 항목

- M 확장 조건: W/H 실험 이후 별도 모델, 양자화 변형 또는 early-exit를 추가할 필요가 있는가
- z_k 정의: anomaly score, health index, confidence, fault probability 중 선택
- 슬랙 정의 엄격도: p95, p99, max 중 어느 기준을 채택하는가
- 데드라인 모델: implicit deadline D=T 또는 constrained deadline D < T

### 서베이 보강 필요

- 고전 실시간 이론 개념 정리: imprecise computation, mode change, EDF·CBS·weakly-hard 통합 노트
- 결함 진단 분류표: RTOS 유무, 데드라인, tail latency, miss 기준의 직접 비교군 보강
- KCC 실행시간 로그: average, p95, p99, max 기준 이용률 재계산

### 투고 전략

- RTAS 2027: stretch goal. 2026년 10월 결정 게이트 통과 시 투고 검토
- RTCSA 2027: 현실적 main target. 2027년 3~4월 예정

## 6. 보고용 근거 문서

- `surveys/comparison_table_ko.md`: Real-Time Fault Diagnosis, elastic scheduling, deadline-aware inference와 PREEMPT_RT 한글 비교표
- `surveys/elastic_scheduling_survey.md`: Elastic scheduling 19편의 이론 계보와 실제 적용 비교
- `manuscript/realtime_fault_diagnosis_related_work_table.md`: Real-Time Fault Diagnosis O/△/X 원고용 압축표
- `manuscript/related_work_draft_ko.md`: 번호 인용과 참고문헌 목록을 포함한 관련연구 한글 초안

---

*이 문서는 2026-07-29 교수님 보고를 위한 초안이다. 서베이 상태는 2026-07-26 기준이며 정량 결과는 실험 완료 후 추가한다.*
