# Real R1 실험 결과 분석

> UOS SHAFT 8kHz W=512 INT8 모델, Pi Zero 2W, n=100/조건, 정확도 100%
> 작성일: 2026-07-09

---

## 1. 결과표 (real R1)

| 부하 | V_Avg | RT_Avg | V_Std | RT_Std | V_Max | RT_Max | D-miss (V/RT) |
|---|---|---|---|---|---|---|---|
| idle | 1.53 | 1.96 | 0.033 | 0.047 | 1.62 | 2.16 | 0/0 |
| cpu | 2.99 | 3.87 | 2.041 | 0.245 | 10.43 | 4.46 | 0/0 |
| memory | 4.85 | 7.31 | 1.800 | 3.236 | 10.72 | 15.72 | 0/0 |
| **io** | **79.38** | **5.20** | **747.6** | **0.735** | **7517.86** | **7.52** | **1/0** |
| combined | 4.13 | 6.75 | 1.164 | 4.496 | 9.07 | 22.48 | 0/0 |

단위: ms. deadline 기준: 64ms.

---

## 2. stress-ng 각 모듈이 무엇을 건드리는가

### 2-1. `--cpu N`
```bash
stress-ng --cpu 4 --timeout 120s
```
- **하는 일**: N개 워커가 소수 계산, 난수 생성, 행렬 연산 등 CPU 집약 연산 반복
- **영향받는 자원**: CPU 사이클, L1/L2/L3 캐시, CPU 스케줄러 큐
- **추론에 미치는 영향**:
  - 추론 스레드와 CPU 코어를 두고 경쟁 → 스케줄링 지연
  - 캐시에 stress-ng 데이터가 올라오면서 모델 가중치 일부가 캐시에서 밀려남
  - PREEMPT_RT 환경에서는 추론 스레드(SCHED_FIFO 80)가 일반 프로세스보다 항상 우선 → jitter 감소

### 2-2. `--vm N --vm-bytes X%`
```bash
stress-ng --vm 2 --vm-bytes 80% --timeout 120s
```
- **하는 일**: N개 워커가 전체 RAM의 X%를 할당하고 반복적으로 읽기/쓰기
- **영향받는 자원**: RAM, TLB, CPU 캐시(특히 L2/L3), page allocator, swap
- **추론에 미치는 영향**:
  - 모델 가중치(~93KB)와 중간 텐서가 캐시에서 밀려남 → 매 추론마다 메인 메모리에서 재로드 필요
  - page fault 빈도 증가 → 커널이 page table을 관리하는 시간 증가
  - Pi Zero 2W는 512MB RAM으로 80% 점유 시 여유 공간이 약 100MB → 심각한 메모리 압박

### 2-3. `--io N`
```bash
stress-ng --io 2 --timeout 120s
```
- **하는 일**: `sync()` 시스템 콜을 반복 호출 → 커널의 page cache를 디스크(SD카드)로 강제 flush
- **영향받는 자원**: 커널 I/O 경로, page cache, 블록 장치 드라이버, SD카드 I/O 큐
- **추론에 미치는 영향**: 아래 3절에서 상세 설명

### 2-4. `--hdd N`
```bash
stress-ng --hdd 1 --timeout 120s
```
- **하는 일**: 대용량 파일을 SD카드에 반복적으로 쓰고 읽음 (기본 1GB 파일)
- **영향받는 자원**: SD카드 I/O 대역폭, 파일시스템 락, 블록 장치 큐
- **추론에 미치는 영향**: `--io`와 동일 경로. 특히 SD카드라는 느린 저장소를 직접 타격

### 2-5. combined (`--cpu 2 --vm 1 --vm-bytes 50% --io 1 --hdd 1`)
- 위 모두 동시 인가. CPU 경쟁 + 캐시 오염 + I/O 차단이 겹침

---

## 3. 왜 I/O 부하에서만 vanilla가 1000배 나쁜가

### 핵심 원인: Linux 커널 I/O 경로의 비선점성

**vanilla Linux의 문제:**

Linux 커널 내부의 I/O 경로(블록 장치 드라이버, page cache writeback)는 전통적으로 spinlock을 사용한다. Spinlock 구간에서는 `preempt_disable()`이 호출되어 **어떤 스레드도 CPU를 빼앗아올 수 없다.**

