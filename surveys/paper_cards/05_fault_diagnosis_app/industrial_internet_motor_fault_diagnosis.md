# An Industrial Internet Application for Real-Time Fault Diagnosis in Industrial Motors

- **그룹**: 5 fault_diagnosis_app
- **연구 섹션**: S1 (embedded RT FD 배경), S3 (q-trigger 구조 비교군)
- **플랫폼 태그**: `PL-SERVER-GPU`
- **실행환경 태그**: `ENV-LINUX` (Siemens IoT2040 edge + local server; OS 세부 미기재)
- **출처/연도**: IEEE Transactions on Automation Science and Engineering, Vol. 17, No. 1, 2020, DOI 10.1109/TASE.2019.2913628
- **저자**: Saul Langarica, Christian Rüffelmacher, Felipe Núñez
- **분석 MD**: `papers/05_fault_diagnosis_app/reviews/Langarica_2020_Cascade_q_Trigger_분석.md`

---

## 두 질문

- **가변 변수**: 없음. W, H, M 모두 고정. Stage 1/2 전환 여부만 runtime에 결정된다.
- **트리거**: machine condition. DIPCA+SPE가 fault를 탐지하고 RBC가 vibration-related variable을 지목할 때만 Stage 2 CNN을 실행한다.

$$\text{Trigger}_{\mathrm{CNN}} = \mathbf{1}\left[\arg\max_i \mathrm{RBC}_i \in \mathcal{V}_{\mathrm{vibration}}\right]$$

System slack S는 고려하지 않는다.

---

## 논문 흐름

### Offline

1. 정상 process-variable data로 DIPCA model과 SPE threshold $J_{\mathrm{SPE}}$를 학습한다.
2. 별도로 raw vibration data로 CNN을 학습한다 (Normal / Unbalance / Inner-race / Outer-race).

### Online cascade

```
Stage 1: 1 Hz process variable 도착
    ↓ DIPCA + SPE
  SPE ≥ J_SPE?
    ├─ No  → Normal
    └─ Yes → RBC
         ↓
  Vibration variable이 원인?
    ├─ No  → Stage 1 결과로 종료
    └─ Yes → Stage 2: 46 kHz raw vibration CNN
```

### 이 논문의 "real-time" 정의

1 Hz로 process data를 polling해 online fault detection과 operator dashboard 알림을 수행하는 industrial monitoring 개념이다. Explicit deadline, per-job response-time distribution, p99, deadline miss는 없다.

---

## RT 등급: B (확정)

| 판정 항목 | 결과 |
|---|---|
| 명시적 deadline | X |
| RTOS 또는 RT-Linux | X |
| Deadline miss / tail latency | X |
| Average latency (stage별) | X (미보고) |
| Machine condition trigger | O (DIPCA+SPE+RBC) |
| System slack trigger | X |
| W/H/M runtime 변경 | X |

---

## 개인연구와의 연결

### 구조적 유사점 — q trigger

저비용 Stage 1이 vibration-related fault evidence를 발견할 때만 고비용 Stage 2 CNN을 실행한다. 이는 개인연구에서 machine condition q가 higher-cost mode를 gate하는 설계의 구조적 선례로 사용할 수 있다.

### Gap — S trigger가 없다

| 항목 | Langarica et al. | 개인연구 |
|---|---|---|
| Machine trigger | Vibration-related fault attribution | Machine condition q |
| System trigger | 없음 | Scheduling slack S |
| Runtime decision | CNN 실행 여부 | a=(W,H,M) 선택 |
| Timing criterion | Online monitoring | Deadline, p99, miss ratio |

CNN이 필요한 상황이라도 deadline slack이 부족한 경우 더 가벼운 M, 더 짧은 W, 또는 조정된 H를 선택하는 runtime policy는 없다.

---

## 세 문장 압축

Langarica et al.은 DIPCA와 SPE로 fault를 먼저 탐지하고, RBC로 fault에 책임이 있는 process variable을 식별하는 two-stage industrial motor diagnosis system을 제안한다. RBC가 vibration-related variable을 지목할 때만 고주파 raw vibration CNN을 실행하므로, machine evidence가 expensive computation을 gate하는 cascade 구조를 갖는다. 그러나 이 trigger는 machine condition만 반영하며, system slack, p99 latency, explicit deadline을 이용한 runtime mode selection은 다루지 않는다.

## Related Work 영어 한 줄

> Langarica et al. used a low-cost statistical detector to trigger CNN-based vibration-fault classification only when machine-side evidence indicated a vibration-related anomaly, but their cascade did not account for system slack or deadline feasibility.

---

## 불확실한 점

1. Stage 1과 Stage 2 각각의 execution time과 end-to-end latency는 보고되지 않는다.
2. Explicit deadline과 deadline-miss ratio는 정의되지 않는다.
3. Online CNN inference에서 W∈{512, 1024} 중 어떤 chunk size를 실배포 설정으로 사용했는지 명확하지 않다.
4. CNN이 edge device(IoT2040), local server 중 어디에서 실행되었는지 세부 배치가 불명확하다.
