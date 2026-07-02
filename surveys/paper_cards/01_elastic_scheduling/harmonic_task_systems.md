# Elastic Scheduling for Harmonic Task Systems

- **그룹**: 1 elastic_scheduling
- **출처/연도**: RTAS 2024
- **저자**: Marion Sudvarg, Ao Li, Daisy Wang, Sanjoy Baruah, Jeremy Buhler, Chris Gill, Ning Zhang, Pontus Ekberg

## 두 질문
- **가변 변수**: task period, task utilization, harmonic period assignment.
- **트리거**: system overload, available CPU bandwidth change, interference/background workload.

## 요점
- 플랫폼: FIMS는 Raspberry Pi 4 single core, ORB-SLAM3는 Linux/LITMUS^RT 기반 multicore system.
- 도메인: harmonic implicit-deadline real-time task systems, FIMS, ORB-SLAM3.
- 핵심 방법: elastic scheduling을 harmonic period constraint가 있는 uniprocessor implicit-deadline task set으로 확장한다. offline lookup table을 만들어 utilization bound 변화 시 online binary search로 harmonic period를 재할당한다.
- 정식화/수식: Chantem et al.의 elastic objective를 사용하고, period assignment가 harmonic constraint와 schedulability constraint를 만족하도록 한다.

## 내 연구 관점
- 한 줄 gap: period/H 조절과 slack 대응에는 가깝지만 vibration FD의 window W, model M, anomaly score trigger, PREEMPT_RT는 다루지 않는다.
- 내 연구에 쓸 곳: `H`를 harmonic/synchronization constraint가 있는 elastic variable로 볼 때 강한 비교군.
- 인용할 문장: "periods must remain harmonic"

## 불확실한 점
- 확인 필요: FIMS deadline miss와 ORB-SLAM3 10.4x RTE 개선 수치는 platform, workload, utilization bound 조건을 재확인해야 한다.
- 확인 필요: ORB-SLAM3의 Linux/LITMUS^RT 조건을 PREEMPT_RT 결과와 혼동하지 않아야 한다.
