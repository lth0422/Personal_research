# A Physics-Aware Lightweight Transformer Network for Intelligent Bearing Fault Diagnosis Under Variable Operating Conditions

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S2 (adaptive fidelity 비교군), S4 (edge inference 자원 측정)
- **플랫폼 태그**: `PL-SBC-SOC`
- **실행환경 태그**: `ENV-LINUX` (OS·kernel 미기재; ONNX Runtime 1.16)
- **출처/연도**: Artificial Intelligence for Engineering, 2026:2, pp.195–207, DOI 10.1049/aie2.70014
- **저자**: Ali Sayghe
- **원문 위치**: `papers/05_fault_diagnosis_app/` (파일명 별도 확인)
- **분석 PDF**: `papers/05_fault_diagnosis_app/reviews/PLT_Bearing_Physics_Aware_Transformer_분석.pdf`

---

## 두 질문

- **가변 변수**: 없음. W(=L), P(patch size), M(PLT-Bearing) 전부 offline 고정. Physics-guided sizing은 학습 전 설계 단계에서만 작동.
- **트리거**: 없음. Bearing characteristic frequency와 sampling frequency로 patch size P를 offline 결정. Runtime mode 변경 trigger 없음.

---

## 초록 번역

기존의 베어링 고장 진단 방법은 산업용 엣지 장치에 배포할 수 있을 정도로 경량성을 유지하면서도, 다양한 운전 조건 전반에서 일반화하는 데 어려움이 있다.

본 논문은 PLT-Bearing이라는 physics-aware transformer를 제안한다. 이 모델은 vision transformer의 tokenisation 방식을 진동 신호에 맞게 수정하며, 다음 세 요소를 결합한다: 겹치는 convolutional patch embedding, sampling frequency에 기반한 patch size 결정, amplitude 변화에 영향을 받지 않는다고 저자가 주장하는 self-attention 구조.

PLT-Bearing은 약 0.52M parameters와 GPU inference latency 8.2 ms만으로 CWRU와 Paderborn University benchmark에서 각각 99.2%, 95.8% accuracy를 달성하였다. 또한 load가 다른 조건으로 fine-tuning 없이 전이하는 zero-shot cross-load 실험에서 평균 90.3% accuracy를 기록하며, 최근 lightweight CNN과 Mamba 기반 state-space model보다 높은 성능을 보였다.

---

## 논문 흐름 + Novelty

### 논리 흐름

1. 기존 CNN은 local pattern에 강하지만 long-range dependency를 충분히 보지 못하고, 표준 ViT는 이미지용 nonoverlapping patch tokenisation을 진동 신호에 그대로 적용해 fault impulse를 patch boundary에서 분절할 수 있다는 문제 제기
2. Depthwise-separable convolution 기반 overlapping Conv-Stem을 사용하여 transient impulse가 최소 한 token 안에 온전히 포함되도록 함
3. Bearing characteristic frequency와 sampling frequency를 이용해 patch size를 정하는 physics-guided patch sizing 제안
4. 4-layer lightweight transformer와 classification token으로 global pattern 학습 + variable load에서 cross-load generalisation 평가
5. CWRU/PU accuracy, zero-shot cross-load, ablation, attention visualisation, GPU/Raspberry Pi 4 latency, INT8 pruning deployment 논의로 검증

### 저자가 주장하는 Novelty

| Novelty | 내용 | 근거 |
|---|---|---|
| 1. Overlapping convolutional tokenisation | Depthwise Conv1D (kernel=P, stride=P/2) + Pointwise Conv1D → 50% overlap; fault impulse가 두 token으로 잘려 불완전하게 관찰되는 문제 해소 | Section 3.3, pp.3-4; Figure 2 |
| 2. Physics-guided patch sizing | P/f_s ≥ 1/f_min → P* = ⌈f_s/f_min⌉; patch가 최소 한 번의 fault impulse cycle을 포함해야 한다는 물리 조건으로 P의 lower bound 정의 | Section 3.2, p.3, Eq.(5) |
| 3. Cross-load amplitude invariance 이론 | load 변화가 진동을 (×c) scaling해도 self-attention의 상대적 pattern이 유지된다고 주장 | Section 3.5.1, p.5, Eq.(13)-(14) — 수학적 문제 있음 (5절 참조) |
| 4. Modern lightweight baseline과 edge latency 비교 | GPU뿐 아니라 Raspberry Pi 4에서도 모델별 latency를 비교 | Section 5.2, Table 5, p.8 |
| 5. Real-world deployment discussion | INT8 quantisation, structured pruning, sensor variability, concept drift, operational validation | Section 6, pp.10-11 |

---

## W 설계 — 물리 근거

