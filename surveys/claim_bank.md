# Claim Bank

연구 주장 후보를 정리하는 파일이다.

## Claims

- classic elastic scheduling은 periodic task의 period/rate를 조절해 overload나 workload 변화에서 schedulability를 유지하는 시스템 축의 대표 관련연구다.
  - 근거 후보: Buttazzo et al. RTSS 1998, Buttazzo et al. IEEE Transactions on Computers 2002.
  - 본 연구 연결: 본 연구의 `H` 또는 diagnosis period를 elastic variable로 정식화할 때 기본 비교군으로 활용 가능하다.
  - 주의: 이 계열은 general real-time scheduling 중심이며, vibration fault diagnosis의 window W, model M, machine condition trigger, PREEMPT_RT/SBC 실험을 직접 다루지는 않는다.

- 최신 elastic scheduling 계열은 task 단위 period 조절을 넘어 parallel DAG task의 subtask workload와 core allocation까지 확장된다.
  - 근거 후보: Sudvarg et al. RTSS 2024.
  - 본 연구 연결: system slack과 schedulability 제약을 보고 workload를 조절하는 최신 비교군으로 사용할 수 있다.
  - 주의: 이 논문도 trigger는 limited resources/schedulability 중심이며, machine condition과 fault-diagnosis utility를 함께 쓰는 구조는 현재 카드 기준 확인되지 않았다.

- real-time DNN serving 계열에서도 runtime에 batch 구성과 model 내부 처리량을 조절해 deadline과 perception quality의 trade-off를 다루는 연구가 있다.
  - 근거 후보: Yao et al. RTCSA 2020, Imprecise DL Services; Xu et al. RTSS 2024, FLEX; Cao et al. arXiv 2026, EdgeServing; Han et al. MobiSys 2024, Pantheon.
  - 본 연구 연결: system slack/deadline 조건으로 runtime mode를 선택한다는 점은 본 연구의 `S -> (W,H,M)` 정책과 비교 가능하다.
  - 주의: Yao et al.은 DNN stage/depth를 imprecise computation으로 조절하고, FLEX는 batch/fusion configuration, EdgeServing은 model/exit/batch, Pantheon은 GPU runtime preemption과 early-exit variant adaptation을 다룬다. 이 계열은 vibration fault diagnosis의 window W, diagnosis period H, anomaly score trigger, PREEMPT_RT 커널 실시간성은 다루지 않는다.

- 입력 크기 조절은 vision perception 분야에서 latency/accuracy/deadline trade-off를 만드는 scheduling variable로 사용되어 왔다.
  - 근거 후보: Hu et al. RTCSA 2021, Hu et al. Real-Time Systems 2022, Liu et al. Real-Time Systems 2023, Hu et al. RTAS 2024.
  - 본 연구 연결: vibration fault diagnosis에서는 image size가 아니라 window size W가 입력 크기 역할을 하며, window는 latency뿐 아니라 결함 정보 보존과도 연결된다.
  - 주의: 위 논문들은 vision domain과 embedded GPU 중심이므로, 본 연구의 MCU/SBC, PREEMPT_RT, vibration FD novelty를 직접 증명하는 근거로 쓰면 안 된다.

- 기존 image resizing 계열은 criticality, object uncertainty, deadline, workload를 trigger로 사용하지만 machine condition과 system slack을 함께 쓰는 구조는 확인되지 않았다.
  - 근거 후보: 네 편 모두 object criticality 또는 deadline/workload 중심.
  - 본 연구 연결: anomaly score 기반 machine condition과 slack 기반 system condition을 함께 쓰는 정책의 차별점 후보.
  - 주의: fault diagnosis 쪽 adaptive window 논문을 추가로 확인한 뒤 claim 강도를 조정해야 한다.

- fault diagnosis에서도 window size W는 단순 전처리 파라미터가 아니라 anomaly representation과 diagnostic sensitivity를 좌우하는 design variable로 다뤄질 수 있다.
  - 근거 후보: Kim et al., Mathematics 2026, ADW.
  - 본 연구 연결: 본 연구의 W 선택을 fault diagnosis 성능 축과 연결하는 근거로 활용 가능하다.
  - 주의: ADW는 deviation score 기반 offline window selection에 가깝고, system slack, deadline, RTOS/PREEMPT_RT를 포함한 runtime scheduling은 다루지 않는다.

- bearing fault diagnosis 문헌에서도 fixed input length 대신 bearing parameter와 sampling frequency를 반영한 adaptive input length selection이 제안되어 있다.
  - 근거 후보: Tang et al., Applied Soft Computing 2023, AANTLN; Tang et al., Engineering Applications of Artificial Intelligence 2023, AILWTLN.
  - 본 연구 연결: window size W를 물리적 결함 정보와 연결해 정해야 한다는 문제의식을 강화하는 비교군으로 활용 가능하다.
  - 주의: 두 논문 모두 system slack, deadline, RTOS/PREEMPT_RT 기반 runtime scheduling을 다루지는 않는다.

- vibration-based bearing fault diagnosis에서도 segment/window length는 speed variation과 real-time processing 가능성에 직접 연결되는 설계 변수로 다뤄진다.
  - 근거 후보: Jalonen et al., ICIT 2024.
  - 본 연구 연결: `W`를 단순 모델 입력 크기가 아니라 motor speed variation, acquisition duration, inference time을 함께 고려하는 변수로 설명할 수 있다.
  - 주의: 해당 논문은 runtime adaptation이 아니라 offline segment length design과 real-time inference evaluation에 가깝다. system slack, H/M selection, PREEMPT_RT는 다루지 않는다.

- 현재까지 정리한 input-adaptive 문헌은 `입력 크기/길이` 또는 `검사 빈도`를 조절하지만, `machine condition + system slack`을 함께 사용해 `W + H + M`을 runtime에 선택하는 구조는 확인되지 않았다.
  - 근거 후보: `surveys/comparison_table.md`의 `Trigger`, `Runtime/Offline`, `RT Constraint`, `Gap` 컬럼.
  - 본 연구 연결: novelty 주장의 중심 후보. 단, elastic scheduling 및 RT-DNN serving 문헌까지 확장 비교한 뒤 claim 강도를 조정해야 한다.
