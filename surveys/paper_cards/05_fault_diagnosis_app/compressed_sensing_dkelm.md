# Fast Fault Diagnosis in Industrial Embedded Systems Based on Compressed Sensing and Deep Kernel Extreme Learning Machines

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S1 embedded real-time fault diagnosis, S2 adaptive diagnostic fidelity
- **플랫폼 태그**: `PL-HET-SOC`
- **실행환경 태그**: `ENV-LINUX`
- **출처/연도**: Sensors, 2022, DOI 10.3390/s22113997
- **저자**: Nanliang Shan, Xinghua Xu, Xianqiang Bao, Shaohua Qiu

## 두 질문
- **가변 변수**: offline compressed ratio/sample dimension과 fixed classifier configuration.
- **트리거**: runtime trigger 없음. Accuracy와 diagnosis-time trade-off를 offline 분석해 compression ratio 80%를 선택한다.

## Abstract 3줄 요약
- Resource-constrained embedded system에서 dense vibration data가 transmission/storage/diagnosis latency를 키우는 문제를 다룬다.
- Compressed sensing으로 low-dimensional samples를 만들고 DKELM이 이를 직접 분류하는 방법을 제안한다.
- CWRU와 physical rotating platform을 Zynq MPSoC/Linux에서 평가한다.

## Conclusion 요약
- Raw data의 일부만 sampling해 diagnosis computation을 줄이면서 accuracy를 유지할 수 있다고 결론짓고, multi-source edge anomaly detection을 future work로 둔다.

## 요점
- 플랫폼: Xilinx Zynq UltraScale+ MPSoC XCZU9EG, quad Cortex-A53 1.5 GHz, Linux, Python/PyTorch/CUDA.
- 도메인: rotating machinery multi-fault diagnosis.
- 핵심 방법 (2~3줄): 48 kHz data를 4800-point window로 나누고 80% compression으로 20% points만 유지한다. CS-DKELM이 reconstruction 없이 compressed signal을 직접 분류한다.
- 정식화/수식 (있으면): fixed `W=4800`; physical-platform average diagnosis time 0.17 s.

## 0708 면담 기준 보강
- **실시간성 수준**: average diagnosis time만 있고 deadline/jitter/p99/miss 없음. 논문도 이를 near-real-time이라 표현한다. `B`.
- **실행시간 가정**: compression ratio와 window/frequency에 따른 empirical diagnosis time.
- **보장 방식**: "100 ms requirement"와 평균을 비교하지만 formal guarantee 없음. 근거: Sections 3.2, 3.6-3.7, Table 8.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): compression/input mode를 runtime q/S에 따라 선택하지 않고 fixed 80%로 배포한다.
- 내 연구에 쓸 곳: `W` 외에 sampling/compression ratio를 fidelity-cost 축으로 보는 S2 비교와 SoC/Linux baseline.
- 인용할 문장 (있으면, 15단어 이내): "Retaining only 20% of the original sampling points"

## 불확실한 점
- 확인 필요: 본문의 100 ms 요구 주장과 physical-platform 0.17 s 평균은 일치하지 않으므로 deadline 충족 사례로 인용하지 않는다.
