# 연구 질문 중심 문헌 분류 체계

- 작성일: 2026-07-23
- 기준: `PROJECT_CONTEXT.md`, `decisions/personal_research_summary_0708.md`
- 목적: 현재 8개 보관 폴더, 0708 서베이 산출물과 원고 related-work 섹션을 하나의 연구 논리로 연결한다.

## 1. 분류 원칙

논문은 MCU 또는 SoC라는 플랫폼만으로 최상위 분류하지 않는다. 본 연구의 핵심 질문은 진동 결함 진단의 품질 변수와 real-time schedulability를 어떻게 연결하는가이기 때문이다.

각 논문에는 다음 세 종류의 정보를 따로 붙인다.

1. **주 섹션**: 논문이 본 연구의 어떤 질문에 답하는가
2. **연구 축 태그**: 가변 변수, trigger, guarantee
3. **플랫폼·실행환경 태그**: MCU/SBC/heterogeneous SoC와 bare metal/RTOS/Linux/PREEMPT_RT를 독립적으로 기록

논문 하나가 여러 섹션과 연결될 수 있지만, 보관 폴더는 가장 강한 기여 하나를 기준으로 유지한다.

## 2. 서베이의 여섯 섹션

### S1. Embedded Real-Time Fault Diagnosis

**질문**: Fault-diagnosis 연구가 “real-time”을 어떻게 정의하고 달성하는가?

- Model compression, quantization, pruning, TinyML
- Embedded deployment와 end-to-end pipeline
- Average latency와 deadline/tail/miss의 구분
- RTOS 사용 여부와 system-level scheduling 유무

이 섹션에는 MCU와 SoC/SBC를 모두 포함한다. 플랫폼별 논문 수를 따로 보고하되, 핵심 분류는 `model-level best-effort`, `empirical deadline-aware`, `schedulability-backed`다.

현재 보관 그룹:

- `05_fault_diagnosis_app`
- `06_platform_preempt_rt`, `07_platform_pi_zero2w`의 fault-diagnosis 직접 사례 일부

0708 산출물 연결: **산출물 1, Real-Time Fault Diagnosis 분류표**

### S2. Adaptive Diagnostic Fidelity

**질문**: 진단 품질을 위해 입력과 모델을 무엇에 따라 바꾸는가?

- Window/input length `W`
- Model 또는 exit `M`
- Sampling frequency와 signal semantics
- Machine condition, anomaly score와 confidence `q`
- Offline design과 runtime adaptation 구분

현재 보관 그룹:

- `02_input_adaptive`
- `05_fault_diagnosis_app`의 adaptive input/model 논문

본 연구 연결: `q -> diagnostic utility(W,M)`를 정의하는 근거

### S3. Elastic Rate and Workload Scheduling

**질문**: System load와 resource constraint 아래에서 period와 computation을 어떻게 탄력적으로 조절하는가?

- Period/rate `T`, diagnosis hop/period `H`
- Execution demand와 workload `C`
- Discrete utilization mode
- System load와 slack `S`
- Offline feasibility와 online adaptation

현재 보관 그룹:

- `01_elastic_scheduling`

0708 산출물 연결: **산출물 2, Elastic Scheduling 실전 응용과 가정**

본 연구 연결: `C(W,M)`과 `T=H/f_s`가 함께 변하는 task model

### S4. Deadline-Aware AI Inference and Mode Selection

**질문**: Deadline 또는 slack을 이용해 inference quality와 configuration을 어떻게 선택하는가?

- Input resolution, model, exit, batch, mapping
- Deadline, queue, resource contention와 slack
- Mandatory/optional execution
- Admission, fallback와 runtime mode selection

현재 보관 그룹:

- `03_rt_dnn_serving`
- `02_input_adaptive`의 deadline-aware perception 일부

본 연구 연결: `S -> feasible modes`와 그 안에서의 quality selection

### S5. Schedulability, Mode Transition, and Miss Semantics

**질문**: Mode를 바꾸거나 overload가 발생할 때 어떤 deadline 보장을 제공하는가?

- Schedulability analysis와 admission control
- Mode-change protocol과 carry-over job
- Weakly-hard deadline과 bounded miss
- Deadline-miss handling, fallback, drop/skip/queue
- Cyclic executive와 imprecise computation

현재 보관 그룹:

- `04_idk_weakly_hard`
- `08_misc_realtime_scheduling`
- `01_elastic_scheduling`의 transition/guarantee 논문 일부

0708 산출물 연결: **산출물 4, 고전 실시간 개념 노트**

본 연구 연결: Static mode feasibility와 transition feasibility를 구분하는 근거

### S6. Runtime Platform and Interference Characterization

**질문**: 제안한 방법을 실제 실행 환경에서 어떻게 검증하고 timing variation의 원인을 설명하는가?

- MCU + Zephyr/FreeRTOS/ThreadX
- Application-class SoC/SBC + Linux/PREEMPT_RT
- CPU/GPU heterogeneous SoC
- Scheduler policy, affinity, priority와 framework runtime
- CPU, memory, I/O, network interference
- Jitter, p95/p99/max, miss, temperature와 resource usage

현재 보관 그룹:

- `06_platform_preempt_rt`
- `07_platform_pi_zero2w`
- `08_misc_realtime_scheduling`의 pipeline/OS timing 논문 일부

0708 산출물 연결: **산출물 3, 부하 설계 전략**

이 섹션은 방법의 novelty보다 evaluation validity와 원인 분석을 담당한다. MCU와 SoC 중 하나를 배제하지 않고, 각 플랫폼에서 얻을 수 있는 근거를 구분한다.

