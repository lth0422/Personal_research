import csv
import os
import time


HEADER = ["run_id", "kernel", "load_type", "pred_class", "latency_ms", "timestamp_us"]


class LatencyLogger:
    def __init__(self, path: str, kernel: str, load_type: str):
        self.path = path
        self.kernel = kernel
        self.load_type = load_type
        self._write_header = not os.path.exists(path)

        os.makedirs(os.path.dirname(path), exist_ok=True)
        self._f = open(path, "a", newline="")
        self._w = csv.writer(self._f)
        if self._write_header:
            self._w.writerow(HEADER)

    def log(self, run_id: int, pred_class: int, latency_ms: float):
        ts_us = int(time.time() * 1e6)
        self._w.writerow([run_id, self.kernel, self.load_type, pred_class, f"{latency_ms:.3f}", ts_us])

    def close(self):
        self._f.flush()
        self._f.close()
