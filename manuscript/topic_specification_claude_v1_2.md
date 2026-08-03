# 주제 구체화 — 실시간 진동 결함 진단을 위한 기계 상태·시스템 여유 기반 진단 모드 선택

> 작성자: Claude (Claude Code) · 버전: v1_2 · 작성일: 2026-08-02
> 동반 산출물: `surveys/survey_master_claude_v1_2.xlsx` (서베이 종합표), Overleaf용 `manuscript/topic_specification_claude_v1_2.tex`

---

## 0. 문서의 목적

- 이 문서는 학위논문의 **주제를 구체화**하기 위한 내부 작업 문서다.
- 지금까지 체계적으로 검토를 마친 두 축, 즉 실시간 결함 진단과 elastic scheduling의 조사 결과를 정리하고, 연구 공백·정식화·실험 설계·남은 과제를 한 곳에 모은다.
- 적응형 입력(S2)과 실시간 DNN 서빙(S4)은 조사를 보강 중이며, 현재까지 확보한 범위만 표로 반영한다.
- 아래 초록·본문은 실제 논문 초안에 옮길 수 있는 형태로 작성하되, 미검증 수치는 넣지 않는다.

---

## 1. 제목 (가제)

- **추천 가제 (국문)**: 엣지 디바이스에서 기계 상태와 시스템 여유를 이용한 실시간 진동 결함 진단의 진단 모드 선택
- **추천 가제 (영문)**: Machine-Condition and Slack-Aware Mode Selection for Real-Time Vibration Fault Diagnosis on Edge Devices

검토 의견 — 제안하신 `Machine Condition and Slack-aware Elastic Real-Time Vibration Fault Diagnosis`

- 좋은 점: 짧고, 두 트리거(기계 상태·slack)와 응용(진동 결함 진단)이 드러난다. v1의 긴 제목보다 낫다.
- 고칠 점 1: `Elastic Real-Time`은 형용사가 겹쳐 어색하고, `Elastic`이 앞에 오면 스케줄링 이론을 새로 제안하는 논문처럼 읽힌다. 우리는 스케줄링을 **적용**하는 논문이므로 제목에서 `Elastic`을 빼는 편이 안전하다.
- 고칠 점 2: 실제 방법은 "진단 모드를 고르는 것"이므로 `Mode Selection`을 넣으면 기여가 분명해진다. 이 분야 제목 관례(`Adaptive Model Selection for Real-Time Heart Disease Detection ...` [19], `Split-and-Merge DNN Execution for Real-Time Object Detection` [18])와도 맞는다.
- 결론: `[방법] for Real-Time [응용] on [플랫폼]` 형태의 추천 가제를 우선하되, 제안하신 제목은 `Elastic`만 빼면 바로 쓸 수 있다.

## 2. Keywords

`real-time fault diagnosis`, `runtime mode selection`, `elastic scheduling`, `anomaly-driven adaptation`

## 3. 국문 초록

- 회전 기계의 진동 결함 진단을 엣지 디바이스에서 실시간으로 수행할 때, 더 큰 입력 window와 더 무거운 모델은 결함을 더 잘 구분하지만 실행시간과 이용률을 함께 키워 데드라인을 넘길 수 있다.
- 본 연구는 진단 태스크의 입력 window `W`, 진단 주기를 정하는 hop `H`, 추론 모델 `M`을 하나의 진단 모드로 묶고, 기계 상태 `q`와 시스템 여유 `S`를 함께 기준으로 삼아 매 진단 시점에 모드를 고르는 방법을 제시한다.
- 정상 상태에서는 가벼운 모드로 여유를 확보하고, 이상 징후가 감지되면 정밀 모드를 고르되 데드라인 안에서 실행 가능한 모드만 후보로 둔다.
- 평가 플랫폼은 Raspberry Pi Zero 2W이며, 검증 실험으로 일반 Linux와 PREEMPT_RT 커널의 응답시간 특성을 비교한다.

## 4. Abstract (English)

- In real-time vibration fault diagnosis on edge devices, a larger input window `W` and a heavier model `M` separate faults more reliably but increase execution time and utilization, which can violate the deadline.
- This work groups the window `W`, the hop `H` that sets the diagnosis period, and the model `M` into a single diagnosis mode, and selects one mode at each diagnosis step using both the machine condition `q` and the system slack `S`.
- Under a normal condition the runtime chooses a light mode to preserve slack; under a suspicious condition it chooses a precise mode, restricting the candidates to modes that run within the deadline.
- The evaluation platform is a Raspberry Pi Zero 2W; a verification experiment compares the response-time behavior of stock Linux and PREEMPT_RT.

---

## 5. 기호 정의

