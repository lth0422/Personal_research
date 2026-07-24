# An Industrial Internet Application for Real-Time Fault Diagnosis in Industrial Motors

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S1 embedded real-time fault diagnosis, S6 platform/interference
- **플랫폼 태그**: `PL-SERVER-GPU`
- **실행환경 태그**: `ENV-LINUX`
- **출처/연도**: IEEE Transactions on Automation Science and Engineering, 2020, DOI 10.1109/TASE.2019.2913628
- **저자**: Saul Langarica, Christian Ruffelmacher, Felipe Nunez

## 두 질문
- **가변 변수**: runtime mode 변수는 없다. Fault stage에 따라 low-rate DIPCA/RBC와 high-rate vibration CNN이 선택된다.
- **트리거**: DIPCA fault detection 후 RBC가 vibration variable을 원인으로 식별하면 CNN bearing/unbalance classification을 실행한다.

## Abstract 3줄 요약
- Industrial Internet architecture에서 motor fault detection, variable identification와 vibration fault classification을 통합한다.
- DIPCA와 RBC로 fault와 원인 variable을 찾고 vibration fault일 때 CNN을 실행한다.
- Siemens pilot setup에서 detection, false alarm과 fault identification을 평가한다.

## Conclusion 요약
- Open-source IIoT stack에서 staged statistical/CNN diagnosis가 동작하며, detection과 identification 성능을 실험적으로 확인했다고 결론짓는다.

## 요점
- 플랫폼: CMS2000/Siemens IoT2040, local Microsoft SQL server, Python/scikit-learn/TensorFlow/Bokeh.
- 도메인: industrial motor multi-variable fault diagnosis.
- 핵심 방법 (2~3줄): Process variables는 1 Hz로 online DIPCA/RBC 처리하고, vibration fault일 때 46 kHz raw data의 512/1024-sample chunks를 CNN으로 분류한다. Fault semantics가 heavy stage 실행을 trigger하는 cascade다.
- 정식화/수식 (있으면): SPE threshold와 RBC contribution; CNN chunk `W in {512,1024}`는 offline 비교.

## 0708 면담 기준 보강
- **실시간성 수준**: 1 Hz periodic analysis architecture이나 per-stage latency, deadline, jitter, miss는 없다. `B`.
- **실행시간 가정**: stage별 timing model이 제시되지 않는다.
- **보장 방식**: statistical threshold와 empirical diagnosis metrics; timing guarantee 없음. 근거: Sections II-D, III-B, IV-D.

## 내 연구 관점
- 한 줄 gap (이 논문이 안 한 것): machine evidence로 stage를 선택하지만 system slack과 stage execution feasibility를 함께 보지 않는다.
- 내 연구에 쓸 곳: `q`가 expensive diagnosis stage/model을 trigger하는 staged pipeline 비교군.
- 인용할 문장 (있으면, 15단어 이내): "a CNN is used to identify the specific type"

## 불확실한 점
- 확인 필요: IoT2040과 local server 중 CNN이 실제로 실행되는 위치와 OS 세부가 명확하지 않다.
