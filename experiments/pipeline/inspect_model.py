"""
Pi에서 실행: python inspect_model.py <model.tflite>
모델 입출력 shape, dtype, 양자화 파라미터 출력
"""
import sys
import numpy as np

try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    import tensorflow.lite as tflite

if len(sys.argv) < 2:
    print("Usage: python inspect_model.py <model.tflite>")
    sys.exit(1)

model_path = sys.argv[1]
interp = tflite.Interpreter(model_path=model_path)
interp.allocate_tensors()

inp = interp.get_input_details()[0]
out = interp.get_output_details()[0]

print(f"=== {model_path} ===")
print(f"Input  shape : {inp['shape']}  dtype: {inp['dtype']}")
print(f"Output shape : {out['shape']}  dtype: {out['dtype']}")

q = inp.get("quantization_parameters", {})
scales = q.get("scales", [])
zps    = q.get("zero_points", [])
if len(scales):
    print(f"Input  quant : scale={scales[0]:.6f}  zero_point={zps[0]}")

q2 = out.get("quantization_parameters", {})
scales2 = q2.get("scales", [])
zps2    = q2.get("zero_points", [])
if len(scales2):
    print(f"Output quant : scale={scales2[0]:.6f}  zero_point={zps2[0]}")

# 더미 추론으로 실제 동작 확인
dummy = np.zeros(inp["shape"], dtype=inp["dtype"])
interp.set_tensor(inp["index"], dummy)
interp.invoke()
result = interp.get_tensor(out["index"])
print(f"Dummy output : {result}")
print("OK: 모델 정상 동작")