| 기호 | 의미 |
| --- | --- |
| `f_s` | 샘플링 주파수 |
| `W_i` | i번째 후보 모드의 입력 window 크기, 샘플 수 |
| `H_i` | i번째 후보 모드의 hop 크기, 샘플 수 |
| `M_i` | i번째 후보 모드의 추론 모델 또는 구성 |
| `m_i` | i번째 후보 진단 모드, `m_i = (W_i, H_i, M_i)` |
| `N` | 후보 모드 개수. 후보 집합은 `{m_1, ..., m_N}` |
| `T_i` | 모드 `m_i`의 진단 주기, `T_i = H_i / f_s` |
| `C_i` | 모드 `m_i`의 추론 실행시간. 분포로 보고하며 평균·p99·최대를 사용 |
| `I` | 다른 workload나 공유 자원에 의한 간섭 시간 |
| `L` | 운영체제 스케줄링 지연 |
| `R_i` | 모드 `m_i`의 관측 응답시간, `R_i = C_i + I + L` |
| `D` | 상대 데드라인 |
| `U_i` | 모드 `m_i`의 이용률, `U_i = C_i / T_i` |
| `U_bg` | 배경 workload와 다른 실시간 태스크의 이용률 |
| `U_bound` | 이용률 상한 |
| `q_k` | k번째 진단 시점의 기계 상태 지표. 본 연구에서는 anomaly score로 구체화 |
| `S_k` | k번째 진단 시점의 시스템 여유, `S_k = D − p99(최근 응답시간)` |
| `Q(m_i, q_k)` | 현재 기계 상태에서 모드 `m_i`가 주는 진단 효용. 정확도 또는 검출 지연으로 측정 |
| `m*_k` | k 시점에 **선택된 하나의 모드**. 별표는 선택 결과를 뜻하며 다른 모드를 포함한다는 의미가 아니다 |

---

## 6. Background

### 6.1 연구 동기

- 회전 기계 진동 결함 진단은 엣지에서 수행할 때 두 요구가 부딪힌다.
  - 진단 신뢰성: 더 긴 window는 더 많은 회전 주기와 주파수 정보를 담아 약한 결함을 더 잘 구분하고, 더 무거운 모델은 결함 구분력이 높다.
  - 실시간성: 엣지 자원은 제한적이며 진단 결과는 데드라인 안에 나와야 한다.
- KCC 2026 결과가 이 충돌을 정량적으로 보여준다 [22].
  - 사용한 FRFconv-TDSNet 모델은 depthwise convolution 연산량이 window 크기의 제곱, 즉 `O(W^2)`에 비례하는 부분이 있어, window를 줄이면 latency가 선형보다 빠르게 감소했다.
  - 같은 데이터를 비중첩 window로 두면 이용률은 다음과 같다.

| W | 최대 실행시간 | 주기 T (8 kHz) | 이용률 U = C/T |
| ---: | ---: | ---: | ---: |
| 512 | 40.3 ms | 64 ms | 0.63 |
| 1024 | 129.8 ms | 128 ms | 1.01 |
| 2048 | 460.3 ms | 256 ms | 1.80 |

- 해석: 정밀한 모드로 갈수록 실행시간 `C`가 커지고, 주기 `T`가 충분히 커지지 않으면 이용률이 1을 넘어 단일 태스크만으로도 데드라인을 지킬 수 없다. 즉 정확도를 올리는 선택이 곧 데드라인을 위협하는 선택이 된다.
- 착안: 이 선택을 고정하지 않는다. 정상일 때는 가벼운 모드로 여유를 확보하고, 이상 징후가 감지되면 정밀 모드로 전환하되 그 전환이 데드라인 안에서 실행 가능한 경우에만 허용한다.
- 조절 대상은 window 하나가 아니라 window·hop·model 세 값을 묶은 진단 모드다. 이 결합이 필요한 이유는 6.4절에서 다룬다.

> KCC 2026 모델은 분류 형태이지만 내부적으로 anomaly detection을 수행하며, 그 anomaly score가 기계 상태 지표 `q`가 된다 [22].

### 6.2 관련 연구 — 실시간 결함 진단 (검토 완료)

- 검토한 진동·회전 기계 결함 진단 논문은 데드라인·꼬리 지연·스케줄 가능성을 결합한 사례가 서베이 범위에서 확인되지 않았고, 모두 best-effort 수준이었다. 다수 논문의 "real-time"은 online 실행이나 낮은 평균 latency를 뜻했다.
- 판정 기준: 데드라인을 명시하고 miss를 측정하면 O, 시간 기준은 있으나 데드라인으로 선언·측정하지 않으면 △, 시간 기준 자체가 없으면 X.

핵심 논문 요약 (전체 표는 엑셀 시트 `1_실시간_결함진단`)

