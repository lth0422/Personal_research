# Embedded TinyML for Predictive Maintenance: Vibration Analysis on ESP32 with Real-Time Fault Detection in Industrial Equipment

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S3 (경량화 대조군)
- **플랫폼 태그**: `PL-MCU`
- **실행환경 태그**: `ENV-OTHER` (OS·firmware·runtime 미기재; TFLite 또는 TFLite Micro 사용 여부 미명시)
- **출처/연도**: International Journal on Computational Modelling Applications, Vol. 2, No. 2, 2025, DOI 10.63503/j.ijcma.2025.114
- **저자**: Shubbham Gupta, Shiv Naresh Shivhare
- **분석 PDF**: `papers/05_fault_diagnosis_app/reviews/Gupta_2025_ESP32_TinyML_SetB_분석.pdf`

---

## 두 질문

- **가변 변수**: 없음. W=256, H=128, f_s=1 kHz 고정. 두 model(1D CNN / CNN-LSTM)을 offline 비교 후 배포 시 하나를 고정한다.
- **트리거**: 없음. Runtime adaptation 없음. Abstract의 "adaptive sampling" 주장은 본문에서 구현을 확인할 수 없다.

---

## 초록 번역

본 논문은 ADXL345 가속도계와 ESP32를 이용해 진동 신호를 MCU에서 직접 처리하는 TinyML 기반 예지보전 시스템을 제안한다. 경량 1D CNN과 CNN-LSTM을 비교하며, 정상·불균형·축 정렬 불량·베어링 마모를 ESP32에서 분류해 클라우드 없이 저지연 상태 감시가 가능하다고 주장한다.

---

## 논문 흐름 + Novelty

### 논리 흐름

1. 기존 산업용 예지보전은 클라우드 서버에 의존해 전송 지연·비용·보안 문제가 있다는 점을 문제로 제기한다.
2. ADXL345로 1 kHz 진동을 수집하고, 256-sample window + 50% overlap으로 분절한 뒤 normalization과 FFT를 전처리로 수행한다.
3. INT8 post-training quantization을 적용한 1D CNN과 CNN-LSTM을 각각 ESP32에 배포한다.
4. Accuracy, inference latency, memory, power를 비교해 어느 model이 resource-constrained MCU에 더 적합한지 평가한다.
5. 1D CNN이 속도·메모리 효율에서 우세하고 CNN-LSTM이 accuracy에서 약간 높다는 결론을 내린다.

### Novelty

이 논문의 contribution은 신규 알고리즘이 아니라 **MCU 직접 배포의 실증**이다. 클라우드 없이 ADXL345 + ESP32만으로 four-class fault diagnosis pipeline을 완성하고, 두 경량 모델의 on-device resource trade-off를 비교한다. 방법론적 novelty는 낮으나 MCU deployment feasibility를 실험으로 보여주는 것이 목적이다.

---

## RT 등급: B (확정)

| 판정 항목 | 결과 | 원문 근거 |
|---|---|---|
| 명시적 deadline | X | 없음 |
| RTOS | X | OS·RTOS 미기재 |
| Deadline miss / p99 / max | X | 미보고 |
| Average latency | O | 1D CNN 13 ms, CNN-LSTM 26 ms (Table 4) |
| Acquisition period (implicit) | △ | T_H = 128 ms 계산 가능하나 deadline으로 선언하지 않음 |
| W/H/M runtime 변경 | X | 전부 고정 |

### Deadline 판정: △

f_s=1 kHz, W=256 → T_W=256 ms; H=128 → T_H=128 ms. 이 hop duration으로부터 inference time(13 ms, 26 ms)이 T_H보다 짧다는 것을 계산할 수 있다. 그러나 논문은 이 관계를 deadline과 비교하는 방식으로 기술하지 않는다. Inference time에 normalization·FFT·segmentation이 포함되는지도 미기재다. 따라서 deadline은 보고된 설정으로부터 해석 가능한 시간 기준이며, 논문의 명시적 주장이 아니다.

---

## 핵심 수치

