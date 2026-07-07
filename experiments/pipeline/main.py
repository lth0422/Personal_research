"""
실행 예시:
  python main.py --kernel rt --load idle
  python main.py --kernel vanilla --load io --data path/to/data.npy
"""
import argparse
import numpy as np

import config
from inference import InferenceEngine
from logger import LatencyLogger


LOAD_TYPES = ["idle", "cpu", "memory", "io", "combined"]
KERNEL_TYPES = ["rt", "vanilla"]


def load_data(data_path: str | None) -> np.ndarray:
    """입력 데이터 로드. 없으면 가우시안 노이즈로 대체."""
    if data_path:
        raw = np.load(data_path)           # shape: (N, 512) float32
        return raw.astype(np.float32)
    # 더미 데이터: 표준정규분포 윈도우 100개
    return np.random.randn(config.MEASURE_RUNS, config.WINDOW_SIZE).astype(np.float32)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--kernel", required=True, choices=KERNEL_TYPES)
    parser.add_argument("--load", required=True, choices=LOAD_TYPES)
    parser.add_argument("--data", default=None, help=".npy 파일 경로 (없으면 더미 사용)")
    parser.add_argument("--out", default=config.LOG_PATH)
    args = parser.parse_args()

    engine = InferenceEngine()
    print(f"모델 로드 완료: input {engine.input_shape}, dtype {engine.input_dtype}")

    print(f"워밍업 {config.WARMUP_RUNS}회...")
    engine.warmup()

    data = load_data(args.data)
    logger = LatencyLogger(args.out, args.kernel, args.load)

    latencies = []
    for i in range(config.MEASURE_RUNS):
        window = data[i % len(data)]
        pred, lat = engine.infer(window)
        logger.log(run_id=i, pred_class=pred, latency_ms=lat)
        latencies.append(lat)

    logger.close()

    lat = np.array(latencies)
    print(f"\n--- 결과 ({args.kernel} / {args.load}) ---")
    print(f"  Min:  {lat.min():.2f} ms")
    print(f"  Avg:  {lat.mean():.2f} ms")
    print(f"  P95:  {np.percentile(lat, 95):.2f} ms")
    print(f"  Max:  {lat.max():.2f} ms")
    print(f"  저장: {args.out}")


if __name__ == "__main__":
    main()