| # | 논문 | 문제 상황 | 조절 대상 | 적응·이상감지 판정 기준 | Deadline | 본 연구와의 차이 |
| --- | --- | --- | --- | --- | :---: | --- |
| [1] | Langarica et al., 2020, IEEE TASE | 산업용 모터 online 진단 | 없음 | DIPCA+SPE 통계량이 관리한계 초과 시 이상 판정 → RBC가 진동 결함 지목 시 무거운 CNN 실행 (1 Hz) | X | q 트리거의 구조적 선례. 시스템 여유 S 미고려, 모드 선택 없음 |
| [6] | Arciniegas et al., 2025, Discover IoT | 모터 진동 이상 알림 | 없음 | K-means 정상군 거리 임계 초과 시 이상 alert | △ | 이상감지가 alert 조건일 뿐 모드 선택 아님 |
| [2] | Lima, 2025, IEEE LCIoT | 회전자봉 파손 진단 | 없음 | offline grid search로 결함 유형별 최적 (f_s, W, H) 선택 | △ | 상태별 최적 W/H가 다름을 grid search로 확인. runtime 규칙·트리거 없음 |
| [3] | Pubalan et al., 2025, ICSIMA | 베어링 분류 (replay) | 없음 | 물리식 W = 60·f_s/RPM (1회전) | △ | 회전속도를 입력 길이로 변환한 물리 근거. runtime 적응 아님 |
| [4] | Yang et al., 2023, IEEE CSCWD | 베어링 이상 진단 (단말-엣지) | 오프로딩 위치 | 단말 AE의 confidence + 허용 latency 예산으로 엣지 오프로딩 결정 | △ | machine evidence + timing을 함께 트리거로 쓰는 가장 가까운 FD 사례. 스케줄 가능성 없음 |
| [5] | He et al., 2023, IEEE TIM | 모터 베어링 음향 진단 | 없음 | 없음 (회전속도로 BPFI/BPFO prior만 갱신) | △ | pipeline 10.294 s가 1 s window 초과. "online ≠ 데드라인 충족" 반례 |

- 이상감지 판정 기준의 관찰: 정량 기준을 제시한 논문은 통계 관리한계(Langarica의 SPE [1])나 클러스터 거리 임계(Arciniegas의 K-means [6])를 쓴다. 두 방식 모두 본 연구의 `q` 임계 설계에 참고가 된다.
- Lima [2]에 대한 표현 교정: 미세 결함이 더 높은 f_s와 더 짧은 hop을 "요구"한 것이 아니라, offline grid search 결과 그러한 설정이 최적으로 **선택**되었다. 즉 기계 상태에 따라 적절한 W/H가 달라진다는 간접 근거이며, runtime 규칙으로 정식화된 것은 아니다.
- Yang et al. [4] 트리거 상세: 단말이 경량 stacked autoencoder를 실행하고, 그 재구성 신뢰도(confidence)와 현재 허용 가능한 latency 예산을 함께 판단해, 무거운 진단을 엣지 서버로 오프로딩할지 결정한다. 기계 증거와 timing을 동시에 보는 점에서 본 연구의 `q + S`와 형태가 가깝지만, 스케줄 가능성 분석은 없다.

### 6.3 관련 연구 — Elastic Scheduling (검토 완료)

- elastic scheduling 문헌은 이론과 적용으로 나눈다. 전체 표는 엑셀 시트 `2_Elastic_Scheduling`.
- 공통 관찰:
  - 트리거는 시스템 내부 신호(부하·자원·메시지 드롭)이거나 offline이며, 외부 기계 상태로 트리거하는 사례는 서베이 범위에서 확인되지 않았다.
  - 조절 대상은 주기·rate·대역폭으로, 조절해도 계산 결과의 의미가 바뀌지 않는다. 정확도 자체를 바꾸는 변수를 다룬 사례는 확인되지 않았다.

이론 논문

| # | 논문 | 조절 대상 | 조절 기준 | 실시간성 보장 수준 | 핵심 정리 |
| --- | --- | --- | --- | --- | --- |
| [9] | Buttazzo et al., 1998/2002, RTSS/IEEE TC | task 주기 T | 시스템 부하, admission | 제한된 모델 내 formal hard | elastic task model 원형. task를 spring으로 보고 부하 시 주기를 늘려 이용률을 낮춤 |
| [10] | Salman et al., 2021, ETFA | 앱 주기 T + reservation | runtime 이벤트 | hard (PRM 이용률 bound) | 2계층. 앱 수준에서 주기로 먼저 흡수하고 실패 시에만 system reservation 조정 |
| [11] | Gifford et al. (Decntr), 2024, RTAS | controller·주기·자원 할당 | offline + mode-change 이벤트 | hard (invariant set + DBF) | multi-mode 제어를 안전·스케줄 공동설계. 전환 시 carry-over 데드라인 완화로 과부하 흡수 |
| [12] | Xu et al. (Safety-Aware), 2023, RTCSA | 공통 주기, miss 패턴 | offline | soft-but-formal (weakly-hard, d_safe) | 주기를 공통화하고 안전한 데드라인 miss 패턴을 automata로 합성 |

