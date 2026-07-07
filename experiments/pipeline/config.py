SAMPLE_RATE = 8000       # Hz (UOS dataset)
WINDOW_SIZE = 512        # samples per inference window (KCC 2026 기준)
N_CLASSES = 8            # UOS 8-class fault types
NUM_THREADS = 4          # Pi Zero 2W 코어 수

# KSC 2026: 축결함 W=512 (KCC 재현 기준)
MODEL_PATH = "models/UOS_SHAFT_8k_model_512_int8.tflite"

# 윈도우 크기별 비교 실험용 (선택)
MODEL_PATHS = {
    512:  "models/UOS_SHAFT_8k_model_512_int8.tflite",
    1024: "models/UOS_SHAFT_8k_model_1024_int8.tflite",
    2048: "models/UOS_SHAFT_8k_model_2048_int8.tflite",
}

# 측정 설정
LOG_PATH = "results/inference_latency.csv"
WARMUP_RUNS = 10         # 첫 N회는 JIT 워밍업으로 제외
MEASURE_RUNS = 100       # 측정 횟수