| 지표 | 1D CNN | CNN-LSTM |
|---|---|---|
| Accuracy | 91.4% | 93.6% |
| Inference latency | 13 ms | 26 ms |
| Flash | 172 KB | 268 KB |
| RAM | 52 KB | 84 KB |
| Total memory | 224 KB | 352 KB |
| p99 / max | 미보고 | 미보고 |

- 플랫폼: ESP32 + ADXL345 3축 가속도계
- 양자화: offline training 후 post-training INT8 quantization
- f_s = 1 kHz (고정), W = 256 samples, H = 128 samples (50% overlap)
- T_W = 256 ms, T_H = 128 ms

**수치 불일치 주의**: Table 4(accuracy 91.4%/93.6%, latency 13 ms/26 ms)와 Figure 5(약 92%/94%, 15 ms/28 ms) 사이에 불일치가 있다. 또한 초록은 "92% 초과 accuracy"를 주장하지만 Table 4의 1D CNN은 91.4%다.

---

## "Adaptive sampling" 판정: 구현 확인 불가

초록에서 한 차례 주장하지만, 본문 어디에서도 runtime 변경 절차가 없다.

| 섹션 | 내용 |
|---|---|
| Abstract, p.1 | "adaptive sampling" 포함한다고 주장 |
| Section 4.1, p.8 | sensor가 fixed sampling frequency로 신호를 취득한다고 설명 |
| Section 5, pp.9–10 | 실제 실험의 sampling rate는 모든 조건에서 고정 1 kHz |
| Section 4.6, p.9 | ESP32 pseudocode: acquisition → normalization → FFT → segmentation → inference 반복. W/H/f_s 조정 단계 없음 |

관련 조건문, threshold, algorithm, 실험 비교가 없으므로 runtime adaptive sampling을 구현한 논문으로 분류하기 어렵다.

---

## 개인연구와의 연결

- **한 줄 gap**: Gupta and Shivhare는 고정 W=256, H=128과 INT8 model을 ESP32에 배포하지만, machine condition q와 system slack S에 따라 W/H/M을 선택하는 runtime policy와 tail-latency 분석은 제공하지 않는다.
- **활용**: fixed W/H TinyML MCU 비교군. M별 accuracy-latency-memory trade-off의 ESP32 기준값.

---

## 세 문장 압축

Gupta and Shivhare는 1 kHz 진동 신호를 256-sample window와 50% overlap으로 분할하고, INT8 1D CNN과 CNN-LSTM을 ESP32에 배포해 four-class bearing fault를 분류한다. 1D CNN은 91.4% accuracy와 13 ms inference, CNN-LSTM은 93.6%와 26 ms를 보고하며 accuracy와 resource cost의 trade-off를 보여준다. 다만 "adaptive sampling"은 초록에서만 언급되고 실제 실험은 W/H/f_s가 고정되어 있어 runtime adaptation은 확인되지 않는다.

## Related Work 영어 한 줄

> Gupta and Shivhare deployed post-training-quantized 1D CNN and CNN-LSTM models on an ESP32 for vibration-based fault classification, but used a fixed sampling rate and fixed window configuration without runtime W/H/M adaptation or tail-latency analysis.

---

## 불확실한 점

1. ESP32의 구체적인 model과 CPU clock이 미기재다.
2. Firmware OS, framework, compiler와 runtime이 미기재다.
3. TensorFlow Lite 또는 TFLite Micro의 실제 사용 여부가 명시되지 않는다.
4. INT8 quantization의 full-integer 여부와 input-output tensor precision이 불명확하다.
5. Inference time 측정 횟수, warm-up, 평균 계산 방법이 미보고다.
6. Maximum, p95, p99 latency와 jitter가 없다.
7. Inference time에 normalization, FFT, segmentation이 포함되는지 불명확하다.
8. Table 4와 Figure 5 수치 불일치 (accuracy 91.4% vs 92%, latency 13 ms vs 15 ms).
9. W=256과 50% overlap의 물리적·신호처리적 선정 근거가 없다.
10. Dataset의 train/validation/test 분할 방식이 미기재다.
