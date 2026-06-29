# Integrating adaptive input length selection strategy and unsupervised transfer learning for bearing fault diagnosis under noisy conditions

- **그룹**: 2 input_adaptive
- **출처/연도**: Applied Soft Computing 148, 2023
- **저자**: Guiting Tang, Cai Yi, Lei Liu, Zhan Xing, Qiuyang Zhou, Jianhui Lin

## 두 질문
- **가변 변수**: input length IL. 논문에서는 adaptive input length AIL을 사용해 bearing parameter, sampling frequency, speed 등을 반영해 입력 길이를 계산한다.
- **트리거**: bearing parameters, sampling frequency, speed, fault characteristic frequency. 추가 실험 조건으로 Gaussian white noise의 SNR을 사용하지만, SNR 자체가 runtime mode selection trigger로 쓰인 것은 아니다.

## 요점
- 플랫폼: computing platform, RTOS, PREEMPT_RT 환경은 확인 필요.
- 도메인: bearing fault diagnosis, unsupervised transfer learning, noisy vibration signal
- 핵심 방법 (2~3줄): AANTLN은 fixed input length 대신 adaptive input length를 사용하고, envelope demodulation, wide kernel, pooling, group convolution, instance normalization, MMD 기반 domain alignment를 결합한다. DEA, EDS, HSTA bearing datasets를 이용해 같은 dataset 내 transfer와 EDS to HSTA cross-domain transfer를 평가한다. 논문은 noisy conditions에서 transfer learning fault diagnosis 성능을 개선하는 데 초점을 둔다.
- 정식화/수식 (있으면): AIL은 envelope spectrum bandwidth, sampling frequency, bearing fault characteristic frequency를 이용해 계산한다. 논문은 `Bw = L fs / Lia` 형태와 bearing characteristic frequency 식을 결합해 adaptive input length를 산출한다.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): bearing fault diagnosis에서 input length를 적응적으로 정하지만, system slack, deadline, RTOS/PREEMPT_RT 조건을 고려한 runtime scheduling 문제는 다루지 않는다.
- 내 연구에 쓸 곳: window/input length가 bearing fault diagnosis 성능과 noise robustness에 영향을 준다는 비교군으로 활용 가능하다.
- 인용할 문장 (있으면, 15단어 이내): "adaptive input length model instead of a fixed input length"

## 불확실한 점
- adaptive input length 계산이 실제 online runtime adaptation으로 구현되는지, 또는 실험 전 input design 절차인지 표현할 때 주의가 필요하다.
- inference latency, deadline miss, system slack, RTOS/PREEMPT_RT 관련 실험은 확인되지 않았다.
- Fig. 6, Fig. 8, Fig. 10, Fig. 11의 세부 수치를 원고에 넣으려면 표/그림 값을 별도로 재확인해야 한다.

