# Neural Network Inference

> 실시간 시스템에서의 신경망 추론 실행 및 타이밍 분석

## 개요
딥러닝 모델(DNN, CNN 등)을 실시간 임베디드 플랫폼에서 실행할 때 발생하는 타이밍 예측 가능성, 지연 시간, 자원 경합 문제를 다룬다. GPU·NPU·DNN 가속기 등 이기종 하드웨어 환경에서의 스케줄링과 WCET 분석이 주요 연구 주제이다.

## 관련 논문
- [[rt-swap-gpu-memory-bottlenecks-multi-dnn-inference]] — CPU 메모리로 GPU 메모리를 확장하는 실시간 스왑 스케줄링 RT-Swap
- [[compressing-vae-ood-detectors-embedded-deployment]] — 양자화·프루닝·지식증류로 경량화한 VAE 기반 OOD 탐지기
- [[rtil-real-time-llm-inference-memory-constrained-gpu]] — 경량+강력 LLM 협업 추론으로 메모리 제한 GPU에서 실시간 LLM 추론
- [[adaptive-model-selection-real-time-heart-disease-detection]] — 심박수 기반 CNN 복잡도 동적 조정 프레임워크 AMS
- [[real-time-multitasking-dnn-nvidia-tensorrt]] — DNN 청크 분할 + 고정우선순위 제한선점 스케줄링으로 GPU 가속 요청 스케줄링
- [[pim-on-device-language-inference-edge-devices]] — Samsung PIM으로 Gemma/Qwen2/TinyBERT 온디바이스 추론을 최대 1.92배 가속
- [[adaptive-cnn-acceleration-fpgas-runtime-reconfigurable]] — 런타임 재구성 가능한 FPGA CNN 가속기 설계 흐름을 HLS4ML/FINN/Vitis AI와 비교
- [[template-based-methodology-dnn-inference-fpga-hw-sw-codesign]] — 레이어별 재사용 가능한 템플릿 코어 기반 FPGA CNN 가속 방법론
- [[simmac-sram-imc-multibit-multiplication-analog-carry]] — DAC-less 아날로그 캐리 연산 기반 8T SRAM IMC 멀티비트 곱셈 가속기

## 관련 개념
