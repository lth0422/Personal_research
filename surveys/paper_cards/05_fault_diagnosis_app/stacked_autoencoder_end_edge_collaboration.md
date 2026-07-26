# A Novel Bearing Fault Diagnosis Method Based on Stacked Autoencoder and End-Edge Collaboration

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S1, S2 (runtime M 선택이 있으나 scheduling 기반이 아님)
- **플랫폼 태그**: `PL-MCU` (End, STM32F407 참조), 확인 불가 (Edge)
- **실행환경 태그**: `ENV-OTHER` (End MCU 환경 미공개; Edge = 멀티스레딩 서버, OS 불명)
- **출처/연도**: IEEE CSCWD 2023, pp. 393–398
- **DOI**: 10.1109/CSCWD57460.2023.10152598
- **저자**: Chen Yang, Zou Lai, Yingchao Wang, Shulin Lan, Lihui Wang, Liehuang Zhu
- **원문 위치**: `papers/05_fault_diagnosis_app/Stacked_Autoencoder_End-Edge_Collaborative_Bearing_Fault_Diagnosis.pdf`
- **재판정 분석**: `papers/05_fault_diagnosis_app/reviews/Yang_2023_EndEdge_TinyML_RT_재판정_개인연구.pdf`

---

## 두 질문

- **가변 변수**: M — End TinyML 단독 판단 또는 Edge 큰 모델로 라우팅하는 decision location. W는 offline 고정(572 points), H는 정의되지 않음.
- **트리거**: C(z) vs. T₁/T₂ (prediction confidence) AND d_r vs. d_e (예상 edge response time vs. maximum allowable latency). 두 조건이 동시에 Algorithm 1에서 사용됨. T₁/T₂는 고정값이고 d_e의 실제 수치는 제시되지 않음.

---

## RT 등급: B (확정)

**B 유지 근거 (원문 section/page 기준)**

| 판정 항목 | 결과 | 원문 근거 |
|---|---|---|
| deadline 정의 | △ 개념적 정의만 있음 | Section III-B, p.395: d_e = "maximum allowable latency", 수치 없음 |
| deadline 수치 | X | 논문 전체에 d_e 값 없음 |
| d_e 산출 방법 | X | 제시 없음 |
| d_e 만족률 실험 | X | Section V-B, Fig. 6(b): 없음 |
| task period / job model | X | 논문 전체에 없음 |
| p99 / tail latency | X | Section V-B: 없음 |
| deadline miss count/rate | X | 없음 |
| WCET bound | X | 없음 |
| schedulability 분석 | X | 없음 |
| 실제 MCU 측정 | X | Section V-A, p.397: "referring to STM32F407"로 계산, 실측 아님 |

**결론**: deadline-aware decision rule은 있지만 empirical deadline-aware real-time evaluation(측정·검증)이 없다.

---

## 핵심 방법 요약

### Offline 설계

- 베어링 특성주파수 분석으로 최소 입력 크기 도출: N ≥ f_s/Δf_min = 12000/21 ≈ 572 (Section IV-A, Eq. (2)–(3), p.396)
- 2-cascade stacked autoencoder 설계: Pre-AE(입력 24 nodes) → Max Pooling → Post-AE(입력 24 nodes). Effective field = 24×24×4 = 2304 원시 samples (Section IV-B, Fig. 3, p.396)
- RAM 6.44 kB, inference delay 351.09 ms (Table I, p.396; 계산값, 실측 불명)

### Runtime 동작

Algorithm 1 (End node, Section III-B, p.395):
1. 추론 실행 → C(z) 계산 (softmax 확률)
2. d_r 획득 (network delay + edge inference time; 측정 방법 불명)
3. if d_r < d_e: confidence로 분기 (T₂ ≤ C(z) < T₁이면 confidence 업로드 + local 결정)
4. if d_r ≥ d_e: C(z) < T₂이면 edge에 interrupt 요청

Edge (Algorithms 2–3, multithreading):
- Queue Q: confidence 오름차순으로 정렬, 가장 낮은 confidence 요청을 우선 처리
- EC 집합: 모든 end node confidence 추적

---

## 실험 결과 (Section V, pp.397–398)

| 지표 | 값 | 비고 |
|---|---|---|
| Binary 분류 정확도 | 100% (SNR≥6), 90.3% (SNR=1) | CWRU dataset, test set 1592 samples |
| End model RAM | 6.44 kB | 계산값 |
| Average collaboration latency | 0.597 s | 200 end devices 가정 시뮬레이션 |
| Max collaboration latency | 12 s 미만 | |
| 60% 초과 sample latency | 0.5 s 미만 | |
| Edge load 감소 | 약 94% | 순차 처리 대비 |

측정 방법·반복 횟수·실제 hardware/OS/network configuration 불명.

---

## 내 연구 관점

**유사점 (참고 가능)**
- Runtime에서 M(decision location)을 confidence + latency 조건으로 선택하는 구조가 본 연구의 A_feasible(k) 구성과 가장 가까운 선행연구
- d_e라는 허용 latency 개념을 진단 정책 입력으로 사용하는 발상은 동일

**결정적 차이**
- W, H를 runtime에 조절하지 않음 (M-only end-edge routing)
- 기계 상태 q와 scheduling slack S를 동시에 사용하지 않음
- d_e의 수치 정의, 산출식, 만족 검증 없음 → empirical RT evaluation 부재
- OS scheduling, WCET bound, schedulability analysis 없음

**인용 맥락**: S2 (adaptive fidelity) 또는 S4 (deadline-aware AI inference) 비교군. "confidence와 latency를 동시에 policy 입력으로 쓰지만, W/H 조절과 q+S 기반 mode selection이 없다"는 맥락에서 인용.

**인용 후보 문장** (Section III-B, p.395): `"constraints of delay and confidence"`

---

## 서베이 표 항목

| 항목 | 내용 |
|---|---|
| 가변 변수 | M — End TinyML vs. Edge 큰 모델 routing |
| 트리거 | confidence C(z) vs. T₁/T₂ AND 예상 edge latency d_r vs. d_e |
| 플랫폼·환경 | STM32F407 참조 계산(MCU); Edge OS 확인 불가 |
| 보장 수준 | B — deadline 정의만 있고 miss/tail 검증 없음 |
| 본 연구와의 gap | W/H 고정, H 미정의, q+S 동시 trigger 없음, RT 검증 없음 |

---

## 세 문장 압축

이 논문은 자원이 극히 제한된 MCU에서 confidence와 예상 edge response time을 기준으로 local 처리와 edge 위임을 runtime에 선택하는 결함 진단 프레임워크를 다룬다. M(decision location)을 confidence와 latency proxy로 조절하지만 W와 H는 offline 고정이며 d_e의 실제 수치와 deadline 만족 검증이 없다. 기계 상태 q와 scheduling slack S를 동시에 보고 W/H/M 조합을 선택하는 것은 다루지 않는다.

---

## 불확실한 점

- End device의 OS/RTOS: 논문에 정보 없음. STM32F407 계산값이 실측인지 FLOPS 기반인지 불명 (Section V-A 표현: "referring to")
- Edge server의 CPU, OS, thread runtime: 언급 없음
- d_r 획득 방법: "current network state"에서 얻는다고만 명시 (Section III-B), 실제 측정 또는 추정 방법 없음
- T₁, T₂ 결정 방법: "standard threshold / critical threshold"로 명명되지만 설정 방법 없음
- Table I delay 351.09 ms: FLOPS 기반 계산인지 실측인지 불명
