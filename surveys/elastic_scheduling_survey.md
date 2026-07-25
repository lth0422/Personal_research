# Elastic Scheduling 서베이 정리

> 작성일: 2026-07-25  
> 대상 카드: `surveys/paper_cards/01_elastic_scheduling/` 19편  
> 목적: 이론 발전 계보와 실제 적용 사례를 구분해 본 연구의 연결점과 gap을 한눈에 파악한다.

본 연구 관련 기호 정의: W=입력 윈도우 크기, H=hop/진단 주기, M=모델, C(W,M)=모드별 실행시간, z=기계 상태, S=시스템 슬랙

---

## Section 1: 이론 발전 계보

### 읽는 법

- **C 가정** 열이 핵심이다. 기존 이론은 거의 C 고정을 전제한다. 본 연구의 C(W,M)처럼 모드에 따라 C가 달라지면 기존 feasibility 조건을 그대로 쓸 수 없다.
- **트리거** 열에 "system overload/부하"만 있으면, 기계 상태 z를 쓰는 본 연구와 차별화 지점이 생긴다.

| 논문 | 연도 | venue | 핵심 확장 (이전 대비) | 가변 변수 | C 가정 | feasibility 조건 | 트리거 | 본 연구와의 gap |
|---|---|---|---|---|---|---|---|---|
| Buttazzo, Lipari, Abeni [1] | 1998 | RTSS | **원형 제안** — spring 모델, elastic coefficient, period 압축 | period T | 고정 | EDF·RM utilization bound | rate 변경 요청, overload | W·H·M·z·PREEMPT_RT 없음 |
| Buttazzo, Lipari, Caccamo, Abeni [2] | 2002 | IEEE TC | 1998 확장 — decompression·SRP blocking 분석·period 안전 전환 규칙 | period T | 고정 | utilization bound + SRP blocking | overload, rate 요청 | 동일. 실행시간 추정은 future work |
| Buttazzo, Abeni [3] | 2000 | CDC | 런타임 C 추정 기반 period 피드백 (별도 계보) | period T | 런타임 관측값 (C_mean·C_max 가중합) | empirical estimated load | 커널이 관측한 실행시간 | soft RT (transient miss 허용). C(W,M) 모드 semantics 없음 |
| Chantem, Hu, Lemmon [4] | 2009 | IEEE TC | **일반화** — constrained deadline D≤T, QP optimization으로 확장 | period T, deadline D | 고정 | QP 기반 heuristic + EDF schedulability | system overload | vibration W·M·z 없음. heuristic, optimal 아님 |
| Tian, Gui [5] | 2011 | RTS | QoC feedback을 elastic scheduling과 결합한 control 특화 확장 | period T, utilization | 고정 | QoC 최대화 constrained optimization | QoC measurement, workload | control QoC ≠ vibration diagnosis utility |
| Marinoni, Buttazzo [6] | 2007 | IEEE TII | elastic scheduling + DVS 통합 — discrete freq·voltage mode 공동 조절 | period T, CPU freq/voltage mode | freq에 따라 scaled (WCET table) | elastic utilization + WCET table | processor utilization vs. available speed | CPU mode ≠ inference model M. z·W 없음 |
| Wang, Li, Wonham [7] | 2016 | IEEE TII | TDES supervisory control — multiple-period safe sequence 형식 합성 | period T (범위에서 선택) | 고정 WCET | non-blocking safe language (TDES) | initial model infeasible 시 offline reconfiguration | runtime slack·z·W·M 없음. offline only |
| Baruah [8] | 2023 | RTNS | constrained deadline elastic task에 PDA 직접 적용 — utilization 근사 대신 정확한 demand-bound | period T | 고정 | processor-demand analysis (exact EDF) | offline period assignment | C(W,M) 가변 없음. runtime trigger 없음 |
| Sudvarg, Gill, Baruah [9] | 2021 | RTS | O(n) 온라인 admission control — O(n²) compression 개선 | utilization, period | 고정 | utilization bound (linear time) | new task admission, overload | algorithm 효율성 연구. 도메인 없음 |
| Sudvarg, Gill, Baruah [10] | 2025 | LITES | quasilinear compression·multiprocessor 확장 (partition EDF, global EDF/RM) | utilization, period | 고정 | utilization bound (quasilinear/polynomial) | overload, resource 변화 | algorithm 효율성 연구. 도메인 없음 |
| Sudvarg et al. [11] | 2024 | RTAS | **harmonic task system 확장** — offline lookup table + online binary search | period T (harmonic 제약) | 고정 | harmonic EDF schedulability | available CPU bandwidth 변화 | H harmonic constraint 참고. z·W·M·PREEMPT_RT 없음 |
| Sudvarg et al. [12] | 2024 | RTSS | **subtask-level 확장** — parallel DAG subtask workload compression, core allocation | subtask workload, utilization, core | resource allocation별 profiling | federated scheduling demand-bound | limited resource, overload | multicore·DAG 중심. vibration 단일 태스크와 구조 다름 |
| Sudvarg (dissertation) [13] | 2024 | PhD | 위 Sudvarg 계열 논문 종합 (constrained-deadline·harmonic·subtask·FIMS·ORB-SLAM3) | 전체 | 전체 | 전체 | 전체 | 개별 출판 논문 우선 인용. dissertation은 배경 보조 |