적용 논문 (어떻게 적용했는가)

| # | 논문 | 조절 대상 | 적용 방법 | 실시간성 보장 수준 |
| --- | --- | --- | --- | --- |
| [13] | Burgio et al., 2010, ICCD | TDMA bus 대역폭 + 주기 | 중앙 master가 각 core의 대역폭 요청을 모아 TDMA slot을 재분배하고, 각 core는 대역폭별 실행시간 LUT를 조회해 elastic 알고리즘으로 주기를 재계산. ERIKA RTOS | soft (offline feasibility 방어 + 실험적 QoC) |
| [14] | Li et al. (ATER), 2025, RTCSA | 센서 샘플링 rate | LTTng로 실행을 관측해 메시지 드롭이 늘면 rate를 낮추고 실행 여유가 생기면 rate를 높임. ROS 2 Humble, 소스 수정 없음 | empirical only |

### 6.4 관련 연구 — 적응형 입력·모델, 실시간 DNN 서빙 (보강 중, 현재 범위)

- 두 축은 조사를 보강 중이며 현재 확보한 범위만 표로 제시한다. 전체 표는 엑셀 시트 `3_적응형_입력_모델`, `4_RT_DNN_서빙`.

적응형 입력·모델 (무엇을 무슨 기준으로 조절하는가)

| # | 논문 | 조절 대상 | 조절 기준 | 목적 | 시점 |
| --- | --- | --- | --- | --- | --- |
| [15] | Kim et al. (ADW), 2026, Mathematics | window size W (H = β·W) | anomaly deviation score (변동성·주기·국부 스파이크 유형별 편차) | 진단 민감도 향상 | offline |
| [16] | Tang et al. (AIL), 2023, Appl. Soft Comput. | input length | 물리식 (베어링 특성 주파수·f_s·회전속도) | 잡음 강건성·전이 진단 | offline |
| [17] | Tang et al. (AILWTLN), 2023, EAAI | input length + 경량 모델 | 물리식 Na = n²·f_s/BW | 경량·전이 진단 | offline |

실시간 DNN 서빙 (어떻게 실시간성을 달성하는가)

| # | 논문 | 조절 대상 | 트리거 | 실시간성 달성 방식 |
| --- | --- | --- | --- | --- |
| [18] | Kang et al. (DNN-SAM), 2022, RTAS | optional subtask 입력 scale | runtime 데드라인 여유 + RoI criticality | 필수/선택 subtask 분리 + non-preemptive EDF 충분조건 + slack reclaim |
| [19] | Li et al. (AMS), 2025, RTCSA | 모델 복잡도·anytime exit | 순간 심박 HR 임계 → D(HR) | 상태 기반 모델 선택 + anytime 파라미터 공유 + watchdog fallback |
| [20] | Xu et al. (FLEX), 2024, RTSS | batch·fusion 구성 | 뷰 criticality·GPU 예산·데드라인 | elastic fusion + CEDF 동적 배칭 |
| [21] | Yao et al. (Imprecise DL), 2020, RTCSA | 실행 depth (필수+선택 단계) | 데드라인 + 선택 단계 효용 | imprecise computation + EDF stage 스케줄 |

### 6.5 연구 공백

- 진단 축: 진동 결함 진단에서 runtime에 W·H·M을 함께 조절하고 데드라인·스케줄 가능성을 결합한 사례가 서베이 범위에서 확인되지 않았다.
- 스케줄링 축: elastic scheduling은 정확도를 바꾸는 변수를 다루지 않고, 트리거가 시스템 내부 또는 offline에 한정된다.
- 결합 축: 기계 상태 `q`와 시스템 여유 `S`를 분리된 역할로 사용해 정확도를 바꾸는 실행 가능한 모드를 고르고 그 스케줄 가능성을 제시한 사례가 서베이 범위에서 확인되지 않았다. 본 연구는 이 결합을 대상으로 한다.

---

## 7. Methodology

- 서술 흐름은 이 분야 논문의 구성, 즉 태스크 모델 → 실행시간·이용률 모델 → 실행 가능 조건 → 상태 기반 선택 정책 → 알고리즘 순서를 따른다. 정식화의 상세는 `manuscript/problem_formulation.md`를 기준으로 한다.

### 7.1 태스크 모델과 진단 모드

- Raspberry Pi Zero 2W에서 진동 결함 진단 태스크가 주기적으로 실행된다. 태스크는 신호 segment를 받아 추론하고 데드라인 안에 결과를 낸다. 원신호는 `f_s`로 취득된다.
- 매 진단 시점 `k`에 후보 집합 `{m_1, ..., m_N}`에서 모드 하나를 고른다.
  - 각 모드 `m_i = (W_i, H_i, M_i)`.
  - 진단 주기 `T_i = H_i / f_s`. 이 주기는 end-to-end 데드라인이나 추론 예산과 구분한다.
