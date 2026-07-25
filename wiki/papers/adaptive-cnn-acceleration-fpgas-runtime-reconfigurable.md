# Adaptive CNN Acceleration on FPGAs: Closing the Gap With State-of-the-Art Solutions

> Multi-Dataflow Composer 기반 런타임 재구성 가능 CNN 가속기 설계 흐름을 HLS4ML, FINN, Vitis AI와 비교 분석

- **Conference**: ESL 2025
- **Tags**: #embedded-ml #neural-network-inference #neural-network-accelerator

## Abstract
This paper presents a comparative study of a design flow for generating Convolutional Neural Network (CNN) accelerators on Field Programmable Gate Arrays (FPGAs), based on an extension of the Multi-Dataflow Composer (MDC) tool, against established frameworks: HLS4ML, FINN and Vitis AI. The proposed design flow explores a previously untapped area of the design space: runtime reconfigurable accelerators. By enabling runtime reconfigurability, it provides adaptivity support, filling a gap in current FPGA-based accelerator design options. The analysis focuses on the trade-offs and benefits of each approach, particularly regarding performance and adaptivity.

이 논문은 Multi-Dataflow Composer(MDC) 툴의 확장을 기반으로 한 FPGA용 CNN 가속기 생성 설계 흐름을, HLS4ML·FINN·Vitis AI 등 기존 프레임워크와 비교 분석한다. 제안된 설계 흐름은 그동안 다뤄지지 않았던 설계 공간 영역인 런타임 재구성 가능 가속기를 탐구한다. 런타임 재구성성을 지원함으로써 기존 FPGA 기반 가속기 설계 옵션에 없던 적응성(adaptivity)을 제공한다. 분석은 성능과 적응성 측면에서 각 접근법의 트레이드오프와 이점에 초점을 맞춘다.

## Key Takeaways
- 어떤 문제를 해결하는가: 기존 FPGA CNN 가속기 설계 프레임워크(HLS4ML, FINN, Vitis AI)가 런타임 적응성을 지원하지 못하는 한계
- 어떤 방법을 사용하는가: MDC 확장을 통한 런타임 재구성 가능 가속기 설계 흐름 제안 및 기존 프레임워크와 비교
- 주요 결과/기여: 런타임 재구성성이라는 미개척 설계 공간을 채우고, 성능·적응성 트레이드오프를 정량 비교

## Related
- [[embedded-ml]]
- [[neural-network-inference]]
- [[neural-network-accelerator]]
- [[template-based-methodology-dnn-inference-fpga-hw-sw-codesign]]

## Source
- DOI: [10.1109/les.2025.3599237](https://doi.org/10.1109/les.2025.3599237)

## My Notes
<!-- This section is written only by the user. The LLM must never edit or delete this section. -->
- **Status**: Unread
- **Interest**: /10
- **Notes**: 