## 3. 플랫폼은 태그로 관리

| 플랫폼 태그 | 의미 | 본 연구에서의 역할 |
| --- | --- | --- |
| `PL-MCU` | STM32/ESP32/Cortex-M | KCC 계보, low-level resource constraint |
| `PL-SBC-SOC` | Raspberry Pi/ARM Cortex-A SBC | 현재 Pi Zero 2W 평가 환경 |
| `PL-HET-SOC` | Jetson 등 CPU/GPU heterogeneous SoC | DNN runtime과 resource interference 비교 |
| `PL-SERVER-GPU` | Edge server/cloud GPU | Scheduling mechanism bridge |
| `PL-DESKTOP` | Desktop/laptop evaluation | Algorithm timing 참고, embedded 직접 비교 제한 |

| 실행환경 태그 | 의미 |
| --- | --- |
| `ENV-BAREMETAL` | OS 없이 직접 실행 |
| `ENV-RTOS` | Zephyr, FreeRTOS, ThreadX, QNX, VxWorks 등 |
| `ENV-LINUX` | 일반 Linux kernel |
| `ENV-PREEMPT_RT` | PREEMPT_RT가 적용된 Linux |
| `ENV-OTHER` | macOS, Windows, custom runtime 또는 확인 필요 |

플랫폼과 실행환경 태그는 검색 coverage와 external validity를 판단하는 데 사용한다. 예를 들어 같은 Raspberry Pi라도 일반 Linux와 PREEMPT_RT는 다른 실행환경이다. 문헌의 이론적 관련성 우선순위는 플랫폼 일치 여부만으로 결정하지 않는다.

## 4. 기존 보관 폴더 매핑

기존 PDF와 paper-card 폴더는 이동하지 않는다. 현재 구조는 파일 소유와 중복 방지에 유용하며, 아래처럼 연구 섹션 태그를 추가해 사용한다.

| 기존 그룹 | 주 섹션 | 보조 섹션 |
| --- | --- | --- |
| `01_elastic_scheduling` | S3 | S5 |
| `02_input_adaptive` | S2 | S4 |
| `03_rt_dnn_serving` | S4 | S5, S6 |
| `04_idk_weakly_hard` | S5 | S4 |
| `05_fault_diagnosis_app` | S1 | S2, S6 |
| `06_platform_preempt_rt` | S6 | S1 |
| `07_platform_pi_zero2w` | S6 | S1 |
| `08_misc_realtime_scheduling` | S5 또는 S6 | S3 |

## 5. 원고용 Related Work 구조

여섯 서베이 섹션을 원고에서 그대로 여섯 절로 만들 필요는 없다. 학위논문 또는 RTAS/RTCSA 원고에서는 다음 네 절로 압축하는 것이 자연스럽다.

### RW1. Real-Time and Embedded Fault Diagnosis

- S1의 model-level best-effort와 deadline-aware 구분
- S6의 MCU/RTOS 및 SoC/Linux 구현 근거 중 fault diagnosis 직접 사례
- 결론: Embedded deployment는 많지만 scheduling guarantee의 수준은 별도 판정이 필요

### RW2. Adaptive Input and Diagnostic Fidelity

- S2의 window/input/model adaptation
- Machine condition과 diagnostic utility
- 결론: `W/M`은 품질 변수지만 대부분 offline이거나 system feasibility와 분리

### RW3. Elastic Scheduling and Mode-Change Guarantees

- S3의 period/workload elasticity
- S5의 admission, transition과 weakly-hard semantics
- 결론: `H/C` 조절과 guarantee 기반은 풍부하지만 vibration diagnosis utility와의 결합은 확인 필요

### RW4. Deadline-Aware AI Inference

- S4의 slack/deadline 기반 model/input/exit 선택
- GPU/vision 중심 scheduling bridge
- 결론: `S -> quality mode`는 이미 존재하며, 본 연구는 vibration temporal semantics와 diagnosis utility, mode feasibility를 검증해야 함

Platform characterization 자체는 long-term manuscript의 독립 related-work 절보다 evaluation methodology에 가깝다. KSC/PREEMPT_RT 트랙에서는 S6가 핵심 related-work 절이 된다.

## 6. 후보 우선순위 기준

플랫폼이 아니라 다음 점수로 원문 확보 순서를 정한다.

| 축 | 0점 | 1점 | 2점 |
| --- | --- | --- | --- |
| Domain | FD 아님 | 인접 condition monitoring | Vibration/machine FD |
| Variable | 고정 | `W/H/M` 중 하나 | 둘 이상 또는 `C/T` 결합 |
| Trigger | 없음/offline | `q` 또는 `S/load` | `q`와 system condition 결합 |
| Guarantee | latency만 | deadline/tail 측정 | schedulability/admission/transition 분석 |
| Evidence | abstract만 | full text 확보 | full text + 재현 가능한 task/platform 조건 |

Platform tag는 동점일 때 현재 evaluation 환경과의 직접성을 판단하는 보조 기준이다.

## 7. 현재 연구 위치

현재 조사 범위에서 연구의 연결 구조는 다음과 같다.

```text
S2: q와 diagnostic utility가 W/M의 선호도를 결정
                    +
S3/S4: S와 deadline이 feasible W/H/M을 제한
                    +
S5: static mode와 transition의 timing condition을 보장
                    +
S6: MCU/RTOS 선행 결과와 SoC/Linux 실험에서 검증
```

이 구조가 최종 novelty를 보장하지는 않는다. 각 연결이 기존 문헌에 있는지와 실제 실험에서 utility 및 deadline 개선이 나타나는지를 계속 검증해야 한다.
