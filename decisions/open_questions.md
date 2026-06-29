# Open Questions

확인이 필요한 사항을 기록하는 파일이다.

## Questions

- classic elastic scheduling 두 편의 정량 결과를 manuscript에서 사용할 경우, HARTIK 실험과 IEEE TC 2002 후반 evaluation 수치를 별도로 재확인해야 한다.
- FLEX의 abstract에 나온 `up to 22.0% recall`, `up to 14.7% mAP` 개선 수치를 manuscript에 인용하려면 Figure 9/10과 baseline 조건을 재확인해야 한다.
- EdgeServing은 현재 로컬 PDF 기준 arXiv v1이다. manuscript 인용 전 최신 version 또는 출판 venue 여부를 확인해야 한다.
- EdgeServing의 SLO violation ratio, P95 latency, accuracy 수치를 manuscript에 넣으려면 figure별 platform, traffic intensity, SLO threshold 조건을 재확인해야 한다.
- Pantheon의 DMR, accuracy improvement, scheduling overhead 수치를 manuscript에 넣으려면 application별 task 구성과 figure 조건을 재확인해야 한다.
- Pantheon의 preemption은 GPU/DNN runtime preemption이다. PREEMPT_RT 커널 preemption 또는 RTOS scheduling과 혼동하지 않도록 원고 표현을 구분해야 한다.
- Yao et al. RTCSA 2020의 `10%~20%` accuracy improvement와 deadline miss 관련 수치를 manuscript에 인용하려면 Figure별 workload, baseline, dataset 조건을 재확인해야 한다.
- Yao et al. RTCSA 2020은 object classification service 중심이다. vibration fault diagnosis와 연결할 때 domain 차이와 utility 정의 차이를 명시해야 한다.
- Jalonen et al. ICIT 2024의 `up to 15.8%` gain과 `3.6% point gain`은 비교 기준과 figure/table 조건을 manuscript 인용 전 재확인해야 한다.
- Jalonen et al. ICIT 2024의 inference time은 MacBook Pro M1 Pro 기반이다. MCU/SBC/PREEMPT_RT 결과와 직접 비교하지 말고, 100 ms acquisition 대비 20.2 ms processing이라는 구조적 참고로만 사용해야 한다.
- elastic scheduling 계열을 원고에서 비교할 때, 각 논문의 scheduler assumption과 feasibility bound를 구분해야 한다.
  - Buttazzo et al. 1998/2002: uniprocessor periodic task, EDF/RM 및 utilization bound 중심.
  - Sudvarg et al. 2024: multicore federated scheduling, parallel DAG task, subtask workload compression.
- `Subtask-Level_Elastic_Scheduling_copy1.pdf`와 `copy2_needs_check.pdf`는 PDF 크기와 텍스트 해시가 달라 완전 중복으로 삭제하지 않았다. 실제 중복 여부는 PDF 원본 비교가 추가로 필요하다.
- image resizing 4편 중 원고 related work에서 대표로 인용할 논문을 선택해야 한다.
  - 후보: RTCSA 2021은 최초 exploration 성격, Real-Time Systems 2022는 journal extension, Real-Time Systems 2023은 resizing과 intermittent inspection 결합, RTAS 2024는 schedulability 관점이 강함.
- 네 편의 정량 결과는 현재 카드에 구체 수치로 넣지 않았다. manuscript에서 수치를 인용하려면 figure/table 값을 별도로 재확인해야 한다.
- fault diagnosis adaptive window 논문과 비교한 뒤, `machine condition + window size` 조합의 novelty claim 강도를 조정해야 한다.
- ADW 논문의 window selection이 실제 online adaptation인지, 또는 offline design procedure인지 원고에서 표현할 때 주의해야 한다. 현재 카드 기준으로는 offline 또는 data-driven selection에 가깝다.
- ADW 논문에서 computing platform, inference latency 측정, deadline 조건, RTOS/PREEMPT_RT 관련 실험은 확인되지 않았다.
- ADW의 optimized window size 수치와 validation accuracy 개선폭을 원고에 인용하려면 Table 3, Table 4, Figure 10, Figure 11 값을 별도로 재확인해야 한다.
- Tang et al.의 AANTLN, AILWTLN에서 adaptive input length가 online runtime adaptation인지, dataset/task별 input design인지 표현할 때 주의해야 한다.
- AANTLN, AILWTLN 논문에서 실험 플랫폼, inference latency, deadline, RTOS/PREEMPT_RT 관련 정보는 확인되지 않았다.
- comparison table의 `Runtime/Offline`과 `RT Constraint` 값은 현재 paper card 기준 정리이다. 원고용으로 사용하기 전 각 논문의 method/evaluation section에서 재확인해야 한다.
