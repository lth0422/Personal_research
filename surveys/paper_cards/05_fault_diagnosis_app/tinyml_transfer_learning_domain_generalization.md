# TinyML-enabled Edge Implementation of Transfer Learning Framework for Domain Generalization in Machine Fault Diagnosis

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S1 (embedded edge FD 배포 대조군), S4 (edge inference 자원 측정)
- **플랫폼 태그**: `PL-MCU` (추론: ESP32), `PL-SBC-SOC` (학습: Raspberry Pi 4B)
- **실행환경 태그**: `ENV-OTHER` (ESP32: TFLite via Arduino IDE; Pi: TensorFlow, RTOS 미사용)
- **출처/연도**: Expert Systems with Applications 213 (2023) 119016
- **DOI**: 10.1016/j.eswa.2022.119016
- **저자**: Supriya Asutkar, Chaitravi Chalke, Kajal Shivgan, Siddharth Tallur (IIT Bombay)
- **원문 위치**: `papers/05_fault_diagnosis_app/TinyML_Transfer_Learning_Domain_Generalization_Machine_Fault_Diagnosis.pdf`

---

## 두 질문

- **가변 변수**: 없음. W (CWRU 20,000 samples, IMS 20,480 samples) 고정; M (2498 파라미터 1D CNN) 고정; H(diagnosis period) 미정의. TL 전략(어느 layer를 fine-tune할지)은 학습 시간에만 선택.
- **트리거**: domain shift (다른 기계/센서/설치 환경) → offline fine-tuning (Pi 4B에서 53–440초 소요). Runtime mode 변경 trigger 없음.

---

## RT 등급: B (확정)

| 판정 항목 | 결과 | 원문 근거 |
|---|---|---|
| 명시적 deadline 수치 | X | 논문 전체에 없음 |
| RTOS 또는 RT-Linux | X | ESP32: Arduino IDE; Pi: TensorFlow, RTOS 미사용 |
| deadline miss 측정 | X | 없음 |
| tail latency (p99/max) | X | Section 3.4: mean inference time만 보고 |
| schedulability 분석 | X | 없음 |
| W/H/M runtime 변경 | X | TL fine-tuning은 offline (학습 시간) |
| 수치 inference latency | △ | Section 3.4: ESP32에서 ~700 ms/input, 267 kB memory |

**핵심 패턴**: TL이 "온라인 학습"으로 표현되지만 이는 Pi에서 수십~수백 초 소요되는 fine-tuning을 뜻한다. Inference가 수행될 때는 모델이 고정되어 있으며 deadline/scheduling 개념이 없다.

---

## 핵심 방법 요약

### 전체 파이프라인 (Figure 1)

```
Raw vibration time series (W samples)
→ 10개 시간영역 통계 특징 추출 (Table 1)
   Mean, Median, MAD, Variance, SD, Kurtosis, Skew, Crest factor, Impulse factor, Shape factor
→ (10 × 1) feature vector
→ 1D CNN 추론 (2498 parameters)
→ 2-class or binary fault label
```

Source domain (CWRU)에서 학습 → 특정 layer 고정 → target domain 데이터로 offline fine-tuning.

### 입력 W 설계

| 데이터셋 | W | Sampling rate | 시간 환산 | Overlap |
|---|---|---|---|---|
| CWRU (source) | 20,000 samples | 20 kHz | 1.0 s | 없음 (non-overlapping) |
| IMS (target 1) | 20,480 samples | 20 kHz | ~1.024 s | 없음 |
| LPS (target 2) | 650 files (15,000 samples/file) | 26.7 kHz | ~0.56 s | 없음 |

W는 신호처리 해상도나 베어링 특성주파수 기반이 아니라 데이터셋 분할 편의로 고정. Runtime 변경 없음.

### 모델 구조 M (Table 4)

```
Input: (10 × 1)
Conv1D (32 filters, kernel 3, ReLU)   ─┐
Conv1D (16 filters, kernel 3, ReLU)   ─┘  총 1680 파라미터 (conv layers)
MaxPool1D (stride 2)
Dropout (0.2)
Flatten (48 nodes)
Dense (16, ReLU)   ─┐
Dense (2, Softmax) ─┘  총 818 파라미터 (dense layers)

Total: 2498 trainable parameters
```

RandomSearch hyperparameter tuning (5-fold CV, 10 iterations).

### Transfer Learning 전략 비교 (Table 5)

| 전략 | 수정 대상 | 핵심 결과 |
|---|---|---|
| No TL | — | domain shift 시 59–80% accuracy |
| TL, W&B, D (기존 관례) | Dense layer weights+biases 재학습 | 정확도 낮음 |
| TL, W&B, C (논문 제안) | Conv layer weights+biases 재학습 | 정확도 가장 높음 (81–100%) |
| TL, B, D | Dense layer biases만 재학습 | 메모리 ~1/3, 정확도 중간 |
| TL, B, C | Conv layer biases만 재학습 | 메모리 ~1/3, 정확도 개선 |

**핵심 발견**: Conv layer가 domain-specific 정보를 담는다 → Conv layer를 fine-tune해야 domain 일반화 효과. 이는 기존 관례(Dense layer 재학습)와 반대.

### Edge 배포 자원 측정

