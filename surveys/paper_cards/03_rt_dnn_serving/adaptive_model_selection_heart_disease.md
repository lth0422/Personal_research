# Adaptive Model Selection for Real-Time Heart Disease Detection on Embedded Systems

- **그룹**: 3 rt_dnn_serving
- **출처/연도**: 2025 IEEE 31st International Conference on Embedded and Real-Time Computing Systems and Applications (RTCSA), DOI 10.1109/RTCSA66114.2025.00028
- **저자**: Yixin Li, Zhiling Li, Abdullah Al Arafat, Donald Johnson, Ning Sui, Anil Gehi, Zhishan Guo

## 두 질문
- **가변 변수**: model complexity/depth. Advanced, Moderate, Lightweight CNN variant 또는 parameter-shared anytime model의 exit path를 선택한다.
- **트리거**: instantaneous heart rate `HR`와 그에 따른 deadline `D(HR)`. 논문 알고리즘은 `HR >= 90`, `70 <= HR < 90`, `HR < 70` threshold로 model을 선택한다.

## Abstract 3줄 요약
- wearable embedded device에서 real-time cardiovascular disease detection은 heart rate 변화와 제한된 계산 자원 때문에 accuracy와 latency를 동시에 만족시키기 어렵다.
- AMS는 real-time heart rate에 따라 CNN model complexity를 동적으로 선택하고, anytime CNN은 residual block, squeeze-and-excitation, global attention을 결합한다.
- PhysioNet database와 Raspberry Pi 4 평가에서 91.5% accuracy와 평균 1.33 ms inference latency per sample을 보고한다.

## Conclusion 요약
- 논문은 heart rate에 따라 processing deadline이 달라지는 ECG monitoring에서 adaptive model selection이 accuracy와 real-time feasibility를 함께 개선한다고 정리한다. Discussion 기준 AMS+Anytime은 parameter sharing으로 memory overhead를 줄이고, high-HR 상황에서는 lightweight path를 사용해 deadline miss를 피하며, lower-HR 상황에서는 deeper path를 사용한다.

## 요점
- 플랫폼: Raspberry Pi 4. 논문은 wearable device와 hardware similarity를 motivation으로 설명한다.
- 도메인: real-time ECG anomaly detection, cardiovascular disease detection, wearable embedded systems.
- 핵심 방법 (2~3줄): ECG segment와 instantaneous HR를 입력으로 받아 HR가 높으면 lightweight model, 중간이면 moderate model, 낮으면 advanced model을 선택한다. Parameter-shared anytime CNN을 사용해 세 model checkpoint를 따로 올리지 않고 exit path를 선택한다. Watchdog 기반 fallback은 deadline 초과 시 shallower model 재실행 또는 timing anomaly flag를 제안한다.
- 정식화/수식 (있으면): `arg max A(M_i)` subject to `T_proc(M_i) <= D(HR)`, `M_i in {M_Adv, M_Mod, M_LW}`. ECG task utilization은 `U(E_i) = C_i(HR) / D_i(HR)`로 표현된다.

## 0708 면담 기준 보강
- **실시간성 수준**: HR-dependent deadline, EDF schedulability model, deadline miss를 다룬다. RTOS/PREEMPT_RT 실험은 확인되지 않았다.
- **실행시간 가정**: model variant 또는 anytime exit path에 따라 `C(M)`이 달라지는 mode-dependent execution time 구조다.
- **보장 방식**: `T_proc(M_i) <= D(HR)` 제약, `U(E_i)=C_i(HR)/D_i(HR)`, shallower model fallback/watchdog를 사용한다. 다만 본 연구의 vibration `C(W,M)`와는 domain과 trigger가 다르다.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): physiological condition인 heart rate와 model selection은 다루지만, vibration fault diagnosis의 window size `W`, hop/diagnosis period `H`, machine anomaly score, PREEMPT_RT kernel timing은 다루지 않는다.
- 내 연구에 쓸 곳: `M` selection을 runtime condition과 deadline function에 연결하는 강한 비교군. 본 연구의 `(machine condition, system slack) -> (W,H,M)` 정책에서 `M` 축을 설명할 때 활용 가능하다.
- 인용할 문장 (있으면, 15단어 이내): "Adaptive Model Selection"

## 불확실한 점
- 확인 필요: 91.5% accuracy, 1.33 ms average latency, zero deadline miss 수치는 PhysioNet 2021, Raspberry Pi 4, two-cycle AMS/Anytime 조건과 연결되어 있으므로 원고 인용 전 Table II/III 및 실험 설정을 재확인해야 한다.
- 확인 필요: heart rate threshold 70/90 bpm은 training distribution percentile 기반이며, vibration anomaly score threshold와 동일한 의미로 쓰면 안 된다.
- 확인 필요: 논문은 Raspberry Pi 4 기반이며 Pi Zero 2W 또는 PREEMPT_RT 실험은 아니다.
