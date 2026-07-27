# TinyML Enabled Real-Time Bearing Fault Classification in Motors Using Vibration Signals

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S3 (경량화 대조군)
- **플랫폼 태그**: `PL-MCU`
- **실행환경 태그**: `ENV-OTHER` (Edge Impulse firmware; OS·RTOS·runtime 미보고)
- **출처/연도**: ACM/IEEE GLSVLSI 2025, DOI 10.1145/3716368.3735272
- **저자**: Yogeswar Reddy Thota, Mojtaba Afshar, Samantha Boden, Brendan Dunlap, Bilal Akin, Tooraj Nikoubin
- **분석 MD**: `papers/05_fault_diagnosis_app/reviews/Thota_2025_GLSVLSI_TinyML_분석.md`

---

## 두 질문

- **가변 변수**: 없음(runtime). W·H·M 전부 고정. FP32 vs. INT8 비교는 offline 설계 선택이며 runtime mode selection이 아니다.
- **트리거**: 없음. Machine condition·system slack 기반 runtime adaptation 없음.

---

## 초록 번역

본 논문은 불규칙하고 비정상적인 진동을 발생시키는 distributed bearing fault를 분류하기 위해 raw 3축 vibration을 직접 입력하는 lightweight 1D CNN TinyML framework를 제안한다. 3000 RPM과 다섯 부하 조건에서 healthy·lubrication failure·contamination·flaking·electrical erosion·composite fault 여섯 상태를 분류하며, 1D CNN이 feature-engineered DNN보다 높은 accuracy를 보였다고 보고한다. Edge Impulse를 통해 ESP32 계열 MCU에 배포한 결과를 제시하지만, latency와 memory 수치는 Table 2와 본문 사이에서 서로 모순된다.

---

## 논문 흐름 + Novelty

### 논리 흐름

1. Handcrafted feature 기반 DNN이 domain expertise에 의존하고 operating condition 변화에 취약하다는 문제를 제기한다. Distributed fault는 localized defect보다 irregular·nonstationary vibration을 만들어 feature engineering이 더 어렵다.
2. Feature-engineered DNN과 raw triaxial 1D CNN을 비교한다. 센서는 ADXL354C MEMS triaxial accelerometer, dataset은 Afshar et al.의 distributed bearing fault dataset이다.
3. Edge Impulse로 FP32·INT8 두 variant를 ESP-EYE에 배포하고 accuracy·latency·RAM·Flash를 측정한다.

### Novelty

새로운 VLSI accelerator나 custom datapath가 아닌 **MCU-targeted TinyML deployment study**에 가깝다.

- Raw triaxial vibration 직접 입력 compact 1D CNN이 feature DNN보다 정확하고 MCU footprint가 작음을 실증
- DNN Flash 25 MB는 MCU 배포 불가능하고 compact 1D CNN 43–70 KB는 가능함을 보여줌

단, energy·clock cycle·memory bandwidth는 측정하지 않아 GLSVLSI의 hardware efficiency 관점에서의 contribution은 제한적이다. Motor 실장 live deployment는 future work로 남겼다.

---

## RT 등급: B (확정)

| 판정 항목 | 결과 | 원문 근거 |
|---|---|---|
| 명시적 deadline | X | 선언 없음 |
| RTOS 또는 PREEMPT_RT | X | OS·RTOS 미보고 |
| Deadline miss / p99 / max | X | 미측정 |
| 평균 inference latency | △ | Table 2에 수치 있으나 본문과 모순 (아래 참조) |
| Hop period H 또는 acquisition period | X | f_s 미보고 → T_W 계산 불가 |
| W/H/M runtime 변경 | X | 없음 |

### Deadline 판정: X

f_s가 없어 T_W를 계산할 수 없다. Acquisition period 자체를 알 수 없으므로 time reference가 없다. Deadline은 X.

---

## 핵심 수치

