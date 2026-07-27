# Real-Time Fault Detection in Induction Motors Using TinyML: An Evaluation of the Edge Impulse Platform

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S3 (경량화 대조군), S5 (mode profiling 구조 참고)
- **플랫폼 태그**: `PL-MCU`
- **실행환경 태그**: `ENV-OTHER` (Edge Impulse firmware + EON Compiler; OS·SDK·TFLite Micro 여부 미보고)
- **출처/연도**: IEEE Latin Conference on IoT, 2025, DOI 10.1109/LCIoT64881.2025.11118459
- **저자**: Joao Pedro B. Lima
- **분석 MD**: `papers/05_fault_diagnosis_app/reviews/Lima_2025_Edge_Impulse_TinyML_분석.md`

---

## 두 질문

- **가변 변수**: 없음(runtime). f_s, T_W, T_H, DSP, ANN depth/width, quantization을 EON Tuner가 **offline grid search**로 탐색한 뒤 단일 구성으로 고정 배포한다.
- **트리거**: 없음. Runtime mode selection 없음.

---

## 초록 번역

본 논문은 유도전동기 회전자 봉 파손을 모터 외함의 진동 신호로 감지하기 위해 Edge Impulse 기반 TinyML 개발 절차를 평가한다. Arduino Nano 33 BLE의 nRF52840 MCU에 모델을 실제 배포하여 4개 봉 파손에서는 98.6%, 1개 봉 파손에서는 95.8%의 test accuracy를 보고한다. INT8 quantization은 4개 봉 파손 모델의 latency를 27 ms에서 1 ms로 줄였지만, 1개 봉 파손에서는 accuracy가 크게 저하되었다.

---

## 논문 흐름 + Novelty

### 논리 흐름

1. Bearing fault가 아닌 **broken rotor bar**(회전자 봉 파손)를 대상으로 한다. 검출 신호는 **모터 외함 접선 방향 진동**이다. Stator current가 더 일반적이나 vibration이 load variation에 더 robust하다는 선행연구를 근거로 선택한다.
2. Binary classification 두 개를 별도로 구성한다 — Normal vs. 1-bar, Normal vs. 4-bars.
3. 원 7600 Hz dataset의 18 s recording을 2 s로 분할하고 Edge Impulse에 업로드한다. EON Tuner가 f_s·T_W·T_H·DSP·ANN depth/width·learning rate·dropout·training cycle을 grid search한다.
4. 최적 구성을 EON Compiler로 INT8 quantization하고 nRF52840에 firmware로 배포해 accuracy·latency·RAM·Flash를 실측한다.

### Novelty

신규 ANN 구조나 학습 알고리즘이 아닌 **Edge Impulse platform의 체계적 평가 contribution**이다.

- Vibration 기반 broken rotor bar 탐지를 Edge Impulse workflow로 구현
- EON Tuner로 f_s·W·H·DSP·ANN을 joint search하고 MCU에 직접 배포
- 4-bar(명확한 고장)와 1-bar(미세한 고장)에서 INT8 quantization 효과가 다름을 실증

### 개인연구와의 차이 — 핵심

Lima는 EON Tuner의 blind grid search로 고장 유형별 "최적 1개" configuration을 뽑아 고정한다. 탐색 결과를 보면 1-bar(미세 고장)는 4-bar보다 더 높은 f_s(1000 vs. 250 Hz)와 더 짧은 T_H(250 vs. 500 ms)가 최적이었다. 이것은 **기계 상태 q(고장 심각도)에 따라 적절한 W·H가 달라진다**는 것을 간접적으로 보여주는 결과다. 그러나 Lima는 이 관계를 runtime 규칙으로 정식화하지 않고 두 개의 별도 모델로 처리한다.

개인연구는 이 관계를 offline에서 $W(q)$, $H(S)$ 규칙으로 도출하고, runtime에 측정된 q와 S에 따라 mode를 선택한다. 탐색이 아닌 **규칙 도출**이라는 점에서 Lima의 grid search와 구조적으로 다르다.

---

## RT 등급: B (확정)

| 판정 항목 | 결과 | 원문 근거 |
|---|---|---|
| 명시적 deadline | X | 선언 없음 |
| RTOS 또는 PREEMPT_RT | X | 미보고 |
| Deadline miss / p99 / max | X | 미측정 |
| 평균 inference latency | O | 27 ms, 39 ms, 1 ms (MCU 직접 측정) |
| Hop period T_H | O | 500 ms (4-bar), 250 ms (1-bar) 명시 |
| W/H/M runtime 변경 | X | offline 고정 배포 |

### Deadline 판정: △