### 핵심 구분: W(전체 window) ≠ P(patch size)

| 기호 | 의미 | CWRU | PU |
|---|---|---|---|
| L (=W) | 전체 input window, 개인연구의 (W)에 대응 | 1024 samples | 16,384 samples |
| P | 한 transformer token이 보는 patch size | 64 samples | 1024 samples |
| s | patch stride (= P/2) | 32 samples | — |
| N_p | token 수 | 31 | 16 |

저자가 물리적으로 유도하는 것은 **전체 input window (W=L)이 아니라 patch size (P)**이다.

### Input window (W) 자체의 선택 근거

원문은 P의 physics-based lower bound를 유도하지만, W(=L) 값의 선택 근거는 별도로 유도하지 않는다.

| Dataset | W (=L) | f_s | T_W |
|---|---|---|---|
| CWRU | 1024 samples | 12,000 Hz | 1024/12000 ≈ 85.3 ms |
| PU | 16,384 samples | 64,000 Hz | 16384/64000 = 256 ms |

**판정**: Physics-aware design의 직접 대상은 patch size (P)이며, 전체 input window (W=L)의 길이는 dataset별 experiment configuration으로 주어진다.

### Patch size P를 결정하는 물리량

베어링 characteristic frequency:

- f_BPFI = (B/2)·f_r·(1 + d_b/d_p·cos α)
- f_BPFO = (B/2)·f_r·(1 - d_b/d_p·cos α)
- f_BSF = (d_p/2d_b)·f_r·[1 - (d_b/d_p·cos α)²]
- f_FTF = (f_r/2)·(1 - d_b/d_p·cos α)

가장 낮은 characteristic fault frequency를 f_min으로 놓는다.

**조건**: 한 patch가 적어도 하나의 완전한 fault impulse cycle을 포함해야 함

P/f_s ≥ 1/f_min → **P* = ⌈f_s/f_min⌉**

(근거: Section 3.2, p.3, Equations (1)-(5))

### CWRU에서의 실제 patch size

- f_s = 12,000 Hz
- 논문 Section 3.2의 P** ≈ /162 (≈74로 해석됨, 원문 f_0 표현 모호)
- Ablation에서 (P=64)가 empirically optimal → 실제 모델 P = 64 사용
- T_P = 64/12,000 ≈ 5.33 ms
- stride s = 32, token 수 N_p = ⌊(1024-64)/32⌋ + 1 = 31

Ablation (CWRU, -4 dB 아님, 정확도 기준):

| Patch size | Accuracy | Parameters |
|---|---|---|
| 32 | 99.9% | 54K |
| **64** | **99.2%** | **520K** |
| 128 | 98.1% | 500K |

---

## 개인연구 (W/H)와의 대응

CWRU continuous monitoring 기준:

- W = 1024, H = 512, f_s = 12,000 Hz
- T_W = 1024/12000 ≈ 85.3 ms
- T_H = 512/12000 ≈ 42.7 ms

이 논문은 명시적으로 고정 mode **a = (W=1024, H=512, M=PLT-Bearing)**를 사용한다고 볼 수 있다. 다만 runtime에 (W/H/M)을 바꾸지는 않는다.

---

## RT 등급: B (확정)

| 판정 항목 | 결과 | 원문 근거 |
|---|---|---|
| 명시적 deadline 수치 | X | 없음 |
| RTOS 또는 RT-Linux | X | OS·kernel 미기재 |
| Deadline miss 측정 | X | 없음 |
| Tail latency (p99/max) | X | 미보고 |
| Schedulability 분석 | X | 없음 |
| Average latency | O | 43.6 ms, 1000 calls (Table 5) |
| Deadline | △ | H/Period 명시되어 D=T_H로 해석 가능하나, miss를 측정하거나 명시하지 않음 |
| W/H/M runtime 변경 | X | 전부 고정 |

**핵심 문제**: H = 512 → T_H ≈ 42.7 ms, R_avg = 43.6 ms. 평균 inference latency가 hop보다 약간 길다. 43.6 - 42.67 ≈ -0.93 ms 마진. Single-threaded sequential pipeline에서 매 hop마다 추론하면 평균 기준으로도 backlog가 생긴다. 논문은 "real-time continuous monitoring"이라고 표현하지만 multi-core pipeline, buffering, deadline miss ratio를 제시하지 않는다.

---

## Pi 4 Latency 수치

### 측정 환경

| 항목 | 값 |
|---|---|
| Device | Raspberry Pi 4 Model B |
| RAM | 4 GB |
| CPU | Cortex-A72, 1.8 GHz |
| Runtime | ONNX Runtime 1.16 |
| Model format | ONNX |
| Preprocessing | Vectorised NumPy |
| Positional encoding | Precomputed/cached |
| Measurement count | 1000 inference calls |
| Batch size / Warm-up / Thread / OS | 확인 불가 (미기재) |

