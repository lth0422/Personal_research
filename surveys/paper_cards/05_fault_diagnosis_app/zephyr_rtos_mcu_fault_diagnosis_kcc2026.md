# Zephyr RTOS 기반 MCU에서의 실시간 기계 결함 진단 추론 성능 분석

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S1 Embedded Real-Time Fault Diagnosis
- **플랫폼 태그**: `PL-MCU`
- **실행환경 태그**: `ENV-RTOS`
- **출처/연도**: KCC 2026. 정식 proceedings metadata 확인 필요.
- **저자**: 이태훈, 박신형, 김태현
- **문서 역할**: 본인 선행연구. 외부 related-work 부재를 주장하는 근거로 집계하지 않는다.

## 두 질문
- **가변 변수**: Offline 실험 조건으로 inference kernel configuration과 input window size `W`를 변경한다. Runtime variable은 없다.
- **트리거**: 없음. Reference/CMSIS-NN kernel과 `W=2048/1024/512`를 사전에 정한 단계별 실험이다.

## Abstract 3줄 요약
- MCU에 배포한 fault-diagnosis DNN의 response time과 jitter가 deadline을 만족하는지 Zephyr RTOS 환경에서 평가한다.
- STM32F407에서 TFLite Micro, CMSIS-NN kernel과 window-size reduction을 단계적으로 적용한다.
- `W=512`에서 평균 inference response time 40.3 ms, deadline 64 ms와 accuracy 99.3%를 보고한다.

## Conclusion 요약
- CMSIS-NN과 window reduction을 결합해 제한된 MCU에서 명시한 deadline을 만족하는 inference condition을 확인한다. 실제 sensor acquisition, multi-task environment와 Raspberry Pi급 상위 platform 확장을 future work로 제시한다.

## 요점
- 플랫폼: STM32F407 Discovery, 168 MHz Cortex-M4, Zephyr v4.3, TFLite Micro, CMSIS-NN.
- 도메인: 8-class rotating-machine shaft fault diagnosis, UOS dataset, 8 kHz and 1400 RPM condition.
- 핵심 방법 (2~3줄): Rx, Inference와 Tx의 세 task pipeline을 구성한다. Reference kernel에서 CMSIS-NN으로 전환한 뒤 input window를 2048에서 512까지 줄이며 inference response time, jitter, deadline satisfaction과 accuracy를 비교한다.
- 정식화/수식 (있으면): Non-overlap을 가정해 `D=W/f_s`로 정의한다. 실험별 평균 response time은 1225.2, 460.3, 129.8, 40.3 ms이고 최종 `W=512` deadline은 64 ms다.

## 0708 면담 기준 보강
- **실시간성 수준**: Zephyr RTOS, explicit deadline, response-time standard deviation과 peak-to-peak jitter, condition별 deadline satisfaction을 제시한다. Deadline-miss ratio, p99/max와 schedulability analysis는 없다.
- **실행시간 가정**: 반복 측정 평균과 jitter를 보고하며 formal WCET 또는 conservative bound를 사용하지 않는다.
- **보장 방식**: `W=512` 조건의 empirical deadline satisfaction. 단일 inference task 중심이며 multi-task schedulability guarantee는 아니다.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): `W`를 offline에서 고정하며 `H/M`, machine condition, system slack과 runtime mode selection을 다루지 않는다.
- 내 연구에 쓸 곳: `W` 변화가 `C`와 deadline satisfaction을 바꾸는 본인 선행 motivation. Pi Zero 2W에서는 platform/runtime이 다르므로 모든 mode를 다시 profile해야 한다.
- 인용할 문장 (있으면, 15단어 이내): 해당 없음.

## 불확실한 점
- 확인 필요: KCC 2026 proceedings의 정식 학회명, 권·호·페이지를 확정한다.
- 확인 필요: 논문 본문에는 anomaly score 또는 runtime anomaly detector가 제시되지 않는다. 후속 연구의 `q`를 이 논문에서 이미 검증한 것처럼 쓰지 않는다.
- 확인 필요: 40.3 ms는 평균 response time이며 max 또는 WCET로 쓰지 않는다.
