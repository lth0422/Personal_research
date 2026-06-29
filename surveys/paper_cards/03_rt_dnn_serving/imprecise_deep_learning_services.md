# Scheduling Real-time Deep Learning Services as Imprecise Computations

- **그룹**: 3 rt_dnn_serving
- **출처/연도**: IEEE RTCSA 2020
- **저자**: Shuochao Yao, Yifan Hao, Yiran Zhao, Huajie Shao, Dongxin Liu, Shengzhong Liu, Tianshi Wang, Jinyang Li, Tarek Abdelzaher

## 두 질문
- **가변 변수**: DNN execution depth, executed stages, mandatory/optional parts, optional stage shedding.
- **트리거**: task deadline, schedulability constraint, input-dependent confidence/utility gain of optional stages.

## 요점
- 플랫폼: Intel i7-4770 CPU, NVIDIA TITAN X Pascal GPU.
- 도메인: real-time edge deep learning service, object classification.
- 핵심 방법 (2~3줄): DNN workflow를 mandatory part와 optional parts를 가진 imprecise computation으로 모델링한다. scheduler는 EDF 기반으로 stage를 GPU에 넘기되, deadline을 만족하면서 confidence/accuracy utility가 큰 optional stage를 우선 실행한다.
- 정식화/수식 (있으면): task `J_i`는 stages `J_i^l`로 구성되며, `l_i` stage까지 실행했을 때 reward `R_i^{l_i}`를 얻는다. 목표는 deadline constraint `F_i^{l_i} <= d_i`를 만족하면서 전체 reward를 최대화하는 depth assignment이다.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): vibration fault diagnosis의 window size W, diagnosis period H, machine condition/anomaly score trigger, PREEMPT_RT 실시간성은 다루지 않는다.
- 내 연구에 쓸 곳: deadline-aware inference에서 computation quality를 줄여 deadline을 맞추는 imprecise computation 비교군. 본 연구의 model M 또는 window W 조절과 utility/deadline trade-off를 설명할 때 참고 가능하다.
- 인용할 문장 (있으면, 15단어 이내): "mandatory part and optional parts"

## 불확실한 점
- 확인 필요: abstract의 `10% ~ 20%` overall accuracy improvement와 deadline miss 관련 수치는 manuscript 인용 전 Figure별 workload와 baseline 조건을 재확인해야 한다.
- 확인 필요: evaluation은 object classification service 중심이므로 vibration fault diagnosis로 연결할 때 domain 차이를 명시해야 한다.
