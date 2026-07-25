# Empowering Edge Devices With Processing-in-Memory for On-Device Language Inference

> Samsung PIM 기술을 활용해 Gemma, Qwen2, TinyBERT의 온디바이스 언어모델 추론을 가속하고 그 효과를 실측 평가

- **Conference**: ESL 2025
- **Tags**: #embedded-ml #neural-network-inference #memory-management

## Abstract
The rapid advancement of deep learning (DL) models has led to a pressing need for efficient on-device DL solutions, particularly for edge devices with limited resources. processing-in-memory (PIM) technology is considered a promising technology to address the worsening memory wall problem by integrating processing capabilities directly into memory modules. This letter evaluates the potential of Samsung PIM technology in enhancing the performance of on-device language inference. We assess the impact of PIM on the inference stage of three transformer models, Gemma, Qwen2, and TinyBERT demonstrating an average 1.92x speed-up in end-to-end latency compared to CPU by offloading all linear layers to PIM. Notably, Qwen2, which has characteristics favorable to PIM, achieves a 1.25x speed-up in end-to-end latency compared to GPU. Our findings emphasize the importance of understanding model characteristics for effective PIM deployment. The results demonstrate the PIM solution's efficiency in enabling on-device language models and its edge deployment potential.

딥러닝 모델의 빠른 발전으로 자원이 제한된 엣지 디바이스에서 효율적인 온디바이스 DL 솔루션에 대한 요구가 커지고 있다. 프로세싱-인-메모리(PIM) 기술은 메모리 모듈에 처리 능력을 직접 통합함으로써 심화되는 메모리 월 문제를 해결할 유망한 기술로 꼽힌다. 이 논문은 온디바이스 언어모델 추론 성능 향상에 있어 삼성 PIM 기술의 잠재력을 평가한다. Gemma, Qwen2, TinyBERT 세 트랜스포머 모델의 추론 단계에 대한 PIM의 영향을 평가하여, 모든 선형 레이어를 PIM으로 오프로딩했을 때 CPU 대비 평균 1.92배의 종단간 지연시간 가속을 입증한다. 특히 PIM에 유리한 특성을 가진 Qwen2는 GPU 대비 1.25배의 가속을 달성한다. 이 연구 결과는 효과적인 PIM 배포를 위해 모델 특성을 이해하는 것의 중요성을 강조한다. 결과는 온디바이스 언어모델을 가능케 하는 PIM 솔루션의 효율성과 엣지 배포 잠재력을 보여준다.

## Key Takeaways
- 어떤 문제를 해결하는가: 자원 제한 엣지 디바이스에서 트랜스포머 기반 언어모델 추론의 메모리 대역폭 병목(메모리 월) 문제
- 어떤 방법을 사용하는가: 선형 레이어를 Samsung PIM으로 오프로딩하여 Gemma/Qwen2/TinyBERT 추론을 실측 평가
- 주요 결과/기여: CPU 대비 평균 1.92배, PIM 친화적인 Qwen2는 GPU 대비 1.25배 가속. 모델 특성에 따른 PIM 효과 차이를 실증적으로 규명

## Related
- [[embedded-ml]]
- [[neural-network-inference]]
- [[memory-management]]
- [[rtil-real-time-llm-inference-memory-constrained-gpu]]

## Source
- DOI: [10.1109/les.2025.3538827](https://doi.org/10.1109/les.2025.3538827)

## My Notes
<!-- This section is written only by the user. The LLM must never edit or delete this section. -->
- **Status**: Unread
- **Interest**: /10
- **Notes**: 
