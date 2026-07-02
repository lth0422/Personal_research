# TinyML Enabled Real-Time Bearing Fault Classification in Motors Using Vibration Signals

- **그룹**: 5 fault_diagnosis_app
- **출처/연도**: GLSVLSI 2025
- **저자**: Yogeswar Reddy Thota, Mojtaba Afshar, Samantha Boden, Brendan Dunlap, Bilal Akin, Tooraj Nikoubin

## 두 질문
- **가변 변수**: model/input representation, fixed window size. DNN with engineered features와 raw-signal 1D-CNN을 비교하며, window는 runtime variable이 아니라 고정 설계값이다.
- **트리거**: 없음=offline model/design selection. machine condition이나 system slack 기반 runtime adaptation은 확인되지 않음.

## 요점
- 플랫폼: Espressif ESP-EYE 또는 ESP32 계열 microcontroller, Edge Impulse for Microcontrollers.
- 도메인: triaxial vibration 기반 motor bearing distributed fault classification.
- 핵심 방법: Afshar et al. dataset의 3000 RPM 조건에서 0%~100% load와 6개 bearing condition을 사용한다. engineered feature DNN과 raw 1D-CNN을 비교하고, raw x/y/z vibration 7500-point sample 기반 1D-CNN을 TinyML로 배포한다.
- 정식화/수식: fixed windowing. 각 segment는 10000 data point로 설명되며, raw-signal 1D-CNN 입력은 7500-point triaxial sample로 설명됨.

## 내 연구 관점
- 한 줄 gap: TinyML fault diagnosis 실시간 배포 사례이지만 W/H/M runtime selection, system slack, PREEMPT_RT 비교는 다루지 않는다.
- 내 연구에 쓸 곳: MCU/edge fault diagnosis related work, raw vibration 기반 embedded inference 비교군, KCC/KSC 배경.
- 인용할 문장: "TinyML for real-time classification"

## 불확실한 점
- 확인 필요: Table 2는 unoptimized float32 latency 30 ms, quantized int8 latency 265 ms로 보이나 abstract/results 문장은 30 ms와 69.7 KB flash를 함께 언급한다. manuscript에서 latency를 인용하기 전 Table 2와 model type을 구분해야 한다.
- 확인 필요: 10000 data point segment와 7500-point raw triaxial sample의 관계를 method section 기준으로 재확인해야 한다.
