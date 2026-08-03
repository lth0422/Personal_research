# 주제 구체화 - Codex v1_2

> 문서 버전: Codex v1_2<br>
> 작성일: 2026-08-02<br>
> 문서 성격: 학위연구 주제 구체화 및 교수님 논의용 개조식 초안<br>
> 현재 근거 범위: 정독 완료 섹션 `elastic scheduling` 19편, `real-time fault diagnosis` 20편<br>
> 현재 한계: `adaptive input`과 `real-time DNN serving`은 정독 완료 전이므로 확정적 novelty 판단에서 제외

---

## 가제

### 국문

**기계 상태와 시스템 시간 여유를 고려한 실시간 진동 결함 진단의 탄력적 모드 선택**

### English

**Machine-Condition- and System-Slack-Aware Elastic Mode Selection for Real-Time Vibration Fault Diagnosis**

### 대안 제목

- **진동 결함 진단을 위한 Feasibility-First Elastic Scheduling: 입력 윈도우와 진단 주기의 런타임 선택**
- **Feasibility-First Runtime Selection of Window Size and Diagnosis Period for Vibration Fault Diagnosis**
- 현재는 첫 번째 가제를 기준으로 사용
- 초기 구현에서 모델을 고정하므로 제목에 `W/H/M joint adaptation`은 사용하지 않음
- Linux와 PREEMPT_RT는 평가 환경이며 논문의 핵심 방법이 아니므로 가제에서 제외

## Keywords

`Real-Time Fault Diagnosis`, `Elastic Scheduling`, `Runtime Mode Selection`, `Vibration Analysis`, `System Slack`, `Deadline-Aware Inference`, `Schedulability`

---

## 0. 연구 핵심 요약

- **대상 문제**
  - 진동 결함 진단의 입력 윈도우 크기 `W`와 진단 주기를 결정하는 hop size `H`가 설계 시점에 고정됨
  - 큰 윈도우와 짧은 진단 주기는 진단 정보와 갱신 빈도를 높일 가능성이 있으나 연산 부하와 마감시간 위반 위험을 증가시킴
  - 작은 윈도우와 긴 진단 주기는 연산 부하를 낮추지만 결함 정보 손실 또는 감지 지연 가능성이 있음

- **핵심 질문**
  - 기계 상태가 정밀 진단을 요구할 때에도 선택한 진단 모드가 시간 제약을 만족하는가?
  - 만족 여부를 실행 후 관찰하는 것이 아니라 선택 전에 어떻게 판정할 것인가?

- **제안 방향**
  - 진단 모드를 `(W, H, M)`의 조합으로 정의
  - 초기 연구에서는 모델 `M`을 고정하고 `(W,H)`만 조절
  - 각 모드의 실행시간 분포와 진단 성능을 사전에 측정
  - 런타임에는 시간 제약을 만족하는 모드만 남긴 뒤 현재 기계 상태에 가장 적합한 모드를 선택

- **평가 환경**
  - Raspberry Pi Zero 2W
  - 일반 Linux와 실시간 선점 기능을 강화한 Linux kernel patch set인 PREEMPT_RT
  - 진동 기반 fault diagnosis inference pipeline

- **주장 수준**
  - 초기 목표: 실측 기반 마감시간 충족 가능성인 `empirical deadline feasibility`
  - 현재 주장하지 않는 것: formal worst-case execution time과 hard real-time guarantee

---

## 1. Background

### 1.1 문제 배경

- 진동 기반 fault diagnosis의 기본 흐름
  - 센서에서 일정 길이의 진동 신호 수집
  - 입력 윈도우 구성
  - 전처리와 추론 수행
  - 진단 결과 출력

- 입력 윈도우 크기 `W`
  - 단위: sample 수
  - 포함되는 회전 주기, 고장 특징 성분과 transient information에 영향
  - 연산량만 줄이는 일반적인 image resizing 변수와 동일하게 취급할 수 없음

- hop size `H`
  - 연속된 두 입력 윈도우 시작점 사이의 sample 간격
  - sampling frequency를 `f_s`라고 할 때 진단 태스크 도착 주기 `T`를 결정

```text
T = H / f_s
```

- 핵심 상충 관계
  - `W` 증가: 더 많은 신호 문맥을 제공할 가능성, 실행시간과 memory 증가 가능성
  - `H` 감소: 더 자주 진단, 시스템 이용률 증가 가능성
  - `W`와 `H`를 별도로 선택하면 실행시간, 진단 성능과 갱신 빈도를 함께 조절 가능

### 1.2 Elastic scheduling에서 확인한 기반

- Classic elastic task model
  - 주기 태스크의 period를 탄성 변수로 설정
  - 시스템 과부하 또는 rate-change request 발생 시 이용률 상한 안에서 period를 재분배 [1], [2]
  - 본 연구의 `H`를 조절하여 진단 주기 `T=H/f_s`를 바꾸는 논리적 기반

- 기존 모델의 대표 가정
  - 태스크 실행시간 `C`를 고정
  - period만 허용 범위 안에서 변경
  - 본 연구에서는 윈도우와 모델 설정에 따라 실행시간 `C(W,M)`도 함께 달라짐

