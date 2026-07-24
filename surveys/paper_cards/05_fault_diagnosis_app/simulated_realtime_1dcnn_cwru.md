# Real-Time Bearing Fault Detection and Visualization Using 1D CNN: A Simulated Deployment with the CWRU Dataset

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S1 embedded real-time fault diagnosis, S2 adaptive diagnostic fidelity
- **플랫폼 태그**: `PL-DESKTOP`
- **실행환경 태그**: `ENV-OTHER`
- **출처/연도**: IEEE ICSIMA 2025, DOI 10.1109/ICSIMA66552.2025.11233248
- **저자**: Barathan Pubalan, Mohd Syahril Ramadhan Mohd Saufi, Mohd Salman Leong, Annisa Jamali

## 두 질문
- **가변 변수**: offline model representation과 cross-load fine-tuning; runtime `W/H/M` 변수는 없다.
- **트리거**: unseen load에서 성능 저하를 확인한 뒤 load별 20 labeled samples/class로 offline few-shot adaptation한다.

## Abstract 3줄 요약
- Acquisition, inference와 GUI를 포함한 bearing RT-FDD pipeline을 제안한다.
- One-revolution 1602-point input의 1D CNN을 2D CNN, SVM, RF와 비교한다.
- CWRU replay simulation에서 0.03 s prediction latency와 cross-load few-shot 개선을 보고한다.

## Conclusion 요약
- 1D CNN이 simulated 0 HP replay에서 가장 낮은 latency를 보였고, unseen load 일반화에는 labeled fine-tuning이 필요하다고 결론짓는다.

## 요점
- 플랫폼: 실제 edge target 없이 CWRU data replay와 GUI를 사용한 simulated deployment.
- 도메인: bearing multi-class fault detection and visualization.
- 핵심 방법 (2~3줄): 48 kHz, 1797 rpm에서 one revolution에 맞춘 1602-point segment를 사용한다. 0 HP 학습 후 1-3 HP에 few-shot transfer한다.
- 정식화/수식 (있으면): `L=f_s/(rpm/60)=1602`; reported 1D-CNN prediction latency 0.03 s.

## 0708 면담 기준 보강
- **실시간성 수준**: simulated replay의 latency만 있고 target OS, deadline, jitter, miss가 없다. `B`.
- **실행시간 가정**: fixed segment/model의 measured prediction latency.
- **보장 방식**: 없음. 근거: Sections III-A/B, IV-A, V.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): live sensor/SoC 배포, PREEMPT_RT와 runtime slack 기반 `W/H/M` 선택이 없다.
- 내 연구에 쓸 곳: physical rotation으로 `W`를 정하는 사례와 simulated real-time 대조군.
- 인용할 문장 (있으면, 15단어 이내): "simulated real-time testing"

## 불확실한 점
- 확인 필요: 0.03 s가 어느 CPU/GPU에서 측정됐는지 본문에 명확한 hardware specification이 없다.