### 이론 계보 흐름 요약

```
Buttazzo 1998 (원형: spring, period compression, EDF/RM bound)
    │
    ├── Buttazzo 2002 (SRP blocking, decompression 공식화)
    │
    ├── Buttazzo & Abeni 2000 (런타임 C 추정 → soft RT 별도 계보)
    │
    ├── Chantem 2009 (D≤T 일반화, QP optimization)
    │       │
    │       └── Baruah 2023 (PDA 정확한 demand-bound)
    │
    ├── Tian 2011 (QoC feedback 결합)
    │
    ├── Marinoni 2007 (DVS discrete mode 결합)
    │
    ├── Wang 2016 (TDES formal safe sequence 합성)
    │
    └── Sudvarg 계열 (2021→RTAS 2024→RTSS 2024→LITES 2025→dissertation)
             │
             admission control O(n) → harmonic → subtask·DAG → quasilinear
```

### 본 연구 관련 핵심 관찰

- **모든 이론 논문은 C 고정을 전제**한다. 본 연구의 C(W,M) — 즉 모드마다 실행시간이 달라지는 구조 — 는 기존 이론의 직접 적용 범위를 벗어난다.
- **트리거가 전부 시스템 부하나 utilization 변화**다. 기계 상태 z(anomaly score)를 트리거로 쓰는 사례는 없다.
- Buttazzo & Abeni 2000이 런타임 C 추정을 쓰는 가장 가까운 사례지만 soft RT이며 진단 utility 개념이 없다.
- Baruah 2023은 D < T 구조를 다루므로 본 연구 diagnosis task deadline model 선택 시 참고할 feasibility 분석 배경이다.

---

## Section 2: 실제 적용 사례

### 읽는 법

- **트리거** 열이 핵심이다. 기계 상태 z(anomaly score) 기반이 있으면 즉시 novelty 재점검 필요.
- **보장 수준** 열에서 hard, soft, empirical을 구분한다.