- 실전 응용에서 확인한 확장
  - 제어 시스템의 **제어 품질(Quality of Control, QoC)**을 유지하기 위해 period를 조절하는 연구 존재 [3]
  - Quality of Control은 제어 응답의 안정성, 추종 오차와 같은 제어 성능의 품질을 의미
  - Decntr는 controller mode와 resource allocation을 사전에 함께 설계하고 runtime mode transition을 다룸 [4]
  - ATER는 Robot Operating System 2인 ROS 2 환경에서 sensor task rate를 runtime에 조절함 [5]

- 본 연구와의 차이
  - 기존 utility: control safety, Quality of Control 또는 task-rate 요구
  - 본 연구 utility: 기계 상태별 결함 진단 성능과 진단 결과의 적시성
  - 기존 variable: period, resource, controller mode
  - 본 연구 variable: 진동 입력 윈도우 `W`, hop size `H`, 향후 model `M`

### 1.3 Real-Time Fault Diagnosis 연구가 대부분 best-effort로 분류된 이유

- **여기서 best-effort의 의미**
  - 논문 저자가 해당 시스템을 best-effort라고 직접 명명했다는 뜻이 아님
  - 현재 비교 기준에서 formal deadline, tail latency, deadline miss와 schedulability evidence가 부족하다는 판정
  - 빠른 평균 실행시간 또는 센서 데이터 수집 주기 안에서 처리 완료만 보인 경우를 포함

- **현재 검토 결과**
  - 정독한 20편은 현재 분류표에서 모두 `B`, 즉 model-level 또는 pipeline-level best-effort로 판정
  - 대표 연구들은 lightweight architecture search, 양자화, pruning, compressed sensing 또는 경량 network로 평균 실행시간과 배포 비용을 낮춤 [7]--[12]
  - 일부 논문은 센서 데이터를 한 번 수집하는 주기인 **데이터 수집 간격(acquisition interval)** 또는 처리량과 실행시간을 비교
  - 그러나 태스크별 마감시간 정의, 최악 구간의 지연시간, 마감시간 위반 횟수와 scheduling 분석을 동시에 제시한 사례는 현재 검토 범위에서 확인하지 못함

- **왜 이런 연구 관행이 형성되었을 가능성이 있는가**
  - 기계 고장 진단 분야의 주된 평가 대상이 진단 정확도, noise robustness와 model size임
  - predictive maintenance application은 제어 루프처럼 공통된 millisecond 단위 deadline이 미리 정의되지 않는 경우가 많음
  - 논문마다 sensing interval, 회전 속도, 고장 진행 시간과 유지보수 요구가 달라 application-level deadline을 일반화하기 어려움
  - 많은 연구가 단일 추론 또는 offline dataset replay로 평가되어 동시 실행 태스크와 운영체제 간섭을 모델링하지 않음
  - 따라서 `real-time`을 deadline guarantee보다 현장에서 충분히 빠르게 동작한다는 operational meaning으로 사용하는 경향이 나타남

- **해석의 한계**
  - 위 설명은 현재 20편의 공통 패턴에서 도출한 해석
  - 분야 전체가 real-time requirement를 갖지 않는다는 의미가 아님
  - 실제 안전 요구, 허용 가능한 detection delay와 miss semantics는 application별 추가 조사가 필요
  - 원고에서는 “확인한 문헌 범위에서는”이라는 범위 제한을 유지

### 1.4 Deadline-aware Deep Neural Network 연구가 주는 반례

- DNN-SAM
  - Deep Neural Network Split-and-Merge인 DNN-SAM
  - object detection을 안전 중요 영역의 mandatory subtask와 전체 image의 optional subtask로 분리
  - mandatory 실행이 일찍 끝나 발생한 남은 시간인 reclaimed slack으로 optional input scale을 선택 [6]
  - non-preemptive Earliest Deadline First scheduling의 충분조건 아래 timing constraint를 분석

- 본 연구에 주는 교훈
  - `system slack -> input fidelity` 자체는 novelty가 아님
  - “slack이 넉넉하면 큰 입력을 선택한다”는 설명만으로는 부족
  - 진동 시간축의 `W/H` 의미, machine condition, mode별 진단 utility와 transition feasibility가 함께 검증되어야 함

### 1.5 현재 연구 gap

- Real-Time Fault Diagnosis 계열
  - model과 input 경량화 연구는 존재 [7]--[12]
  - 명시적 마감시간, tail behavior, scheduling과 runtime diagnosis-mode selection의 결합은 현재 검토 범위에서 제한적

- Elastic Scheduling 계열
  - period와 resource adaptation, schedulability 분석은 존재 [1]--[5]
  - vibration window의 신호 의미와 machine-condition-driven utility는 다루지 않음

- Deadline-Aware DNN 계열
  - slack 기반 input fidelity 선택이 이미 존재 [6]
  - 주로 vision input의 공간 해상도와 GPU scheduling을 대상으로 함

- 남은 연구 자리
  - 진동 진단의 시간축 mode `(W,H)`를 정의
  - machine condition에 따라 필요한 diagnostic fidelity를 구분
  - system timing feasibility를 먼저 검사
  - feasibility를 만족하는 범위 안에서 diagnosis mode 선택

---

## 2. Research Questions and Current Answers

### 2.1 정밀 모드로 전환해도 항상 schedulable한가?

