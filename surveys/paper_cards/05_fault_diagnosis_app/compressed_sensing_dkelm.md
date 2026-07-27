# Fast Fault Diagnosis in Industrial Embedded Systems Based on Compressed Sensing and Deep Kernel Extreme Learning Machines

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S3 (경량화 대조군), S4 (input fidelity–cost trade-off 참고)
- **플랫폼 태그**: `PL-HET-SOC`
- **실행환경 태그**: `ENV-LINUX` (Linux, Python 3.8, PyTorch 1.7.0; CUDA 10.2/cuDNN 7.0 명시되나 Zynq에 NVIDIA CUDA 없어 실행 환경 내부 불명확성 있음)
- **출처/연도**: Sensors, Vol. 22, 2022, Art. 3997, DOI 10.3390/s22113997
- **저자**: Nanliang Shan, Xinghua Xu, Xianqiang Bao, Shaohua Qiu
- **분석 MD**: `papers/05_fault_diagnosis_app/reviews/Shan_2022_CS_DKELM_분석.md`

---

## 두 질문

- **가변 변수**: 없음. W=4800 고정, compression ratio=80% 고정, M(CS-DKELM) 고정. Offline ablation에서 CR을 50–95%로 sweep하지만 배포 후 runtime 변경 없음.
- **트리거**: 없음. Accuracy–time trade-off를 offline 분석해 CR=80%를 선택하고 배포한다. Machine condition이나 system slack에 반응하지 않는다.

---

## 초록 번역

본 논문은 자원이 제한된 산업용 임베디드 시스템에서 고주파 monitoring data를 빠르게 진단하기 위해 compressed sensing과 deep kernel extreme learning machine을 결합한 CS-DKELM을 제안한다. 원 신호를 저차원 compressed representation으로 줄인 뒤 복원하지 않고 DKELM에 직접 입력하여, transmission·storage·computation 부담을 줄이면서 높은 진단 정확도를 유지하는 것이 핵심이다.

---

## 논문 흐름 + Novelty

### 논리 흐름

1. 고주파 센서에서 많은 데이터가 생성되어 transmission·storage·computation 부담이 크고, 기존 경량화는 model compression만 다루어 sampling 단계의 data volume은 그대로라는 문제를 제기한다.
2. Compressed sensing으로 N=4800 samples를 M=960 차원으로 projection한다 (CR=80%). Fourier transform 후 Gaussian random measurement matrix를 사용한다.
3. Compressed representation을 원 신호로 복원하지 않고 DKELM이 직접 분류한다.
4. DKELM은 stacked ELM-AutoEncoder에 RBF kernel을 추가해 sparse compressed signal의 nonlinear separability를 보완하고, PSO로 hyperparameter를 offline 최적화한다.
5. CWRU dataset과 physical rotating test-bench에서 accuracy, diagnosis time, compression ratio sweep을 평가한다.

### Novelty

| # | 내용 | 근거 |
|---|---|---|
| 1 | Sampling부터 classification까지 통합 경량화 pipeline | Section 1, p.3 |
| 2 | Reconstruction 없는 compressed-domain 직접 분류 | Section 2.2, pp.5–6 |
| 3 | Sparse signal용 DKELM — ELM-AE + RBF kernel | Section 2.3–2.4, pp.6–8 |
| 4 | Compression ratio별 accuracy–time trade-off 실험 분석 | Section 3.4, Figure 10 |
| 5 | Sliding window incremental computation (이전 window 중복 계산 재사용) | Section 3.6 |

---

## RT 등급: B (확정)

| 판정 항목 | 결과 | 원문 근거 |
|---|---|---|
| Deadline 명시 | △ | "100 ms requirement" 언급 (Section 3.3) — 단, "industry standard" 한 줄에 근거 없음 |
| Deadline 만족 검증 | X | 60.7 ms는 100 ms 미만이나 per-window latency인지 batch total인지 불명확; physical platform 170 ms는 초과 |
| p99 / max / miss | X | 미보고 |
| RTOS | X | Linux 범용 OS |
| Schedulability 분석 | X | 없음 |
| W/H/M runtime 변경 | X | 전부 고정 |

### Deadline 판정: △

Section 3.3에서 "대부분 산업 시스템의 real-time requirement는 100 ms 이내"라고 주장하고 Table 2의 60.7 ms와 비교한다. 그러나:

- 100 ms 기준의 출처나 계산 근거가 없다 — "요즘 산업에서는 이걸 deadline으로 둔다" 수준의 한 줄 주장이다
- T_W = 4800/48000 = 100 ms와 일치하지만 원문이 이를 연결하지 않는다
- 60.7 ms가 단일 window latency인지 300-sample batch total인지 명확하지 않다
- Physical test-bench에서 average 170 ms, Table 6에서 0.16±0.23 s로 100 ms를 초과한다

