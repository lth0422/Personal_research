# 실험 설계서 — KSC 2026

> **단일 기준점 문서.** 이 파일을 먼저 읽고 작업한다.
> PROJECT_CONTEXT.md 7절(단기 KSC 2026)과 정합성을 유지한다.
> 수정 시 반드시 git commit + 날짜 기록.

---

## 1. 연구 질문

Pi Zero 2W(Cortex-A53) 위에서 실시간 진동 결함 진단 파이프라인을 구동할 때,
일반 Linux 커널과 PREEMPT_RT 커널의 timing behavior 차이가 실질적으로 의미 있는 수준인가?

하위 질문:
- 부하가 증가할수록 두 커널의 jitter 격차가 어떻게 변하는가?
- deadline miss rate는 어느 부하 조건에서 처음 발생하는가?
- PREEMPT_RT 적용이 inference latency 분포(tail)에 미치는 영향은 무엇인가?

---

## 2. 플랫폼

| 항목 | 내용 |
| --- | --- |
| 보드 | Raspberry Pi Zero 2W |
| SoC | BCM2710A1, Cortex-A53 quad-core 1GHz |
| RAM | 512MB LPDDR2 |
| 저장 | microSD (class 10 이상 권장) |
| OS A | Raspberry Pi OS Lite (64-bit, 커널 버전 기록 필요) |
| OS B | 동일 베이스 + PREEMPT_RT 패치 (패치 버전 기록 필요) |
| 추론 런타임 | TFLite (XNNPACK 백엔드) — CMSIS-NN은 Cortex-M 전용이므로 사용 불가 |
| 모델 | FRFconv-TDSNet, INT8 양자화 (KCC 2026 동일 모델) |
| 데이터 | UOS dataset (이성재 et al., Data in Brief 2024), 1400 RPM, 8-class, 8kHz |

> PREEMPT_RT 패치 실효성은 cyclictest 분포 비교로 먼저 검증한다.
> 분포가 vanilla와 차이 없으면 패치 적용 여부를 재확인해야 한다.

---

## 3. 실험 조건 (2 × 5 factorial)

| 요인 | 수준 |
| --- | --- |
| 커널 | vanilla Linux, PREEMPT_RT |
| 부하 | idle, CPU stress, memory stress, I/O stress, combined |

combined = CPU + memory + I/O 동시 인가.

stress-ng 명령 기준:

```bash
# CPU stress (N은 코어 수, Pi Zero 2W = 4)
stress-ng --cpu 4 --timeout 60s

# Memory stress
stress-ng --vm 2 --vm-bytes 80% --timeout 60s

# I/O stress
stress-ng --io 2 --hdd 1 --timeout 60s

# Combined
stress-ng --cpu 2 --vm 1 --vm-bytes 50% --io 1 --hdd 1 --timeout 60s
```

> 부하 파라미터는 예비 실험 후 조정 가능. 변경 시 이 파일에 반영.

---

## 4. 파이프라인 구조

KCC 2026의 3-task 구조를 Pi 환경에 이식한다.

```
[Sensor (시뮬레이션)] --msgq--> [Inference] --msgq--> [Logger]
```

- **Sensor task**: UOS dataset의 raw 진동 데이터를 파일에서 읽어 8kHz 주기로 메시지 큐 전달.
  실제 ADC 없음 → 타이머 기반 파일 스트리밍으로 시뮬레이션.
  주기: 1/8000 s × W (window 단위로 묶어 전달).
- **Inference task**: 수신한 window를 TFLite로 추론. window size W=512 고정(KCC 기준).
  시작 타임스탬프 t_start, 종료 t_end 기록.
- **Logger task**: 결과 + latency 측정값 CSV 기록. 성능 부하 최소화 목적으로 별도 스레드.

스레드 우선순위 (PREEMPT_RT 환경):
- Sensor: SCHED_FIFO, priority 90
- Inference: SCHED_FIFO, priority 80
- Logger: SCHED_OTHER 또는 낮은 priority

vanilla 환경:
- 동일 코드, priority 설정 유지 (실제 RT 보장은 안 되나 비교를 위해 동일 구조 유지)

---

## 5. 측정 지표

### 5-1. cyclictest (커널 latency 기초 검증)

```bash
sudo cyclictest --mlockall --smp --priority=80 --interval=1000 --distance=0 --duration=60s --histfile=hist_vanilla.txt
sudo cyclictest --mlockall --smp --priority=80 --interval=1000 --distance=0 --duration=60s --histfile=hist_rt.txt
```