- W와 H를 분리하는 이유: 진동 진단에서 "얼마나 많은 신호 맥락을 보는가(W)"와 "얼마나 자주 진단하는가(H)"는 서로 다른 설계 선택이다.

모드 후보 설정 (첫 구현)

- 첫 구현은 M을 고정하고 discrete `(W, H)`만 다룬다. M은 필요성과 보장 조건이 확인된 뒤 확장한다.
- W 후보는 KCC 측정값 {512, 1024, 2048}을 기준으로 하고, 물리식 하한 `W ≥ 60·f_s/RPM` [3]을 반영해 회전속도에서 정보가 보존되는 최소 window를 정한다.
- 예시 후보 집합 (플랫폼 profiling 후 확정)

| 모드 | W | H | 성격 |
| --- | ---: | ---: | --- |
| `m_1` | 512 | 512 | 가벼움 |
| `m_2` | 1024 | 512 | 중간 |
| `m_3` | 1024 | 1024 | 중간, 주기 김 |
| `m_4` | 2048 | 2048 | 정밀 |

- 모드 개수 N은 4~6개를 목표로 하고, offline profiling으로 각 모드의 실행시간을 측정해 실행 가능 여부를 미리 표로 만든다.

### 7.2 실행시간과 이용률

- 각 모드의 추론 실행시간 `C_i`는 단일 값이 아니라 분포로 보고한다. 후보군으로 평균·p99·최대를 사용한다.
- 관측 응답시간은 다음과 같다.

```
R_i = C_i + I + L
```

- `I`는 다른 workload·공유 자원 간섭, `L`은 운영체제 스케줄링 지연이다.
- PREEMPT_RT에서 static hard WCET를 증명 없이 주장하지 않는다. 초기 정식화는 실측 응답시간의 p99 또는 최대를 기준으로 한다.

```
R_i(p99) ≤ D
```

- 모드의 이용률과 총 이용률:

```
U_i = C_i / T_i,   T_i = H_i / f_s
U_total(m_i) = U_bg + U_i
```

### 7.3 실행 가능 조건과 선택 정책

- 2026-07-08 면담 이후 첫 연구 질문: 이상 징후 시 정밀 모드로 전환해도 정적으로 스케줄 가능한가, 그 보장을 어떻게 제시하는가.
- 정책은 실행 가능한 모드 집합 안에서만 진단 효용이 큰 모드를 고른다.

```
실행 가능 모드 집합:
  F(k) = { m_i : U_bg + C_i(p99)/T_i ≤ U_bound  그리고  R_i(p99) ≤ D }

선택된 모드:
  m*_k = argmax_{m_i ∈ F(k)}  Q(m_i, q_k)
```

- 여기서 `m*_k`는 k 시점에 선택된 **하나의 모드**이며, 다른 모드를 포함한다는 뜻이 아니다.
- `Q(m_i, q_k)`는 현재 기계 상태에서 모드가 주는 진단 효용이며, 정확도 또는 검출 지연으로 측정한다. 이 개념은 실시간 추론 문헌의 utility·reward 정식화 [19, 21]에 대응한다.
- `F(k)`가 비면 사전 정의된 fallback 모드를 실행한다.
  - 데드라인 miss를 감지한 뒤 가벼운 모델을 재실행하는 방식은 그 자체로 timing 보장이 아니다. 따라서 초기 구현은 offline에서 실행 가능함이 확인된 모드를 우선하고, 재실행은 재실행에 필요한 시간을 미리 확보한 경우에만 둔다.
- 시스템 여유는 평균이 아니라 최근 응답시간의 p99 또는 최대로 정의한다.

```
S_k = D − p99(최근 응답시간)
```

### 7.4 기계 상태와 이상감지 기준

- 기계 상태 `q_k`는 anomaly score로 구체화한다. 첫 구현은 KCC 모델이 내부적으로 내는 anomaly score를 후보로 둔다 [22].
- 정량 임계 설계는 검토한 두 방식을 후보로 한다.
  - 통계 관리한계 방식: Langarica [1]의 SPE 관리한계처럼, 정상 데이터 분포에서 신뢰수준 기반 임계를 정한다.
  - 분포 percentile 방식: AMS [19]가 심박 임계를 학습 분포 percentile로 정한 것처럼, 검증 데이터의 anomaly score percentile로 정상·의심·경고 구간을 나눈다.
- `q`는 모드의 진단 효용 순위를 정하고, `S`는 실행 가능한 모드를 제한한다. 두 신호의 역할을 분리하는 것이 정책의 핵심이다.

### 7.5 알고리즘 (offline / online 분리)

Offline 단계

