# DNN-SAM: Split-and-Merge DNN Execution for Real-Time Object Detection

- **그룹**: 3 rt_dnn_serving
- **연구 섹션**: S4 deadline-aware AI inference and mode selection (slack → 입력 fidelity 직접 비교군), S5 schedulability
- **출처/연도**: IEEE RTAS 2022, DOI 10.1109/RTAS54340.2022.00021
- **저자**: Woosung Kang, Siwoo Chung, Jeremy Yuhyun Kim, Youngmoon Lee, Kilho Lee, Jinkyu Lee, Kang G. Shin, Hoon Sung Chwa
- **분석 MD**: `papers/03_rt_dnn_serving/reviews/dnn_sam.pdf`

## 두 질문
- **가변 변수**: optional subtask의 spatial input scale. `0`을 포함한 이산 후보 집합 `S^O = {0, 160, 256, 320, 416, 512, 608, 672}`에서 선택한다. mandatory subtask는 매 frame safety-critical RoI를 원 해상도로 처리하며, DNN model이나 layer depth는 바꾸지 않는다.
- **트리거**: 두 신호가 서로 다른 결정을 담당한다.
  - LiDAR·camera·IMU 기반 time-to-collision(ToC)으로 RoI criticality(위치·크기)를 정한다. `ToC_threshold = 2 s` (60 km/h에서 약 33 m 이내를 critical로 간주).
  - runtime system slack으로 optional input scale을 정한다. slack 안에 들어가는 가장 큰 scale을 고른다.

## Abstract 3줄 요약
- 다중 카메라 실시간 객체 검출은 영상 영역별 safety criticality가 다른데 기존 DNN 실행은 전체 영상을 동일 해상도·연산량으로 처리한다.
- DNN-SAM은 한 inference를 critical RoI용 mandatory subtask와 down-scaled 전체 영상용 optional subtask로 나누고 결과를 merge한다.
- 두 scheduler가 mandatory를 우선하며 optional input scale을 deadline과 slack에 맞춰 조절해, 기존 대비 RoI accuracy 2.0~3.7배, latency 4.8~9.7배 개선을 보고한다.

## 논리 흐름 + Novelty
- 기존 DNN inference의 한계: 전체 영상 동일 처리, safety-critical 영역 우선 없음, 여러 DNN task를 FIFO로 실행, accuracy↑ 시 execution time↑, 배포 후 고정 model 하나만 제공.
- Split-and-Merge: 하나의 job을 mandatory(RoI crop, 원 해상도)와 optional(전체 영상 down-scale)로 분할. **DNN layer·weight를 나누는 게 아니라 동일 unmodified FCN(YOLOv3)에 서로 다른 input을 전달**하며 두 thread가 같은 parameter를 공유해 model을 복제하지 않는다. 결과는 global coordinate로 변환 후 IoU + cut-off redundancy metric으로 중복 제거해 merge한다.
- **Novelty (시스템·스케줄링 contribution)**: 새 architecture·재학습이 아니라 (1) imprecise-computation형 mandatory/optional execution model, (2) unmodified DNN에 crop/scaled input을 전달하는 transparent split-and-merge interface, (3) mandatory early return, (4) RoI criticality 기반 differentiated service, (5) runtime slack에 따른 optional input-scale selection, (6) non-preemptive EDF 기반 sufficient schedulability analysis.

## 핵심 수치

### 기본 정보
| 지표 | 값 |
|---|---|
| 플랫폼 | NVIDIA Jetson AGX Xavier, Ubuntu 18.04.4, CUDA 10.0, DarkNet, YOLOv3 |
| Dataset | KITTI in-vehicle camera, 7,481 images. classes: car, pedestrian |
| Execution | GPU subtask-level non-preemptive |
| Mandatory input | 최대 256×256 RoI crop |
| Optional scale 집합 | `{0, 160, 256, 320, 416, 512, 608, 672}` (0 = optional 생략) |
| Deadline | `D_i = T_i` (implicit) |

### 스케줄링 모델
- Task: `τ_i = (τ_i^M, τ_i^O, T_i, D_i)`, `τ_i^M = (R_i^M, C_i^M)`, `τ_i^O = (S_i^O, C_i^O)`
- Mandatory cost: `C_i^M = c^RoI + c^Split + c^Infer` = 9.0 + 7.5 + 40.3 = **56.8 ms** (측정 최대)
- Optional cost: `C_i^O(s) = c^Infer(s) + c^Merge` (scale별 표: 160→34.0, 256→40.9, 512→137.3, 672→226.5 ms 측정 최대)
- Non-preemptive EDF sufficient condition (Eq. 3):

$$\frac{\max_{\tau^M \in \tau} C_i^M}{\min_{\tau_i^M \in \tau} T_i} + \sum_{\tau_i^M \in \tau} \frac{C_i^M}{T_i} \le 1$$

  첫째 항은 non-preemptive blocking(higher-priority job이 실행 중 lower-priority subtask에 막힘)을 보수적으로 반영, 둘째 항은 mandatory utilization 합. Eq.3 만족 시 EDF-MandFirst·EDF-Slack 모두 mandatory와 선택된 optional sub-job의 deadline miss 없음. **단 sufficient condition이라 불만족이 곧 unschedulable은 아님.**
- EDF-Slack reclaim: `Slack(t_cur, d_1) = d_1(t_cur) − t_cur − p`, `s* = argmax {C^O(s) | C^O(s) ≤ Slack}`. runtime 전체에서 `U^M(t) + U^O(t) ≤ 1` 유지.
- 두 scheduler: EDF-MandFirst(O(1), mandatory 항상 우선, 단순 slack), EDF-Slack(O(n), earlier-deadline optional 먼저 가능, reclaimable slack).

