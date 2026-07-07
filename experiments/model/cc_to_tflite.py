"""
.cc (C 배열) → .tflite 바이너리 변환
사용: python cc_to_tflite.py
"""
import re
from pathlib import Path

MODEL_DIR = Path(__file__).parent

for cc_file in sorted(MODEL_DIR.glob("*.cc")):
    text = cc_file.read_text()
    hex_values = re.findall(r"0x([0-9a-fA-F]{2})", text)
    if not hex_values:
        print(f"[SKIP] {cc_file.name}: hex 값 없음")
        continue

    data = bytes(int(h, 16) for h in hex_values)

    # 파일명에서 윈도우 크기·종류 추출: UOS_SHAFT_8k_model_512_int8
    # .cc 파일명 → .tflite
    out_name = cc_file.stem.replace(
        "converted_UOS_", "UOS_"  # 중복 prefix 제거
    ) + ".tflite"
    # stem이 이미 깔끔하면 그냥 .tflite
    out_path = MODEL_DIR / (cc_file.stem.split("_tflite")[0] + ".tflite")

    out_path.write_bytes(data)
    print(f"[OK] {cc_file.name} → {out_path.name}  ({len(data)/1024:.1f} KB)")
