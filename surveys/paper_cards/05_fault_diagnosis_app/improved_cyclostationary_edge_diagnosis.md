# Real-Time Fault Diagnosis of Motor Bearing via Improved Cyclostationary Analysis Implemented onto Edge Computing System

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S1 embedded real-time fault diagnosis
- **플랫폼 태그**: `PL-MCU`
- **실행환경 태그**: `ENV-OTHER`
- **출처/연도**: IEEE Transactions on Instrumentation and Measurement, 2023, DOI 10.1109/TIM.2023.3295476
- **저자**: Changbo He, Pengpeng Han, Jingfeng Lu, Xiaoxian Wang, Juncai Song, Zhixiong Li, Siliang Lu

## 두 질문
- **가변 변수**: runtime mode 변수는 없다. 회전속도에서 계산한 fault prior와 spectral integration band가 signal에 따라 정해진다.
- **트리거**: hall signal로 얻은 speed와 sound spectrum의 fault-frequency 일치가 diagnosis를 결정한다.

## Abstract 3줄 요약
- 진동 센서 설치가 어려운 motor에서 sound와 hall signal을 이용한 non-contact online bearing diagnosis를 다룬다.
- Improved cyclostationary frequency-energy estimation을 STM32F407 edge node에 C로 구현한다.
- Inner/outer-race fault experiment에서 weak cyclic features와 LCD online diagnosis를 확인한다.

## Conclusion 요약
- Speed-derived fault prior와 sound cyclostationary feature를 비교해 online 상태 판별이 가능하다고 결론짓는다.

## 요점
- 플랫폼: STM32F407 168 MHz, FPU/DSP library, AD7606 ADC, LCD; OS/RTOS는 명시되지 않는다.
- 도메인: motor bearing inner/outer-race fault, acoustic edge diagnosis.
- 핵심 방법 (2~3줄): 5 kHz로 sound/hall을 동시 수집하고 speed별 theoretical fault frequency를 계산한다. Spectral correlation density에서 energy band를 선택해 weak cyclic component를 강화한다.
- 정식화/수식 (있으면): signal length 5000 samples, acquisition 1 s; 전체 pipeline 10.294 s.

## 0708 면담 기준 보강
- **실시간성 수준**: online display이나 1 s acquisition 뒤 9.196 s spectral analysis가 필요하다. deadline/RTOS/jitter 없음, best-effort `B`.
- **실행시간 가정**: fixed 5000-sample analysis의 step별 measured time.
- **보장 방식**: 없음. 평균/단일 step timing만 제시한다. 근거: Section IV-D, Fig. 11.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): processing time이 acquisition period보다 길지만 mode reduction이나 scheduling 대응이 없다.
- 내 연구에 쓸 곳: "online/real-time" 명칭과 deadline 충족은 별개라는 S1 반례 및 speed-aware machine trigger 사례.
- 인용할 문장 (있으면, 15단어 이내): "total time consumption is 10.294 s"

## 불확실한 점
- 확인 필요: 반복 측정 분포가 없어 10.294 s가 평균/대표 단일 실행인지 명확하지 않다.