| 지표 | 의미 |
| --- | --- |
| min latency | 커널 최소 응답 시간 |
| avg latency | 평균 응답 시간 |
| max latency | 최악 응답 시간 (jitter 상한 추정) |
| p99, p999 | 분포 꼬리 |

### 5-2. 파이프라인 latency (메인 측정)

각 inference 호출마다 기록:

| 지표 | 계산 방법 |
| --- | --- |
| activation jitter | 연속 두 Inference task 시작 간격의 편차 (σ, peak-to-peak) |
| inference latency | t_end - t_start (단일 추론) |
| end-to-end latency | Sensor 데이터 생성 시각 → Logger 기록 완료 시각 |
| deadline miss | end-to-end latency > D (deadline). D는 KCC 기준 64ms 또는 별도 설정 |
| p95, p99 | 분포 백분위 |
| σ | 표준편차 |

### 5-3. 시스템 자원

| 지표 | 수집 방법 |
| --- | --- |
| CPU utilization | `top -b -d 1` 또는 `/proc/stat` 파싱 |
| CPU temperature | `/sys/class/thermal/thermal_zone0/temp` |
| Memory usage | `/proc/meminfo` |
| throughput | 단위 시간당 완료된 inference 횟수 |

---

## 6. 수집 계획

### 실험 1회 단위

1. 부팅 후 5분 안정화.
2. cyclictest 60초 (부하 없음 상태).
3. 파이프라인 실행 + stress-ng 부하 인가 → 5분 측정.
4. 결과 CSV/log 저장.
5. 재부팅 후 다음 조건.

### 반복 횟수

각 (커널, 부하) 조합당 최소 3회 반복. 결과 이상치 확인 후 필요 시 5회로 늘림.

총 run 수: 2 커널 × 5 부하 × 3 반복 = 30 run.

### 파일 저장 규칙

```
results/
├── cyclictest/
│   ├── vanilla_idle_r1.txt
│   ├── vanilla_idle_r2.txt
│   ├── rt_idle_r1.txt
│   └── ...
└── pipeline/
    ├── vanilla_idle_r1.csv
    ├── vanilla_cpu_r1.csv
    ├── rt_combined_r3.csv
    └── ...
```

CSV 컬럼 (파이프라인 결과):

```
run_id, kernel, load, repeat, window_idx, t_sensor, t_infer_start, t_infer_end, t_log, result_class, deadline_miss
```

---

## 7. 분석 방법

1. **분포 비교**: vanilla vs PREEMPT_RT, 각 부하 조건별 jitter/latency 박스플롯 + CDF.
2. **통계 검정**: Wilcoxon rank-sum test (정규성 미보장 가정). p < 0.05 기준.
3. **deadline miss rate**: (miss 횟수 / 전체 inference 횟수) × 100%.
4. **tail latency 비교**: p95, p99, max 값을 커널 × 부하 조건 표로 정리 → manuscript Table 2 후보.
5. **온도·utilization 추이**: 부하 조건별 시계열 그래프.

---

## 8. 예상 결과 및 기여

- PREEMPT_RT는 idle/저부하에서 vanilla와 비슷하지만 고부하(combined)에서 jitter 상한이 유의미하게 낮을 것으로 예상.
- deadline miss는 vanilla에서 combined 부하 시 먼저 발생할 것으로 예상.
- 기여: MCU(STM32, KCC)에서 SBC(Pi Zero 2W)로 올라왔을 때 PREEMPT_RT가 실질적으로 필요한 조건을 정량 제시.
- KSC 2026 Figure 구성안: (a) cyclictest CDF, (b) inference latency 박스플롯 × 부하, (c) deadline miss rate 표.

---

## 9. 주의·제약

- CMSIS-NN 사용 불가 (Cortex-M 전용). XNNPACK이 기본 백엔드.
  → KCC 대비 속도 다름. speedup 수치 직접 비교 금지.
- Pi Zero 2W는 발열로 throttling 가능. 온도 로그 필수. throttle 발생 시 해당 run 제외 또는 별도 표기.
- 실제 센서 없음 → 파일 스트리밍 시뮬레이션. 이 한계를 manuscript에 명시.
- stress-ng 버전·옵션은 재현 가능하도록 `pi_setup/env.md`에 기록.

---

## 10. 디렉토리 역할 분담

