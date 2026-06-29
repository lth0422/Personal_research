# Anomaly Deviation-Based Window Size Selection of Sensor Data for Enhanced Fault Diagnosis Efficiency in Autonomous Manufacturing Systems

- **그룹**: 2 input_adaptive
- **출처/연도**: Mathematics 2026, 14, 471
- **저자**: Minjae Kim, Sangyoon Lee, Dongkeun Oh, Byungho Park, Jeongdai Jo, Changwoo Lee

## 두 질문
- **가변 변수**: window size W. Hop size H는 `H = beta W`로 정의되지만 독립적인 최적화 변수로 다루지는 않는다.
- **트리거**: variability, cycle, local spike anomaly pattern에서 계산한 anomaly deviation score. 논문 기준으로는 offline 또는 data-driven window size selection에 가깝다.

## 요점
- 플랫폼: computing platform, RTOS, PREEMPT_RT 환경은 확인 필요. 실험 데이터는 roll-to-roll tension data와 rotating bearing vibration data를 사용한다.
- 도메인: autonomous manufacturing, time-series anomaly detection, fault diagnosis
- 핵심 방법 (2~3줄): ADW는 window size를 단순 preprocessing parameter가 아니라 anomaly representation과 diagnostic sensitivity를 좌우하는 design variable로 정의한다. 정상/고장 데이터에서 variability, cycle, local spike 유형별 deviation을 계산하고, 이를 통합해 window size를 선택한다. 검증은 tension data와 bearing vibration data에서 수행되며, SVM을 primary classifier로 사용한다.
- 정식화/수식 (있으면): dominant period `T0 = 1/f0`를 기준으로 `[Wmin, Wmax]`를 정의하고, candidate window set에서 anomaly deviation을 평가한다. Sliding window는 `H = beta W` 형태의 hop size를 사용한다.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): fault diagnosis의 window size selection을 다루지만, system slack, deadline, RTOS/PREEMPT_RT 조건을 고려한 runtime scheduling 정책은 다루지 않는다.
- 내 연구에 쓸 곳: window size와 fault diagnosis의 직접 비교군. 본 연구에서 W를 정확도 축뿐 아니라 latency/deadline 축과 결합해야 하는 이유를 설명할 때 참고 가능하다.
- 인용할 문장 (있으면, 15단어 이내): "window size as a core design variable"

## 불확실한 점
- ADW가 실제 online adaptation인지, 또는 offline window selection 절차인지 표현할 때 주의가 필요하다. 현재 카드 기준으로는 offline 또는 data-driven selection에 가깝다.
- computing platform, inference latency 측정, deadline 조건, RTOS/PREEMPT_RT 관련 실험은 확인되지 않았다.
- optimized window size 수치와 validation accuracy 개선폭을 원고에 인용하려면 Table 3, Table 4, Figure 10, Figure 11 값을 별도로 재확인해야 한다.