| 지표 | 값 |
|---|---|
| 플랫폼 | Espressif ESP-EYE, ESP32 계열; clock·RAM·Flash 사양 미보고 |
| 실행 환경 | Edge Impulse firmware; OS·RTOS·bare-metal 여부·runtime 미보고 |
| 센서 | ADXL354C triaxial MEMS accelerometer |
| 고장 유형 | Distributed bearing fault 6-class (Healthy/Lubrication/Contamination/Flaking/Erosion/Composite) |
| f_s | 미보고 |
| W | 10000 samples (Section 3.1) 또는 7500 samples (1D CNN input) — 모순 |
| T_W | 계산 불가 |
| H | "minimal overlap"만 기재, 정확한 hop 미보고 |
| 모델 | 3-layer 1D CNN (Conv 16f-k5 → Conv 8f-k3 → Conv 8f-k3) + Dense 32–16 + Softmax 6 |
| Quantization | INT8 (PTQ·QAT 구분 미기재) |
| 파라미터 수·FLOPs | 미보고 |
| Energy / power / clock cycle | 미보고 |

### 모델 variant 비교 (Table 2 기준)

| Variant | Accuracy | Latency | Total RAM | Flash |
|---|---:|---:|---:|---:|
| 1D CNN FP32 | 99.26% | **30 ms** | **29.3 KB** | 43.3 KB |
| 1D CNN INT8 | 99.36% | **265 ms** | **61.2 KB** | 69.7 KB |

**Table 2 vs. 본문 모순**: Abstract·Section 4는 INT8에 "30 ms, 29.3 KB RAM"을 귀속하지만, 이 값은 Table 2의 FP32 행 수치다. INT8이 FP32보다 느리고 큰 이유도 설명되지 않는다. 원문만으로 INT8의 정확한 latency·RAM을 신뢰성 있게 확정하기 어렵다.

| DNN 비교 | Accuracy | Latency | Flash |
|---|---|---|---|
| Feature DNN (학습) | 85%–98% (위치별 모순) | 미보고 | 미보고 |
| Feature DNN INT8 배포 | 68.01% | 1212 ms | 25.0 MB |

DNN은 25 MB Flash로 MCU 배포 불가능하고, accuracy도 68%로 크게 저하됐다.

---

## 세 문장 압축

Thota et al.은 distributed bearing fault 여섯 상태를 raw triaxial vibration으로 분류하는 compact 1D CNN을 제안하고 Edge Impulse를 통해 ESP-EYE에 배포한다. Table 2는 FP32 30 ms·29.3 KB와 INT8 265 ms·61.2 KB를 보고하지만 본문은 INT8에 30 ms와 29.3 KB를 귀속해 수치 일관성이 없다. f_s·H·explicit deadline·tail latency·energy와 q+S 기반 runtime mode adaptation은 다루지 않는다.

## Related Work 영어 한 줄

> Thota et al. deployed a compact raw-signal 1D CNN for six-class distributed bearing-fault diagnosis on an ESP32-class device via Edge Impulse, but did not define the sensing period or deadline and reported internally inconsistent latency and memory figures for the quantized model.

---

## 불확실한 점

1. ESP-EYE 정확한 chip revision과 clock 미보고
2. OS·FreeRTOS·bare-metal 여부 미보고
3. Edge Impulse 내부 runtime이 TFLite Micro인지 EON Compiler 기반인지 미보고
4. INT8 PTQ·QAT 구분 미기재
5. f_s 미보고 → T_W 계산 불가
6. W=10000(Section 3.1)과 raw 1D CNN input 7500의 관계 불명확
7. H·exact overlap·stride 미보고
8. INT8 latency가 265 ms(Table 2)인지 30 ms(본문)인지 모순 미해결
9. INT8 RAM이 FP32보다 증가한 이유 미설명
10. Latency 측정 횟수·mean·SD·max·p99 미보고
11. Energy·power·mJ per inference 미보고
12. 1D CNN parameter 수·MACs 미보고
13. DNN accuracy가 98%·85%·68.01%로 세 곳에서 다르게 제시된 이유
14. Live motor-mounted sensing-to-classification end-to-end 시스템 미구현
15. Dataset split이 recording 단위인지 overlapping segment 단위인지 미기재