### Latency 비교 (Table 5, ms per sample, Pi 4)

| Method | Raspberry Pi 4 |
|---|---|
| 1D-CNN | 68.4 ms |
| LSTM | 185.2 ms |
| CNN-LSTM | 210.7 ms |
| ResNet-18 | 510.3 ms |
| Transformer | 102.1 ms |
| MobileNet-1D | 55.2 ms |
| MambaFault | 88.9 ms |
| **PLT-Bearing** | **43.6 ms** |

- p99/max/min/SD/jitter: 모두 미보고
- W=1024 기준인지 W=16384 포함 평균인지 명시 없음 (W=1024 가능성 높음)

INT8 pruning 참고:
- FP32 full: 8.6 MB, 0.52M params, CWRU 99.2%, Pi 4 43.6 ms
- INT8: 2.2 MB, accuracy loss <0.3%, Pi 4 latency 미보고
- INT8 + pruning: 1.1 MB, 0.28M INT8, 별도 Pi 4 latency 미보고
- Cortex-M7 43 ms 추정값 있으나 실험 세부조건 미기재 → 원고 근거로 쓰지 않음

---

## 세 문장 압축

이 논문은 표준 ViT의 비중첩 patch가 진동 fault impulse를 boundary에서 분절하고 variable-load generalisation이 약하다는 문제를 해결하기 위해, overlapping depthwise Conv-Stem과 lightweight transformer를 제안한다. Bearing characteristic frequency와 sampling frequency로 patch size P를 정하지만, 전체 input window W는 dataset별 고정이며 runtime에는 (W/H/M)을 변경하지 않는다. Raspberry Pi 4에서 평균 43.6 ms inference를 보고하지만 hop T_H ≈ 42.7 ms보다 약간 길고 max·p99·miss·scheduling 분석이 없어 q+S 기반 deadline-aware mode selection과는 차이가 있다.

## Related Work 영어 한 줄

> Sayghe proposed a physics-aware lightweight transformer with overlapping convolutional tokenisation and characteristic-frequency-guided patch sizing, but the model uses a fixed (W/H/M) configuration and reports only average Raspberry Pi latency without deadline-miss or tail analysis.

---

## 서베이 표 항목

| 항목 | 내용 |
|---|---|
| 가변 변수 | 없음 — W/H/M 전부 offline 고정 |
| 트리거 | 없음 |
| 플랫폼·환경 | Raspberry Pi 4 Model B; ONNX Runtime 1.16; OS·kernel 미기재 |
| 경량화·배포 기법 | 물리 인식 경량 Transformer (patch 수 최소화) + ONNX Runtime; 0.52M param |
| 보장 수준 | B — avg 43.6 ms (1000 calls), max/p99/miss 없음 |
| 본 연구와의 gap | W/H 고정, deadline 미정의, q+S trigger 없음, timing margin 부족 |

---

## 불확실한 점

1. **Characteristic frequency 원문 내부 모순**: Section 3.2는 CWRU f_0를 "smallest defect frequency" (BPFI ≈ 162 Hz로 추정)로 표현하고 P** ≈ /162라 하지만, Section 5.7의 CWRU 계산값은 FTF ≈ 14 Hz로 가장 낮다. f_min=14 Hz이면 P* = ⌈12000/14⌉ ≈ 858이며 실제 P=64와 크게 달라진다. FTF·BSF·BPFO를 제외하고 BPFI만 사용하는 이유를 원문이 명시하지 않음.
2. **PU patch bound도 수식과 불일치**: f_s=64,000, f_min≈8 Hz → P*=8000이지만 실제 P=1024. 원문은 전체 segment (L=16384)가 모든 fault cycle을 포함하므로 token level constraint를 보존한다고 설명하지만, 개별 token size P=1024는 그 bound를 만족하지 않음.
3. **Softmax amplitude invariance 증명 수학적 문제**: softmax(cz) ≠ softmax(z) 일반적으로 성립하지 않음. Novelty 3의 핵심 이론 근거에 수학적 오류 가능성.
4. **Data preprocessing 문장 충돌**: Section 4.2에서 "segmented into nonoverlapping samples"와 "using a sliding window with 50% overlap"이 공존.
5. **43.6 ms의 W 기준**: CWRU(W=1024)만인지 PU(W=16384) 포함인지 명시 없음.
6. **Pi 4 측정 조건**: OS, warm-up 횟수, thread 수, CPU governor, core affinity 전부 미기재.