```
[vanilla Linux에서 I/O stress 상황]

stress-ng --io: sync() 호출
  → 커널: page cache flush 시작
    → spinlock 획득 → preempt_disable()
      → SD카드가 느리므로 수백ms ~ 수초 걸림
        → 추론 스레드(우선순위 80)가 CPU 대기
          → 추론 스레드가 블록되는 시간 = I/O 완료 시간
```

Pi Zero 2W의 SD카드는 eMMC/NVMe보다 훨씬 느리다. SD카드 쓰기 latency는 수십 ms~수 초까지 튈 수 있다. 이 시간 동안 추론 스레드는 아무것도 할 수 없어서 **7517ms(7.5초) 블록**이 발생했다.

**PREEMPT_RT의 해결:**

PREEMPT_RT 패치는 다음을 수행한다:
- 커널 내부 spinlock → `rt_mutex`(sleepable lock)로 변환
- I/O 경로에 preemption point 추가
- 인터럽트 핸들러를 kernel thread로 실행 (스케줄링 가능)

결과적으로 추론 스레드(SCHED_FIFO 80)는 I/O 작업 중에도 CPU를 빼앗아와서 실행될 수 있다. RT에서 io Max가 7.52ms인 이유다.

**cyclictest와의 연관:**

cyclictest에서 I/O 부하 시 vanilla 2034μs가 측정된 것은 OS 스케줄링 지연이었다. 실제 추론에서는 이 지연이 7517ms로 증폭되었는데, 그 이유는:
- cyclictest는 단순 타이머 wake-up 측정 (짧은 커널 경로)
- 추론은 invoke() 전체를 측정 → 여러 메모리 접근, 연산 동안 I/O 블록이 걸리면 더 오래 걸림
- 특히 실제 데이터(8MB npz 로드)를 쓰면 메모리 접근 패턴이 복잡해져 I/O 경로 진입 빈도 증가

---

## 4. 왜 나머지 조건에서 vanilla가 더 좋게 나왔나

### 4-1. PREEMPT_RT의 오버헤드

PREEMPT_RT는 결정론적 스케줄링을 위해 다음 비용을 지불한다:

| 오버헤드 항목 | 내용 |
|---|---|
| rt_mutex | spinlock 대비 취득/해제 비용 증가 |
| 인터럽트 스레드화 | 매 인터럽트마다 thread scheduling 결정 |
| 선점 체크 증가 | 더 자주 preemption point 확인 |
| 우선순위 상속 | priority inversion 방지 프로토콜 실행 |

이 오버헤드는 **I/O 경로 차단이 없는 조건(cpu, memory, combined)에서는 이득보다 손해가 크다.**

### 4-2. 조건별 분석

**cpu 부하:**
- vanilla Std 2.041ms vs RT Std 0.245ms → jitter는 RT가 8배 안정적
- vanilla Max 10.43ms vs RT Max 4.46ms → worst-case는 RT 우세
- vanilla Avg 2.99ms vs RT Avg 3.87ms → 평균은 vanilla 우세
- 해석: RT가 jitter와 worst-case를 잡아주지만, 평균 비용은 RT 오버헤드 때문에 더 높음
- **결론: 실시간 보장 관점에서는 RT가 유리 (Max, Std 기준)**

**memory 부하:**
- vanilla Max 10.72ms vs RT Max 15.72ms → 이번 R1에서는 RT가 오히려 나쁨
- 원인 가설:
  - RT 커널의 추가 스레드(인터럽트 스레드 등)가 이미 메모리가 부족한 상황에서 page fault를 더 많이 유발
  - n=100 표본 한계 — 특정 샘플에서 RT가 큰 latency를 기록했을 수 있음
- **R2/R3 반복으로 수렴 여부 확인 필요**

**combined 부하:**
- vanilla Max 9.07ms vs RT Max 22.48ms → vanilla가 크게 유리
- RT Max 22.48ms는 combined에서 우발적 spike 가능성
- 이 결과가 반복되면 combined 환경에서 RT 오버헤드가 매우 크다는 의미
- **R2/R3 필수 확인 항목**

### 4-3. n=100의 한계

100개 샘플로 tail latency(Max, P99)를 측정하는 것은 통계적으로 불안정하다.
- Max는 단 1개의 이상치에 의해 결정됨
- RT combined Max 22.48ms가 실제 경향인지, 1회성 spike인지 알 수 없음
- 최소 R2/R3 반복 후 300샘플 pooling이 필요

