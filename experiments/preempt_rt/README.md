# preempt_rt

PREEMPT_RT 패치 적용 기록 및 실효성 검증 절차.

---

## 현재 상태

- [x] PREEMPT_RT 패치 적용 완료
- [ ] 아래 검증 절차 수행 필요

---

## 기록해야 할 항목 (적용 후 채울 것)

```
패치 버전 (uname -r 결과):
패치 소스:
빌드 날짜:
```

---

## 실효성 검증 절차

PREEMPT_RT 적용이 실제로 jitter를 낮췄는지 반드시 확인한다.
분포 차이가 없으면 패치 적용이 제대로 되지 않은 것이므로 재확인이 필요하다.

### Step 1. PREEMPT 설정 확인

```bash
uname -r
# 출력 예시: 6.1.x-rt-v8 (rt 포함 여부 확인)

zcat /proc/config.gz | grep PREEMPT
# CONFIG_PREEMPT_RT=y 가 있어야 함
```

### Step 2. cyclictest 실행 (vanilla / RT 각각)

두 커널 모두 동일 명령어로 측정. 결과를 `results/cyclictest/` 에 저장.

```bash
# 실행 전: 불필요한 서비스 중지
sudo systemctl stop bluetooth triggerhappy avahi-daemon 2>/dev/null || true

# cyclictest 실행 (60초, 1ms 주기, 모든 코어)
sudo cyclictest \
  --mlockall \
  --smp \
  --priority=80 \
  --interval=1000 \
  --distance=0 \
  --duration=60 \
  --histfile=hist_rt_idle.txt \
  --quiet

# vanilla 커널에서는 동일 명령어, 저장 파일명만 hist_vanilla_idle.txt 로 변경
```

### Step 3. 결과 비교

아래 지표를 비교표에 기록한다.

| 지표 | vanilla | PREEMPT_RT | 비고 |
| --- | --- | --- | --- |
| min (us) | | | |
| avg (us) | | | |
| max (us) | | | |
| p99 (us) | | | |

max latency 차이가 10배 이상이면 PREEMPT_RT 효과 확인됨.
차이가 거의 없으면 패치 적용 상태를 재확인할 것.

### Step 4. 부하 조건별 반복

idle 검증 후, stress-ng 5종 부하를 각각 걸고 동일 측정 반복.
명령어 예시 (CPU stress):

```bash
stress-ng --cpu 4 &
STRESS_PID=$!
sudo cyclictest --mlockall --smp --priority=80 --interval=1000 --distance=0 --duration=60 --histfile=hist_rt_cpu.txt --quiet
kill $STRESS_PID
```

---

## 결과 파일 명명 규칙

```
results/cyclictest/{kernel}_{load}_r{반복번호}.txt
  kernel: vanilla | rt
  load:   idle | cpu | mem | io | combined
  예시:   results/cyclictest/rt_combined_r2.txt
```