- **질문**
  - 이상 징후가 발생해 더 큰 윈도우 또는 더 짧은 진단 주기가 필요할 때 해당 모드는 마감시간을 만족하는가?
  - mode transition 순간까지 포함해 어떻게 보장할 것인가?

- **현재 답변**
  - 모든 후보 모드를 자유롭게 선택하지 않음
  - 사전 profiling과 admission test를 통과한 mode bank만 runtime 후보로 사용
  - runtime에는 현재 부하를 반영하여 다시 feasible mode set을 계산
  - 정밀 모드가 infeasible하면 가장 정밀한 모드가 아니라 **가장 유용한 feasible mode**를 선택
  - mode transition cost와 진행 중인 inference의 carry-over demand를 별도 비용으로 포함

- **현재 보장 수준**
  - 응답시간 분포의 99번째 백분위수인 p99 또는 관찰된 최댓값인 observed max 기반 empirical feasibility
  - formal hard real-time 보장은 conservative execution bound와 scheduler assumption이 확보된 뒤에만 검토

### 2.2 실험에서 시스템 부하를 주어야 하는가?

- **질문**
  - fault diagnosis만 단독 실행하면 되는데 중앙처리장치인 Central Processing Unit, CPU와 memory 또는 input/output 부하를 추가할 필요가 있는가?

- **현재 답변**
  - **필요함. 단, 임의의 stress 목록을 실험의 최종 부하로 확정하면 안 됨.**

- **부하가 필요한 이유**
  - system slack은 경쟁 workload가 없으면 대부분 일정하여 runtime adaptation의 필요성을 검증하기 어려움
  - Linux에서는 scheduling delay, cache와 memory bandwidth, input/output blocking이 tail response time에 영향을 줄 수 있음
  - mode별 feasibility boundary가 system interference에 따라 어떻게 이동하는지 확인해야 함
  - 제안 정책이 단순히 빠른 mode를 고르는 것이 아니라 변화한 여유 안에서 feasible mode를 고른다는 점을 검증해야 함

- **부하 설계 원칙**
  - 1단계: CPU, memory, input/output 등 단일 자원 부하로 민감도 파악
  - 2단계: 실제 pipeline과 함께 실행될 background task를 모사한 대표 workload 구성
  - 3단계: 유사 Linux/PREEMPT_RT 논문의 부하 설계를 근거로 강도와 조합 결정
  - 부하 강도는 low/medium/high라는 이름만 붙이지 않고 실제 CPU utilization, memory bandwidth와 input/output rate로 기록
  - stress workload 자체가 novelty가 아니라 policy의 feasibility 판정과 robustness를 검증하는 수단

### 2.3 모델은 고정해서 사용해야 하는가?

- **질문**
  - 연구 목표가 `(W,H,M)` elastic scheduling이라면 처음부터 여러 model `M`을 함께 변경해야 하는가?

- **현재 답변**
  - 초기 구현에서는 **모델을 고정**하는 것이 타당

- **고정하는 이유**
  - `W`와 `H`의 효과를 model architecture 변화와 분리하여 측정 가능
  - model loading, memory replacement와 cache warm-up이 만드는 transition cost 제거
  - mode 수 폭증을 막아 schedulability 분석과 baseline 비교를 명확하게 유지
  - 첫 번째 contribution을 diagnosis-specific `(W,H)` coupling과 feasibility-first selection으로 집중

- **일반화 방법**
  - runtime policy는 model 내부 구조가 아니라 mode별 execution profile과 utility table을 사용
  - 다른 model도 동일한 profiling interface를 통과하면 mode bank에 추가 가능
  - 정책은 공통으로 유지하되 mode bank는 model별로 다시 구성

- **후속 확장 조건**
  - 서로 다른 model이 `(W,H)`만으로 얻지 못하는 새로운 accuracy-latency Pareto point를 제공할 때 `M` 추가
  - model-switch overhead를 포함해도 장기적인 이점이 남을 때 `M` 추가
  - 위 조건을 만족하지 않으면 학위연구에서도 `M`은 고정하고 제한사항으로 명시

### 2.4 시스템 시간 여유가 부족하거나 충분하다는 기준은 무엇인가?

- **질문**
  - “slack이 부족하다” 또는 “slack이 넉넉하다”를 어떤 숫자로 판정할 것인가?

- **현재 답변**
  - 모든 모드에 공통인 임의 threshold 하나를 사용하지 않음
  - 후보 모드마다 **모드별 feasibility margin**을 계산

- **시간 기준**

```text
TimeMargin_j(k)
  = Deadline_j
  - PredictedTailResponse_j(k)
  - TransitionCost_current_to_j
  - GuardBand_j
```

- `PredictedTailResponse_j(k)`
  - mode `j`의 offline p99 또는 observed max profile
  - 최근 runtime interference로 보정

- `TransitionCost_current_to_j`
  - buffer 재구성, policy 결정과 mode switch 비용

- `GuardBand_j`
  - profiling 오차와 run 간 변동을 흡수하는 안전 여유
  - calibration run과 validation run을 분리하여 validation에서 target miss ratio를 넘지 않는 최소값으로 설정
  - 하나의 값만 보고하지 않고 guard band sensitivity analysis 수행

- **이용률 기준**