```
1. 후보 모드 집합 {m_1, ..., m_N} 구성 (W 후보 + 물리식 하한 반영)
2. 각 모드의 실행시간 C_i 측정 → 평균 / p99 / 최대 기록
3. 부하 조건별로 실행 가능 여부를 표로 작성 (mode feasibility table)
4. anomaly score 임계 (정상 / 의심 / 경고) 를 검증 데이터로 보정
```

Online 단계 (매 진단 시점 k)

```
1. anomaly score q_k 계산
2. 최근 응답시간으로 slack S_k 계산
3. 실행 가능 모드 집합 F(k) 계산 (이용률·응답시간 조건)
4. F(k) 안에서 Q(m_i, q_k) 가 최대인 모드 m*_k 선택
5. F(k) 가 비면 사전 정의 fallback 모드 실행
6. 잦은 전환을 막기 위한 hysteresis 적용
```

### 7.6 W·H·M을 함께 묶는 이유

- 입력 적응은 1차원이 아니다. `W`를 줄이면 `C`가 줄지만, 더 짧은 `H`와 짝지어지면 주기 `T`도 줄어든다.
- `U_i = C_i / T_i`이므로 두 경우가 갈린다.

| 경우 | 변화 | 이용률 U | 스케줄 가능성 |
| --- | --- | --- | --- |
| 1 | W↓ → C↓, H·T 고정 | 감소 | 개선 |
| 2 | W↓ → C↓, H·T 도 감소 | 증가할 수 있음 | 악화 가능 |

- 따라서 window 하나가 아니라 모드 `(W, H, M)`에서 골라야 한다. 이 관찰이 모드를 묶는 근거다.

---

## 8. Experiment

### 8.1 플랫폼과 검증 실험

- 평가 플랫폼: Raspberry Pi Zero 2W (Cortex-A53), Raspberry Pi OS Lite.
- 추론 backend: CMSIS-NN은 Cortex-M 전용이므로 Cortex-A에서는 XNNPACK 또는 reference 구현을 사용한다.
- 일반 Linux와 PREEMPT_RT 비교는 **본 연구의 주 실험이 아니라 검증 실험**이다. 플랫폼의 응답시간·jitter 특성을 파악해 실행시간 모델의 신뢰성을 확인하는 용도다. cyclictest 분포로 PREEMPT_RT 패치의 실효성을 별도 검증한다.

### 8.2 baseline과 제안 정책

| 정책 | q 사용 | S 사용 | 설명 |
| --- | :---: | :---: | --- |
| static-light | X | X | 항상 가벼운 모드 고정 |
| static-precise | X | X | 항상 정밀 모드 고정 |
| q-only | O | X | 기계 상태만 보고 모드 선택, 실행 가능 여부 미확인 |
| S-only | X | O | 여유만 보고 모드 선택, 기계 상태 미반영 |
| 제안 (q + S) | O | O | 실행 가능한 모드 안에서 기계 상태 기반 진단 효용 최대 모드 선택 |

### 8.3 기계 상태 시나리오

- anomaly score를 [0, 1]로 정규화한다고 가정하고, 정상·의심·경고 구간을 나눈다.
- 후보 임계 (검증 데이터 percentile로 보정)

| 구간 | anomaly score 후보 임계 | 정책 동작 |
| --- | --- | --- |
| 정상 | < 0.3 | 가벼운 모드로 여유 확보 |
| 의심 | 0.3 ~ 0.7 | 중간 모드 |
| 경고 | > 0.7 | 정밀 모드, 단 실행 가능한 경우만 |

- 세 구간을 오가는 anomaly score 궤적을 재생하고, 각 궤적에서 정책이 고르는 모드 열과 그에 따른 진단 효용·데드라인 miss를 baseline과 비교한다.

### 8.4 측정 지표

- 실시간성: 데드라인 miss 비율, p99·최대 응답시간, activation jitter, 이용률.
- 진단: 정확도 또는 검출 지연.
- 정책 효과: 제안 정책이 static·단일 트리거 baseline 대비 데드라인 miss를 늘리지 않으면서 진단 효용을 개선하는지.
- 오버헤드: 모드 선택은 표 조회와 비교로 이루어져 실행시간 대비 무시 가능할 것으로 예상한다. ATER [14]처럼 1회 실측해 무시 가능함을 확인만 하고, 지속 측정은 하지 않는다.

> 위 값과 결과는 아직 측정하지 않았으며 설계로만 제시한다.

---

## 9. Novelty

- 본 연구의 위치는 두 축이 만나는 빈 교차점이다.
  - 트리거 축: 검토한 문헌은 시스템 내부 신호 또는 offline로 트리거된다. 외부 기계 상태로 트리거하는 사례가 서베이 범위에서 확인되지 않았다.
  - 조절 대상 축: 검토한 문헌은 주기·rate·대역폭 등 의미가 보존되는 변수를 조절한다. 정확도를 바꾸는 변수를 조절한 사례가 확인되지 않았다.