| 폴더 | 내용 |
| --- | --- |
| `pi_setup/` | OS 이미지, 패키지 버전, TFLite 빌드 방법, 환경 변수 |
| `preempt_rt/` | 패치 버전, 빌드 절차, cyclictest 검증 결과 |
| `pipeline/` | 파이프라인 C/Python 소스, Makefile, 실행 스크립트 |
| `results/` | 측정 결과 원본 (CSV, txt). 분석 스크립트는 여기에 두거나 별도 `analysis/` |

---

## 11. 현재 상태 (2026-07-09 기준)

### 완료

- [x] Pi Zero 2W 입수
- [x] PREEMPT_RT 패치 적용 (APT 방식: linux-image-rpi-v8-rt)
- [x] PREEMPT_RT 실효성 검증 — cyclictest R1 완료
  - 결과: `experiments/results/cyclictest/summary.md`
  - 핵심: I/O 부하 시 vanilla 2034 μs vs RT 78 μs (26x 차이)
- [x] FRFconv-TDSNet INT8 모델 변환
  - .cc C배열 → .tflite 바이너리 6종 (SHAFT/BEARING × 512/1024/2048)
  - 위치: `experiments/model/*.tflite`
- [x] 파이프라인 코드 작성
  - `experiments/pipeline/`: config.py, inference.py, logger.py, main.py, inspect_model.py
- [x] Pi에 GitHub 클론 + venv 세팅 + ai-edge-litert 설치
- [x] 더미 데이터 inference latency R1 (vanilla + RT, 5조건 × 100회)
  - 결과: `experiments/results/pipeline/inference_latency.csv`
- [x] **실제 데이터(UOS SHAFT 8k W=512) RT R1 측정 완료**
  - 결과: `experiments/results/pipeline/rt_real_r1.csv`
  - deadline miss: 전 조건 0 (기준 64ms)
  - 주의: 데이터셋이 클래스순 정렬 → 셔플 추가 (main.py 수정)

### 진행 중 — **현재 단계**

- [ ] vanilla 실제 데이터 R1 측정 (`vanilla_real_r1.csv`)

### 미완료

- [ ] vanilla/RT real R2, R3 반복 (통계 신뢰도)
- [ ] cyclictest R2, R3 반복
- [ ] 정확도 검증 (셔플 후 재측정 필요)
- [ ] 분석 스크립트 작성 (`experiments/results/analysis/`)
- [ ] manuscript Figure/Table 생성

---

### RT real R1 결과 (UOS SHAFT 8k W=512, n=100, cpu는 2번째 run 기준)

| 부하 | Avg | Std | P2P | P99 | Max | D-miss |
|---|---|---|---|---|---|---|
| idle | 1.96 | 0.047 | 0.30 | 2.06 | 2.16 | 0 |
| cpu | 3.87 | 0.245 | 1.40 | 4.45 | 4.46 | 0 |
| io | 5.20 | 0.735 | 3.11 | 7.41 | 7.52 | 0 |
| **combined** | **6.75** | **4.496** | **19.99** | **22.08** | **22.48** | **0** |
| **memory** | **7.31** | **3.236** | **12.52** | **15.42** | **15.72** | **0** |

**더미 R1 대비 변화:**
- idle: 거의 동일 (1.95→1.96ms)
- io: 크게 증가 (3.55→5.20ms) — 실제 데이터 메모리 접근 패턴 영향
- combined Max: 7.96→22.48ms — 실제 데이터 + 복합 부하 시 tail 급증
- 정확도: cpu 중복 측정 및 클래스 셔플 미적용으로 신뢰도 낮음 → 재측정 필요

---

### R1 결과 요약 (inference latency, ms)

**vanilla:**

| 부하 | Min | Avg | P95 | P99 | Max |
|---|---|---|---|---|---|
| idle | 1.52 | 1.56 | 1.61 | 1.63 | 1.75 |
| cpu | 1.68 | 2.66 | 3.28 | 3.42 | 3.47 |
| io | 1.87 | 2.72 | 3.54 | 4.02 | 4.12 |
| combined | 1.95 | 2.81 | 3.51 | 4.61 | 6.63 |
| **memory** | **3.35** | **6.43** | **14.60** | **18.11** | **18.28** |

**PREEMPT_RT:**

| 부하 | Min | Avg | P95 | P99 | Max |
|---|---|---|---|---|---|
| idle | 1.71 | 1.95 | 2.08 | 2.14 | 2.16 |
| cpu | 2.50 | 3.18 | 3.60 | 4.03 | 4.51 |
| io | 2.21 | 3.55 | 4.16 | 4.37 | 4.58 |
| combined | 2.85 | 4.54 | 6.46 | 7.88 | 7.96 |
| **memory** | **2.83** | **4.18** | **7.47** | **7.82** | **8.08** |

