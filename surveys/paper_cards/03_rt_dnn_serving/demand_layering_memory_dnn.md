# Demand Layering for Real-Time DNN Inference with Minimized Memory Usage

- **그룹**: 3 rt_dnn_serving
- **출처/연도**: RTSS 2022
- **저자**: Mingoo Ji, Saehanseul Yi, Changjin Koo, Sol Ahn, Dongjoo Seo, Nikil Dutt, Jong-Chan Kim

## 두 질문
- **가변 변수**: layer loading/pipeline architecture, circular buffer size, memory-delay trade-off.
- **트리거**: 없음=system design/optimization. Runtime slack 또는 machine condition trigger는 확인되지 않음.

## 요점
- 플랫폼: Nvidia Jetson AGX Xavier, integrated GPU, NVMe SSD.
- 도메인: real-time DNN inference memory optimization on embedded GPU systems.
- 핵심 방법: 전체 model parameter를 미리 memory에 올리는 대신, layer 단위로 SSD에서 읽고 실행한 뒤 이전 layer parameter를 버린다. read/copy/kernel을 pipeline화해 memory 절감에 따른 delay overhead를 숨긴다.
- 정식화/수식: DNN inference delay를 read, copy, kernel operation으로 나누고, pipeline architecture와 buffer size로 memory-delay trade-off를 조절한다.

## 내 연구 관점
- 한 줄 gap: embedded DNN의 memory-delay trade-off를 다루지만 vibration FD, W/H/M runtime adaptation, PREEMPT_RT는 다루지 않는다.
- 내 연구에 쓸 곳: Pi Zero 2W 또는 SBC에서 memory/resource constraint를 논할 때 DNN inference memory 측면 비교군.
- 인용할 문장: "memory-delay tradeoff"

## 불확실한 점
- 확인 필요: 96.5% memory reduction, 14.8% average delay overhead, near-zero overhead 수치는 representative DNN과 pipeline configuration 조건을 Section V에서 재확인해야 한다.
- 확인 필요: Jetson AGX Xavier + GPU/SSD architecture이므로 MCU 또는 Pi Zero 2W CPU inference와 직접 비교하면 안 된다.
