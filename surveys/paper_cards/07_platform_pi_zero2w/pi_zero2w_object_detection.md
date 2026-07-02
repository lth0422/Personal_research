# Real-Time Object Detection Using Raspberry Pi Zero 2W: An Optimized Approach

- **그룹**: 7 platform_pi_zero2w
- **출처/연도**: International Research Journal on Advanced Engineering and Management 2025
- **저자**: Jeya Agastin K, P Hareesh Kumar, Hariharan K, Kailash Aravind K

## 두 질문
- **가변 변수**: YOLOv5n optimization/quantization configuration.
- **트리거**: 없음 또는 offline optimization.

## 요점
- 플랫폼: Raspberry Pi Zero 2 W.
- 도메인: edge object detection, low-power computer vision.
- 핵심 방법: YOLOv5n을 Raspberry Pi Zero 2W에서 실행하기 위해 FP32 to INT8 post-training quantization과 TensorFlow Lite runtime을 사용하는 optimized pipeline을 제시한다.
- 정식화/수식: 확인 필요.

## 내 연구 관점
- 한 줄 gap: object detection/vision 중심이며 PREEMPT_RT, vibration FD, deadline miss/jitter 평가는 확인되지 않았다.
- 내 연구에 쓸 곳: Pi Zero 2W에서 TFLite/quantized inference를 수행하는 배경 사례.
- 인용할 문장: "Raspberry Pi Zero 2W"

## 불확실한 점
- 확인 필요: venue 품질과 peer-review status를 원고 인용 전 확인해야 한다.
- 확인 필요: inference throughput, FPS, latency, accuracy 수치는 표와 실험 조건을 재확인해야 한다.
