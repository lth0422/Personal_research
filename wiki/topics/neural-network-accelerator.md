# Neural Network Accelerator

> 신경망 추론을 위한 전용 하드웨어 가속기(FPGA, IMC 등) 설계

## 개요
FPGA, ASIC, In-Memory Computing 등 다양한 하드웨어 플랫폼에서 CNN·Transformer 등 신경망 연산을 가속하기 위한 아키텍처 설계와 설계공간 탐색을 다룬다. 재사용 가능한 하드웨어 코어, 런타임 재구성성, 아날로그/디지털 연산 최적화 등이 핵심 주제이다.

## 관련 논문
- [[adaptive-cnn-acceleration-fpgas-runtime-reconfigurable]] — 런타임 재구성 가능한 FPGA CNN 가속기 설계 흐름을 HLS4ML/FINN/Vitis AI와 비교
- [[template-based-methodology-dnn-inference-fpga-hw-sw-codesign]] — 레이어별 재사용 가능한 템플릿 코어 기반 FPGA CNN 가속 방법론
- [[simmac-sram-imc-multibit-multiplication-analog-carry]] — DAC-less 아날로그 캐리 연산 기반 8T SRAM IMC 멀티비트 곱셈 가속기

## 관련 개념
