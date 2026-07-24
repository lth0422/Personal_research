# Real-Time Fault Diagnosis Related-Work Table Draft

이 표는 `surveys/realtime_fault_diagnosis_survey_protocol.md`의 판정 규칙을 사용하는 원고용 초안이다. 현재 paper card 기준의 예비 판정이며, 원문 재검토 후 `?`와 `△`를 확정해야 한다.

2026-07-21 LINER·Claude 검색에서 수집한 신규 fault-diagnosis 후보 14편은 2026-07-24 full-text 판정을 완료해 아래에 추가했다. 최종 원고에는 직접성이 높은 5~8편만 남기고 나머지는 survey 근거로 유지한다.

## 기호

- O: 원문에서 확인
- △: 부분 충족 또는 간접 근거
- X: 해당 없음 확인
- ?: 확인 필요
- P: 제안 연구의 계획이며 아직 검증되지 않음

## 압축 비교표

| Work | Platform | Execution environment | RTOS | PREEMPT_RT | Deadline | Tail/miss | Sched. analysis | Model opt. | System scheduling | Runtime adapt. | Joint `W/H/M` | `q+S` | RT level |
| --- | --- | --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Ma et al., Architecture Search FD | Desktop CPU | Other OS | X | X | X | X | X | O | X | X | X | X | B |
| Lee and Kim, FRFconv-TDSNet | Raspberry Pi 4B | Linux, RT extension ? | X | X | X | X | X | O | X | X | X | X | B |
| Jalonen et al., Time-Varying Speed FD | Laptop SoC | Other OS | X | X | X | X | X | O | X | X | X | X | B |
| Thota et al., TinyML Bearing FD | MCU | Runtime ? | ? | X | X | ? | X | O | X | X | X | X | B |
| Choi et al., Low-Cost MCU Shaft FD | MCU | Bare metal | X | X | X | X | X | O | X | X | X | X | B |
| Zhang et al., Fast Short-Time Root-MUSIC | STM32H743 | FreeRTOS | O | X | X | X | X | O | X | X | X | X | B |
| Yang et al., Stacked AE End-Edge | STM32F407-class + edge | Runtime ? | ? | X | △ | X | X | O | △ | O | X | X | B |
| He et al., Cyclostationary Edge FD | STM32F407 | Runtime ? | ? | X | X | X | X | △ | X | X | X | X | B |
| Pubalan et al., Simulated 1D-CNN | Simulation | Other | X | X | X | X | X | O | X | X | X | X | B |
| Arciniegas et al., TinyML Motor Vibration | ESP32S3 | Runtime ? | ? | X | X | X | X | O | X | X | X | X | B |
| Gupta and Shivhare, TinyML ESP32 | ESP32 | Runtime ? | ? | X | X | X | X | O | X | X | X | X | B |
| Lima, Edge Impulse Motor FD | nRF52840 | Runtime ? | ? | X | X | X | X | O | X | X | X | X | B |
| Alasiry et al., Dual-MCU Monitoring | STM32F103 + ESP32 | Runtime ? | ? | X | X | X | X | X | △ | X | X | X | B |
| Zhan et al., APTL-net | Jetson Xavier NX | Linux | X | X | X | X | X | O | X | X | X | X | B |
| Garay et al., Multimodal TinyML | Cortex-M4F + gateway | Arduino Mbed OS | O | X | X | △ | X | O | X | X | X | X | B |
| Langarica et al., Industrial Internet FD | IIoT edge + server | Linux/server stack | X | X | X | X | X | X | X | △ | X | X | B |
| Shan et al., CS-DKELM | Zynq MPSoC | Linux | X | X | X | X | X | O | X | X | X | X | B |
| Sayghe, Physics-Aware Transformer | Raspberry Pi 4 | Linux | X | X | X | X | X | O | X | X | X | X | B |
| Bhaventhan et al., Vibration PdM | Raspberry Pi 4 | Linux ? | X | X | X | X | X | O | X | X | X | X | B |
| KCC 2026 system | MCU | Zephyr RTOS | O | X | O | O | △ | O | O | X | X | X | E |
| Proposed work | Pi Zero 2W | Linux + PREEMPT_RT | X | P | P | P | P | - | P | P | P* | P | Target H/conditional H |

`P*`: 초기 연구 범위는 joint `W/H`를 코어로 두고 `M`은 고정하거나 제한된 보조 변수로 두는 안을 우선 검토한다.

## RT Level

- H: explicit deadline과 보수적 execution-time bound에 기반한 schedulability/admission guarantee
- W: bounded deadline miss를 보장하는 weakly-hard 접근
- E: deadline과 tail/miss를 측정하지만 formal guarantee는 없음
- B: average latency, throughput 또는 acquisition interval 대비 처리시간 중심의 best-effort 접근

## Caption Draft

Comparison of real-time support in embedded machine fault-diagnosis studies. Model-level optimization is common in the currently reviewed studies, whereas explicit deadlines, system-level scheduling, and runtime adaptation are limited or absent. The proposed features remain targets pending implementation and schedulability validation.

## 작성 주의

- Proposed work의 `P`는 실험과 분석 완료 전까지 O로 바꾸지 않는다.
- “기존 연구에는 scheduling이 없다”가 아니라 “정의한 검색 범위와 판정 기준에서 확인한 direct RT-FD 문헌에는 제한적이었다”로 쓴다.
- RTOS, average latency 또는 observed max만으로 hard real-time을 주장하지 않는다.
- 최종 원고에는 직접 비교군 5~8편만 남기고, 경량화 대조군과 scheduling bridge를 본문에서 각각 설명한다.
- Platform tag는 우선순위가 아니라 external-validity 정보다. 직접성은 fault-diagnosis domain, runtime variable, trigger, deadline과 guarantee로 판단한다.
