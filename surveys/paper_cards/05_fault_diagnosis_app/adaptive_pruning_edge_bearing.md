# Edge-Oriented Bearing Fault Diagnosis via Triple-Lightweight Network With Adaptive Pruning

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S3 (경량화 대조군), S4 (edge inference 자원 측정)
- **플랫폼 태그**: `PL-HET-SOC`
- **실행환경 태그**: `ENV-LINUX` (Ubuntu 20.04, JetPack 5.1.2, TensorRT 8.5.1.7)
- **출처/연도**: IEEE Transactions on Instrumentation and Measurement, Vol. 75, 2026, DOI 10.1109/TIM.2026.3699722
- **저자**: Zhaokang Zhan, Siqi Zhang, Jiacan Xu, Dazhong Ma
- **분석 MD**: `papers/05_fault_diagnosis_app/reviews/Zhan_2026_APTL_Net_Adaptive_Pruning_분석.md`

---

## 두 질문

- **가변 변수**: 없음. W (sample 수 미보고), H (미정의), M (offline pruning으로 하나의 고정 모델 생성) 전부 고정.
- **트리거**: 없음. "Adaptive pruning"은 training-time에 dependency graph와 weight importance를 기반으로 parameter group을 제거하는 offline 절차다. Runtime에 machine condition이나 system slack에 반응하지 않는다.

---

## 초록 번역

본 논문은 클라우드 전송 지연과 edge device의 제한된 계산·저장 자원을 해결하기 위해 APTL-net을 제안한다. APTL-net은 경량 sequence model, FDD 기반 weight-sharing multiscale feature extraction, dependency-aware pruning을 결합하며, Jetson Xavier NX에서 99.54% accuracy를 유지하면서 parameter, FLOPs, inference latency를 각각 47.82%, 49.98%, 20.59% 줄였다고 보고한다.

---

## 논문 흐름 + Novelty

### 논리 흐름

1. 기존 bearing FD는 cloud server에 의존해 raw vibration transmission latency와 보안 문제가 생기고, 기존 lightweight model은 representation capacity가 감소하며, 기존 pruning은 layer 간 dependency를 충분히 고려하지 못한다고 문제를 제기한다.
2. Triple-lightweight 세 요소를 순서대로 적용한다 (아래 표 참고).
3. CWRU cross-domain task와 Jetson Xavier NX 실물 테스트 벤치에서 accuracy, FLOPs, parameter, latency, power, energy를 비교한다.

### Triple-Lightweight 세 요소

| 단계 | 제안 요소 | 경량화 원리 |
|---|---|---|
| Model construction | Parallel training + recursive inference (retentive network 계열) | Training에서는 병렬 계산, inference에서는 recurrent state update로 constant memory·linear complexity 지향 |
| Feature extraction | FDD 기반 weight-sharing multiscale convolution | FFT로 dominant period 추출 후 동일 convolution kernel을 여러 scale에 공유해 multiscale representation의 parameter·연산 증가 억제 |
| Structural pruning | Dependency-aware adaptive pruning (offline) | Layer 간 dependency graph를 보존하며 importance가 낮은 parameter group을 일관되게 제거 후 fine-tuning |

### Adaptive Pruning — offline training-time pruning으로 확정

"Adaptive"는 runtime adaptation이 아니라 **training 과정에서 model dependency와 importance distribution에 맞추어 pruning group을 자동 결정한다**는 뜻이다.

절차 (근거: Section III-C–D, Algorithm 1):

1. Group sparse regularization으로 중요도가 낮은 parameter group에 강한 penalty를 부여하면서 pretrain
2. Dependency graph를 구성해 interlayer·intralayer 연결을 추적
3. 연결된 convolution, normalization, skip path parameter를 group으로 묶음
4. 그룹 importance $I(g)=\sum_{w\in g}\|w\|_2$가 낮은 순으로 target pruning rate $P$에 맞추어 제거
5. Fine-tuning으로 성능 회복

배포 후에는 pruning이 완료된 고정 APTL-net을 Jetson Xavier NX에서 실행한다.

---

## RT 등급: B (확정)

| 판정 항목 | 결과 | 원문 근거 |
|---|---|---|
| 명시적 deadline | X | 없음 |
| RTOS 또는 RT-Linux | X | Ubuntu 20.04 범용 OS |
| Deadline miss / p99 / max | X | 미보고 |
| Average latency | O | 14.782 ms (50% pruned forward pass, Table V) |
| Standard deviation | O | 9.227 ms (TensorRT edge deployment, Table VIII) — 매우 큰 jitter |
| W/H/M runtime 변경 | X | 전부 고정 |