```text
UtilMargin_j(k)
  = UtilizationBound
  - OtherTaskUtilization(k)
  - DiagnosisUtilization_j
```

- **판정**
  - `TimeMargin_j(k) >= 0`이고 `UtilMargin_j(k) >= 0`: 현재 조건에서 mode `j`가 empirically feasible
  - 둘 중 하나라도 음수: 현재 조건에서 mode `j` 선택 금지
  - 따라서 slack의 “부족/충분”은 절대 상태가 아니라 **선택하려는 mode에 상대적인 상태**

- **DNN-SAM과의 관계**
  - DNN-SAM은 actual mandatory execution 이후 deadline까지 남은 slack에 들어가는 최대 optional scale을 선택 [6]
  - 본 연구는 하나의 job 내부 optional scale보다 다음 diagnosis job의 `(W,H)` mode를 선택
  - DNN-SAM의 reclaimed-slack 원칙은 참고하되, Linux 측정 변동과 transition cost를 포함한 보수적 prediction 필요

### 2.5 Diagnostic utility는 무엇으로 정하는가?

- **질문**
  - feasible mode가 여러 개이면 “가장 유용한 mode”를 어떤 지표로 결정할 것인가?

- **현재 답변**
  - timing metric과 diagnosis metric을 근거 없이 하나의 weighted sum으로 합치지 않음
  - 먼저 timing feasibility를 통과시키고, 남은 mode만 diagnostic utility로 비교
  - 초기에는 **사전순위 방식(lexicographic ordering)**을 사용

- **정상 상태의 utility 순서**
  1. 사전에 정한 최소 진단 성능을 만족
  2. 진단 결과의 최대 갱신 간격을 만족
  3. 위 조건을 만족하는 mode 중 diagnosis utilization이 가장 작은 mode 선택

- **이상 의심 또는 fault 상태의 utility 순서**
  1. fault class recall 또는 false-negative rate 우선
  2. detection delay를 정의할 수 있으면 더 짧은 mode 우선
  3. 동률이면 더 짧은 결과 갱신 간격 우선
  4. 다시 동률이면 utilization이 작은 mode 우선

- **threshold 설정 원칙**
  - 최소 진단 성능과 허용 detection delay에 대한 application requirement가 있으면 해당 값을 사용
  - 요구사항이 없으면 임의의 단일값을 주장하지 않고 Pareto frontier와 threshold sensitivity를 제시
  - static dataset만으로 detection delay를 정의할 수 없으면 해당 metric을 제외하고 그 한계를 명시

- **반드시 확인할 사항**
  - anomaly score, model confidence와 machine degradation은 같은 개념이 아님
  - machine-condition indicator는 calibration과 false-negative behavior를 검증한 뒤 선택
  - utility 정의가 확정되지 않으면 condition-aware policy의 contribution도 확정하지 않음

### 2.6 기대하는 최종 답

- `W`와 `H`가 진단 성능, 실행시간과 갱신 빈도에 미치는 영향 정량화
- mode별 feasible region과 infeasible region 구분
- machine condition만 사용하는 정책과 system slack만 사용하는 정책의 실패 조건 확인
- 두 정보를 함께 사용했을 때 얻는 추가 이점을 baseline 대비 검증

---

## 3. Methodology

### 3.1 용어와 기호

| 용어 | 기호 | 의미 |
| --- | --- | --- |
| 입력 윈도우 크기 | `W_j` | mode `j`가 사용하는 진동 sample 수 |
| hop size | `H_j` | 연속 진단 윈도우 시작점 사이의 sample 수 |
| model configuration | `M_j` | model 또는 inference 설정. 초기에는 고정 |
| sampling frequency | `f_s` | 초당 vibration sample 수 |
| 진단 도착 주기 | `T_j` | `H_j/f_s` |
| 실행시간 | `C_j` | inference path가 CPU에서 실제 실행된 시간 |
| 응답시간 | `R_j` | release부터 진단 완료까지 걸린 end-to-end 시간 |
| 마감시간 | `D_j` | mode `j`의 결과가 완료되어야 하는 상대시간 |
| 다른 태스크 이용률 | `U_other` | sensing, logging 또는 background task가 점유하는 CPU 이용률 |
| 진단 태스크 이용률 | `U_diag,j` | mode `j`의 실행시간을 도착 주기로 나눈 값 |
| 기계 상태 지표 | `z_k` | step `k`의 anomaly score, health index 또는 검증된 상태값 |

- 단일 문자 `a` 대신 의미가 드러나는 `mode_j` 사용

```text
mode_j = (W_j, H_j, M_j)
T_j = H_j / f_s
```

- 초기 mode bank

```text
ModeBank_initial = { mode_j = (W_j, H_j, M_fixed) }
```

### 3.2 Offline mode bank 생성

- 후보 `W/H` 선정
  - vibration signal의 물리적 admissibility 확인
  - memory와 model input constraint 확인
  - adaptive-input 문헌 정독 후 최종 후보 확정

- mode별 profile
  - execution time: mean, p95, p99, observed max
  - response time: mean, p95, p99, observed max
  - memory usage
  - 정상 및 fault condition별 classification metric
  - 가능한 경우 detection delay와 maximum update gap

