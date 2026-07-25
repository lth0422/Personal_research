# Compressing Runtime Memory Usage via Activation Remapping for Deploying Deep Neural Networks on MCUs

> Huffman 인코딩 기반 activation remapping으로 MCU 상 DNN의 런타임 메모리 사용량을 압축하는 기법

- **Conference**: ESL 2025
- **Tags**: #embedded-ml #memory-management

## Abstract
Deploying deep neural networks (DNNs) on microcontroller units (MCUs) has received increasing attentions. Most existing DNN compression algorithms focus on reducing the parameters of DNN to fit the storage constraints of MCUs. However, runtime memory of MCUs is more limited, and these methods are insufficiently optimized for memory usage, which lower the inference efficiency of DNN models on MCUs. Therefore, we propose a runtime memory compression method based on activation remapping to optimize the runtime memory usage on MCUs. By analyzing the frequency distribution of activation values, we introduce Huffman encoding and remap activation values by dynamic range merging to compress the runtime memory usage of MCUs. In addition, a global frequency table based on activation distributions is designed to further reduce the computation and storage overheads on MCUs. Experimental results show that our method can improve the memory compression ratio of MobileNet by up to 26.9% with the accuracy loss of less than 1%, compared with three state-of-the-art methods.

마이크로컨트롤러(MCU)에 심층 신경망(DNN)을 배포하는 것에 대한 관심이 높아지고 있다. 기존 대부분의 DNN 압축 알고리즘은 MCU의 저장 공간 제약에 맞추기 위해 DNN의 파라미터 수를 줄이는 데 초점을 맞춘다. 그러나 MCU의 런타임 메모리는 더욱 제한적이며, 이러한 방법들은 메모리 사용량 최적화가 충분하지 않아 MCU 상 DNN 모델의 추론 효율을 떨어뜨린다. 따라서 이 연구는 MCU의 런타임 메모리 사용량을 최적화하기 위해 activation remapping 기반 런타임 메모리 압축 기법을 제안한다. activation 값의 빈도 분포를 분석해 Huffman 인코딩을 도입하고, 동적 범위 병합을 통해 activation 값을 재매핑함으로써 MCU의 런타임 메모리 사용량을 압축한다. 또한 activation 분포 기반의 전역 빈도표를 설계해 MCU의 연산·저장 오버헤드를 추가로 줄인다. 실험 결과, 제안 방법은 3가지 최신 기법 대비 MobileNet의 메모리 압축률을 최대 26.9% 개선하면서 정확도 손실은 1% 미만으로 유지한다.

## Key Takeaways
- 어떤 문제를 해결하는가: MCU에서 DNN 추론 시 파라미터 압축만으로는 해결되지 않는 런타임 메모리(activation) 사용량 제약
- 어떤 방법을 사용하는가: activation 값 빈도 분포 기반 Huffman 인코딩과 동적 범위 병합을 통한 activation remapping, 전역 빈도표 활용
- 주요 결과/기여: MobileNet 기준 기존 최신 기법 대비 메모리 압축률 최대 26.9% 개선, 정확도 손실 1% 미만

## Related
- [[embedded-ml]]
- [[memory-management]]

## Source
- DOI: [10.1109/les.2025.3571799](https://doi.org/10.1109/les.2025.3571799)

## My Notes
<!-- This section is written only by the user. The LLM must never edit or delete this section. -->
- **Status**: Unread
- **Interest**: /10
- **Notes**: 