SD 9.227 ms는 average 16.588 ms의 56%에 달한다. p99 latency가 보고되지 않지만 분산이 크다는 점은 scheduling 측면에서 중요한 약점이다.

---

## 핵심 수치

### 플랫폼

| 항목 | 내용 |
|---|---|
| Device | NVIDIA Jetson Xavier NX |
| OS | Ubuntu 20.04 |
| SDK | JetPack 5.1.2 |
| Inference runtime | TensorRT 8.5.1.7 |
| Framework | PyTorch, CUDA, cuDNN |
| Measurement | Edge deployment configuration별 50 independent runs |

### Latency (Table V vs Table VIII 구분 필수)

| 조건 | Inference time |
|---|---:|
| Table V — Baseline forward pass | 18.615 ms |
| Table V — 50% pruned forward pass | 14.782 ms |
| 50% pruned + preprocessing (1.42 ms) | 본문 기준 16.36 ms |
| Table VIII — Original edge deployment | 324.052 ms |
| Table VIII — 50% pruned edge deployment | 234.958 ms |
| Table VIII — TensorRT optimized edge deployment | 16.588 ms (SD 9.227 ms) |

Table V는 neural-network forward pass만 측정한다. Table VIII는 edge deployment configuration 전체를 비교하지만 각 경로의 batch size와 pipeline boundary가 충분히 설명되지 않는다. 14.782 ms와 16.588 ms를 동일 조건으로 직접 비교하면 안 된다.

### 모델 수치 (50% pruning 기준)

| 지표 | 값 |
|---|---|
| Accuracy | 99.54% (CWRU cross-domain 평균) |
| Parameters | 0.96 M (baseline 1.84 M) |
| FLOPs | 10.81 G (baseline 21.61 G) |
| Memory | 365 MiB (TensorRT deployment) |
| Power | 평균 5.21 W |
| Energy | 86.4 mJ/inference |

---

## 개인연구와의 연결

| 관점 | Zhan et al. | 개인연구 |
|---|---|---|
| W | 고정 (sample 수 미보고) | Runtime mode 변수 |
| H | 미정의 | Runtime diagnosis period |
| M | Offline pruning → 고정 단일 모델 | 여러 mode 중 runtime 선택 |
| "Adaptive" 대상 | Training-time topology와 pruning group | Runtime a=(W,H,M) |
| Trigger | Weight importance + dependency graph (offline) | Machine condition q + system slack S |
| Timing 평가 | Average latency + SD (p99/max/miss 없음) | p99, max, deadline miss, schedulability |
| Platform | Jetson Xavier NX (GPU SoC) | Pi Zero 2W + PREEMPT_RT |

SD 9.227 ms는 Pi Zero 2W + PREEMPT_RT 환경에서의 jitter 제어 필요성을 간접적으로 보여주는 참고 자료로 활용할 수 있다.

---

## 세 문장 압축

Zhan et al.은 recursive inference, FDD 기반 weight-sharing multiscale feature extraction, dependency-aware structured pruning을 결합한 APTL-net을 제안한다. Adaptive pruning은 runtime adaptation이 아니라 sparse training 이후 importance가 낮은 dependent parameter group을 제거하고 fine-tuning하는 offline training-time pruning이다. Jetson Xavier NX에서 50% pruning model은 99.54% accuracy와 14.782 ms forward-pass latency를 보였지만, W sample 수와 explicit deadline, p99 latency는 보고하지 않으며 SD 9.227 ms로 jitter가 크다.

## Related Work 영어 한 줄

> Zhan et al. combined recursive inference, weight-shared multiscale feature extraction, and dependency-aware training-time pruning for efficient bearing diagnosis on a Jetson Xavier NX, but their deployed topology remained fixed and did not adapt W/H/M according to machine condition or system slack.

---

## 불확실한 점

1. Input window W의 구체적인 sample 수가 원문에 명시되지 않는다.
2. Sliding-window stride, overlap, diagnosis period H가 미보고다.
3. Table V와 Table VIII의 정확한 execution-path 차이 (batch size, pipeline boundary)가 불명확하다.
4. Maximum, p95, p99 latency와 deadline-miss ratio가 없다.
5. Preprocessing, data transfer, feature extraction, TensorRT inference 각각의 세부 latency가 분리되지 않는다.
6. Jetson power mode, clock setting, CPU/GPU affinity가 미기재다.
7. Online physical validation에서의 exact sample rate와 input cadence가 불명확하다.