- profile 분리
  - calibration run: prediction과 guard band 설정
  - validation run: 설정한 feasibility rule의 miss ratio 검증
  - test run: baseline과 최종 비교

### 3.3 Feasibility 판정

- 진단 태스크 이용률

```text
U_diag,j = C_j,tail / T_j
```

- 전체 이용률

```text
U_total,j(k) = U_other(k) + U_diag,j
```

- 응답시간 예측

```text
R_pred,j(k)
  = ProfiledTailResponse_j
  + RuntimeInterferenceCorrection(k)
```

- feasible mode set

```text
ModeFeasible(k) = {
  mode_j in ModeBank_initial |
  TimeMargin_j(k) >= 0 and
  UtilMargin_j(k) >= 0
}
```

- `ModeFeasible(k)`가 비어 있는 경우
  - 가장 가벼운 fallback mode 실행 가능 여부를 별도 검사
  - fallback도 불가능하면 overload event 기록
  - 이미 소비한 실행시간을 무시한 재실행은 timing guarantee로 인정하지 않음

### 3.4 Runtime policy

1. 최근 response-time history와 다른 태스크 이용률 `U_other` 갱신
2. 모든 후보 mode의 `TimeMargin`과 `UtilMargin` 계산
3. infeasible mode 제거
4. 현재 기계 상태 `z_k`에 맞는 utility 순서로 feasible mode 정렬
5. 가장 높은 순위의 mode 선택
6. hysteresis와 minimum residence time 확인 후 전환
7. 선택 결과, margin과 실제 response time 기록

### 3.5 Mode transition

- 측정 대상
  - window buffer 재구성
  - policy decision
  - unfinished inference 처리
  - model 변경 시 loading과 cache warm-up
  - 전환 직후 activation jitter

- 초기 모델 고정의 이점
  - model loading 비용 제거
  - transition 분석을 `W/H` 변경으로 제한

- oscillation 방지
  - machine-condition threshold hysteresis
  - minimum residence time
  - 연속 `N`회 조건 충족 후 전환
  - `N`은 sensitivity analysis로 결정

---

## 4. Experiment

### 4.1 실험 목적

- mode별 진단 성능과 timing cost profile 구축
- 부하와 kernel에 따른 feasible region 변화 측정
- feasibility rule의 prediction accuracy 검증
- runtime policy와 baseline의 diagnosis-timing trade-off 비교
- mode transition cost를 포함해도 정책 이점이 유지되는지 확인

### 4.2 플랫폼과 고정 조건

| 항목 | 초기 설정 |
| --- | --- |
| Board | Raspberry Pi Zero 2W, Cortex-A53 quad-core, 512 MB RAM |
| Operating system | Raspberry Pi OS Lite 64-bit |
| Kernel | 일반 Linux, PREEMPT_RT |
| Inference runtime | 실제 사용한 TFLite/LiteRT backend와 version 기록 |
| Initial model | FRFconv-TDSNet의 8-bit integer quantization인 INT8 설정, 첫 실험에서는 고정 |
| Signal | UOS shaft-fault dataset의 8 kHz 조건부터 시작 |
| Repetition | 조건별 최소 3회 후 tail 안정성에 따라 확대 |

- 반드시 기록할 통제 변수
  - kernel version
  - thread 수와 CPU affinity
  - scheduling policy와 priority
  - CPU frequency governor
  - temperature와 throttling
  - data loading, preprocessing, inference와 logging 경계

### 4.3 실험 단계

| 단계 | 질문 | 산출물 |
| --- | --- | --- |
| E1. Mode profiling | `W/H`별 cost와 utility가 어떻게 다른가 | mode profile table |
| E2. Feasibility validation | profile 기반 판정이 독립 run에서도 맞는가 | feasible-mode map, false-admission rate |
| E3. Load sensitivity | 부하에 따라 feasible set이 어떻게 바뀌는가 | resource별 tail/miss 변화 |
| E4. Runtime policy | joint policy가 single-trigger/static보다 나은가 | utility-timing Pareto comparison |
| E5. Transition | switch cost와 transient miss가 발생하는가 | transition-cost matrix |
| E6. Model generalization | 다른 model에도 같은 policy interface가 적용되는가 | 선택적 확장 실험 |

### 4.4 독립 변수

```text
Kernel    = {Linux, PREEMPT_RT}
LoadType  = {idle, cpu, memory, io, representative-mixed}
LoadLevel = measured resource intensity
Mode      = candidate (W, H, M_fixed)
Condition = dataset-supported machine condition
Policy    = baseline and proposed policies
```

- `suspicious` condition이 dataset 또는 detector에서 독립적으로 정의되지 않으면 임의로 생성하지 않음
- 필요한 경우 normal/fault 또는 calibrated score 구간으로 제한

### 4.5 Baselines와 기대 비교