따라서 △로 판정한다. Acquisition period(100 ms)는 존재하지만 deadline 선언의 근거가 부실하고 실제 검증이 일관되지 않는다.

---

## 핵심 수치

| 지표 | 값 |
|---|---|
| 플랫폼 | ALINX FPGA board; Zynq UltraScale+ MPSoC XCZU9EG; quad Cortex-A53 1.5 GHz |
| 실행환경 | Linux, Python 3.8, PyTorch 1.7.0, CUDA 10.2, cuDNN 7.0 (Zynq에 NVIDIA GPU 없어 환경 불명확) |
| W | 4800 samples, f_s=48 kHz → T_W=100 ms |
| CS 압축 후 | M=960 dimensions, CR=80% |
| H | CWRU: stride 미보고; physical: non-overlapping → H=4800 |
| 논문 주장 diagnosis time | 60.7 ms (Table 2, CWRU 300-sample test) |
| Physical platform average | 0.17 s = 170 ms (Table 8) |
| Table 6 average | 0.16±0.23 s (SD > mean) |
| Accuracy | CWRU 99.97%±0.44 (20회); physical 99.67%±0.47 |
| Model size | 미보고 |
| Memory | DDR4 8 GB, eMMC 32 GB |

### Compression ratio별 trade-off (Figure 10)

| CR | Retained dim | Accuracy | Diagnosis time |
|---:|---:|---:|---:|
| 50% | 2400 | 100% | 0.4014 s |
| 70% | 1440 | 99.92% | 0.1649 s |
| 80% | 960 | 99.86% | 0.0637 s |
| 85% | 720 | 97.69% | 0.0605 s |
| 90% | 480 | 90.71% | 0.0571 s |
| 95% | 240 | 83.28% | 0.0489 s |

---

## CS 압축과 개인연구의 W 축소 비교

### 구조적 유사점

둘 다 model에 전달되는 input을 줄여 diagnosis cost를 감소시키며, accuracy–time trade-off를 갖는다.

### 결정적 차이

| 관점 | Shan et al. CS | 개인연구 W 축소 |
|---|---|---|
| Observation duration | 4800 samples temporal interval 유지 후 압축 | W/f_s 자체가 짧아짐 |
| Acquisition time 감소 | 실험은 Nyquist data 후처리 → 실제 감소 미입증 | W/f_s 직접 감소 |
| Runtime adaptation | 없음 (CR=80% 고정 배포) | q+S 기반 선택 예정 |
| Trigger | 없음 | machine condition + system slack |

이 논문의 CR sweep(Section 3.4)은 input dimension–accuracy–time trade-off를 실험으로 보여준다는 점에서, 개인연구의 mode profiling 설계 시 참고할 수 있는 구조적 선례다.

---

## 세 문장 압축

Shan et al.은 4800-sample vibration window를 compressed sensing으로 960차원까지 줄인 뒤 복원 없이 DKELM에 직접 입력하는 CS-DKELM을 제안한다. Compression ratio를 높일수록 diagnosis time은 감소하지만 accuracy도 하락하며, 80% compression에서 60.7 ms testing time을 근거로 100 ms real-time requirement를 만족한다고 주장한다. 그러나 100 ms 기준은 "산업 관행"이라는 한 줄 주장에 불과하고 physical test-bench에서의 average time은 170 ms이며, per-window timing boundary·p99·deadline miss는 보고되지 않는다.

## Related Work 영어 한 줄

> Shan et al. reduced fault-diagnosis cost by directly classifying compressed vibration measurements with a kernelised extreme learning machine, but used a fixed offline compression ratio and did not adapt the acquisition or model configuration according to machine condition or system slack.

---

## 불확실한 점

1. CS와 DKELM이 Zynq PS(ARM), PL(FPGA), 별도 accelerator 중 어디에서 실행되는지 미명시다.
2. CUDA 10.2와 cuDNN 7.0이 XCZU9EG에서 어떻게 사용되는지 불명확하다.
3. 60.7 ms가 단일 window latency인지 300-sample test-set batch total인지 불명확하다.
4. Table 2, Table 6, Table 8에서 포함하는 processing stage가 동일한지 확인되지 않는다.
5. CWRU segmentation의 stride와 overlap이 미보고다.
6. Maximum, p95, p99 latency와 deadline-miss ratio가 없다.
7. 실제 compressive acquisition hardware를 사용했는지, Nyquist data에 software projection만 적용했는지 불명확하다.
8. Table 6의 standard deviation(0.23 s)이 mean(0.16 s)보다 큰 원인이 설명되지 않는다.
9. 100 ms real-time requirement의 출처나 산업 표준 reference가 없다.