---

## 5. 실험 구조 요약

```
[cyclictest]          [inference pipeline]
OS 스케줄링 지연    →  실제 추론 태스크 레이턴시
(타이머 wake-up)       (invoke() 전체)

I/O: 26x 차이      →  I/O: 1000x 차이 (7517ms)
                       ↑ OS 지연이 실제 태스크로 증폭됨
                       ↑ SD카드 특성상 I/O latency 자체가 큼
```

두 지표를 함께 측정해야 하는 이유: cyclictest만으로는 실제 추론이 얼마나 영향받는지 알 수 없다. cyclictest 26x 차이가 실제 추론에서 1000x로 나타날 수도 있기 때문이다.

---

## 6. 실제 데이터가 더미 데이터보다 I/O spike가 큰 이유 — 심층 고찰

### 6-1. 오해: "추론 중 SD카드를 직접 읽어서" (틀린 설명)

현재 파이프라인에서 `np.load(npz_path)`는 **main.py 시작 시 1회만** 실행된다. 이후 추론 루프는 RAM에 올라온 배열에서 데이터를 꺼낸다. 즉, **추론 중에 SD카드를 직접 읽지 않는다.**

### 6-2. 올바른 설명: page cache 크기 차이

더미 데이터와 실제 데이터의 차이는 **page cache 점유량**이다.

```
더미 데이터:   100 × 512 × 4 bytes ≈ 200KB  (tiny, 캐시 압박 없음)
실제 데이터:   4000 × 512 × 4 bytes ≈ 8MB   (page cache 점유 증가)
              + 모델 가중치 ~93KB
              + Python 런타임, venv 라이브러리 수백 MB
```

stress-ng `--io`의 `sync()` 시스템 콜은 **page cache 전체를 SD카드로 flush**한다. flush 대상이 클수록 커널이 I/O 경로(non-preemptible)에 머무는 시간이 길어진다. 실제 데이터를 쓰면 flush 대상이 더 많아 → vanilla 커널에서 추론 스레드가 더 오래 블록된다.

### 6-3. UART 스트리밍 방식 제안 — 객관적 평가

KCC 실험 흐름처럼 **PC → UART → Pi → 추론**으로 구성하면 어떨까?

**제안의 타당성:**

장점:
- 데이터가 SD카드 page cache에 없음 → sync() flush 대상에서 완전 제외
- 실제 임베디드 시나리오와 일치 (KCC와 동일 흐름)
- UART는 character device → block device(SD카드)와 다른 커널 경로 → io stress 영향 분리 가능
- 데이터 소스가 외부(PC)이므로 실험 환경이 더 독립적

단점 및 제약:
- Pi Zero 2W의 UART (`/dev/ttyAMA0`, GPIO 14/15) + PC측 USB-UART 어댑터 필요
- PC측 전송 스크립트 작성 필요 (UOS dataset → UART 스트리밍)
- 전송 속도 제약: W=512 at 8kHz = 64ms 주기마다 512×4=2048 bytes → 최소 256Kbps 필요
- Baud rate 460800 이상 설정 권장
- 타이밍 동기화 복잡도 증가

**평가 결론:**

UART 방식은 더 엄밀하고 실제적인 실험이지만, **KSC 2026 논문 범위에서는 현재 방식도 충분히 유효하다.** 다만 아래 한계를 논문에 명시해야 한다:

> "실험에서 입력 데이터는 파일(npz)로 사전 로드되어 RAM에 저장된 후 순차적으로 공급되었다. 실제 센서 스트리밍 환경과 달리 데이터 수신 경로(UART 등)가 I/O 스트레스와 상호작용하는 효과는 측정되지 않았다."

UART 방식은 **학위논문 또는 추후 실험**에서 확장 항목으로 적합하다.

---

## 7. 남은 질문 (R2/R3 확인 항목)

- memory/combined에서 vanilla 우세가 지속되는가, 아니면 R1 노이즈인가
- RT combined Max 22.48ms는 재현되는가
- io deadline miss는 R2/R3에서도 반복되는가 (재현성)
- 300샘플 pooling 후 Wilcoxon 검정 p-value
- UART 스트리밍 방식 도입 시 io 조건 결과가 달라지는가 (향후 과제)
