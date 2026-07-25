# Memory Management

> 실시간 시스템에서의 메모리 대역폭 규제 및 캐시 관리

## 개요
멀티코어 시스템에서 공유 메모리 계층(LLC, DRAM)의 경합이 실시간 태스크의 타이밍 예측 가능성을 저해한다. 메모리 대역폭 조절, 캐시 뱅크 관리, 스크래치패드 메모리 활용 등을 통해 간섭을 제어하는 기법을 다룬다.

## 관련 논문
- [[parrp-space-isolation-caches-shared-data]] — 교체 정보 파티셔닝으로 공유 데이터 캐시 공간 격리를 지원하는 ParRP
- [[rt-swap-gpu-memory-bottlenecks-multi-dnn-inference]] — CPU 메모리로 GPU 메모리를 확장하는 실시간 스왑 스케줄링 RT-Swap
- [[duration-based-instruction-cache-locking]] — LRU age bit 기반 시간 단위 하드웨어 명령어 캐시 락킹
- [[rtil-real-time-llm-inference-memory-constrained-gpu]] — 경량+강력 LLM 협업 추론으로 메모리 제한 GPU에서 실시간 LLM 추론
- [[iommu-interference-mixed-criticality-systems]] — IOMMU IOTLB 경합이 유발하는 DMA 지연 실측 분석
- [[gpu-aware-pub-sub-communication-real-time-edge-computing]] — CUDA 공유 메모리로 GPU-호스트 복사를 없앤 GPU-Aware Pub/Sub GAPS
- [[gpu-based-heterogeneous-socs-gpu-cache-locking]] — 타이밍 예측성 인식 캐시 락킹으로 GPU SoC 메모리 경합 완화
- [[pim-on-device-language-inference-edge-devices]] — Samsung PIM으로 Gemma/Qwen2/TinyBERT 온디바이스 추론을 최대 1.92배 가속
- [[simmac-sram-imc-multibit-multiplication-analog-carry]] — DAC-less 아날로그 캐리 연산 기반 8T SRAM IMC 멀티비트 곱셈 가속기
- [[compressing-runtime-memory-activation-remapping-dnn-mcu]] — Huffman 인코딩 기반 activation remapping으로 MCU 런타임 메모리 최적화

## 관련 개념