| Baseline | 선택 정보 | 예상되는 약점 | 제안 방법이 기대하는 이점 |
| --- | --- | --- | --- |
| Static-Light | 항상 가장 가벼운 mode | 이상 상태에서도 진단 fidelity가 낮을 수 있음 | feasible할 때 더 높은 fault utility 선택 |
| Static-Heavy | 항상 가장 정밀한 mode | 부하 증가 시 tail latency와 miss 위험 | infeasible mode를 사전에 제외 |
| Condition-Only | machine condition만 사용 | system overload를 무시 | condition 요구를 feasibility 안에서 반영 |
| Slack-Only | system slack만 사용 | 기계 상태와 진단 필요도를 무시 | 같은 slack에서도 condition별 다른 mode 선택 |
| DNN-SAM-style Slack Selection | slack 안의 최대 fidelity 선택 [6] | vibration-specific utility와 `H` 의미가 없음 | temporal `W/H`와 condition utility 결합 |
| Offline Oracle | run 전체를 사후에 알고 최적 mode 선택 | runtime 구현 불가능 | achievable upper bound와 policy regret 측정 |

- **예상 결과와 검증 기준의 구분**
  - 위 이점은 현재 결과가 아니라 검증할 hypothesis
  - 제안 정책이 모든 baseline보다 모든 metric에서 우수하다고 가정하지 않음
  - 최소 기대: Condition-Only 대비 timing 위반 감소, Slack-Only 대비 fault-state utility 개선
  - Static-Light 대비 utility를 개선하면서 miss ratio를 악화시키지 않는지 확인
  - Static-Heavy 대비 utility 손실과 timing 안정성 개선의 trade-off 제시

### 4.6 평가 지표

- **Timing**
  - activation jitter
  - inference time과 end-to-end response time
  - p50, p95, p99와 observed max
  - deadline miss ratio
  - consecutive miss와 maximum update gap
  - false admission: feasible로 예측했지만 deadline을 위반한 비율
  - mode-switch overhead와 transition jitter

- **Diagnosis**
  - macro F1
  - class-wise recall
  - false-negative rate
  - detection delay, 정의 가능한 경우
  - condition별 선택 mode 분포

- **System**
  - CPU utilization과 per-core load
  - memory usage와 bandwidth proxy
  - input/output activity
  - temperature와 throttling
  - policy overhead와 switch frequency

### 4.7 Ablation study

- machine condition 제거: Slack-Only와 동일해지는지 확인
- system feasibility 제거: Condition-Only의 miss 증가 여부 확인
- transition cost 제거: 낙관적 feasibility 판정의 오류 확인
- p99 대신 mean 사용: tail miss를 숨기는지 확인
- `H` 고정: `W` 단독 adaptation과 `(W,H)` 결합의 차이 확인
- guard band 변화: utility와 false-admission의 민감도 확인

### 4.8 성공 조건

- mode별 diagnostic utility와 tail response-time 차이가 반복 실험에서 재현됨
- 부하 변화에 따라 feasible mode set이 실제로 달라짐
- validation run에서 설정한 false-admission 또는 miss 목표를 만족
- Proposed policy가 Condition-Only보다 timing violation을 줄임
- Proposed policy가 Slack-Only보다 fault-state diagnostic utility를 높임
- transition overhead를 포함해도 static baseline 대비 유의미한 trade-off 확보

- 위 조건이 성립하지 않을 경우
  - policy 복잡성을 늘리지 않음
  - mode bank, utility, deadline 또는 machine-condition indicator를 먼저 재정의

---

## 5. Novelty and Expected Benefits

### 5.1 단독 novelty로 주장할 수 없는 요소

- period를 부하에 따라 조절: classic elastic scheduling에 존재 [1], [2]
- control utility에 따라 rate 조절: Quality of Control elastic scheduling에 존재 [3]
- mode와 resource의 offline co-design 및 transition: Decntr에 존재 [4]
- runtime sensor rate regulation: ATER에 존재 [5]
- slack에 따라 input fidelity 선택: DNN-SAM에 존재 [6]
- lightweight fault-diagnosis deployment: 다수 연구에 존재 [7]--[12]

### 5.2 현재 novelty candidate

- **진동 진단에 특화된 mode model**
  - spatial image scale이 아닌 temporal signal window `W`와 diagnosis period `H`를 분리
  - mode-dependent cost `C(W,M)`와 condition-dependent diagnostic utility를 함께 profile

- **Feasibility-first joint trigger**
  - machine condition은 필요한 diagnosis fidelity를 결정
  - system margin은 해당 fidelity를 현재 실행할 수 있는지 제한
  - 두 신호를 weighted sum 하나로 섞지 않고 역할을 분리

- **모드 상대적 slack 판정**
  - 임의의 global low/high slack threshold 대신 후보 mode별 time/utilization margin 계산
  - transition cost와 profiling uncertainty를 포함

- **정직한 guarantee boundary**
  - 빠른 평균 latency와 deadline-aware feasibility를 구분
  - measurement-based bound에서 가능한 주장과 formal guarantee를 분리

### 5.3 기대 이점

- 정상 상태
  - 필요 이상의 정밀 mode 사용 감소
  - background task가 사용할 수 있는 resource margin 확보

- 이상 의심 또는 fault 상태
  - 시간 제약을 만족하는 범위에서 더 높은 recall 또는 더 짧은 detection delay를 가진 mode 선택

- 부하 증가 상태
  - condition-only policy가 선택할 수 있는 infeasible 정밀 mode를 사전에 차단
  - deadline miss 후 복구하는 방식보다 선택 전 admission을 우선

