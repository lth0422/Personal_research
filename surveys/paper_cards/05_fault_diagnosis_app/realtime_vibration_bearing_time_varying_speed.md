# Real-Time Vibration-Based Bearing Fault Diagnosis Under Time-Varying Speed Conditions

- **그룹**: 5 fault_diagnosis_app
- **출처/연도**: IEEE ICIT 2024, DOI 10.1109/ICIT58233.2024.10540813
- **저자**: Tuomas Jalonen, Mohammad Al-Sa'd, Serkan Kiranyaz, Moncef Gabbouj

## 두 질문
- **가변 변수**: runtime adaptation 변수는 확인되지 않음. 설계 변수로 segment/window length `L=2000 samples`를 선택한다.
- **트리거**: 없음 또는 offline design. time-varying rotational speed와 noise 조건에서 robust real-time CNN을 평가하지만, runtime mode switching trigger는 확인되지 않는다.

## 요점
- 플랫폼: MacBook Pro, ARM-based M1 Pro chip, integrated 16-core GPU, 16-core neural engine, 16 GB RAM.
- 도메인: vibration-based bearing fault diagnosis under time-varying speed.
- 핵심 방법 (2~3줄): KAIST time-varying speed bearing dataset의 2채널 vibration signal을 20 kHz로 downsample한 뒤 2000-sample segment로 나누고, lightweight CNN으로 4-class bearing state를 분류한다. segment length는 motor speed variation frequency analysis를 바탕으로 0.1 s가 되도록 선택했다.
- 정식화/수식 (있으면): `L=2000`, `P=N/L`; input size는 `2000 x 2`. 모델은 5개 convolutional blocks, dense layer, dropout, softmax로 구성되고 558,660 trainable parameters를 가진다.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): system slack, deadline-aware scheduling, diagnosis period H, model M 선택, RTOS/PREEMPT_RT 비교는 다루지 않는다.
- 내 연구에 쓸 곳: vibration FD에서 window/segment length가 물리적 speed variation과 real-time processing time에 연결되는 직접 비교군.
- 인용할 문장 (있으면, 15단어 이내): "20 ms to process 100 ms"

## 불확실한 점
- 확인 필요: `up to 15.8%` gain과 `3.6% point gain`은 비교 기준과 figure/table 조건을 원고 인용 전 재확인해야 한다.
- 확인 필요: MacBook Pro 기반 inference time이므로 MCU/SBC/PREEMPT_RT 결과와 직접 비교하지 않도록 주의해야 한다.
