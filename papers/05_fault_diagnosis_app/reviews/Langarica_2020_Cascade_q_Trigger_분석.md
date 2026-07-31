# Langarica et al. (2020) — Real-Time Industrial Motor Fault Diagnosis 분석

> **대상 논문**  
> S. Langarica, C. Rüffelmacher, and F. Núñez,  
> “An Industrial Internet Application for Real-Time Fault Diagnosis in Industrial Motors,”  
> *IEEE Transactions on Automation Science and Engineering*, Vol. 17, No. 1, 2020.  
> DOI: 10.1109/TASE.2019.2913628
>
> **개인연구 기준**
>
> $$
> a=(W,H,M), \quad \text{trigger}=q+S
> $$
>
> **핵심 참조 포인트**  
> Machine condition evidence가 expensive computation을 trigger하는 cascade 구조

---

# 0. 초록 번역

본 논문은 산업용 모터의 고장을 실시간으로 탐지하고 진단하는 Industrial Internet application을 구현한다. 저비용의 DIPCA와 RBC로 고장을 우선 탐지·식별하고, 진동 측정값이 원인으로 판단될 때만 CNN을 실행해 불평형과 베어링 고장 유형을 세분화한다. 실험에서는 99% 이상의 fault detection rate, 5% 이하의 false alarm rate, 90% 이상의 identification accuracy를 보고한다.

---

# 1. 논문 흐름 요약

## 1.1 Offline procedure

시스템은 정상 운전 데이터를 이용해 DIPCA model과 fault-detection threshold를 학습한다.

1. 정상 process-variable data를 정규화한다.
2. DIPCA를 이용해 principal component subspace와 residual subspace를 구성한다.
3. SPE statistic의 threshold $J_{\mathrm{SPE}}$를 계산한다.
4. 별도로 raw vibration data를 이용해 CNN을 학습한다.

CNN은 Normal condition, Unbalance fault, Inner-race fault, Outer-race fault를 구분한다.

## 1.2 Online Stage 1 — Lightweight fault detection and preliminary identification

새로운 process-variable measurement가 도착할 때마다 다음 절차를 수행한다.

1. 새 measurement를 정규화한다.
2. SPE statistic을 계산한다.
3. 다음 조건을 검사한다.

$$
\mathrm{SPE}(\hat{x}) \ge J_{\mathrm{SPE}}
$$

4. Threshold를 넘지 않으면 normal behavior로 판정한다.
5. Threshold를 넘으면 fault를 탐지하고 RBC로 어떤 variable이 fault에 가장 크게 기여했는지 식별한다.

이 단계는 temperature, speed, RMS, DKW 등 저속으로 수집되는 process variable을 이용한다.

## 1.3 Stage 1 → Stage 2 전환 조건

RBC 결과에서 fault의 원인이 vibration-related measurement로 판단될 때만 Stage 2로 전환한다.

```text
DIPCA + SPE
    ↓
Fault detected?
    ├─ No  → Normal
    └─ Yes
         ↓
       RBC
         ↓
Vibration-related variable?
    ├─ No  → Stage 1 결과로 종료
    └─ Yes → CNN 실행
```

전환 조건은 다음처럼 요약할 수 있다.

$$
\text{Trigger}_{\mathrm{CNN}}
=
\mathbf{1}
\left[
\arg\max_i \mathrm{RBC}_i
\in
\mathcal{V}_{\mathrm{vibration}}
\right]
$$

여기서 $\mathcal{V}_{\mathrm{vibration}}$은 vibration-related process variable 집합이다.

## 1.4 Online Stage 2 — Expensive vibration classification

Stage 1에서 vibration-related fault가 의심될 때만 고주파 raw vibration data에 CNN을 적용한다.

- Stage 1 process data sampling rate: 1 Hz
- Raw vibration sampling rate: 46 kHz
- CNN input candidate chunk: 512 또는 1024 samples

CNN은 vibration fault의 root cause를 Normal, Unbalance, Inner fault, Outer fault 중 하나로 분류한다.

