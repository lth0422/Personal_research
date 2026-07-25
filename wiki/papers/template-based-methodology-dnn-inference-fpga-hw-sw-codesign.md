# A Template-Based Methodology for Efficient DNNs Inference on FPGA Devices With HW-SW Co-Design

> 컨볼루션·풀링·덴스 레이어별 재사용 가능한 코어를 설계하는 템플릿 기반 FPGA CNN 가속 방법론

- **Conference**: ESL 2025
- **Tags**: #embedded-ml #neural-network-inference #neural-network-accelerator

## Abstract
Convolutional neural networks (CNNs) are the epitome of artificial intelligence (AI)-based applications. The computationally intensive convolution operation is the core of the entire architecture. Acceleration of CNN-based applications requires several algorithmic level manipulations and optimization for resource-constrained devices. In this work, we have proposed a template-based methodology for CNN acceleration on field programmable gate arrays (FPGA) hardware by designing reusable cores for individual layers like convolution, pooling, and dense layers. We explored various optimization techniques to achieve the best-hardware-designing strategy with data reuse and design space exploration. We have verified our methodology for LeNet-5 with kernel 5x5 and a custom CNN with kernel 3x3 for classification. The hardware-system design was validated on FPGA Xilinx XC7Z020 FPGA. Our proposed methodology achieves 2.9 GOPS/s performance outperforming existing implementation by 1.28x.

컨볼루션 신경망(CNN)은 AI 기반 응용의 정수라 할 수 있다. 연산 집약적인 컨볼루션 연산이 전체 아키텍처의 핵심이다. CNN 기반 응용의 가속을 위해서는 자원 제약 디바이스를 위한 여러 알고리즘 수준의 조작과 최적화가 필요하다. 이 연구에서는 컨볼루션, 풀링, 덴스 레이어 등 개별 레이어별로 재사용 가능한 코어를 설계함으로써 FPGA 하드웨어 상에서 CNN을 가속하는 템플릿 기반 방법론을 제안한다. 데이터 재사용과 설계 공간 탐색을 통해 최적의 하드웨어 설계 전략을 달성하기 위한 다양한 최적화 기법을 탐구했다. 이 방법론은 커널 5×5의 LeNet-5와 커널 3×3의 커스텀 CNN을 분류 작업에 적용하여 검증되었다. 하드웨어 시스템 설계는 Xilinx XC7Z020 FPGA에서 검증되었다. 제안된 방법론은 2.9 GOPS/s의 성능을 달성해 기존 구현 대비 1.28배 우수한 성능을 보였다.

## Key Takeaways
- 어떤 문제를 해결하는가: 자원 제약 FPGA 디바이스에서 CNN 가속을 위한 레이어별 하드웨어 설계 및 최적화 문제
- 어떤 방법을 사용하는가: 컨볼루션·풀링·덴스 레이어별 재사용 가능한 템플릿 코어 설계, 데이터 재사용 기반 설계 공간 탐색
- 주요 결과/기여: LeNet-5·커스텀 CNN 검증을 통해 2.9 GOPS/s 성능 달성, 기존 구현 대비 1.28배 성능 향상

## Related
- [[embedded-ml]]
- [[neural-network-inference]]
- [[neural-network-accelerator]]
- [[adaptive-cnn-acceleration-fpgas-runtime-reconfigurable]]

## Source
- DOI: [10.1109/les.2025.3538159](https://doi.org/10.1109/les.2025.3538159)

## My Notes
<!-- This section is written only by the user. The LLM must never edit or delete this section. -->
- **Status**: Unread
- **Interest**: /10
- **Notes**: 
