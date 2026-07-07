# Real-Time Dolphin Whistle Detection on Raspberry Pi Zero 2 W with a TFLite Convolutional Neural Network

- **그룹**: 7 platform_pi_zero2w
- **출처/연도**: Robotics 2025, 14, 67
- **저자**: Rocco De Marco, Francesco Di Nardo, Alessandro Rongoni, Laura Screpanti, David Scaradozzi

## 두 질문
- **가변 변수**: TFLite model optimization, number of interpreter threads.
- **트리거**: 없음 또는 offline configuration. thread 수와 optimized/non-optimized model을 실험적으로 비교하지만 runtime adaptation은 확인되지 않는다.

## Abstract 3줄 요약
- Raspberry Pi Zero 2 W에서 TFLite CNN으로 bottlenose dolphin whistle을 real-time detection하는 저비용 TinyML 시스템을 다룬다.
- TensorFlow CNN을 TFLite로 변환하고 최적화해 model size를 줄인 뒤, 0.8 s spectrogram segment를 입력으로 사용한다.
- thread 수에 따른 latency, throughput, CPU load, temperature, memory를 평가하며, Pi Zero 2W에서 sustained inference 가능성을 보인다.

## Conclusion 요약
- 결론은 Pi Zero 2W가 TFLite-optimized CNN deployment에 viable platform이라고 정리한다. optimized model은 CPU utilization, memory footprint, thermal profile, latency, throughput에서 개선을 보였으며, future work로 marine-specific dataset과 multi-class classifier 확장을 제안한다.

## 요점
- 플랫폼: Raspberry Pi Zero 2 W Rev 1.0, Raspberry Pi OS Lite 64-bit, kernel 6.6.51+rpt-rpi-v8, TFLite_runtime 2.14.0.
- 도메인: TinyML acoustic detection, dolphin whistle detection.
- 핵심 방법 (2~3줄): TensorFlow CNN을 TFLite로 변환/최적화해 Raspberry Pi Zero 2 W에서 bottlenose dolphin whistle을 실시간 검출한다. 0.8 s spectrogram segment를 입력으로 사용하고, thread 수를 1~8개로 바꾸며 latency, throughput, CPU load, temperature, memory를 측정한다.
- 정식화/수식 (있으면): input spectrogram은 `300 x 150` pixels, 0.8 s segment. 최적화 모델 크기는 37.5 MB에서 9 MB로 감소한 것으로 보고된다.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): vibration fault diagnosis, PREEMPT_RT 비교, deadline miss rate, RT scheduling은 다루지 않는다.
- 내 연구에 쓸 곳: Pi Zero 2W에서 TFLite 기반 실시간 inference가 가능함을 보이는 직접 플랫폼 비교군. thread 수, latency, throughput, temperature 측정 항목 참고 가능.
- 인용할 문장 (있으면, 15단어 이내): "120 ms and sustained throughput"

## 불확실한 점
- 확인 필요: 120 ms latency와 8 spectrograms/second 수치는 optimized model, 4-thread 조건 기준으로 원고 인용 전 Figure 3/4와 실험 설정을 재확인해야 한다.
- 확인 필요: audio spectrogram detection이므로 vibration FD latency/deadline과 직접 비교하지 말고 플랫폼 가능성 근거로만 사용해야 한다.
