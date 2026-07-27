# Real-Time Bearing Fault Detection and Visualization Using 1D CNN: A Simulated Deployment with the CWRU Dataset

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S3 (경량화 대조군), S5 (W 결정 방식 참고)
- **플랫폼 태그**: `PL-DESKTOP`
- **실행환경 태그**: `ENV-OTHER` (MATLAB App Designer; OS·CPU·MATLAB version 미보고)
- **출처/연도**: IEEE ICSIMA 2025, DOI 10.1109/ICSIMA66552.2025.11233248
- **저자**: Barathan Pubalan, Mohd Syahril Ramadhan Mohd Saufi, Mohd Salman Leong, Annisa Jamali
- **분석 MD**: `papers/05_fault_diagnosis_app/reviews/Pubalan_2025_ICSIMA_Simulated_RT_FDD_분석.md`

---

## 두 질문

- **가변 변수**: 없음. W=1602, f_s=48 kHz, M(1D CNN) 전부 고정. H 미정의. Cross-load few-shot adaptation은 offline fine-tuning이며 runtime mode 변경이 아니다.
- **트리거**: 없음. Runtime mode selection 없음. Unseen load의 정확도 저하를 사후 확인한 뒤 offline adaptation하는 구조다.

---

## 초록 번역

본 논문은 연속 진동 데이터 처리, 저지연 결함 분류, GUI 기반 시각화를 통합한 bearing fault detection framework를 제안한다. CWRU 데이터를 실시간처럼 순차 재생한 실험에서 1D CNN은 prediction당 0.03 s의 가장 짧은 latency를 보였으며, 다른 부하 조건에서는 few-shot transfer learning으로 정확도를 회복하였다. 다만 실제 산업 장치에 배포한 결과가 아니라 PC 환경에서 수행한 simulated real-time validation이다.

---

## 논문 흐름 + Novelty

### 논리 흐름

1. 기존 bearing fault diagnosis 연구가 acquisition, inference, visualization, cross-load generalization을 하나로 통합하지 못한다는 한계를 제기한다.
2. Offline phase에서 CWRU 데이터를 segmentation·preprocessing·학습하고, simulated real-time phase에서 저장된 segment를 순차 재생해 1D CNN prediction과 MATLAB GUI 시각화를 수행한다.
3. 1D CNN 입력 W를 shaft one-revolution 기준으로 설계한다.

$$W = \frac{60 f_s}{\mathrm{RPM}} = \frac{60 \times 48{,}000}{1797} \approx 1602 \text{ samples}$$

4. 1D CNN, 2D CNN-STFT, 2D CNN-CWT, SVM, RF를 accuracy와 per-prediction latency로 비교한다.
5. 0 HP 학습 모델을 1–3 HP에 zero-shot 평가하고, class당 20개 sample의 few-shot transfer learning으로 성능을 회복한다.

### "Simulated Deployment" 확인

실제 MCU·SBC·embedded GPU에 모델을 올린 것이 아니다. 저장된 CWRU segment를 MATLAB App Designer에서 순차 입력한 소프트웨어 replay다. Figure 5 GUI의 DAQ 설정 항목은 표시되나 성능 검증은 모두 CWRU replay로 수행된다. Future work에 "live hardware-in-the-loop testing"이 명시되어 있어 현재 실험에 실제 sensor 배포가 없었음을 확인할 수 있다.

### Novelty

신규 convolution 연산·손실 함수·압축 알고리즘 제안이 아닌 **simulated system integration과 cross-load validation contribution**이다.

- CWRU replay를 이용한 per-model prediction latency 비교
- Data-processing pipeline, 1D CNN inference, MATLAB GUI visualization, prediction confidence aggregation을 하나의 RT-FDD framework로 구성
- 0 HP → 1–3 HP의 few-shot transfer learning 성능 비교

### 개인연구 관점: W 결정 방식

이 논문의 $W$는 임의 sample 수가 아니라 **회전속도라는 machine condition을 물리적 입력 길이로 변환한 결과**다. 수식 자체는 $W(\mathrm{RPM}) = 60 f_s / \mathrm{RPM}$으로 RPM이 달라지면 $W$도 달라지나, 논문이 runtime에 RPM을 감지해 $W$를 자동 재설정하는 구조는 확인되지 않는다. 이 point는 개인연구에서 "기계 상태 q → W 결정"의 선행 근거로 인용 가능하다.

---

## RT 등급: B (확정)

