# Real-Time Fault Diagnosis Related-Work Table Draft

이 표는 `surveys/realtime_fault_diagnosis_survey_protocol.md`의 판정 규칙을 사용하는 원고용 초안이다. 현재 paper card 기준의 예비 판정이며, 원문 재검토 후 `?`와 `△`를 확정해야 한다.

## 기호

- O: 원문에서 확인
- △: 부분 충족 또는 간접 근거
- X: 해당 없음 확인
- ?: 확인 필요
- P: 제안 연구의 계획이며 아직 검증되지 않음

## 압축 비교표

| Work | RTOS | Explicit deadline | Tail/jitter/miss | Sched. analysis | Model optimization | System-level scheduling | Runtime adaptation | Joint `W/H/M` | Trigger `q+S` | RT level |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Ma et al., Lightweight Architecture Search FD | X | X | X | X | O | X | X | X | X | B |
| Lee and Kim, FRFconv-TDSNet | X | X | X | X | O | X | X | X | X | B |
| Jalonen et al., Time-Varying Speed FD | X | X | X | X | O | X | X | X | X | B |
| Thota et al., TinyML Bearing FD | ? | X | ? | X | O | X | X | X | X | B |
| Choi et al., Low-Cost MCU Shaft FD | X | X | X | X | O | X | X | X | X | B |
| KCC 2026 system | O | O | O | △ | O | O | X | X | X | E |
| Proposed work | P | P | P | P | - | P | P | P* | P | Target H or conditional H |

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
