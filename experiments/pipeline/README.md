# pipeline

실시간 결함 진단 파이프라인 코드 및 실행 방법.
experiment_design.md 4절(파이프라인 구조)과 정합성 유지.

---

## 파이프라인 구조

```
[Sensor Thread]  →  msgq  →  [Inference Thread]  →  msgq  →  [Logger Thread]
   SCHED_FIFO 90              SCHED_FIFO 80            SCHED_OTHER
```

- Sensor: UOS dataset 파일을 읽어 8kHz 타이머로 window 단위 전달 (ADC 시뮬레이션)
- Inference: TFLite XNNPACK으로 추론, 타임스탬프 기록
- Logger: 결과 + latency CSV 기록

---

## 예정 파일 구조

```
pipeline/
├── README.md          ← 이 파일
├── main.py            ← 진입점, 스레드 초기화
├── sensor.py          ← Sensor thread: 파일 스트리밍
├── inference.py       ← Inference thread: TFLite 추론
├── logger.py          ← Logger thread: CSV 기록
├── config.py          ← 파라미터 (W, deadline, 경로 등)
└── run_experiment.sh  ← stress-ng 연동 자동화 스크립트
```

---

## config.py 설정 항목

```python
WINDOW_SIZE = 512          # window size W (KCC 기준)
SAMPLE_RATE = 8000         # Hz
DEADLINE_MS = 64.0         # ms (KCC 기준)
MODEL_PATH = "../pi_setup/models/frfconv_tdsnet_int8.tflite"
DATA_PATH  = "../pi_setup/data/uos_1400rpm.npy"  # 전처리된 raw array
RESULT_DIR = "../results/pipeline/"
```

---

## 타임스탬프 측정 기준

```python
import time

t_sensor   = time.perf_counter()   # Sensor가 window를 큐에 넣는 시각
t_infer_start = time.perf_counter()  # Inference 시작
t_infer_end   = time.perf_counter()  # Inference 종료
t_log      = time.perf_counter()   # Logger 기록 완료

inference_latency  = (t_infer_end - t_infer_start) * 1000   # ms
end_to_end_latency = (t_log - t_sensor) * 1000              # ms
deadline_miss      = end_to_end_latency > DEADLINE_MS
```

---

## 실행 방법 (예정)

```bash
# 단독 실행 (부하 없음)
python3 main.py --kernel rt --load idle --repeat 1

# stress-ng 연동 (run_experiment.sh 사용)
bash run_experiment.sh --kernel rt --load cpu --repeat 1
```

---

## 체크리스트

- [ ] sensor.py 작성
- [ ] inference.py 작성 (TFLite XNNPACK 확인)
- [ ] logger.py 작성
- [ ] config.py 작성
- [ ] run_experiment.sh 작성
- [ ] 예비 실행 (단독, idle 조건)
- [ ] 스레드 priority 설정 확인 (SCHED_FIFO 권한 필요)