### 결과 (2-task: 7 FPS, 3 FPS; baseline: Vanilla DarkNet FIFO)
| 지표 | 값 |
|---|---|
| RoI accuracy (Car) | 5.7% → 21.0% (**3.7×**) |
| RoI accuracy (Pedestrian) | 14.4% → 29.3% (**2.0×**) |
| Overall AP (EDF-Slack) | Car 38.2%, Pedestrian 45.4% |
| RoI inference response | 평균 **9.7× 빠름** |
| Entire-image result | 평균 **4.8× 빠름** |
| Emergency braking (1/10 AV) | perception-reaction 1.9× 감소, worst-case 정지 1.3 m < safety 1.5 m |

## Deadline·RT 판정
| 판정 항목 | 결과 | 근거 |
|---|---|---|
| 명시적 deadline | O | periodic, `D_i = T_i` |
| Schedulability 분석 | O | non-preemptive EDF sufficient condition Eq.3, Theorems 1-2 |
| WCET 근거 | 측정 최대 | 각 component 1,000회 실행 max |
| Formal WCET | X | static timing analysis·hardware bound 없음 |
| Deadline miss 평가 | O | FPS requirement vs observed minimum FPS |
| Miss ratio / p99 | X | 미보고 |
| Multi-task interference | O | 1~4 concurrent DNN tasks |

- **RT 등급**: 측정 기반 조건부 schedulability. non-preemptive EDF sufficient condition + theorem을 제공하므로 best-effort(B)보다 강하나, `C^M`·`C^O(s)`가 formal WCET가 아니라 1,000회 측정 max라 unseen execution이 초과하면 theorem 전제가 깨진다. 즉 **E와 H 사이의 조건부 보장**이다. (분석 노트는 이를 W로 표기했으나, 본 프로젝트 등급 정의상 W=weakly-hard `(m,k)`와는 구분해야 한다. DNN-SAM은 weakly-hard가 아님.)

## 개인연구 관점 — novelty 차원 ①~⑥
| 차원 | DNN-SAM | 근거 |
|---|:---:|---|
| ① 정확도 바꿈 | O | optional scale↓ → execution cost·accuracy 함께 감소 |
| ② 외부 기계상태 트리거 | △ | LiDAR·IMU ToC는 external physical state로 critical RoI를 정하지만 machine-health condition q는 아님 |
| ③ slack을 별도 제약으로 | O | mandatory schedulability를 보존하는 feasible slack 안에서 optional scale 선택 |
| ④ W·H·M 공동 (W/H 분리) | X | spatial scale 하나만 runtime 조절. period·model 고정, temporal W와 hop H 분리 안 함 |
| ⑤ 진동 FD | X | autonomous-driving vision object detection |
| ⑥ 스케줄 가능성 검증 | O | Eq.3, Theorems 1-2, non-preemptive EDF. 단 measurement-based WCET 조건부 |

> 참고: DNN-SAM ②는 △로 확정. ToC가 external physical state라는 점에서 [24] Chwa(②=O)와 일관되게 X가 아닌 △로 판정한다(machine-health condition q는 아니므로 O도 아님). v1_4 문서 novelty 표(md·tex·xlsx)도 △로 통일 완료.

## 내 연구 관점
- 한 줄 gap: DNN-SAM은 schedulability를 먼저 보존한 뒤 runtime slack으로 input fidelity를 최대화하는 강한 선례지만, GPU vision에서 spatial scale만 조절하며 vibration-domain의 temporal `W`, hop `H`, model `M`과 machine-health state `q`를 공동 선택하지 않는다.
- 내 연구에 쓸 곳: (1) "system slack → 입력 fidelity" 정책의 가장 강한 직접 비교군. `F(k) = {s : C^O(s) ≤ Slack}`, `s* = argmax Q(s)` 구조가 개인연구 feasibility-first 정책과 형식적으로 동일. (2) non-preemptive EDF sufficient condition + slack reclaim은 To-Do 10.2(모드 전환 안전 조건·이용률 bound 재유도)의 직접 참고. (3) 측정 최대를 WCET로 쓰는 조건부 보장 방식은 우리 PREEMPT_RT 실측 기반 feasibility와 같은 성격 — 단 formal WCET가 아님을 명확히 구분해야 함.
- Related Work 영어 한 줄:
  > Kang et al. used non-preemptive EDF scheduling and runtime slack reclamation to maximize the input scale of optional object-detection subtasks while preserving mandatory-task schedulability, but their policy adapted only spatial image fidelity on a GPU and did not jointly select temporal windows, diagnosis periods, and models using machine-health state.

## 불확실한 점
1. `C_i^M`·`C_i^O(s)`는 formal WCET가 아니라 1,000회 측정 maximum이다.
2. Profiling 이후 더 큰 execution time 발생 시 theorem guarantee 유지 여부 미검증.
3. KITTI에 IMU data가 없어 main evaluation은 constant vehicle speed 가정.
4. ToC threshold 2 s가 모든 driving condition에서 안전한지는 논문 범위 밖.
5. RoI max 256×256은 camera FOV·speed limit에 따라 사전 설정, 자동 최적화 아님.
6. accuracy 2.0~3.7배는 2-task/7·3 FPS의 Baseline-Downscaled 대비 RoI AP.
7. latency 4.8~9.7배는 EDF-MandFirst average result이며 모든 workload 보편값 아님.
8. deadline miss ratio·p99 latency 미보고, per-job response-time distribution 없음.
9. CPU-side RoI/split/merge/scheduler의 preemption·interference model, CPU-GPU shared-memory·bus interference upper bound 미분석.
10. optional scale과 accuracy의 단조 관계는 formal guarantee 없이 profiling 경향에 의존.
