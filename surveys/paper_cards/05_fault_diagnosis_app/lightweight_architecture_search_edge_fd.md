# A Real-Time Mechanical Fault Diagnosis Approach Based on Lightweight Architecture Search Considering Industrial Edge Deployments

- **그룹**: 5 fault_diagnosis_app
- **출처/연도**: Engineering Applications of Artificial Intelligence 2023
- **저자**: Sihan Ma, Hongchun Sun, Sheng Gao, Guixing Zhou

## 두 질문
- **가변 변수**: model architecture, layer/module combination, candidate operation, time-loss weight. Runtime variable은 아님.
- **트리거**: 없음=offline architecture search. 실제 device computing time을 objective에 넣지만 runtime system slack에 따른 adaptation은 확인되지 않음.

## 요점
- 플랫폼: test time은 AMD Ryzen 5 4600H CPU에서 측정. embedded/FPGA deployment 가능성을 논의하지만 target embedded board 실측은 확인되지 않음.
- 도메인: bearing, gear, rotor를 포함한 rotating machinery fault diagnosis.
- 핵심 방법: variable-layer differentiable architecture search와 group/dilated convolution search space를 사용한다. 정확도 objective에 실제 계산 시간 기반 `L_time`을 결합해 lightweight diagnostic model을 찾는다.
- 정식화/수식: architecture search objective에 measured time 기반 `L_time`을 추가한다.

## 내 연구 관점
- 한 줄 gap: lightweight model을 offline으로 찾지만, diagnosis window W, diagnosis period H, system slack 기반 runtime mode selection은 다루지 않는다.
- 내 연구에 쓸 곳: model M을 선택 가능한 축으로 볼 때, lightweight FD model 설계 관련 비교군.
- 인용할 문장: "real-time performance and edge deployment"

## 불확실한 점
- 확인 필요: 실시간성 수치는 CPU test-set 처리 시간 중심이다. RTOS/PREEMPT_RT deadline miss 또는 per-sample worst-case latency로 해석하면 안 된다.
- 확인 필요: Case 1/Case 2 수치는 dataset과 sample count가 다르므로 manuscript 인용 전 Table 3, Table 4 조건을 분리해야 한다.
