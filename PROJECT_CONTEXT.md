# PROJECT_CONTEXT

> 이 repo에서 작업하는 모든 에이전트(Claude Code 등)는 작업 시작 전 이 문서를 먼저 읽는다.
> 연구 배경·핵심 식·용어·작성 규칙의 단일 기준점(single source of truth)이다.

---

## 1. 연구자

- 이태훈 / 서울시립대 기계정보공학과 석사과정 (RTES Lab, 실시간 임베디드 시스템)
- 지도교수: 김태현 교수님
- 졸업 목표: 2027년 8월
- 선호: 시스템/실시간 측면 > AI 모델 최적화 측면

---

## 2. 연구 한 줄 요약

제한된 엣지 디바이스에서, 기계 상태와 시스템 상태를 동시에 고려하여
실시간 결함 진단을 안정적으로 수행하는 방법을 연구한다.

핵심 아이디어: **adaptive window 연구(정확도 축) + elastic scheduling(시스템 축)을 결합**하여,
진단 task의 입력 윈도우·진단 주기·모델을 기계 상태에 따라 runtime에 조율한다.

---

## 3. 연구 단계

| 단계 | 내용 | 산출물 |
| --- | --- | --- |
| KSC 2025 (완료) | STM32F401 + 베어메탈 | 기반 |
| KCC 2026 (완료) | STM32F407 + Zephyr RTOS, 실시간 추론 성능 분석 | 논문 + 6월 포스터 |
| KSC 2026 (단기) | Pi Zero 2W, Linux vs PREEMPT_RT 실시간성 비교 | 9월 제출 목표 |
| 학위논문 (중기) | (W,H,M) 기반 elastic scheduling | 핵심 |
| 장기 | 추론 + OTTA 학습을 동일 RT 스케줄링에 통합 | 본인 코어 |

---

## 4. KCC 2026 핵심 결과 (중기 연구의 근거)

- 플랫폼: STM32F407 + Zephyr RTOS v4.3, TFLite Micro + CMSIS-NN
- 모델: FRFconv-TDSNet, INT8 양자화, tensor arena 56KiB (CCM RAM)
- 데이터: UOS dataset (이성재 et al., Data in Brief 2024), 1400 RPM, 8-class 축 결함, 8kHz
- 파이프라인: 3-task (Rx → Inference → Tx), k_msgq, UART + DMA
- 최종: W=512에서 40.3ms, deadline 64ms 충족, 정확도 99.30%, σ=0.009ms, jitter(peak-to-peak) 0.045ms
- 총 speedup 30.4x (CMSIS-NN 2.7x × window 축소 11.4x)
- **핵심 발견 1**: DWConv 복잡도 O(W²) → window 축소 시 latency가 superlinear하게 감소
- **핵심 발견 2**: 같은 W라도 sampling frequency에 따라 noise robustness가 달라짐

> 모델은 fault classification으로 보이지만, 내부적으로 anomaly detection을 수행한다.
> anomaly score(연속값)가 elastic scheduling의 트리거 신호가 된다.

---

## 5. 중기 연구 정식화 (problem statement 초안)

```
하한:  W_phys ≤ W            결함 정보 보존 (베어링 물리 / 분리도)
상한:  W ≤ W_sys(D)          deadline 만족, KCC의 latency~O(W²)에서 W_sys = sqrt((D-β)/α)

feasibility (elastic utilization):
       Σ_other (C_i / T_i)  +  C(W,M) / H  ≤  U_lub
       elastic 변수: (W, H, M)

목적:  진단 utility 최대화
정책:  π : (기계 상태 q=anomaly score, 시스템 slack S) → (W, H, M)
       정상 → 가벼운 mode로 slack 확보 / 이상 → 정밀 mode 전환
```

기호: W=window size, H=hop size/진단 주기, M=model, C=실행시간, T=주기, U_lub=이용률 상한, D=deadline, S=slack

---

## 6. 연구 차별점 (novelty)

