# results

측정 결과 원본 저장 폴더. 분석 전 원본을 그대로 보존한다.

---

## 디렉토리 구조

```
results/
├── cyclictest/          ← cyclictest 히스토그램 (.txt)
└── pipeline/            ← 파이프라인 latency 결과 (.csv)
```

---

## 파일 명명 규칙

### cyclictest

```
{kernel}_{load}_r{N}.txt
  kernel: vanilla | rt
  load:   idle | cpu | mem | io | combined
  N:      1, 2, 3 (반복 번호)

예시: rt_combined_r2.txt
```

### pipeline CSV

```
{kernel}_{load}_r{N}.csv
예시: vanilla_cpu_r1.csv
```

#### CSV 컬럼

```
run_id, kernel, load, repeat, window_idx,
t_sensor, t_infer_start, t_infer_end, t_log,
inference_latency_ms, e2e_latency_ms,
result_class, deadline_miss,
cpu_temp_C, cpu_util_pct
```

---

## 유효 run 기준

아래 조건에 해당하는 run은 `invalid/` 폴더로 이동하고 사유를 기록한다.

- CPU 온도 > 80°C (throttling 의심)
- `vcgencmd get_throttled` 결과가 0x0이 아닌 run
- 측정 도중 프로세스 비정상 종료

---

## 분석 스크립트 (예정 위치)

```
results/
└── analysis/
    ├── plot_latency.py      ← 박스플롯, CDF
    ├── calc_stats.py        ← p95, p99, σ, deadline miss rate
    └── compare_kernels.py   ← Wilcoxon rank-sum test
```