| 논문 | 연도 | venue | 응용 도메인 | 가변 변수 | 트리거 | 플랫폼·환경 | 보장 수준 | 본 연구와의 gap |
|---|---|---|---|---|---|---|---|---|
| Burgio et al. [15] | 2010 | ICCD | MPSoC 실시간 제어 (shared TDMA bus) | TDMA slot·bandwidth, period T | core workload 변화로 bandwidth 요청 발생 | STBus MPSoC, ERIKA RTOS, EDF | TDMA isolation + WCET table + elastic bound (hard 지향) | 중앙 master + offline WCET table 필요. z·W·M 없음 |
| Salman et al. [16] | 2021 | ETFA | 분산 CPS — compositional/hierarchical 실시간 | period T, reservation bandwidth | bandwidth 초과, period 변경 요청 | uniprocessor compositional evaluation | two-level (application period → system bandwidth) | vibration W·M·z·PREEMPT_RT 없음. reservation ↔ slack S mapping 별도 필요 |
| Gifford et al. (Decntr) [17] | 2024 | RTAS | 멀티모드 CPS 제어 (automotive) — controller + scheduling + resource co-design | controller, period T, core mapping, cache·bandwidth allocation | runtime mode-change event (ex. 장애물 감지) | Intel Xeon 16-core + CAT·MemGuard profiling / RPi 3 B+ WCET | DBF schedulability (mode별·transition별), linear plant safety invariant | **구조적으로 가장 가까운 비교군.** vibration window W, diagnosis utility, anomaly score, PREEMPT_RT measurement 없음 |
| Xu et al. (Safety-Aware) [18] | 2023 | RTCSA | Automotive safety-critical feedback control | common period T (boosting·compressing) | offline only — WCET·plant model·safety margin 입력 | Julia 구현, control model 평가 | weakly-hard constraint + automata schedule synthesis (offline) | runtime slack·z·W·M 없음. offline synthesis only. safety margin ≠ diagnosis utility |
| Li et al. (ATER) [19] | 2025 | RTCSA | ROS 2 자율 시스템 publish-subscribe task chain | sensor sampling rate R_tmr (timer period 역수) | runtime observer: message drop indicator, 처리율 vs. backlog | Intel Core i7 desktop, Ubuntu 22.04, ROS 2 Humble | empirical feedback regulation (hard deadline·admission 없음) | **diagnosis period H와 가장 직접 대응.** 그러나 vibration W·M, anomaly z, feasible-mode admission, PREEMPT_RT 없음 |

### 실제 적용 계열 관찰

- **Decntr** — 사전 profiling한 feasible mode set 안에서 runtime event로 mode를 선택하는 구조가 본 연구와 가장 가깝다. 차이: 제어 안전 invariant vs. 진단 utility, controller/resource co-design vs. W·H·M 선택.
- **ATER** — runtime rate regulation이 diagnosis period H 조절과 직접 대응된다. 차이: empirical soft RT vs. feasible-mode admission. 기계 상태 트리거 없음.
- **Safety-Aware** — weakly-hard miss와 application-level utility를 연결한다. 본 연구에서 일부 deadline miss를 허용할 경우의 비교군.
- **Burgio, Salman** — elastic scheduling을 시스템 자원(bus·reservation)과 결합한 사례. 본 연구는 단일 SBC에서 C(W,M)과 H를 함께 조절하므로 구조가 다름.

---

## 전체 Summary

### 본 연구가 채우는 자리

| 항목 | 기존 이론·적용 최선 사례 | 본 연구 |
|---|---|---|
| C 가정 | 고정 (이론), offline profiling table (Decntr) | 측정 기반 C(W,M) — 모드마다 달라짐 |
| 트리거 | 시스템 부하·utilization·bandwidth 변화 | 기계 상태 z (anomaly score) + 시스템 슬랙 S |
| 가변 변수 | period T (대부분), subtask workload (Sudvarg RTSS) | W, H, M 동시 |
| 플랫폼 | 이론 (uniprocessor), MPSoC, ROS 2 desktop | Pi Zero 2W + Linux/PREEMPT_RT |
| 도메인 | general RT, control, autonomous driving | 진동 기반 결함 진단 |
| 진단 utility 정의 | QoC (Tian), control safety (Decntr, Safety-Aware) | 미정 — anomaly score 기반 후보 |

### 인용 우선순위 (본 연구 원고 기준)

- **이론 배경**: Buttazzo 1998·2002 (원형), Chantem 2009 (일반화), Baruah 2023 (D<T)
- **runtime C 피드백 근거**: Buttazzo & Abeni 2000 (단, soft RT 한계 명시)
- **구조적 비교군**: Decntr 2024 (mode set offline synthesis + runtime selection)
- **H 조절 비교군**: ATER 2025 (rate regulation, empirical)
- **application safety 비교군**: Safety-Aware 2023 (weakly-hard miss 허용 논거)
- **알고리즘 overhead**: Sudvarg 2021, LITES 2025 (runtime mode switch 비용 배경)

