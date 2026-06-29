# A novel transfer learning network with adaptive input length selection and lightweight structure for bearing fault diagnosis

- **그룹**: 2 input_adaptive
- **출처/연도**: Engineering Applications of Artificial Intelligence 123, 2023
- **저자**: Guiting Tang, Cai Yi, Lei Liu, Xingguo Yang, Du Xu, Qiuyang Zhou, Jianhui Lin

## 두 질문
- **가변 변수**: input length IL. 논문에서는 adaptive input length Na를 sampling frequency, bearing structure, bearing running speed에 따라 계산한다.
- **트리거**: bearing parameters, sampling frequency, bearing running speed, bearing characteristic frequency. 논문에서는 transfer task와 dataset 차이를 고려하지만 system load나 slack은 trigger로 쓰지 않는다.

## 요점
- 플랫폼: computing platform, RTOS, PREEMPT_RT 환경은 확인 필요.
- 도메인: bearing fault diagnosis, transfer learning, lightweight CNN
- 핵심 방법 (2~3줄): AILWTLN은 adaptive input module, lightweight network, transfer learning method로 구성된다. 입력 길이는 envelope spectrum과 bearing characteristic frequency 기반으로 계산하고, group convolution과 instance normalization으로 lightweight network를 구성하며, MMD로 source/target feature distribution 차이를 줄인다. CWRU, PU, SWJTU bearing datasets에서 81개 transfer diagnosis task를 수행한다.
- 정식화/수식 (있으면): adaptive input length `Na`는 sampling frequency `fs`, envelope spectrum bandwidth, bearing characteristic frequency를 이용해 계산된다. 논문은 `Na = n^2 fs / BW`와 bearing pass frequency 식을 결합한다.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): input length와 lightweight model을 함께 다루지만, deadline-aware inference, diagnosis period 또는 hop size, system slack 기반 scheduling은 다루지 않는다.
- 내 연구에 쓸 곳: 본 연구에서 window size W와 model M을 함께 조절하는 문제의 related work 비교군으로 활용 가능하다.
- 인용할 문장 (있으면, 15단어 이내): "adaptive input length selection and lightweight structure"

## 불확실한 점
- 논문에서 adaptive input length가 runtime에 계속 바뀌는 정책인지, dataset/task별 input design인지 표현할 때 주의가 필요하다.
- 실험 플랫폼, inference latency, deadline, RTOS/PREEMPT_RT 관련 정보는 확인되지 않았다.
- FLOPs, Params, accuracy 수치를 원고에 인용하려면 Table 4와 Fig. 8, Fig. 10 값을 별도로 재확인해야 한다.

