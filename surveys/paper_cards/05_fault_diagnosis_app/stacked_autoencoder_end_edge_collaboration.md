# A Novel Bearing Fault Diagnosis Method Based on Stacked Autoencoder and End-Edge Collaboration

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S1 embedded real-time fault diagnosis, S2 adaptive diagnostic fidelity, S4 deadline-aware AI inference
- **플랫폼 태그**: `PL-MCU`
- **실행환경 태그**: `ENV-OTHER`
- **출처/연도**: IEEE CSCWD 2023, DOI 10.1109/CSCWD57460.2023.10152598
- **저자**: Chen Yang, Zou Lai, Yingchao Wang, Shulin Lan, Lihui Wang, Liehuang Zhu

## 두 질문
- **가변 변수**: end의 TinyML 결과를 수용할지 edge diagnosis를 요청할지와 edge의 terminal service order.
- **트리거**: end confidence thresholds `T1/T2`, 허용 diagnosis latency, critical request 여부.

## Abstract 3줄 요약
- MCU의 잔여 자원과 edge server를 함께 사용해 저비용·저지연 bearing diagnosis를 수행하는 문제를 다룬다.
- Bearing characteristic frequency로 최소 입력 범위를 정하고, stacked autoencoder와 confidence/delay 기반 end-edge collaboration을 제안한다.
- CWRU 기반 binary diagnosis와 200-node simulation에서 memory, latency와 edge-load 감소를 평가한다.

## Conclusion 요약
- 두 autoencoder를 cascade해 peak memory를 낮추고, confidence와 delay 제약에 따른 edge 개입으로 noisy diagnosis의 비용을 줄일 수 있다고 결론짓는다.

## 요점
- 플랫폼: STM32F407급 168 MHz, 192 kB RAM을 참조한 계산/시뮬레이션; 실제 MCU deployment 여부는 명확하지 않다.
- 도메인: bearing fault anomaly detection과 end-edge collaboration.
- 핵심 방법 (2~3줄): 12 kHz CWRU에서 characteristic-frequency 분리를 위해 최소 572 raw points를 도출한다. 24-point pre/post autoencoder와 pooling으로 2304 raw points의 receptive field를 만들고 confidence가 낮으면 edge에 요청한다.
- 정식화/수식 (있으면): `N >= f_s/Delta f_min ~= 572`; two-cascade model 6.44 kB RAM, modeled inference 351.09 ms.

## 0708 면담 기준 보강
- **실시간성 수준**: 허용 latency를 policy 입력으로 쓰지만 RTOS, deadline miss, jitter는 없다. empirical/simulation `B`.
- **실행시간 가정**: end/edge diagnosis delay를 policy가 사용하며 fixed model별 값으로 취급한다.
- **보장 방식**: confidence와 maximum allowable latency 기반 heuristic; schedulability test는 없다. 근거: Sections III-A/B, V-B.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): local `W/H/M`을 slack에 따라 선택하지 않고, 불확실한 sample을 remote edge로 넘긴다.
- 내 연구에 쓸 곳: machine evidence와 timing constraint를 동시에 trigger로 사용하는 가장 가까운 S2/S4 비교군.
- 인용할 문장 (있으면, 15단어 이내): "constraints of delay and confidence"

## 불확실한 점
- 확인 필요: MCU 수치는 "referring to STM32F407" 기반 계산으로 보여 실제 board timing 측정인지 명확하지 않다.
- 확인 필요: 200-node edge experiment는 가정된 service capacity를 사용하므로 physical network 결과로 표현하지 않는다.