**ESP32 DevKit V1 추론 (Section 3.4)**:
- Framework: TFLite via Arduino IDE
- Inference time: ~700 ms per 10-feature input (단일 측정, 방법론 세부 미기재)
- Memory: 267 kB
- Accuracy (same-domain): 100%

**Raspberry Pi 4B 학습 (Table 5)**:
- Memory: 10–34 MB (전략에 따라)
- Training time: 53–440 s (전략에 따라; bias-only가 가장 빠름)

**통계 특징 계산 시간 on Pi (Table 2, 5000 samples)**:
- 10개 특징 총합: <0.5 s (Median이 가장 느림 0.219 s)
- Spectrogram: 0.741 s, 11.6 MB → edge 가능
- Scalogram: 101.159 s, 5 MB → edge 비현실적

→ 통계 특징 기반 접근의 edge 적합성을 정량적으로 보여주는 자료.

---

## 내 연구 관점

**같은 점 (참고 가능)**
- 통계 특징 10개를 W에서 추출하여 CNN 입력으로 사용 → 본 연구의 W 설계 시 raw input vs. 통계 특징 선택 근거
- ESP32 + TFLite로 2498 파라미터 모델 배포 성공: 경량 모델의 edge 실현 가능성 수치 근거
- Pi 4B에서 online fine-tuning memory 측정 → Pi Zero 2W 환경의 mode 전환 비용 추정 참고

**결정적 차이 (gap)**

| 관점 | Asutkar et al. | 개인연구 |
|---|---|---|
| W | 데이터셋 단위 고정 (1 s) | 가변 (mode tuple의 변수) |
| H | 미정의 | diagnosis period 변수 |
| M | 단일 CNN 고정 | 복수 mode/model 후보 |
| 적응 | offline TL (53–440 s) | runtime q+S 기반 mode selection |
| 도메인 shift | 새 도메인에서 재학습 | 기계 상태 q를 runtime에 감지 |
| Scheduling | 없음 | PREEMPT_RT task interference 분석 |
| Deadline | 없음 | 명시적 D 정의 예정 |

**인용 맥락**: S1 대조군. "통계 특징 기반 경량 TinyML 배포의 사례. Domain 일반화를 위한 conv layer fine-tuning이 유효함을 보이지만, 적응은 offline에 머물고 runtime W/H/M mode selection을 다루지 않는다." 또한 Table 2의 통계 특징 vs. spectrogram/scalogram 계산 시간 비교는 본 연구의 특징 설계 근거로 인용 가능.

**Related Work용 영어 문장**:
> Asutkar et al. proposed a TinyML-based transfer learning framework for domain-shift generalization in bearing fault diagnosis, demonstrating inference feasibility on an ESP32 microcontroller using only 10 time-domain statistical features and 2498 CNN parameters. The adaptation to new machine domains requires offline fine-tuning of 53–440 s on a Raspberry Pi single-board computer, and the framework defines neither input-window or diagnosis-period adaptation at runtime nor scheduling constraints on the inference task.

---

## 서베이 표 항목

| 항목 | 내용 |
|---|---|
| 가변 변수 | 없음 — W/H/M 전부 offline 고정; TL 전략 선택은 학습 시간 |
| 트리거 | domain shift (수동 감지) → offline fine-tuning |
| 플랫폼·환경 | ESP32 DevKit V1 (TFLite 추론) + Raspberry Pi 4B (TF 학습); RTOS 없음 |
| 경량화·배포 기법 | 통계 특징 10개 (raw W → (10×1) 특징 압축) + TFLite (ESP32 배포) + 2498 파라미터 경량 CNN |
| 보장 수준 | B — ~700 ms inference on ESP32 (수치 있음, 단일 측정), deadline/tail 없음 |
| 본 연구와의 gap | offline TL 적응, W/H 고정, q+S trigger 없음, RT scheduling 없음 |

---

## 세 문장 압축

이 논문은 CWRU를 source domain으로 학습한 경량 1D CNN (2498 파라미터)을 IMS 및 저정밀 센서 LPS 데이터로 transfer learning하여 domain 일반화를 달성하고 ESP32에서 TFLite로 추론하는 구조를 다룬다. Conv layer weights+biases 재학습이 Dense layer 재학습보다 domain 일반화 정확도가 높고, bias만 재학습하면 메모리를 약 1/3로 줄일 수 있지만 모든 fine-tuning은 offline에서 수십~수백 초가 소요된다. W/H/M runtime mode selection, 기계 상태 q와 scheduling slack S 기반 적응, deadline 정의 및 tail latency 측정은 다루지 않는다.

---

## 불확실한 점

- ESP32 ~700 ms: "approximately 700 ms inference time per input file" (Section 3.4) — 반복 횟수, warm-up 포함 여부, batch size 불명
- LPS data의 정확한 sliding window 크기: "650 files with 15,000 samples" 언급이 있으나 window size 명시 없음
- H (runtime diagnosis hop): 정의 없음. inference-on-demand 방식 추정
- Feature computation과 CNN inference가 동일 device에서 sequential하게 수행되는지 pipeline인지 불명
- Pi 4B에서의 TL training이 standard Python TensorFlow를 사용하는지 확인 (논문에 TensorFlow라고 명시)
