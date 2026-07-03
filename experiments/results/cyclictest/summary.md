# Cyclictest 결과 요약

단위: μs (마이크로초). Max 값 기준 (4코어 중 최댓값).
측정일: 2026-07-03
플랫폼: Raspberry Pi Zero 2W, Raspberry Pi OS Lite 64-bit
커널 전환 방법: /boot/firmware/config.txt의 `kernel=kernel8_rt.img` 주석 처리 → vanilla

## Max Latency 비교표 (μs)

| 부하 조건 | PREEMPT_RT | vanilla | 배율 (vanilla/RT) |
|---|---|---|---|
| idle | 46 | 196 | **4.3x** |
| CPU stress | 68 | 145 | **2.1x** |
| Memory stress | 340 | 601 | **1.8x** |
| I/O stress | 78 | 2034 | **26.1x** ← 핵심 |
| Combined | 210 | 1798 | **8.6x** |

## 코어별 상세 (Max μs)

| 부하 | Core 0 | Core 1 | Core 2 | Core 3 |
|---|---|---|---|---|
| idle (RT) | 29 | 46 | 23 | 42 |
| CPU (RT) | 48 | 46 | 66 | 68 |
| I/O (RT) | 63 | 59 | 78 | 67 |
| Combined (RT) | 174 | 210 | 154 | 162 |
| Memory (RT) | 296 | 340 | 334 | 211 |
| idle (vanilla) | 196 | 37 | 38 | 33 |
| CPU (vanilla) | 130 | 145 | 117 | 94 |
| I/O (vanilla) | 1199 | **2034** | 637 | 634 |
| Combined (vanilla) | 458 | **1798** | 146 | 870 |
| Memory (vanilla) | 601 | 315 | **593** | 318 |

## 핵심 분석

### I/O 부하 — 가장 극적인 차이 (26x)
- vanilla Linux: I/O 경로가 non-preemptible하여 블록 장치 접근 중 인터럽트 지연이 폭증
- PREEMPT_RT: I/O 서브시스템까지 선점 가능하게 패치 → 78 μs 유지
- Core 1이 2034 μs 스파이크 (약 2 ms) — 실시간 태스크 데드라인 위협 수준

### Memory 부하 — RT 커널에서도 취약 (1.8x, 가장 작은 배율)
- 페이지 폴트 및 메모리 스왑은 RT 패치로 완전히 해결 불가
- 두 커널 모두 메모리 압박에서 최대 jitter 발생
- vanilla 601 μs vs RT 340 μs — 격차는 있으나 두 커널 공통 약점

### CPU 부하 — 가장 작은 차이 (2.1x)
- 순수 CPU 연산은 커널 선점 경로와 무관하여 차이가 작음
- vanilla도 145 μs 수준 유지 → CPU 집약적 환경에서는 RT 이점 제한적

### Combined 부하 — I/O 병목이 지배 (8.6x)
- vanilla Core 1에서 1798 μs 스파이크: I/O 서브시스템 경합이 combined에서도 dominate
- RT: I/O 선점 덕분에 210 μs로 억제

## KSC 2026 논문 관점

결함 진단 파이프라인 데드라인 D를 기준으로:
- 실시간 커널 필요성 주장 근거: I/O 부하 시 vanilla 2034 μs vs RT 78 μs
- "OS scheduling jitter가 센서 데이터 수집 타이밍에 미치는 영향"이 핵심 메시지
- Memory 부하에서 RT도 취약하다는 점 → 추가 최적화 필요성 언급 가능

## 파일 목록

- rt_idle_r1.txt / vanilla_idle_r1.txt
- rt_cpu_r1.txt / vanilla_cpu_r1.txt
- rt_mem_r1.txt / vanilla_mem_r1.txt
- rt_io_r1.txt / vanilla_io_r1.txt
- rt_combined_r1.txt / vanilla_combined_r1.txt