**실시간성 핵심 지표 비교 (R1, n=100):**

| 부하 | V_Avg | RT_Avg | V_Std | RT_Std | Std비(RT/V) | V_Max | RT_Max | Max비(RT/V) |
|---|---|---|---|---|---|---|---|---|
| idle | 1.56 | 1.95 | 0.035 | 0.084 | 2.44x↑ | 1.75 | 2.16 | 1.23x↑ |
| cpu | 2.66 | 3.18 | 0.549 | 0.286 | **0.52x↓** | 3.47 | 4.51 | 1.30x↑ |
| io | 2.72 | 3.55 | 0.584 | 0.381 | **0.65x↓** | 4.12 | 4.58 | 1.11x↑ |
| combined | 2.81 | 4.54 | 0.648 | 0.965 | 1.49x↑ | 6.63 | 7.96 | 1.20x↑ |
| **memory** | **6.43** | **4.18** | **4.353** | **1.361** | **0.31x↓** | **18.28** | **8.08** | **0.44x↓** |

↓ = RT가 감소(개선), ↑ = RT가 증가(악화). deadline miss: 전 조건 0 (기준 64ms).

**관찰:**
- **memory**: jitter(Std) 68% 감소, Max 56% 감소 — RT가 압도적으로 유리. 메모리 압박 시 RT 커널의 결정적 페이지 폴트 처리가 캐시 오염 영향을 억제
- **cpu/io**: jitter(Std)는 RT가 줄여주지만 Max는 오히려 vanilla보다 높은 역전 현상 — RT 오버헤드가 드물게 큰 latency spike를 만듦
- **idle**: RT 오버헤드가 jitter를 2.44배 키움 — 저부하 환경에서는 RT가 불리
- **combined**: R1 100샘플로는 통계 불안정, R2/R3 반복 필요
- cyclictest I/O 26x 차이가 inference latency에 재현되지 않는 이유: 추론 자체가 I/O 미수행 → I/O non-preemptible 경로가 직접 영향을 주지 않음
- **평균보다 Std·P2P·Max가 실시간성의 핵심 지표** — 평균만 보면 RT 효과를 오해할 수 있음

---

## 12. 이 실험의 목적과 연구 맥락

### 이 실험이 검증하는 것

Pi Zero 2W에서 FRFconv-TDSNet INT8 추론을 실행할 때, **OS 커널 종류(vanilla vs PREEMPT_RT)가 추론 레이턴시 분포에 미치는 영향**을 정량화한다.

측정 대상:
- 단일 추론 레이턴시 (invoke() 시간)
- 레이턴시 분포의 tail (P95, P99, Max)
- 부하 조건(idle / CPU / memory / I/O / combined)별 변화

### 전체 연구 내 위치

```
[KCC 2026 - 완료]
  STM32F407 + Zephyr, W=512, 40.3ms, deadline 64ms, 정확도 99.30%
  → MCU에서의 가능성 검증

[KSC 2026 - 현재 진행 중]  ← 지금 여기
  Pi Zero 2W + Linux/PREEMPT_RT
  - OS 스케줄링 jitter가 실시간 추론에 미치는 영향 정량화
  - "MCU(Zephyr)에서 SBC(Linux)로 올라왔을 때 무엇이 달라지는가"

[학위논문 - 중장기]
  W/H/M elastic scheduling 정식화
  - 가변 입력크기 + 기계 상태 기반 adaptive mode selection
  - RTAS 2027 / RTCSA 2027 목표
```

### KSC 논문에서 이 실험이 하는 역할

cyclictest(OS latency)와 파이프라인 inference latency를 함께 제시하여:
1. OS 레벨 jitter(cyclictest) → 실제 추론 tail latency에 어떻게 이어지는지
2. PREEMPT_RT가 필요한 부하 조건이 어디인지 (idle에서는 차이 없을 수 있음)
3. Pi Zero 2W에서 deadline 64ms 유지 가능 여부

### 센서 없이 실험하는 이유

Pi Zero 2W는 ADC가 없어 아날로그 진동 센서를 직접 연결할 수 없다.
현재는 UOS dataset의 사전 수집 데이터를 numpy 배열로 로드하여 inference latency만 측정한다.
실제 센서 연결은 추후 디지털 가속도계(MPU-6050 등) 도입 시 확장 예정이며, 이 한계는 논문에 명시한다.