T_H=500 ms (4-bar), T_H=250 ms (1-bar)가 명시되어 있고 inference latency(27 ms, 39 ms) < T_H 이나, 논문은 이를 deadline으로 선언하지 않고 miss·p99·max를 측정하지 않는다.

---

## 핵심 수치

| 지표 | 값 |
|---|---|
| 플랫폼 | Arduino Nano 33 BLE; Nordic nRF52840 (Cortex-M4, 64 MHz, 256 KB RAM, 1 MB Flash) |
| 실행 환경 | Edge Impulse firmware + EON Compiler (OS·TFLite Micro 여부 미보고) |
| 센서 | Motor casing tangential vibration accelerometer (모델 미보고) |
| 고장 유형 | Broken rotor bar (NOT bearing fault) |
| 원 dataset f_s | 7600 Hz |
| f_s 탐색 후보 | 100, 250, 500, 1000 Hz |
| T_W 후보 | 1000, 2000 ms |
| T_H 후보 | 250, 500, 1000, 2000 ms |
| Model 후보 | Dense ANN; first-layer 20/40 neurons, 2/3 layers, dropout 0/0.25/0.5 |
| DSP 후보 | FFT 16/32 points, Haar wavelet, Biorthogonal 1.3 wavelet |
| Quantization 후보 | FP32, INT8 |

### 최종 선택 구성 비교

| 항목 | 4-bar FP32 | 4-bar INT8 | 1-bar FP32 | 1-bar INT8 |
|---|---:|---:|---:|---:|
| f_s | 250 Hz | 250 Hz | 1000 Hz | 1000 Hz |
| T_W | 1000 ms | 1000 ms | 1000 ms | 1000 ms |
| W (samples) | 250 | 250 | 1000 | 1000 |
| T_H | 500 ms | 500 ms | 250 ms | 250 ms |
| H (samples) | 125 | 125 | 250 | 250 |
| DSP | Biorthogonal 1.3 | Biorthogonal 1.3 | Haar | Haar |
| Accuracy | 98.6% | 98.1% | 95.8% | 68.3% |
| Latency | 27 ms | 1 ms | 39 ms | 미보고 |
| RAM | 1.4 KB | 미보고 | 1.6 KB | 미보고 |
| Flash | 14.5 KB | 미보고 | 21.4 KB | 미보고 |

**latency 해석:** 27 ms, 39 ms, 1 ms는 model inference 시간이다. window acquisition, majority voting, E2E decision latency가 아니다. 4-bar 모델은 2-second sample 안에서 3개 subsample prediction을 majority vote한 뒤 최종 class를 결정한다.

---

## 세 문장 압축

Lima는 모터 외함 진동으로 broken rotor bar를 탐지하는 TinyML pipeline을 Edge Impulse에서 grid search하고 Arduino Nano 33 BLE에 실제 배포한다. 4-bar model은 FP32 27 ms에서 INT8 1 ms로 단축하며 98.1% accuracy를 유지한 반면, 미세한 1-bar model은 quantization 시 accuracy가 95.8%에서 68.3%로 크게 저하되었다. 그러나 탐색은 offline blind search이며, 기계 상태와 시스템 slack에 따른 W·H·M 선택 규칙 도출과 runtime mode selection, explicit deadline, p99, miss 분석은 다루지 않는다.

## Related Work 영어 한 줄

> Lima evaluated Edge Impulse for jointly profiling sensing windows, DSP front ends, neural-network configurations, and quantization on an nRF52840, but selected a fixed configuration through offline grid search without deriving a runtime rule relating machine condition and system slack to W/H/M.

---

## 불확실한 점

1. Edge Impulse firmware 내부 inference runtime이 TFLite Micro인지 여부
2. Arduino core, EON Compiler·SDK version
3. RTOS 또는 bare-metal 실행 여부
4. Accelerometer 모델과 live sensing pipeline 구성
5. MCU latency 측정 횟수·mean·SD·max·p99 (대표 단일 수치만 제시)
6. 4-bar INT8 모델의 RAM·Flash 미보고
7. 1-bar INT8 latency·RAM·Flash 미보고
8. 1-bar quantization 전 accuracy가 95.8%와 97.4%로 위치에 따라 다름 (Table III 조건 재확인 필요)
9. 2-second sample의 final majority-vote decision latency
10. Feature-extraction latency가 reported inference latency에 포함되는지
11. 전체 EON Tuner grid 결과 미공개 (최적 2개 구성만 제시)
12. 87.5%와 100% load data의 train/val/test 분배 방식
13. Confidence threshold 60%와 majority voting이 accuracy 수치에 반영되었는지