- 연구적 이점
  - fault diagnosis의 “빠른 평균 추론”과 real-time systems의 “예측 가능한 completion”을 같은 비교 기준으로 연결
  - adaptive input 연구와 elastic scheduling 연구 사이의 공통 mode interface 제공

### 5.4 novelty 확정 전 필요한 반증 점검

- Adaptive input 8편에서 machine-condition-triggered temporal window adaptation 존재 여부
- RT-DNN 13편에서 condition과 slack을 동시에 사용하는 mode selection 존재 여부
- DNN-SAM 외에 transition cost와 measured uncertainty를 포함하는 input-fidelity selection 존재 여부
- 동일한 `W/H` formulation을 vibration fault diagnosis에 적용한 연구 존재 여부

---

## 6. Scope and Limitations

- 본 문서는 학위연구만 다룸
- 짧은 학회 트랙의 독립적인 kernel comparison 논리는 제외
- Raspberry Pi Zero 2W의 Linux와 PREEMPT_RT 비교는 method evaluation의 한 요인으로만 사용
- 현재 모델 `M`은 고정
- 현재 연구는 weakly-hard real-time system을 기본 target으로 하지 않음
- p99와 observed max는 formal worst-case execution time이 아님
- 진동 fault diagnosis 전체 분야에 scheduling 연구가 없다고 단정하지 않음
- adaptive input과 RT-DNN 정독 후 novelty와 baseline을 수정할 수 있음

---

## 7. To-Do List

### 7.1 Adaptive Input

- [ ] `02_input_adaptive` 8편 원문 정독
- [ ] temporal vibration window와 spatial image resizing 차이 정리
- [ ] window 선택이 offline design인지 runtime adaptation인지 재판정
- [ ] machine condition이 실제 trigger인지 확인
- [ ] `W`별 fault recall, macro F1과 detection delay 근거 정리
- [ ] mode utility 정의를 본 문서 2.5절에 반영

### 7.2 Real-Time DNN

- [ ] `03_rt_dnn_serving` 13편 원문 정독
- [ ] DNN-SAM의 slack 계산과 측정 기반 최대 실행시간 가정 재검토 [6]
- [ ] SCENIC, MURAL, AMS와 EdgeServing의 variable/trigger/guarantee 비교
- [ ] actual slack reclaim과 next-job prediction 방식 비교
- [ ] model selection을 초기 범위에 넣을 근거가 있는지 판단
- [ ] baseline과 novelty table을 본 문서 4.5절과 5절에 반영

### 7.3 Schedulability and Transition

- [ ] admission test에 사용할 scheduler assumption 확정
- [ ] `Deadline_j`와 `UtilizationBound` 설정 근거 확보
- [ ] p99, observed max 또는 upper confidence bound 중 initial criterion 선택
- [ ] profiling uncertainty 기반 guard band 설정 절차 구현
- [ ] mode-change protocol과 carry-over job 문헌 정독

### 7.4 Experiment Design

- [ ] 유사 Linux/PREEMPT_RT 연구의 부하 설계 조사
- [ ] 실제 동시 실행 task와 synthetic stress의 대응 관계 정리
- [ ] candidate `W/H` mode bank 확정
- [ ] machine-condition indicator와 calibration 방법 확정
- [ ] application-level diagnostic requirement 확보 여부 확인
- [ ] requirement가 없을 경우 Pareto와 sensitivity 중심 평가 설계

---

## 8. Decision Gates

| Gate | 질문 | 통과 기준 | 실패 시 조치 |
| --- | --- | --- | --- |
| G1. Mode value | `W/H`별 diagnostic utility 차이가 있는가 | 반복 가능한 recall/F1/delay 차이 | `W` 축소 또는 `H` 중심 재정의 |
| G2. Load need | 부하에 따라 feasible set이 달라지는가 | tail/miss 또는 margin의 일관된 변화 | load-aware trigger 축소 |
| G3. Feasibility | admission rule이 독립 run에서 유효한가 | target false-admission 이하 | guard band와 profile 방법 수정 |
| G4. Joint trigger | joint policy가 single-trigger보다 유리한가 | timing 또는 utility 한 축 개선, 다른 축 비열화 | trigger와 utility 단순화 |
| G5. Transition | switch cost를 포함해도 이점이 남는가 | residence interval 내 overhead 상쇄 | mode 수 축소, hysteresis 강화 |
| G6. Model axis | 다른 model이 Pareto frontier를 넓히는가 | `(W,H)`만으로 없는 point 확보 | model 고정 유지 |
| G7. Claim level | formal guarantee가 가능한가 | conservative bound와 analysis 확보 | empirical feasibility로 제한 |

---

## 9. 예상 논문 구성

1. **Introduction**
   - fixed diagnosis configuration의 문제
   - real-time fault diagnosis와 elastic scheduling 사이의 gap
   - research questions와 contributions
2. **Background and Related Work**
   - embedded real-time fault diagnosis
   - adaptive diagnostic fidelity
   - elastic scheduling과 mode transition
   - deadline-aware DNN inference
3. **System Model and Problem Formulation**
   - diagnosis mode `(W,H,M)`
   - machine condition, system margin과 diagnostic utility
   - feasible mode set
4. **Feasibility-First Runtime Mode Selection**
   - offline mode bank
   - mode-relative slack 판정
   - runtime policy와 fallback
   - transition control
