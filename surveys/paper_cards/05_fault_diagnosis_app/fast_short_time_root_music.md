# A Novel Fast Short-Time Root-MUSIC Method for Vibration Monitoring of High-Speed Spindles

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S1 embedded real-time fault diagnosis, S2 adaptive diagnostic fidelity
- **플랫폼 태그**: `PL-MCU`
- **실행환경 태그**: `ENV-RTOS`
- **출처/연도**: arXiv:2506.17600, 2025
- **저자**: Huiguang Zhang, Baoguo Liu, Wei Feng, Zongtang Li

## 두 질문
- **가변 변수**: 분석 중 선택되는 frequency point/model order 수. 입력 frame은 16 ms로 고정된다.
- **트리거**: signal subspace의 singular-value 구조에 따른 algorithm-internal selection이며, system slack이나 machine condition에 따른 runtime mode 전환은 아니다.

## Abstract 3줄 요약
- High-speed spindle의 짧은 관측 시간과 높은 frequency resolution 요구를 함께 만족시키는 문제를 다룬다.
- FFT-accelerated Lanczos bidiagonalization과 Root-MUSIC을 결합한 fSTrM을 제안한다.
- Politecnico di Torino dataset과 STM32H743/FreeRTOS 구현에서 micro-defect 검출 및 millisecond processing을 보고한다.

## Conclusion 요약
- 16 ms frame에서 high-resolution fault-frequency 추출이 가능하다고 결론짓지만, 여러 fault와 variable load 검증은 후속 과제로 남긴다.

## 요점
- 플랫폼: STM32H743 Cortex-M7 600 MHz, FreeRTOS 10.4.3, CMSIS-DSP 1.10.0.
- 도메인: ultra-high-speed spindle bearing vibration monitoring.
- 핵심 방법 (2~3줄): Hankel matrix의 subspace decomposition을 FFT와 Lanczos로 가속하고 unit-circle polynomial rooting으로 fault frequency를 추출한다. 51.2 kHz vibration data와 16 ms frame을 사용한다.
- 정식화/수식 (있으면): complexity를 `O(N^3)`에서 `SN log2 N + S^2(N+S) + M^2(N+M)`으로 줄인다고 제시한다.

## 0708 면담 기준 보강
- **실시간성 수준**: FreeRTOS 실제 MCU에서 mean processing time을 측정했으나 deadline, jitter, max, miss는 없다. best-effort 근실시간 `B`.
- **실행시간 가정**: signal-dependent frequency-point 수에 따라 변할 수 있으나 WCET/profile model은 없다.
- **보장 방식**: 평균 실행시간과 frame duration 비교만 있고 schedulability 보장은 없다. 근거: Sections 4.1.2, 5.2.2, 6.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): `W/H/M` mode selection과 system slack 기반 admission은 없으며 fixed 16 ms frame을 사용한다.
- 내 연구에 쓸 곳: 짧은 `W`에서도 physics-based frequency resolution을 유지하려는 S1/S2 비교군.
- 인용할 문장 (있으면, 15단어 이내): "16 ms signal frames"

## 불확실한 점
- 확인 필요: abstract의 2.4 ms와 본문/결론의 2.8 ms가 불일치한다.
- 확인 필요: 결론의 12.8 MB memory footprint는 본문의 1 MB SRAM 사양과 양립하기 어려워 원고 수치로 사용하지 않는다.
