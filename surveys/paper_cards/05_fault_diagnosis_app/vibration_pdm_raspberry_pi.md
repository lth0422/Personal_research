# Vibration-Based Predictive Maintenance for Motors Using Edge AI

- **그룹**: 5 fault_diagnosis_app (배경 참고용 — RT 없음, 경량화 기법 미명시)
- **연구 섹션**: S1 embedded RT FD 대조군 (약한 비교군)
- **플랫폼 태그**: `PL-SBC-SOC`
- **실행환경 태그**: `ENV-LINUX` (OS 이름·version 원문 미기재, 추정)
- **출처/연도**: IEEE RAEEUCCI 2026, DOI: 10.1109/RAEEUCCI67649.2026.11504862
- **저자**: Bhaventhan R, Daniel Stanlyraj X, S. Purushothaman
- **원문 위치**: `papers/05_fault_diagnosis_app/Vibration_PdM_Edge_AI_Raspberry_Pi.pdf`
- **재판정 분석**: `papers/05_fault_diagnosis_app/reviews/Vibration-Based_Predictive_Maintenance_for_Motors_Using_Edge_AI.pdf`

---

## 두 질문

- **가변 변수**: 없음. W/H/M 전부 고정. Conv1D(32)-Pool-Conv1D(64)-Pool-Dense64-Dense4 단일 모델을 연속 실행.
- **트리거**: 없음. Softmax 출력이 4-class label을 결정하며 runtime mode 변경 trigger는 없음.

---

## RT 등급: B (확정)

**B 유지 근거 (원문 section/page 기준)**

| 판정 항목 | 결과 | 원문 근거 |
|---|---|---|
| 명시적 deadline 수치 | X | 논문 전체에 없음 |
| RTOS 또는 RT-Linux 사용 | X | OS/RTOS/kernel 정보 미기재, 전체 |
| deadline miss 측정 | X | 없음 |
| tail latency (p99/max) 측정 | X | 없음 |
| 수치 평균 inference latency | X | Section VI-E p.6: "low computational delay" 정성 표현만 |
| schedulability 분석 | X | task model, utilization, RTA 없음 |
| WCET bound | X | 없음 |
| W/H/M runtime 변경 | X | 단일 고정 CNN 연속 실행 |

**핵심 패턴**: "low latency", "real-time", "near real-time monitoring"은 cloud offloading 대비 local execution의 일반적 장점으로 주장될 뿐, 수치로 입증되지 않는다.

---

## 핵심 방법 요약

### 시스템 구성

- 플랫폼: Raspberry Pi 4 Model B
- 센서: ADXL345 tri-axial accelerometer (본문 기술) — **단, Figure 1과 불일치 (아래 참고)**
- 디스플레이: OLED (진단 결과 표시)
- 도메인: BLDC motor 4-class fault diagnosis
- RPM 조건: 1000, 1500, 2000 RPM

### 모델 구조 (Figure 1, p.3)

```
Input: (15 × 1)  ← 원문 내부 불일치 있음
Conv1D - 32 filters, kernel 3, ReLU
MaxPooling1D - pool 2
Conv1D - 64 filters, kernel 3, ReLU
MaxPooling1D - pool 2
Flatten
Dense 64, ReLU
Dense 4, Softmax
→ 4-class: Imbalance / Normal / Misalignment / Bearing Wear
```

parameter 수, model 크기(KB), 배포 framework 모두 원문 미기재.

### 경량화·배포 기법

TFLite, INT8 양자화, pruning, ONNX, Edge Impulse, TensorRT 중 어느 것도 원문에 언급되지 않는다. "lightweight CNN", "deployed on edge computing platform", "computationally efficient" 등 정성 표현만 있으며 실제 배포 format과 runtime interpreter는 확인 불가. "표준 Keras/TF를 Pi에서 직접 실행했다"고도 단정할 수 없다 (library 이름 미기재).

### 실험 결과

- 약 50회 repeated runs, fault severity 28–30% (low severity)
- 평균 accuracy ≈ 92%
- confusion matrix, precision/recall/F1, test sample 수, train/validation/test split 모두 없음
- 수치 inference latency 없음

