# 0708 면담 반영 서베이 계획

이 문서는 `decisions/personal_research_summary_0708.md`의 교수님 피드백을 서베이 작업 단위로 바꾼 실행 계획이다.

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

### 1. Real-Time Fault Diagnosis 분류표

위치: `surveys/comparison_table_ko.md`

목표:
- 최근 real-time fault diagnosis 문헌을 RTOS 유무, deadline 유무, platform, 실시간성 접근 방식으로 분류한다.
- TinyML, quantization, pruning, lightweight architecture search를 `best-effort 근실시간`과 구분한다.

핵심 판정 기준:
- `진짜 실시간`: RTOS, deadline, jitter, p95/p99/max latency, deadline miss, schedulability 중 일부를 명시적으로 다룸.
- `근실시간`: 평균 inference time 또는 model size만 줄이고 deadline guarantee나 scheduling 분석이 없음.

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

### 현재 정독 및 재검토 큐

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

1. KCC 데이터로 `U=C/T`를 max, average, p99 기준으로 계산한다.
2. `surveys/comparison_table_ko.md`의 real-time fault diagnosis 표를 보강한다.
3. elastic scheduling 응용 문헌의 가정표를 보강한다.
4. mode change와 imprecise computation 노트를 만든다.
5. 교수님께 보낼 요약 문서 또는 PPT 골격을 만든다.