| | 가변 변수 | 트리거 | 플랫폼 | 도메인 |
| --- | --- | --- | --- | --- |
| Classic elastic (Buttazzo) | period T | 시스템 부하 | 이론 | 일반 |
| Sudvarg 계보 (RTAS/RTSS 2024) | period, subtask | 부하 | 멀티코어 | 일반 |
| elastic-DNN (FLEX 등) | batch, fusion | 자원 경합 | edge GPU | perception |
| Canvas/image resizing | 입력 크기 | criticality | embedded GPU | vision |
| AIL / ADW | window | 없음 (offline) | — | fault diagnosis |
| **본 연구** | **W + H + M 동시** | **기계 상태 + slack** | **MCU/SBC + PREEMPT_RT** | **진동 FD** |

→ 마지막 행이 비어있는 조합 = 연구 자리. 최신 동향(AI-for-RT, 가변/stochastic task, elastic)의 교차점.

---

## 7. 단기 KSC 2026

- 주제: Pi Zero 2W 기반 실시간 결함 진단 파이프라인에서 일반 Linux와 PREEMPT_RT 실시간성 비교
- KCC future work 3개(실제 센서 / 다중 태스크 / 상위 플랫폼)를 잇는 직계 후속
- 플랫폼: Raspberry Pi Zero 2W (Cortex-A53), Raspberry Pi OS Lite ± PREEMPT_RT
- 측정: cyclictest, stress-ng 부하 5종(idle/CPU/mem/IO/combined)
- 지표: activation jitter, inference/end-to-end latency, deadline miss, p95/p99, σ, CPU util/temp, memory, throughput
- 주의: PREEMPT_RT 패치 실효성은 cyclictest 분포 비교로 검증 필요 (너무 쉽게 적용된 정황)
- 참고: CMSIS-NN은 Cortex-M 전용 → Pi(Cortex-A)에서는 XNNPACK 또는 reference

---

## 8. 작성 규칙

- 학술 문서에 괄호 사용 자제 (교수님 지침)
- 교수님 보고용 = 개조식 간결 / 내부 노트 = 상세
- 단정적 표현 자제, 불확실하면 decisions/open_questions.md 에 기록
- 한국어로 작업

---

## 9. repo 구조

```
personal-research/
├── PROJECT_CONTEXT.md        # 이 문서 (공통 기준점)
├── CLAUDE.md                 # Claude Code 지침
├── README.md
├── surveys/                  # 머리 트랙 — 서베이
│   ├── claim_bank.md         # 내 연구 주장 모음
│   ├── related_work_map.md
│   ├── comparison_table.md   # 6번 표 (확장판, Table 1 될 것)
│   └── paper_cards/          # 논문별 카드
├── papers/                   # PDF 원본 (그룹 1~7)
├── experiments/              # 손 트랙 — KSC 실험
│   ├── pi_setup/
│   ├── preempt_rt/
│   ├── pipeline/             # sensing/windowing/inference/logging
│   └── results/
├── manuscript/               # KSC 논문 초안
├── prompts/                  # 재사용 프롬프트
└── decisions/
    └── open_questions.md     # 미해결 질문
```

---

## 10. 보유 논문 그룹 (papers/)

1. elastic_scheduling — Buttazzo 1998/2002, Chantem 2009, Orr 2020, Salman 2021, Tian 2011, Sudvarg(박사논문/RTAS24/RTSS24/Admission), FLEX
2. input_adaptive — AIL 2편, ADW, image resizing 4편(Canvas resizing 포함)
3. rt_dnn_serving — EdgeServing, Pantheon, BCEdge, DEMS-A, Demand Layering, Imprecise Computations, Early-Exit 2편
4. idk_weakly_hard — IDK 2편, Weakly-Hard CBS Linux, Period Assignment Cascade
5. fault_diagnosis_app — TinyML bearing, Time-Varying Speed FD, lightweight FD
6. platform_preempt_rt — OSPERT 2024, MDPI ARM 2021, DLR pattern recognition, vision displacement
7. platform_pi_zero2w — Dolphin whistle, RT object detection