| 판정 항목 | 결과 | 원문 근거 |
|---|---|---|
| 명시적 deadline | X | 선언 없음 |
| RTOS 또는 PREEMPT_RT | X | PC MATLAB simulation |
| Deadline miss / p99 / max | X | 미측정 |
| 평균 추론 latency | △ | 0.03 s per prediction 보고; 측정 hardware·횟수 미기재 |
| 주기적 trigger·acquisition period | △ | T_W=33.375 ms 계산 가능; H 미정의 |
| W/H/M runtime 변경 | X | 없음 |

### Deadline 판정: △

f_s=48 kHz, W=1602 → T_W≈33.375 ms. Shaft one-revolution period(≈33.39 ms)와 거의 일치하는 물리 기반 window duration이 존재한다. 그러나 논문은 이를 deadline으로 선언하지 않고, H를 정의하지 않으며, miss·max·p99를 측정하지 않는다. 또한 30 ms inference < T_W 33.375 ms이지만 이는 사후 계산이며 논문이 one-revolution 내 completion을 검증하지 않는다.

---

## 핵심 수치

| 지표 | 값 |
|---|---|
| 플랫폼 | PC (CPU·GPU·RAM 사양 미보고); 실 embedded target 없음 |
| 실행 환경 | MATLAB App Designer; OS·version 미보고 |
| W | 1602 samples (one revolution, 1797 rpm, 48 kHz) |
| H | 미정의 (overlap·stride 없음) |
| f_s | 48 kHz |
| T_W | 약 33.375 ms |
| T_H | 계산 불가 |
| 1D CNN prediction latency | 0.03 s = 30 ms |
| 2D CNN-STFT latency | 0.13 s |
| 2D CNN-CWT latency | 2.44 s |
| SVM / RF latency | 약 0.07 s |
| 1D CNN accuracy (0 HP, 5-run) | 97.37% mean, ±0.56 SD |
| 파라미터 수 / FLOPs / 모델 크기 | 미보고 |

**0.03 s의 의미:** pre-segmented input 하나를 모델에 전달해 prediction 하나를 얻는 시간이다. H, diagnosis period, acquisition period, E2E latency, explicit deadline이 아니다.

### RPM에 따른 W 변화 (설계 원리)

| 부하 | RPM | 계산된 one-revolution W |
|---:|---:|---:|
| 0 HP | 1797 | 약 1602 samples |
| 1 HP | 1772 | 약 1625 samples |
| 2 HP | 1750 | 약 1646 samples |
| 3 HP | 1730 | 약 1665 samples |

원문은 cross-load 실험에서 각 RPM에 맞춰 W를 재계산했는지 명확히 설명하지 않는다.

---

## 세 문장 압축

Pubalan et al.은 shaft one-revolution segment와 1D CNN을 이용하고 MATLAB GUI에서 CWRU 데이터를 순차 재생하는 simulated RT-FDD framework를 제안한다. 0 HP에서 1D CNN은 97.37% mean accuracy와 0.03 s per-prediction latency를 보였으며, unseen load 성능 저하는 class당 20개 sample의 few-shot transfer learning으로 회복하였다. 그러나 실제 embedded deployment, H, explicit deadline, p99, deadline miss, q+S 기반 runtime mode selection은 다루지 않는다.

## Related Work 영어 한 줄

> Pubalan et al. derived a physics-based one-revolution input length from shaft speed and demonstrated a 30-ms 1D-CNN prediction pipeline through sequential CWRU replay, but did not validate deadline-aware operation on real edge hardware or adapt W/H/M at runtime according to machine condition and system slack.

---

## 불확실한 점

1. Simulated replay를 수행한 PC의 CPU·GPU·RAM 사양 미보고
2. OS와 MATLAB version 미보고
3. 0.03 s latency의 측정 횟수·minimum·maximum·SD 미보고
4. 0.03 s에 preprocessing과 GUI update가 포함되는지 여부
5. H·stride·overlap·segment arrival cadence 미정의
6. Cross-load 조건에서 RPM별 W를 runtime에 재계산했는지 여부
7. Parameter count·FLOPs·model file size·memory usage 미보고
8. Convolution kernel size·stride·padding·dropout rate 등 CNN 세부 구조 미보고
9. "Each incoming data point immediately" 설명과 1602-sample segment inference 사이의 관계
10. 30 ms inference < T_W 33.375 ms이나 논문이 이를 deadline 충족으로 해석하지 않음
11. Confidence aggregation의 monitoring duration과 prediction count 실험별 동일 여부
