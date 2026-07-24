# Vibration-Based Predictive Maintenance for Motors Using Edge AI

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S1 embedded real-time fault diagnosis
- **플랫폼 태그**: `PL-SBC-SOC`
- **실행환경 태그**: `ENV-LINUX`
- **출처/연도**: IEEE RAEEUCCI 2026, DOI 10.1109/RAEEUCCI67649.2026.11504862
- **저자**: Bhaventhan R, Daniel Stanlyraj X, S. Purushothaman

## 두 질문
- **가변 변수**: runtime adaptation 변수 없음. Fixed 1D CNN을 사용한다.
- **트리거**: Softmax classification 결과가 motor condition을 결정하며 mode-switch trigger는 없다.

## Abstract 3줄 요약
- Raspberry Pi 4와 ADXL345로 BLDC motor vibration을 local 분류하는 predictive-maintenance system을 제안한다.
- 1D CNN으로 normal, imbalance, misalignment와 bearing wear를 분류한다.
- Three speeds의 custom experiment에서 multi-class feasibility를 보고한다.

## Conclusion 요약
- Edge 1D CNN이 low-severity motor fault의 local monitoring에 적용 가능하다고 주장하며, 더 큰 dataset과 load 조건 검증을 future work로 둔다.

## 요점
- 플랫폼: Raspberry Pi 4 Model B, ADXL345, OLED; OS/runtime 세부는 없다.
- 도메인: BLDC motor multi-class vibration fault diagnosis.
- 핵심 방법 (2~3줄): 1000/1500/2000 rpm에서 vibration data를 수집해 normalized 1D sequence로 CNN을 학습·배포한다. 약 92% accuracy를 보고하지만 window, sampling rate와 numeric latency는 제시하지 않는다.
- 정식화/수식 (있으면): 확인된 runtime mode 수식 없음.

## 0708 면담 기준 보강
- **실시간성 수준**: "low latency" 서술만 있고 수치, deadline, jitter, miss, PREEMPT_RT가 없다. `B`.
- **실행시간 가정**: 확인 필요.
- **보장 방식**: 없음. 근거: Sections V-E, VI-E, VII.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): 동일 계열 SoC/Linux이지만 timing methodology와 `W/H/M` adaptation이 없다.
- 내 연구에 쓸 곳: Pi/Linux fault diagnosis application background의 약한 비교군.
- 인용할 문장 (있으면, 15단어 이내): 없음.

## 불확실한 점
- 확인 필요: sampling rate, window/hop, model size, latency와 Linux version이 없어 재현 및 실시간성 판단이 제한된다.