세 가지 구체적 차별점

1. **조절 대상**: 기존은 주기·rate·입력 크기 중 하나를 조절한다 [9~21]. 본 연구는 window·hop·model 세 축을 함께 고르며, 특히 W와 H를 분리해 "정보량"과 "진단 빈도"를 독립 변수로 둔다.
2. **트리거**: 기존 트리거는 시스템 내부 부하·자원·드롭 [13, 14] 또는 offline [12]이거나, 조건 하나만 본다. DNN-SAM은 slack만 [18], AMS는 생리 상태만 [19], Langarica는 이상감지만 본다 [1]. 본 연구는 기계 상태 `q`와 시스템 여유 `S`를 분리된 역할로 함께 사용한다. `q`는 진단 효용 순위를, `S`는 실행 가능 모드를 정한다.
3. **도메인과 보장**: 진동 결함 진단에서 실행 가능한 모드 집합 안에서 선택하고, Pi Zero 2W의 일반 Linux와 PREEMPT_RT에서 실측 응답시간으로 스케줄 가능성을 확인한다. 검토한 FD 문헌이 best-effort에 머문 지점을 데드라인·꼬리 지연과 결합한다.

각 축에서 가장 가까운 논문 대비

- DNN-SAM [18]: slack으로 입력 fidelity를 고르지만 단일 트리거이고 공간 vision·GPU 대상이다. 본 연구는 시간축 window와 기계 상태를 함께 쓴다.
- AMS [19]: 상태로 모델을 고르지만 생리 신호이고 시스템 여유를 보지 않는다. 본 연구는 여유로 실행 가능성을 제한한다.
- Langarica [1]: 이상감지로 무거운 추론을 gate하지만 시스템 여유가 없어 모드 선택이 아니다. 본 연구는 여유와 결합해 W·H·M을 고른다.
- ADW [15]: 이상 편차로 W를 정하지만 offline이다. 본 연구는 runtime에 여유 제약 아래 고른다.

---

## 10. To-Do

### 10.1 서베이 보강

- [ ] 적응형 입력(S2) 조사 완결: ADW·AIL·AILWTLN 외 image resizing·MURAL 계열의 조절 대상·기준·시점을 확정해 엑셀 시트 3과 6.4절 갱신.
- [ ] 실시간 DNN 서빙(S4) 조사 완결: DNN-SAM·AMS·FLEX·Imprecise 외 EdgeServing·Pantheon·SCENIC·early-exit 계열의 실시간성 달성 방식을 확정해 엑셀 시트 4와 6.4절 갱신.

### 10.2 정식화·방법 확정

- [ ] 진단 효용 `Q`의 구체 정의: 정확도 기반, 검출 지연 기반, 또는 이탈 거리 d_safe [12] 기반 중 우리 상황에 가장 적합한 형태를 정한다.
- [ ] 모드 전환의 스케줄 가능성 조건 정리. `C = C(W, M)`이 설정에 따라 바뀌므로 이용률 bound를 우리 구조에 맞게 유도한다.
- [ ] 후보 모드 집합의 W·H 값과 개수 N 확정. 첫 구현은 M 고정.
- [ ] fallback 모드와 전환 hysteresis 정도 확정.

### 10.3 실험·마일스톤

- [ ] Pi Zero 2W에서 모드별 실행시간 profiling, mode feasibility table 작성. KCC 이용률 표를 평균·p95·p99·최대로 재계산.
- [ ] 검증 실험: 일반 Linux vs PREEMPT_RT 응답시간·jitter 비교.
- [ ] 정책 평가: baseline 5종과 제안 정책 비교.

### 10.4 미결 설계 질문

- `q`를 anomaly score, health index, confidence 중 무엇으로 확정할지.
- 실행 가능 판정의 기준을 p95, p99, 최대 중 무엇으로 둘지.
- 전환이 잦아지지 않도록 hysteresis를 얼마나 둘지.

---

## 참고문헌