> **핵심 구조:** 항상 CNN을 실행하지 않고, 저비용 statistical detector가 vibration fault evidence를 제시할 때만 고비용 CNN을 실행한다.

---

# 2. 이 논문의 “real-time”과 개인연구의 차이

## 2.1 논문에서의 real-time

이 논문에서 real-time은 새로운 process measurement가 주기적으로 도착할 때 online fault detection과 identification을 수행하고, fault가 확인되면 dashboard를 통해 즉시 operator에게 알리는 online monitoring 의미에 가깝다. Online process data는 1초당 1 sample의 속도로 database에서 가져와 분석한다.

논문은 실제 industrial pilot setup과 IIoT architecture를 구현했다는 점을 강조하지만, explicit deadline, per-job response-time distribution, p99 latency, deadline-miss ratio는 제시하지 않는다.

## 2.2 개인연구와의 차이

개인연구는 다음과 같이 machine condition과 system slack을 동시에 사용한다.

$$
\text{trigger}=q+S
$$

반면 Langarica et al.은 machine-side evidence만 사용한다.

$$
\text{trigger}=q_{\mathrm{vibration}}
$$

즉 vibration-related fault evidence가 CNN 실행 여부를 결정하지만, 현재 CPU load, remaining slack, p99 response time, deadline feasibility는 고려하지 않는다.

---

# 3. 개인연구에 쓸 수 있는 부분

- **Machine condition trigger의 설계 근거:** 저비용 Stage 1이 vibration-related fault evidence를 발견했을 때만 고비용 CNN을 실행한다. 이는 모든 입력에 expensive model을 실행하지 않고 machine condition $q$가 higher-cost mode를 gate할 수 있다는 구조적 근거로 활용할 수 있다.

- **System-aware trigger의 gap:** Stage 2 진입은 machine evidence만으로 결정되며 system slack $S$는 보지 않는다. 따라서 CNN이 필요한 상황이라도 deadline slack이 부족한 경우 더 가벼운 $M$, 더 짧은 $W$, 또는 조정된 $H$를 선택하는 runtime policy는 제공하지 않는다.

| 항목 | Langarica et al. | 개인연구 |
|---|---|---|
| Machine trigger | Vibration-related fault attribution | Machine condition $q$ |
| System trigger | 없음 | Scheduling slack $S$ |
| Expensive stage | CNN | Larger $W$, shorter $H$, heavier $M$ 등 |
| Runtime decision | CNN 실행 여부 | $a=(W,H,M)$ 선택 |
| Timing criterion | Online operation | Deadline, p99, miss ratio |

---

# 4. 세 문장 압축

Langarica et al.은 DIPCA와 SPE로 fault를 먼저 탐지하고, RBC로 fault에 책임이 있는 process variable을 식별하는 two-stage industrial motor diagnosis system을 제안한다. RBC가 vibration-related variable을 지목할 때만 고주파 raw vibration CNN을 실행하므로, machine evidence가 expensive computation을 gate하는 cascade 구조를 갖는다. 그러나 이 trigger는 machine condition만 반영하며, system slack, p99 latency, explicit deadline을 이용한 runtime mode selection은 다루지 않는다.

---

# 5. Related Work 영어 한 줄

> Langarica et al. used a low-cost statistical detector to trigger CNN-based vibration-fault classification only when machine-side evidence indicated a vibration-related anomaly, but their cascade did not account for system slack or deadline feasibility.

---

# 6. 불확실한 점

- Stage 1과 Stage 2 각각의 execution time과 end-to-end latency는 보고되지 않는다.
- Explicit deadline과 deadline-miss ratio는 정의되지 않는다.
- Per-job average, maximum, p95, p99 latency는 보고되지 않는다.
- Online CNN inference에서 512와 1024 sample 중 어떤 chunk size를 실제 배포 설정으로 사용했는지는 명확하지 않다.
- CNN execution이 edge device, local server, 또는 다른 application-layer host 중 어디에서 수행되었는지 세부 배치가 명확하지 않다.