---

## 참고문헌

### 이론 발전 계보

[1] G.C. Buttazzo, G. Lipari, L. Abeni, "Elastic Task Model For Adaptive Rate Control," Proc. 19th IEEE Real-Time Systems Symposium (RTSS), 1998

[2] G.C. Buttazzo, G. Lipari, M. Caccamo, L. Abeni, "Elastic Scheduling for Flexible Workload Management," IEEE Transactions on Computers, Vol. 51, No. 3, 2002

[3] G. Buttazzo, L. Abeni, "Adaptive Rate Control through Elastic Scheduling," Proc. 39th IEEE Conference on Decision and Control (CDC), 2000

[4] T. Chantem, X.S. Hu, M.D. Lemmon, "Generalized Elastic Scheduling for Real-Time Tasks," IEEE Transactions on Computers, 2009

[5] Y.-C. Tian, L. Gui, "QoC Elastic Scheduling for Real-Time Control Systems," Real-Time Systems, 2011

[6] M. Marinoni, G. Buttazzo, "Elastic DVS Management in Processors With Discrete Voltage/Frequency Modes," IEEE Transactions on Industrial Informatics, 2007

[7] X. Wang, Z. Li, W.M. Wonham, "Dynamic Multiple-Period Reconfiguration of Real-Time Scheduling Based on Timed DES Supervisory Control," IEEE Transactions on Industrial Informatics, 2016

[8] S. Baruah, "Improved Uniprocessor Scheduling of Systems of Sporadic Constrained-Deadline Elastic Tasks," RTNS 2023

[9] M. Sudvarg, C. Gill, S. Baruah, "Linear-Time Admission Control for Elastic Scheduling," Real-Time Systems, 2021

[10] M. Sudvarg, C. Gill, S. Baruah, "Improved Elastic Scheduling Algorithms for Implicit-Deadline Tasks," Leibniz Transactions on Embedded Systems (LITES), 2025

[11] M. Sudvarg, A. Li, D. Wang, S. Baruah, J. Buhler, C. Gill, N. Zhang, P. Ekberg, "Elastic Scheduling for Harmonic Task Systems," RTAS 2024

[12] M. Sudvarg, D. Wang, J. Buhler, C. Gill, "Subtask-Level Elastic Scheduling," RTSS 2024

[13] M.B. Sudvarg, "Improved Models of Elastic Scheduling," PhD Dissertation, 2024

[14] J. Orr, J. Condori Uribe, C. Gill, S. Baruah, K. Agrawal, S. Dyke, A. Prakash, I. Bate, C. Wong, S. Adhikari, "Elastic Scheduling of Parallel Real-Time Tasks with Discrete Utilizations," RTNS 2020

### 실제 적용 사례

[15] P. Burgio, M. Ruggiero, F. Esposito, M. Marinoni, G. Buttazzo, L. Benini, "Adaptive TDMA Bus Allocation and Elastic Scheduling," IEEE International Conference on Computer Design (ICCD), 2010

[16] S.M. Salman, S. Mubeen, F. Markovic, A.V. Papadopoulos, T. Nolte, "Scheduling Elastic Applications in Compositional Real-Time Systems," ETFA 2021

[17] R. Gifford, F. Galarza-Jimenez, L.T.X. Phan, M. Zamani, "Decntr: Optimizing Safety and Schedulability with Multi-Mode Control and Resource Allocation Co-Design," RTAS 2024

[18] S. Xu, B. Ghosh, C. Hobbs, P.S. Thiagarajan, P. Joshi, S. Chakraborty, "Safety-Aware Implementation of Control Tasks via Scheduling with Period Boosting and Compressing," RTCSA 2023

[19] R. Li, Z. Song, M. Lv, J.-M. Wu, C.J. Xue, J. Wang, N. Guan, "ATER: Adaptive Task Execution Rate Regulation for Enhanced Real-Time Performance in ROS 2," RTCSA 2025
