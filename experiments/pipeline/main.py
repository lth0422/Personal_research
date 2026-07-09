"""
실행 예시:
  python main.py --kernel rt --load idle
  python main.py --kernel vanilla --load io --data ../../2026_zephyr/UOS_shaft_8k_dataset/8k_test_set_512.npz
"""
import argparse
import numpy as np

import config
from inference import InferenceEngine
from logger import LatencyLogger


LOAD_TYPES = ["idle", "cpu", "memory", "io", "combined"]
KERNEL_TYPES = ["rt", "vanilla"]


def load_data(data_path: str | None) -> tuple:
    """
    Returns:
        windows: (N, 1, 512, 1) float32
        labels:  (N,) int64 or None (더미일 경우)
    """
    if data_path and data_path.endswith(".npz"):
        npz = np.load(data_path)
        windows = npz["data"].astype(np.float32)   # (N, 1, 512, 1)
        labels  = npz["label"].astype(np.int64)
        # 클래스순 정렬 방지: 항상 셔플
        idx = np.random.permutation(len(windows))
        windows, labels = windows[idx], labels[idx]
        print(f"데이터 로드: {windows.shape[0]}개 샘플 (셔플됨), {data_path}")
        return windows, labels

    if data_path and data_path.endswith(".npy"):
        raw = np.load(data_path).astype(np.float32)
        return raw, None

    # 더미: 가우시안 노이즈
    print("더미 데이터 사용 (가우시안 노이즈)")
    windows = np.random.randn(config.MEASURE_RUNS, 1, config.WINDOW_SIZE, 1).astype(np.float32)
    return windows, None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--kernel", required=True, choices=KERNEL_TYPES)
    parser.add_argument("--load",   required=True, choices=LOAD_TYPES)
    parser.add_argument("--data",   default=None, help=".npz 또는 .npy 경로 (없으면 더미)")
    parser.add_argument("--out",    default=config.LOG_PATH)
    parser.add_argument("--deadline", type=float, default=64.0, help="deadline (ms), 기본 64ms")
    args = parser.parse_args()

    engine = InferenceEngine()
    print(f"모델 로드: input {engine.input_shape}, dtype {engine.input_dtype}")

    print(f"워밍업 {config.WARMUP_RUNS}회...")
    engine.warmup()

    windows, labels = load_data(args.data)
    logger = LatencyLogger(args.out, args.kernel, args.load)

    latencies, preds, n_miss = [], [], 0
    n_runs = min(config.MEASURE_RUNS, len(windows))

    for i in range(n_runs):
        window = windows[i % len(windows)]
        pred, lat = engine.infer(window)
        miss = lat > args.deadline
        if miss:
            n_miss += 1
        logger.log(run_id=i, pred_class=pred, latency_ms=lat)
        latencies.append(lat)
        preds.append(pred)

    logger.close()

    lat = np.array(latencies)
    print(f"\n--- 결과 ({args.kernel} / {args.load}) ---")
    print(f"  Min:    {lat.min():.2f} ms")
    print(f"  Avg:    {lat.mean():.2f} ms")
    print(f"  Std:    {lat.std():.3f} ms")
    print(f"  P2P:    {lat.max()-lat.min():.2f} ms")
    print(f"  P95:    {np.percentile(lat, 95):.2f} ms")
    print(f"  P99:    {np.percentile(lat, 99):.2f} ms")
    print(f"  Max:    {lat.max():.2f} ms")
    print(f"  D-miss: {n_miss}/{n_runs} (deadline={args.deadline}ms)")

    if labels is not None:
        true_labels = [int(labels[i % len(labels)]) for i in range(n_runs)]
        correct = sum(p == t for p, t in zip(preds, true_labels))
        print(f"  Acc:    {correct}/{n_runs} = {correct/n_runs*100:.2f}%")

    print(f"  저장:   {args.out}")


if __name__ == "__main__":
    main()
