# 저비용 마이크로컨트롤러 환경에서의 경량 딥러닝 기반 회전기계 축 결함 진단 시스템

- **그룹**: 5 fault_diagnosis_app
- **출처/연도**: 2025 한국소프트웨어종합학술대회 논문집
- **저자**: 최성현, 김서랑, 김태현

## 두 질문
- **가변 변수**: 없음. FRFconv-TDSNet 기반 fixed model, fixed input length를 사용한다.
- **트리거**: 없음=offline model training/deployment. machine condition 또는 system slack 기반 runtime adaptation은 확인되지 않음.

## 요점
- 플랫폼: STM32F401RET6, STM32 Nucleo-64, X-CUBE-AI, USB digital accelerometer, LCD panel.
- 도메인: 회전기계 축 결함 진단. Healthy, looseness, misalignment, unbalance 8-class.
- 핵심 방법: 1400 RPM 조건에서 클래스별 3000개 vibration sample을 수집하고, FRFconv-TDSNet을 STM32 MCU에 배포해 sensing, inference, LCD output을 통합한다.
- 정식화/수식: 8-class classification. 각 sample은 2048 data point, sampling frequency는 16 kHz.

## 내 연구 관점
- 한 줄 gap: MCU에서 end-to-end fault diagnosis system을 구현했지만 RTOS task scheduling, deadline miss, jitter, PREEMPT_RT 비교, W/H/M runtime adaptation은 아직 다루지 않는다.
- 내 연구에 쓸 곳: KCC/KSC 연구 흐름의 직전 선행 시스템, MCU baseline, RTOS 적용 필요성의 배경.
- 인용할 문장: "약 0.8초 이내"

## 불확실한 점
- 확인 필요: sensing 151.205 ms, inference 555.872 ms, output 56.158 ms의 합과 abstract의 약 0.8초 표현은 일관되지만, deadline이나 주기 조건은 명시되지 않았다.
- 확인 필요: 이 논문은 future work로 RTOS task화와 real-time scheduling을 언급하므로, KCC 2026/Zephyr 결과와 연결할 때 선후 관계와 플랫폼 차이를 구분해야 한다.