- [1] S. Langarica, C. Rüffelmacher, F. Núñez, "An Industrial Internet Application for Real-Time Fault Diagnosis in Industrial Motors," IEEE Trans. Automation Science and Engineering, 2020.
- [2] J. P. B. Lima, "Real-Time Fault Detection in Induction Motors Using TinyML: An Evaluation of the Edge Impulse Platform," IEEE Latin Conf. on IoT (LCIoT), 2025.
- [3] B. Pubalan, M. S. R. M. Saufi, M. S. Leong, A. Jamali, "Real-Time Bearing Fault Detection and Visualization Using 1D CNN: A Simulated Deployment with the CWRU Dataset," IEEE ICSIMA, 2025.
- [4] C. Yang, Z. Lai, Y. Wang, S. Lan, L. Wang, L. Zhu, "A Novel Bearing Fault Diagnosis Method Based on Stacked Autoencoder and End-Edge Collaboration," IEEE CSCWD, 2023.
- [5] C. He, P. Han, J. Lu, X. Wang, J. Song, Z. Li, S. Lu, "Real-Time Fault Diagnosis of Motor Bearing via Improved Cyclostationary Analysis Implemented onto Edge Computing System," IEEE Trans. Instrumentation and Measurement, 2023.
- [6] S. Arciniegas, D. Rivero, J. Piñan, E. Diaz, F. Rivas, "IoT Device for Detecting Abnormal Vibrations in Motors Using TinyML," Discover Internet of Things, 2025.
- [7] S. Ma, H. Sun, S. Gao, G. Zhou, "A Real-Time Mechanical Fault Diagnosis Approach Based on Lightweight Architecture Search Considering Industrial Edge Deployments," Engineering Applications of Artificial Intelligence, 2023.
- [8] 최성현, 김서랑, 김태현, "저비용 마이크로컨트롤러 환경에서의 경량 딥러닝 기반 회전기계 축 결함 진단 시스템," 한국소프트웨어종합학술대회 (KSC), 2025.
- [9] G. C. Buttazzo, G. Lipari, L. Abeni, "Elastic Task Model for Adaptive Rate Control," IEEE RTSS, 1998; G. C. Buttazzo, G. Lipari, M. Caccamo, L. Abeni, "Elastic Scheduling for Flexible Workload Management," IEEE Trans. Computers, 2002.
- [10] S. M. Salman, S. Mubeen, F. Marković, A. V. Papadopoulos, T. Nolte, "Scheduling Elastic Applications in Compositional Real-Time Systems," IEEE ETFA, 2021.
- [11] R. Gifford, F. Galarza-Jiménez, L. T. X. Phan, M. Zamani, "Decntr: Optimizing Safety and Schedulability with Multi-Mode Control and Resource Allocation Co-Design," IEEE RTAS, 2024.
- [12] S. Xu, B. Ghosh, C. Hobbs, P. S. Thiagarajan, P. Joshi, S. Chakraborty, "Safety-Aware Implementation of Control Tasks via Scheduling with Period Boosting and Compressing," IEEE RTCSA, 2023.
- [13] P. Burgio, M. Ruggiero, F. Esposito, M. Marinoni, G. Buttazzo, L. Benini, "Adaptive TDMA Bus Allocation and Elastic Scheduling," IEEE ICCD, 2010.
- [14] R. Li, Z. Song, M. Lv, J.-M. Wu, C. J. Xue, J. Wang, N. Guan, "ATER: Adaptive Task Execution Rate Regulation for Enhanced Real-Time Performance in ROS 2," IEEE RTCSA, 2025.
- [15] M. Kim, S. Lee, D. Oh, B. Park, J. Jo, C. Lee, "Anomaly Deviation-Based Window Size Selection of Sensor Data for Enhanced Fault Diagnosis Efficiency in Autonomous Manufacturing Systems," Mathematics, 2026.
- [16] G. Tang, C. Yi, L. Liu, Z. Xing, Q. Zhou, J. Lin, "Integrating Adaptive Input Length Selection Strategy and Unsupervised Transfer Learning for Bearing Fault Diagnosis under Noisy Conditions," Applied Soft Computing, 2023.
- [17] G. Tang, C. Yi, L. Liu, X. Yang, D. Xu, Q. Zhou, J. Lin, "A Novel Transfer Learning Network with Adaptive Input Length Selection and Lightweight Structure for Bearing Fault Diagnosis," Engineering Applications of Artificial Intelligence, 2023.
- [18] W. Kang, S. Chung, J. Y. Kim, Y. Lee, K. Lee, J. Lee, K. G. Shin, H. S. Chwa, "DNN-SAM: Split-and-Merge DNN Execution for Real-Time Object Detection," IEEE RTAS, 2022.
- [19] Y. Li, Z. Li, A. A. Arafat, D. Johnson, N. Sui, A. Gehi, Z. Guo, "Adaptive Model Selection for Real-Time Heart Disease Detection on Embedded Systems," IEEE RTCSA, 2025.
- [20] Y. Xu, Z. Liu, X. Fu, S. Liu, F. Wu, G. Chen, "FLEX: Adaptive Task Batch Scheduling with Elastic Fusion in Multi-Modal Multi-View Machine Perception," IEEE RTSS, 2024.
- [21] S. Yao, Y. Hao, Y. Zhao, H. Shao, D. Liu, S. Liu, T. Wang, J. Li, T. Abdelzaher, "Scheduling Real-Time Deep Learning Services as Imprecise Computations," IEEE RTCSA, 2020.
- [22] 이태훈 외, KCC 2026 선행연구 (STM32F407 + Zephyr RTOS 실시간 추론 성능 분석). 정식 서지정보 확정 필요.
