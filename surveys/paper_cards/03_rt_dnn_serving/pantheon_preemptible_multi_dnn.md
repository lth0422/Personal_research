# Pantheon: Preemptible Multi-DNN Inference on Mobile Edge GPUs

- **그룹**: 3 rt_dnn_serving
- **출처/연도**: ACM MobiSys 2024, DOI 10.1145/3643832.3661878
- **저자**: Lixiang Han, Zimu Zhou, Zhenjiang Li

## 두 질문
- **가변 변수**: DNN task execution order, chunk-level preemption point, early-exit/model variant after preemption.
- **트리거**: real-time DNN task arrival, relative deadline/priority change, deadline miss risk after preemption/resume.

## 요점
- 플랫폼: NVIDIA Jetson Xavier NX, Jetson Nano. autonomous car field evaluation도 확인됨.
- 도메인: mobile edge GPU, concurrent real-time multi-DNN inference.
- 핵심 방법 (2~3줄): Pantheon은 mobile edge GPU의 two-tier stream priority만으로 real-time DNN task 간 fine-grained preemption을 제공한다. DNN을 chunk 단위로 나누고 early exits와 nested redundancy를 이용해, preempted task가 재개될 때 남은 deadline에 맞는 variant로 조정한다.
- 정식화/수식 (있으면): deadline miss rate는 deadline을 놓친 job 수를 전체 job 수로 나눈 값으로 정의된다. job이 deadline을 놓치면 해당 job accuracy는 0으로 계산한다.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): vibration fault diagnosis의 window size W, diagnosis period H, machine condition/anomaly score trigger, PREEMPT_RT 실험은 다루지 않는다.
- 내 연구에 쓸 곳: deadline-aware inference와 preemptible multi-DNN scheduling 비교군. 본 연구에서 model M 또는 mode를 deadline/slack에 따라 바꾸는 논리와 비교 가능하다.
- 인용할 문장 (있으면, 15단어 이내): "fine-grained preemption"

## 불확실한 점
- 확인 필요: deadline miss rate, accuracy improvement, scheduling overhead 수치는 figure별 application/task 조건을 원고 인용 전 재확인해야 한다.
- 확인 필요: Pantheon의 preemption은 GPU/DNN runtime 설계 중심이므로 PREEMPT_RT 커널 preemption과 혼동하지 않도록 원고에서 구분해야 한다.