---

## 원문 내부 불일치 (중요)

Figure 1 (p.3)의 입력: MPU1 (AX AY AZ GX GY GZ) + MPU2 (AX AY AZ GX GY GZ) + VIB1/VIB2 SOUND → **total 15 features, input shape = (15×1)**

그러나 Abstract와 본문은 **ADXL345 3축 가속도계 단독**으로 raw vibration sequence를 입력으로 사용한다고 설명한다.

| 불일치 항목 | 본문 설명 | Figure 1 |
|---|---|---|
| 센서 구성 | ADXL345 단일 3축 | MPU×2 + Sound×2 = 15 채널 |
| 입력 표현 | raw time-domain sequence | (15×1) feature vector |

이 불일치로 인해 실제 Raspberry Pi 입력 tensor와 sensor configuration을 원문만으로 재현하기 어렵다.

---

## 내 연구 관점

**같은 점 (배경 참고 가능)**
- Raspberry Pi 기반 edge FD — Pi Zero 2W와 같은 Linux-class SBC 계열
- 진동 시계열로 motor fault 분류 (같은 도메인)
- Cloud 없이 local inference 수행
- 1000/1500/2000 RPM 다속도 조건 평가

**결정적 차이 (gap)**
W/H 미정의, 수치 latency 없음, 경량화 기법 미명시, RT scheduling 없음, q+S 기반 mode selection 없음.

**인용 맥락**: "Raspberry Pi 기반 edge fault diagnosis의 사례로서 4-class multi-speed 분류를 local에서 수행하지만, 입력 window, 진단 주기, 수치 latency, RT deadline, runtime adaptation을 다루지 않는다"는 약한 비교군 인용.

**Related Work용 영어 문장** (분석 PDF p.11):
> Bhaventhan et al. deployed a lightweight 1D-CNN on a Raspberry Pi 4 for four-class motor fault diagnosis across multiple operating speeds. However, the study does not report explicit input-window or diagnosis-period settings, quantitative inference latency, real-time deadlines, or runtime adaptation of the window/model configuration.

---

## 서베이 표 항목

| 항목 | 내용 |
|---|---|
| 가변 변수 | 없음 — W/H/M 전부 고정 |
| 트리거 | 없음 — continuous fixed-model inference |
| 플랫폼·환경 | Raspberry Pi 4 Model B, OS/RTOS 미기재 |
| 경량화 기법 | 없음 (원문 미명시, 표준 CNN 직접 실행 추정) |
| 보장 수준 | B — "low latency" 정성 표현만, 수치 없음 |
| 본 연구와의 gap | W/H 미정의, 경량화 미명시, RT scheduling 없음, q+S trigger 없음 |

---

## 세 문장 압축

이 논문은 Raspberry Pi 4에서 진동 기반 1D-CNN을 실행하여 정상, 불평형, 축정렬 불량, 베어링 마모를 약 92% 정확도로 분류한다. 단일 고정 모델을 사용하며 W, H, overlap, 수치 latency, 경량화·배포 runtime은 원문에서 확인되지 않고 센서 설명과 Figure 1 간 내부 불일치가 존재한다. 기계 상태 q와 scheduling slack S를 함께 이용한 deadline-aware W/H/M runtime mode selection은 다루지 않는다.

---

## 불확실한 점

- Raspberry Pi OS/distribution 및 kernel version: 원문 미기재
- Python 및 DL framework 이름: 원문 미기재 (Keras 유사 표현만)
- ADXL345 sampling rate 및 interface (I2C/SPI): 미기재
- 실제 input tensor shape: Figure 1의 (15×1)과 본문 raw sequence 설명 불일치로 확인 불가
- W (input window size): 미기재. Figures 2–9의 x축이 약 300 sample이나 W=300이라는 명시 없음
- H (diagnosis hop/period): 미기재
- Model parameter 수 및 크기(KB): 미기재
- 배포 runtime (TFLite / native TF / 기타): 미기재
