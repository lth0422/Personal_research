import numpy as np
import time

try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    import tensorflow.lite as tflite  # fallback: full TF 설치 환경

import config


class InferenceEngine:
    def __init__(self):
        self.interpreter = tflite.Interpreter(
            model_path=config.MODEL_PATH,
            num_threads=config.NUM_THREADS,
        )
        self.interpreter.allocate_tensors()
        self._in = self.interpreter.get_input_details()[0]
        self._out = self.interpreter.get_output_details()[0]

        # 모델 입력 dtype (float32 or int8)
        self.input_dtype = self._in["dtype"]
        self.input_shape = self._in["shape"]

        # INT8 양자화 파라미터 (float→int8 변환에 필요)
        quant = self._in.get("quantization_parameters", {})
        self.scale = quant.get("scales", [1.0])[0]
        self.zero_point = quant.get("zero_points", [0])[0]

    def preprocess(self, window: np.ndarray) -> np.ndarray:
        """raw float32 window → 모델 입력 tensor"""
        x = window.astype(np.float32)
        if self.input_dtype == np.int8:
            x = np.clip(np.round(x / self.scale + self.zero_point), -128, 127).astype(np.int8)
        return x.reshape(self.input_shape)

    def infer(self, window: np.ndarray) -> tuple:
        """
        Returns:
            pred_class (int): argmax class index
            latency_ms (float): invoke() 단독 측정 시간
        """
        tensor = self.preprocess(window)
        self.interpreter.set_tensor(self._in["index"], tensor)

        t0 = time.perf_counter()
        self.interpreter.invoke()
        t1 = time.perf_counter()

        output = self.interpreter.get_tensor(self._out["index"])
        latency_ms = (t1 - t0) * 1000.0
        pred_class = int(np.argmax(output))
        return pred_class, latency_ms

    def warmup(self):
        dummy = np.zeros(config.WINDOW_SIZE, dtype=np.float32)
        for _ in range(config.WARMUP_RUNS):
            self.infer(dummy)
