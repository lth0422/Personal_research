# FRFconv-TDSNet: Lightweight, Noise-Robust Convolutional Neural Network Leveraging Full-Receptive-Field Convolution and Time-Domain Statistics for Intelligent Machine Fault Diagnosis

- **그룹**: 5 fault_diagnosis_app
- **출처/연도**: IEEE Transactions on Instrumentation and Measurement 2024
- **저자**: Seongjae Lee, Taehyoun Kim

## 두 질문
- **가변 변수**: model architecture, receptive field/kernel design, TDS integration. Window/input length는 evaluation에서 fixed 2048 data points.
- **트리거**: 없음=offline model design/evaluation. machine condition 또는 system slack 기반 runtime adaptation은 확인되지 않음.

## Abstract 3줄 요약
- noisy industrial environment와 resource-constrained edge device에서 real-time machine fault diagnosis가 어렵다는 문제를 다룬다.
- full-receptive-field convolution과 time-domain statistics를 결합한 lightweight CNN인 FRFconv-TDSNet을 제안한다.
- 평가에서는 noisy data accuracy와 edge inference time 측면에서 비교 모델 대비 우수성을 보였다고 보고한다.

## Conclusion 요약
- 결론은 FRF convolution이 전체 입력 범위의 global feature를 추출하고 TDS integration이 noisy data에서 오분류를 줄이는 역할을 한다고 설명한다. Raspberry Pi 4B에서 10k 미만 parameter와 5 ms 미만 inference time을 보고하지만, 본 연구 원고에서 수치를 쓸 때는 Figure 6 조건을 재확인해야 한다.

## 요점
- 플랫폼: Raspberry Pi 4B, PyTorch Mobile, XNNPACK backend.
- 도메인: vibration 기반 bearing/gear fault diagnosis under noisy environments.
- 핵심 방법: input length 전체를 덮는 full-receptive-field convolution과 mean, peak, RMS, crest factor TDS features를 결합한다. noise-free data로 학습하고 AWGN noisy test data에서 robustness를 평가한다.
- 정식화/수식: `y = softmax(W * [FRF(Pre(x)); TDS(x)] + b)`. TDS는 mean, peak, RMS, crest factor.

## 내 연구 관점
- 한 줄 gap: 본 연구의 KCC 모델 배경과 직접 연결되지만, runtime W/H/M selection이나 PREEMPT_RT 실시간성은 다루지 않는다.
- 내 연구에 쓸 곳: KCC 2026 모델 선택 근거, noise robustness와 edge inference 배경, model M 후보 설명.
- 인용할 문장: "less than 5 ms"

## 불확실한 점
- 확인 필요: Raspberry Pi 4B inference time은 Figure 6 기반이며, 정확한 average/max 수치는 figure에서 재확인해야 한다.
- 확인 필요: 본 repo의 KCC 결과인 STM32F407 + Zephyr + TFLite Micro 측정과 직접 비교할 때 platform/framework 차이를 명확히 구분해야 한다.
