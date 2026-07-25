# SIMMAC: SRAM IMC-Based Multibit Multiplication With Analog Carry Computation

> DAC 없이 아날로그 캐리 연산으로 멀티비트 곱셈을 수행하는 8T SRAM In-Memory Computing 기반 CNN 가속기 SIMMAC

- **Conference**: ESL 2025
- **Tags**: #neural-network-inference #neural-network-accelerator #memory-management

## Abstract
Several applications, ranging from artificial intelligence to encryption, require dense multi-bit matrix multiplications. With the advent of big-data applications and edge deployment, a recent paradigm shift focuses on energy-efficient computation methodologies such as In-Memory Computing (IMC). In this work, we propose SRAM IMC based Multi-bit Multiplication with Analog Carry computation (SIMMAC), a novel 8T SRAM-based IMC accelerator for multi-bit multiplication with reconfigurable bit-precision. To address the present-day challenges of IMC architectures, we propose a novel input and weight mapping strategy along with analog carry addition for in-memory computation. The proposed input and weight mapping strategy renders the implementation to be DAC-less, hence boosting the performance of the IMC Macro in terms of area and power. The novel analog carry addition methodology computes the multi-bit product within the IMC Macro, eliminating the need for peripheral digital shift-and-add circuits. With the proposed Convolutional Neural Network(CNN) workload mapping analyzed in this study, our architecture executes the Matrix Vector Multiplication (MVM) across all tiles in a single product cycle of 40ns. Our architecture achieves 98% accuracy for MNIST classification and 819.2 GOPS and 56.5 TOPS/W at 200MHz operating frequency at TSMC 65 nm technology node.

AI부터 암호화까지 다양한 응용이 조밀한 멀티비트 행렬 곱셈을 요구한다. 빅데이터 응용과 엣지 배포의 등장과 함께, 최근 패러다임은 In-Memory Computing(IMC)과 같은 에너지 효율적 연산 방법론에 초점을 맞추고 있다. 이 연구에서는 재구성 가능한 비트 정밀도로 멀티비트 곱셈을 수행하는 새로운 8T SRAM 기반 IMC 가속기인 SIMMAC(SRAM IMC 기반 아날로그 캐리 연산 멀티비트 곱셈)을 제안한다. 오늘날 IMC 아키텍처의 과제를 해결하기 위해, 인메모리 연산을 위한 새로운 입력·가중치 매핑 전략과 아날로그 캐리 덧셈을 제안한다. 제안된 입력·가중치 매핑 전략은 구현을 DAC-less화하여 IMC 매크로의 면적·전력 성능을 향상시킨다. 새로운 아날로그 캐리 덧셈 방법론은 IMC 매크로 내부에서 멀티비트 곱을 계산해, 주변 디지털 시프트-덧셈 회로의 필요성을 없앤다. 본 연구에서 분석한 CNN 워크로드 매핑을 통해, 제안 아키텍처는 모든 타일에 걸친 행렬-벡터 곱셈(MVM)을 40ns의 단일 곱 사이클로 실행한다. 이 아키텍처는 MNIST 분류에서 98% 정확도, TSMC 65nm 공정·200MHz 동작 주파수에서 819.2 GOPS 및 56.5 TOPS/W를 달성한다.

## Key Takeaways
- 어떤 문제를 해결하는가: In-Memory Computing 기반 멀티비트 행렬곱 가속에서 ADC/DAC와 주변 디지털 회로로 인한 면적·전력 오버헤드
- 어떤 방법을 사용하는가: DAC-less 입력/가중치 매핑 전략과 아날로그 캐리 덧셈을 결합한 8T SRAM IMC 매크로 설계
- 주요 결과/기여: 단일 40ns 사이클 MVM 실행, MNIST 98% 정확도, 819.2 GOPS·56.5 TOPS/W 달성(TSMC 65nm)

## Related
- [[neural-network-inference]]
- [[neural-network-accelerator]]
- [[memory-management]]

## Source
- DOI: [10.1109/les.2025.3559208](https://doi.org/10.1109/les.2025.3559208)

## My Notes
<!-- This section is written only by the user. The LLM must never edit or delete this section. -->
- **Status**: Unread
- **Interest**: /10
- **Notes**: 