5. **Implementation**
   - Raspberry Pi Zero 2W inference pipeline
   - Linux와 PREEMPT_RT runtime configuration
6. **Evaluation**
   - mode profiling
   - load sensitivity와 feasibility validation
   - baseline comparison
   - ablation과 transition overhead
7. **Discussion**
   - model generalization
   - guarantee boundary
   - application requirement와 limitations
8. **Conclusion**

---

## 참고문헌

[1] G. C. Buttazzo, G. Lipari, and L. Abeni, "Elastic Task Model for Adaptive Rate Control," *IEEE RTSS*, 1998.

[2] G. C. Buttazzo, G. Lipari, M. Caccamo, and L. Abeni, "Elastic Scheduling for Flexible Workload Management," *IEEE Transactions on Computers*, vol. 51, no. 3, 2002.

[3] Y.-C. Tian and L. Gui, "QoC Elastic Scheduling for Real-Time Control Systems," *Real-Time Systems*, 2011.

[4] R. Gifford, F. Galarza-Jimenez, L. T. X. Phan, and M. Zamani, "Decntr: Optimizing Safety and Schedulability with Multi-Mode Control and Resource Allocation Co-Design," *IEEE RTAS*, 2024, doi: 10.1109/RTAS61025.2024.00032.

[5] R. Li, Z. Song, M. Lv, J.-M. Wu, C. J. Xue, J. Wang, and N. Guan, "ATER: Adaptive Task Execution Rate Regulation for Enhanced Real-Time Performance in ROS 2," *IEEE RTCSA*, 2025, doi: 10.1109/RTCSA66114.2025.00019.

[6] W. Kang, S. Chung, J. Y. Kim, Y. Lee, K. Lee, J. Lee, K. G. Shin, and H. S. Chwa, "DNN-SAM: Split-and-Merge DNN Execution for Real-Time Object Detection," *IEEE RTAS*, 2022, doi: 10.1109/RTAS54340.2022.00021.

[7] S. Ma, H. Sun, S. Gao, and G. Zhou, "A Real-Time Mechanical Fault Diagnosis Approach Based on Lightweight Architecture Search Considering Industrial Edge Deployments," *Engineering Applications of Artificial Intelligence*, 2023.

[8] S. Lee and T. Kim, "FRFconv-TDSNet: Lightweight, Noise-Robust Convolutional Neural Network Leveraging Full-Receptive-Field Convolution and Time-Domain Statistics for Intelligent Machine Fault Diagnosis," *IEEE Transactions on Instrumentation and Measurement*, 2024.

[9] T. Jalonen, M. Al-Sa'd, S. Kiranyaz, and M. Gabbouj, "Real-Time Vibration-Based Bearing Fault Diagnosis Under Time-Varying Speed Conditions," *IEEE ICIT*, 2024, doi: 10.1109/ICIT58233.2024.10540813.

[10] C. Yang, Z. Lai, Y. Wang, S. Lan, L. Wang, and L. Zhu, "A Novel Bearing Fault Diagnosis Method Based on Stacked Autoencoder and End-Edge Collaboration," *IEEE CSCWD*, 2023, doi: 10.1109/CSCWD57460.2023.10152598.

[11] A. Sayghe, "A Physics-Aware Lightweight Transformer Network for Intelligent Bearing Fault Diagnosis Under Variable Operating Conditions," *Artificial Intelligence for Engineering*, 2026, doi: 10.1049/aie2.70014.

[12] Z. Zhan, S. Zhang, J. Xu, and D. Ma, "Edge-Oriented Bearing Fault Diagnosis via Triple-Lightweight Network With Adaptive Pruning," *IEEE Transactions on Instrumentation and Measurement*, 2026, doi: 10.1109/TIM.2026.3699722.

---

## 근거 문서

- `PROJECT_CONTEXT.md`
- `decisions/personal_research_summary_0708.md`
- `decisions/professor_report_0729.md`
- `surveys/elastic_scheduling_survey.md`
- `manuscript/realtime_fault_diagnosis_related_work_table.md`
- `surveys/paper_cards/03_rt_dnn_serving/dnn_sam.md`
- `surveys/claim_bank.md`
- `manuscript/problem_formulation.md`

---

## v1_2에서 반영한 TH 피드백

- 가제에서 제한 자원 Linux 표현 제거
- 서술형 본문을 개조식 중심으로 변경
- Real-Time Fault Diagnosis가 best-effort로 판정된 이유와 분야적 배경 추가
- 데이터 수집 간격과 Quality of Control 등 용어를 처음 등장할 때 설명
- Research Questions를 질문과 현재 답변 구조로 변경
- 부하 실험의 필요성과 설계 근거 추가
- 초기 model 고정 이유와 확장 조건 추가
- 단일 문자 `a`를 `mode_j`로 교체
- background utilization을 `U_other`로 바꾸고 의미 설명
- DNN-SAM을 참고하여 mode-relative slack 기준 구체화
- diagnostic utility의 사전순위와 threshold 설정 원칙 추가
- 단기 논문 트랙 내용을 제외하고 학위연구 중심으로 재구성
- novelty, expected benefits와 baseline별 검증 가설 보강
- 본문에서 사용한 선행연구에 참고문헌 번호 연결
